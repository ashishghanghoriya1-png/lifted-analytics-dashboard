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
    labels = [
        ('summary', 'Executive Diagnostic & Implementation Assessment'),
        ('priority', 'Curricular Deficits & Competency Vulnerabilities'),
        ('action', 'Prescriptive Strategic Interventions')
    ]
    for zone in zones:
        data = zone_data[zone]
        entry = bundle.get('zones', {}).get(zone, {})
        valid = entry.get('source_hash') == fingerprint(data)
        brief = entry.get('brief', {}) if valid else {}
        valid = valid and all(isinstance(brief.get(k), str) and brief[k].strip() for k in ('summary', 'priority', 'action'))
        weakest = min(data['competencies'], key=lambda c: c['mastery'])
        if not valid:
            brief = {
                'summary': f"The {zone} Zone footprint spans {data['schools']} primary institutions. Leadership governance attendance is recorded at {data['hos_pct']}, while the Teacher Practice Adoption Index currently stands at {data['tp_adoption_index']}/100.",
                'priority': f"{weakest['name']} constitutes the primary instructional bottleneck at {weakest['mastery']}% mastery. Pre-call formative assessment data dissemination trails operational benchmarks at {data['tp_fa_remediation']}%.",
                'action': f"1. Prioritise structured coaching cadences for the {data['red_schools']} Intensive (Priority Red) institutions. 2. Institutionalise daily micro-remedial classroom blocks for {weakest['name']}. 3. Enforce pre-interaction formative assessment data uploads.",
            }
        source = f"Analytical Synthesis · Qwen 3.5 Engine · Validated Snapshot {entry.get('generated_at', 'Sep 2026')}" if valid else 'Analytical Synthesis · Programme Snapshot Week Ending 11 Sep 2026'

        brief_blocks = ''.join(
            f"<div style='margin:10px 0 6px 0;'><div style='font-size:12px;font-weight:700;color:#1E3A8A;text-transform:uppercase;letter-spacing:0.03em;margin-bottom:2px;'>{escape(title)}</div><p style='color:#0F172A;font-size:13px;line-height:1.65;margin:0;'>{escape(brief[key])}</p></div>"
            for key, title in labels
        )
        sec_html = (
            f"<section style='border-top:1.5px solid #BFDBFE;padding-top:16px;margin-top:18px;'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:8px;'>"
            f"<h3 style='color:#1E3A8A;font-size:16px;font-weight:700;margin:0;'>{escape(zone)} Zone</h3>"
            f"<div style='display:flex;gap:6px;flex-wrap:wrap;'>"
            f"<span style='background:#DBEAFE;color:#1E40AF;font-size:11px;font-weight:700;padding:3px 8px;border-radius:6px;'>{data['schools']} Schools</span>"
            f"<span style='background:#FFE4E6;color:#9F1239;font-size:11px;font-weight:700;padding:3px 8px;border-radius:6px;'>{data['red_schools']} Intensive (Red)</span>"
            f"<span style='background:#D1FAE5;color:#065F46;font-size:11px;font-weight:700;padding:3px 8px;border-radius:6px;'>HoS Attendance: {escape(str(data['hos_pct']))}</span>"
            f"<span style='background:#FEF3C7;color:#92400E;font-size:11px;font-weight:700;padding:3px 8px;border-radius:6px;'>TP Adoption: {data['tp_adoption_index']}/100</span>"
            f"</div></div>"
            + brief_blocks
            + f"<div style='margin-top:10px;font-size:11px;color:#64748B;font-weight:500;'>{escape(source)}</div>"
            f"</section>"
        )
        sections.append(sec_html)
    return ''.join(sections)
