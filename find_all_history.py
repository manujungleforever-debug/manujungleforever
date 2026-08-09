import os, json

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')

results = []

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
        
        if 'manujungleforever' in file_uri.lower():
            entries = data.get('entries', [])
            if not entries: continue
            
            # get the most recent timestamp
            latest_time = max([e.get('timestamp', 0) for e in entries])
            
            # just store the folder and uri
            results.append((file_uri, len(entries), latest_time, folder_path, data))
    except Exception as e:
        pass

results.sort(key=lambda x: x[0])
for uri, count, latest_time, folder_path, data in results:
    print(f"{uri} - {count} versions - Latest: {latest_time}")
