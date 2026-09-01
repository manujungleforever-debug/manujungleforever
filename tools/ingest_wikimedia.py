#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/ingest_wikimedia.py

Standalone Data Ingestion Script:
- Fetches all media files from Wikimedia Commons 'Category:Manú_National_Park'
- Extracts full licensing and author metadata (Artist, License, LicenseUrl, ImageDescription)
- Downloads images/videos safely with rate-limiting, 429 backoff, and error recovery
- Generates 'Manú National Park/metadata.json' in strict UTF-8 without BOM
- Zero impact on frontend files, CSS, or production site routes.
"""

import os
import re
import sys
import json
import time
import requests
import html

WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"
CATEGORY = "Category:Manú_National_Park"
USER_AGENT = "ManuJungleForever-Bot/1.0 (https://www.manujungleforever.com; discover@manujungleforever.com) python-requests/2.31.0"

ALLOWED_EXTS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.webm', '.mov', '.svg')

def strip_html(text):
    if not text:
        return ""
    clean = html.unescape(text)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()

def sanitize_filename(name):
    if name.startswith("File:"):
        name = name[5:]
    base, ext = os.path.splitext(name)
    if not ext:
        ext = '.jpg'
    clean_base = re.sub(r'[^\w\s\.-]', '', base, flags=re.UNICODE)
    clean_base = re.sub(r'[\s_]+', '_', clean_base).strip('._')
    return f"{clean_base}{ext.lower()}"

def fetch_category_files(category_name):
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    
    files = []
    cmcontinue = None
    page_num = 1

    print(f"[*] Conectando a Wikimedia Commons para la categoría: {category_name}...")

    while True:
        params = {
            "action": "query",
            "generator": "categorymembers",
            "gcmtitle": category_name,
            "gcmnamespace": 6, # File namespace
            "gcmlimit": 50,
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "format": "json"
        }
        if cmcontinue:
            params["gcmcontinue"] = cmcontinue

        try:
            resp = session.get(WIKIMEDIA_API, params=params, timeout=25)
            if resp.status_code == 429:
                time.sleep(5)
                continue
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[!] Error al consultar API de Wikimedia (Página {page_num}): {e}")
            break

        query = data.get("query", {})
        pages = query.get("pages", {})

        for page_id, page_info in pages.items():
            title = page_info.get("title", "")
            imageinfo_list = page_info.get("imageinfo", [])
            if not imageinfo_list:
                continue

            info = imageinfo_list[0]
            url = info.get("url")
            mime = info.get("mime", "image/jpeg")
            extmeta = info.get("extmetadata", {})

            if not url:
                continue

            clean_name = sanitize_filename(title)
            ext = os.path.splitext(clean_name)[1].lower()
            if ext not in ALLOWED_EXTS:
                continue

            author_raw = extmeta.get("Artist", {}).get("value", "") or extmeta.get("Author", {}).get("value", "Desconocido")
            license_raw = extmeta.get("LicenseShortName", {}).get("value", "") or extmeta.get("License", {}).get("value", "CC / Dominio Público")
            license_url = extmeta.get("LicenseUrl", {}).get("value", "")
            description_raw = extmeta.get("ImageDescription", {}).get("value", "") or extmeta.get("ObjectName", {}).get("value", title)

            author = strip_html(author_raw) or "Desconocido"
            license_name = strip_html(license_raw) or "CC / Dominio Público"
            description = strip_html(description_raw) or clean_name

            file_entry = {
                "title": title,
                "url": url,
                "filename": clean_name,
                "mime_type": mime,
                "author": author,
                "license": license_name,
                "license_url": license_url,
                "description": description
            }
            files.append(file_entry)

        print(f"    - Página {page_num}: {len(pages)} archivos analizados (Total acumulado: {len(files)})", flush=True)

        if "continue" in data and "gcmcontinue" in data["continue"]:
            cmcontinue = data["continue"]["gcmcontinue"]
            page_num += 1
            time.sleep(0.8)
        else:
            break

    return files

def download_file_with_retry(session, url, target_path, max_retries=5):
    for attempt in range(1, max_retries + 1):
        try:
            r = session.get(url, stream=True, timeout=35)
            if r.status_code == 429:
                wait_time = int(r.headers.get("Retry-After", 2 + (attempt * 2)))
                print(f"    [!] 429 Rate Limit detectado. Pausando {wait_time}s (Intento {attempt}/{max_retries})...", flush=True)
                time.sleep(wait_time)
                continue
            r.raise_for_status()
            with open(target_path, 'wb') as out_f:
                for chunk in r.iter_content(chunk_size=65536):
                    if chunk:
                        out_f.write(chunk)
            return True
        except Exception as e:
            if attempt == max_retries:
                print(f"    [!] Error definitivo descargando {target_path}: {e}", flush=True)
                return False
            time.sleep(2 * attempt)
    return False

def download_and_generate_metadata(output_dir="downloads/Manú National Park"):
    os.makedirs(output_dir, exist_ok=True)
    
    files = fetch_category_files(CATEGORY)
    print(f"\n[+] Total de archivos multimedia válidos encontrados: {len(files)}", flush=True)
    
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    metadata_list = []
    downloaded_count = 0
    skipped_count = 0
    error_count = 0

    for idx, f in enumerate(files, 1):
        filename = f["filename"]
        target_path = os.path.join(output_dir, filename)
        r2_path = f"Manú National Park/{filename}"

        item_meta = {
            "filename": filename,
            "r2_path": r2_path,
            "mime_type": f["mime_type"],
            "attribution": {
                "author": f["author"],
                "license": f["license"],
                "license_url": f["license_url"],
                "description": f["description"],
                "source": "Wikimedia Commons"
            }
        }
        metadata_list.append(item_meta)

        if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
            skipped_count += 1
            continue

        print(f"[{idx}/{len(files)}] Descargando: {filename}...", flush=True)
        ok = download_file_with_retry(session, f["url"], target_path)
        if ok:
            downloaded_count += 1
        else:
            error_count += 1
        time.sleep(0.8)

    metadata_json_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_json_path, 'w', encoding='utf-8') as mf:
        json.dump(metadata_list, mf, indent=2, ensure_ascii=False)

    print("\n" + "="*60, flush=True)
    print(f"[OK] Proceso de Ingesta Completado Exitosamente", flush=True)
    print(f"    - Archivos descargados nuevos: {downloaded_count}", flush=True)
    print(f"    - Archivos previamente existentes: {skipped_count}", flush=True)
    print(f"    - Errores ignorados: {error_count}", flush=True)
    print(f"    - Manifiesto generado: {metadata_json_path}", flush=True)
    print(f"    - Total registros en metadata.json: {len(metadata_list)}", flush=True)
    print("="*60, flush=True)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "downloads/Manú National Park"
    download_and_generate_metadata(out)
