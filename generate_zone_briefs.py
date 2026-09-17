"""Run locally: python generate_zone_briefs.py [--model qwen3.5:4b-q4_K_M]."""
import argparse
import ast
from datetime import datetime, timezone
import json
from pathlib import Path
import urllib.request
from lifted_digest import fingerprint
from workbook_data import zone_evidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='qwen3.5:4b-q4_K_M')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    snapshot = json.loads((root / 'workbook_snapshot.json').read_text(encoding='utf-8'))
    zones = {z: zone_evidence(snapshot, z) for z in sorted({r['Zone'] for r in snapshot['schools']})}
    bundle = {'model': args.model, 'source': snapshot['source_file'], 'zones': {}}
    schema = {'type': 'object', 'properties': {key: {'type': 'string'} for key in ('summary', 'priority', 'action')}, 'required': ['summary', 'priority', 'action'], 'additionalProperties': False}
    for zone, data in zones.items():
        print(f'Analysing {zone} with {args.model}...', flush=True)
        prompt = ('Analyse ONLY the verified Excel evidence supplied below. Return JSON summary, priority, action, '
                  'each one short sentence. Summary must quote allocated schools and completed/planned teacher batches. '
                  'Priority must explain that zone learning and teacher-practice actuals are missing. '
                  'Action must recommend collecting missing evidence or completing recorded pending training. '
                  'Never invent percentages, school diagnoses, learning gaps, causal explanations or dates. '
                  'Label recommendations as suggestions. Do not call the snapshot live/current. No markdown. '
                  + json.dumps(data))
        payload = {'model': args.model, 'prompt': prompt, 'stream': False, 'think': False, 'format': schema, 'options': {'temperature': 0, 'num_predict': 650, 'num_ctx': 4096}}
        request = urllib.request.Request('http://127.0.0.1:11434/api/generate', data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(request, timeout=600) as response:
            result = json.load(response)
        brief = json.loads(result['response'])
        if not all(isinstance(brief.get(k), str) and brief[k].strip() for k in schema['required']):
            raise ValueError(f'Incomplete response for {zone}; existing briefs left unchanged')
        bundle['zones'][zone] = {'source_hash': fingerprint(data), 'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), 'brief': brief}
        print(json.dumps(brief), flush=True)
    output = root / 'verified_zone_briefs.json'
    temp = output.with_suffix('.tmp')
    temp.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temp.replace(output)


if __name__ == '__main__':
    main()
