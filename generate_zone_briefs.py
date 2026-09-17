"""Run locally: python generate_zone_briefs.py [--model qwen3.5:4b-q4_K_M]."""
import argparse
import ast
from datetime import datetime, timezone
import json
from pathlib import Path
import urllib.request
from lifted_digest import fingerprint


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='qwen3.5:4b-q4_K_M')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    tree = ast.parse((root / 'app.py').read_text(encoding='utf-8'))
    zones = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ZONE_FLN_DATA' for t in n.targets))
    bundle = {'model': args.model, 'source': 'app.py ZONE_FLN_DATA snapshot; week ending 11 September 2026', 'zones': {}}
    schema = {'type': 'object', 'properties': {key: {'type': 'string'} for key in ('summary', 'priority', 'action')}, 'required': ['summary', 'priority', 'action'], 'additionalProperties': False}
    for zone, data in zones.items():
        print(f'Analysing {zone} with {args.model}...', flush=True)
        prompt = ('Analyse this zone programme snapshot only. This is not live data or external research. '
                  'Return JSON with summary, priority, action. Each value must be plain text, 1-2 short sentences. '
                  'Use exact supplied evidence. Identify weakest competencies and implementation gaps. '
                  'Distinguish recommended actions from observed facts. Do not invent causes, targets, dates, '
                  'people, school-level findings or causal impact. All percentages are percentage values; '
                  'tp_adoption_index is an index score, not a percentage. School categories may not sum to schools; '
                  'do not invent reconciliations. Avoid markdown. Zone: ' + zone + '\n' + json.dumps(data))
        payload = {'model': args.model, 'prompt': prompt, 'stream': False, 'think': False, 'format': schema, 'options': {'temperature': 0, 'num_predict': 650, 'num_ctx': 4096}}
        request = urllib.request.Request('http://127.0.0.1:11434/api/generate', data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(request, timeout=600) as response:
            result = json.load(response)
        brief = json.loads(result['response'])
        if not all(isinstance(brief.get(k), str) and brief[k].strip() for k in schema['required']):
            raise ValueError(f'Incomplete response for {zone}; existing briefs left unchanged')
        bundle['zones'][zone] = {'source_hash': fingerprint(data), 'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), 'brief': brief}
        print(json.dumps(brief), flush=True)
    output = root / 'zone_briefs.json'
    temp = output.with_suffix('.tmp')
    temp.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temp.replace(output)


if __name__ == '__main__':
    main()
