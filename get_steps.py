import json

with open(r'C:\Users\evera\.gemini\antigravity-ide\brain\ba1561b1-e76a-4d16-b42f-e9002c7d927a\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            idx = data.get('step_index', 0)
            if 530 <= idx <= 540:
                if 'content' in data:
                    print(f"Step {idx}: {data['content'][:500]}")
                if 'tool_calls' in data:
                    for tc in data['tool_calls']:
                        if tc['name'] in ('multi_replace_file_content', 'replace_file_content'):
                            print(f"Tool {tc['name']} args: {str(tc['args'])[:800]}")
        except Exception as e:
            pass
