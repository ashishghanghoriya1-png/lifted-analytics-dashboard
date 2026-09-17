"""Portable zone briefs grounded in the dashboard's programme snapshot."""
import hashlib
import json
from html import escape
from pathlib import Path


def fingerprint(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def load_briefs(path=None):
    try:
        data = json.loads((Path(path) if path else Path(__file__).with_name('zone_briefs.json')).read_text(encoding='utf-8'))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def render_digest(zones, zone_data, bundle):
    sections = []
    for zone in zones:
        data = zone_data[zone]
        entry = bundle.get('zones', {}).get(zone, {})
        valid = entry.get('source_hash') == fingerprint(data)
        brief = entry.get('brief', {}) if valid else {}
        valid = valid and all(isinstance(brief.get(k), str) and brief[k].strip() for k in ('summary', 'priority', 'action'))
        weakest = min(data['competencies'], key=lambda c: c['mastery'])
        if not valid:
            brief = {
                'summary': f"Literacy proficiency is {data['lit_prof']}% and numeracy proficiency is {data['num_prof']}% in the dashboard snapshot.",
                'priority': f"{weakest['name']} is the lowest-mastery competency at {weakest['mastery']}%.",
                'action': f"Prioritise coaching for {data['red_schools']} intensive-support schools and review evidence for {weakest['name']} at the next programme meeting.",
            }
        source = (f"Qwen analysis | {bundle.get('model', '')} | Generated {entry.get('generated_at', '')}" if valid else 'Data summary | Qwen brief pending refresh')
        sections.append(
            f"<section style='border-top:1px solid #BFDBFE;padding-top:14px;margin-top:14px;'>"
            f"<h3 style='color:#1E3A8A;font-size:16px;margin:0 0 6px;'>{escape(zone)} Zone</h3>"
            f"<p style='color:#475569;font-size:12px;'>{data['schools']} schools · {data['red_schools']} intensive support · HoS attendance {escape(data['hos_pct'])}</p>"
            + ''.join(f"<p style='color:#0F172A;margin:8px 0;'><strong>{label}:</strong> {escape(brief[key])}</p>" for key, label in [('summary', 'Assessment'), ('priority', 'Priority'), ('action', 'Recommended next step')])
            + f"<p style='color:#475569;font-size:11px;'>{escape(source)}</p></section>"
        )
    return ''.join(sections)
