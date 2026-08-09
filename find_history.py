import os, json, shutil

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')
target_files = [
    r'guided-tours\index.html',
    r'blog\index.html',
    r'contact\index.html',
    r'index.html',
    r'about-2\index.html'
]

results = {}

for folder in os.listdir(history_dir):
    folder_path = os.path.join(history_dir, folder)
    if not os.path.isdir(folder_path): continue
    
    entries_file = os.path.join(folder_path, 'entries.json')
    if not os.path.exists(entries_file): continue
    
    try:
        with open(entries_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        file_uri = data.get('resource', '')
        if not file_uri: continue
        
        # Check if this history matches any of our target files
        for target in target_files:
            if target.replace('\\', '/') in file_uri.replace('\\', '/'):
                if target not in results:
                    results[target] = []
                    
                for entry in data.get('entries', []):
                    entry_id = entry.get('id')
                    timestamp = entry.get('timestamp')
                    source = entry.get('source', 'local')
                    
                    entry_path = os.path.join(folder_path, entry_id)
                    if os.path.exists(entry_path):
                        size = os.path.getsize(entry_path)
                        results[target].append({
                            'id': entry_id,
                            'timestamp': timestamp,
                            'path': entry_path,
                            'size': size,
                            'source': source
                        })
    except Exception as e:
        pass

for target, entries in results.items():
    print(f"=== {target} ===")
    entries.sort(key=lambda x: x['timestamp'], reverse=True)
    for i, e in enumerate(entries[:10]):
        print(f"  {i}. {e['timestamp']} - Size: {e['size']} - Source: {e['source']} - Path: {e['path']}")
    print()
