"""Read the programme hub without substituting missing results or exporting contacts."""
import hashlib
import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import openpyxl


def text(value):
    return '' if value is None else str(value).strip()


def number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def zone(value):
    value = text(value).lower()
    for needle, name in [('west', 'West'), ('central', 'Central'), ('civil', 'Civil'), ('south', 'South')]:
        if needle in value:
            return name
    return 'Unmapped'


def read_workbook(raw, filename):
    book = openpyxl.load_workbook(io.BytesIO(raw), data_only=True)
    required = ['School Allocation', 'Leadership Update 9 Sep', "Manager's Check-in", 'Competency Based Inputs (wip)', 'TP adoption KPI and targets', 'Accountability & Risk', 'Result Framework OY4']
    missing = [name for name in required if name not in book.sheetnames]
    if missing:
        raise ValueError('Missing required sheets: ' + ', '.join(missing))
    result = {'source_file': filename, 'source_sha256': hashlib.sha256(raw).hexdigest(), 'extracted_at': datetime.now(timezone.utc).isoformat(), 'warnings': []}
    schools = []
    s = book['School Allocation']
    if text(s['A1'].value) != 'School ID' or text(s['B1'].value) != 'Zone':
        raise ValueError('School Allocation headers changed; expected School ID and Zone in A1/B1.')
    for r in range(2, s.max_row + 1):
        if not s.cell(r, 1).value:
            continue
        schools.append({'School ID': text(s.cell(r, 1).value), 'Zone': zone(s.cell(r, 2).value), 'School': text(s.cell(r, 4).value), 'PoC': text(s.cell(r, 7).value), 'Grade 3 teachers': number(s.cell(r, 9).value), 'Source': f'School Allocation!A{r}:I{r}'})
    if not schools or len({x['School ID'] for x in schools}) != len(schools):
        raise ValueError('School allocation is empty or contains duplicate school IDs.')
    result['schools'] = schools
    s = book['Leadership Update 9 Sep']
    training = []
    for r in range(4, s.max_row + 1):
        z = zone(s.cell(r, 1).value)
        if z == 'Unmapped' or number(s.cell(r, 2).value) is None:
            continue
        batch = re.search(r'(\d+)\s*/\s*(\d+)', text(s.cell(r, 6).value))
        training.append({'Zone': z, 'HoS total': number(s.cell(r, 2).value), 'HoS attended': number(s.cell(r, 3).value), 'Teacher batches completed': int(batch[1]) if batch else None, 'Teacher batches planned': int(batch[2]) if batch else None, 'Source': f'Leadership Update 9 Sep!A{r}:F{r}'})
    if len(training) != 4 or len({x['Zone'] for x in training}) != 4:
        raise ValueError('Expected one training-reach row per zone; check the leadership sheet layout.')
    result['training'] = training
    result['visit_reach'] = [{'Period': text(s.cell(r, 1).value), 'Recorded visits': number(s.cell(r, 2).value), 'Source': f'Leadership Update 9 Sep!A{r}:B{r}'} for r in range(14, 17) if s.cell(r, 1).value]
    s = book["Manager's Check-in"]
    period = ''
    visits = []
    for r in range(4, s.max_row + 1):
        a = text(s.cell(r, 1).value)
        if re.search(r'\d', a) and ('September' in a or 'Insights' in a):
            period = a
        name = text(s.cell(r, 4).value)
        if not name or name == 'Team member Name':
            continue
        planned, achieved = number(s.cell(r, 5).value), number(s.cell(r, 6).value)
        if planned is None and achieved is None:
            continue
        visits.append({'Period': period, 'Team member': name, 'Zone as recorded': text(s.cell(r, 2).value) or 'Not recorded', 'Planned': planned, 'Achieved': achieved, 'EoP': number(s.cell(r, 8).value), 'EoL': number(s.cell(r, 9).value), 'Source': f"Manager's Check-in!A{r}:J{r}"})
    result['visits'] = visits
    s = book['Competency Based Inputs (wip)']
    competencies, subject = [], ''
    for r in range(7, s.max_row + 1):
        if text(s.cell(r, 2).value) in ['Numeracy', 'Literacy']:
            subject = text(s.cell(r, 2).value)
        if s.cell(r, 6).value and number(s.cell(r, 7).value) is not None:
            competencies.append({'Subject': subject, 'Competency': text(s.cell(r, 6).value), 'Performance %': s.cell(r, 7).value * 100, 'Target %': s.cell(r, 8).value * 100 if number(s.cell(r, 8).value) is not None else None, 'Source': f'Competency Based Inputs (wip)!F{r}:I{r}'})
    result['competencies'] = competencies
    s = book['TP adoption KPI and targets']
    result['practice_targets'] = [{'Indicator': text(s.cell(r, 2).value), 'Weight': text(s.cell(r, 4).value), 'Target': text(s.cell(r, 5).value), 'Actual': 'Not available', 'Source': f'TP adoption KPI and targets!B{r}:E{r}'} for r in range(4, 24) if s.cell(r, 2).value]
    s = book['Accountability & Risk']
    result['risks'] = [{'Date': text(s.cell(r, 1).value), 'Deliverable': text(s.cell(r, 2).value), 'Owner': text(s.cell(r, 3).value), 'Risk': text(s.cell(r, 9).value), 'Type': text(s.cell(r, 10).value), 'Severity': text(s.cell(r, 11).value), 'Mitigation': text(s.cell(r, 13).value), 'Source': f'Accountability & Risk!A{r}:N{r}'} for r in range(4, s.max_row + 1) if text(s.cell(r, 9).value).lower() not in ['', 'na', 'n/a']]
    s = book['Result Framework OY4']
    result['framework'] = [{'Indicator': text(s.cell(r, 6).value), 'Target as recorded': text(s.cell(r, 7).value), 'Timeframe': text(s.cell(r, 8).value), 'Result as recorded': text(s.cell(r, 9).value), 'Baseline as recorded': text(s.cell(r, 10).value), 'Source': f'Result Framework OY4!F{r}:J{r}'} for r in range(7, s.max_row + 1) if text(s.cell(r, 6).value)]
    for t in training:
        count = sum(school['Zone'] == t['Zone'] for school in schools)
        if count != t['HoS total']:
            result['warnings'].append(f"{t['Zone']}: {count} allocated schools versus {t['HoS total']} HoS in training reach; denominators differ.")
    book.close()
    return result


def zone_evidence(data, selected):
    return {'zone': selected, 'source_sha256': data['source_sha256'], 'school_count': sum(s['Zone'] == selected for s in data['schools']), 'training': next((t for t in data['training'] if t['Zone'] == selected), None), 'limitations': 'No verified zone-specific learning results, RAG classification, or teacher-practice actuals. Training is from Leadership Update 9 Sep; do not claim live or current-week data.'}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('workbook')
    args = parser.parse_args()
    path = Path(args.workbook)
    data = read_workbook(path.read_bytes(), path.name)
    Path(__file__).with_name('workbook_snapshot.json').write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f"Extracted {len(data['schools'])} schools; contacts and personal staff notes excluded.")
