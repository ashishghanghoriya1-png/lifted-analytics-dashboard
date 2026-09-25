from pathlib import Path
import hashlib
import json
import pandas as pd
import streamlit as st
from workbook_data import read_workbook, zone_evidence

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='LIFTed Analytics Dashboard', layout='wide', page_icon='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=')
st.title('LIFTed Analytics Dashboard')
st.caption('Programme evidence, directly from the management workbook')


@st.cache_data(show_spinner=False)
def parse_upload(raw, name):
    return read_workbook(raw, name)


upload = st.sidebar.file_uploader('Upload programme workbook', type=['xlsx'], help='Replaces the data for this session. Does not publish or save your workbook.')
local_workbook = ROOT / 'LiftED Cohort 2_Program Management Hub.xlsx'
try:
    if upload:
        data = parse_upload(upload.getvalue(), upload.name)
        source_mode = 'Uploaded workbook'
    elif local_workbook.exists():
        data = parse_upload(local_workbook.read_bytes(), local_workbook.name)
        source_mode = 'Local Excel workbook'
    else:
        data = json.loads((ROOT / 'workbook_snapshot.json').read_text(encoding='utf-8'))
        source_mode = 'Published Excel extract'
except Exception as error:
    st.error(f'Workbook could not be loaded: {error}')
    st.stop()
st.sidebar.caption(source_mode + ': ' + data['source_file'])
st.sidebar.caption('To update the published default, regenerate the extract from the latest workbook.')
zones = sorted({s['Zone'] for s in data['schools']})
selected = st.sidebar.multiselect('Zones', zones, default=zones)
schools = [s for s in data['schools'] if s['Zone'] in selected]
owners = sorted({s['PoC'] for s in schools if s['PoC']})
owner = st.sidebar.selectbox('School allocation PoC', ['All owners'] + owners)
school_scope = [s for s in schools if owner == 'All owners' or s['PoC'] == owner]
st.sidebar.caption('Zone selection applies to reach, allocation and zone briefs. PoC applies to school allocation only. Other sections show their own recorded scope and period.')
with st.expander('Data source and checks'):
    st.write(f"Workbook: {data['source_file']}")
    st.write(f"Extracted: {data['extracted_at']}")
    st.code(data['source_sha256'], language=None)
    st.write('Tables include source sheet and row references. Blank values remain unavailable. Targets and historical baselines are not reported as current results.')
    for warning in data['warnings']:
        st.warning(warning)


def table(rows):
    if not rows:
        st.info('No matching records in the workbook.')
    else:
        frame = pd.DataFrame(rows)
        st.dataframe(frame, hide_index=True, use_container_width=True)
        return frame


def complete_sum(rows, key):
    values = [r.get(key) for r in rows]
    return sum(values) if values and all(isinstance(v, (int, float)) for v in values) else None


def display(value, suffix=''):
    return 'Not available' if value is None else f'{value:g}{suffix}'


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


tabs = st.tabs(['Executive Summary', 'School support command centre', 'Student Learning & SLOs', 'Teacher Practice Adoption', 'Field Operations Cadence', 'Competency pack analytics', 'Impact and evaluation', 'Risks and Decisions', 'School AI Brief'])
with tabs[0]:
    st.subheader('Programme reach')
    training = [r for r in data['training'] if r['Zone'] in selected]
    attended, hos = complete_sum(training, 'HoS attended'), complete_sum(training, 'HoS total')
    done, planned = complete_sum(training, 'Teacher batches completed'), complete_sum(training, 'Teacher batches planned')
    a, b, c = st.columns(3)
    a.metric('Allocated schools', len(schools))
    b.metric('HoS attendance', display(round(attended / hos * 100, 1), '%') if attended is not None and hos else 'Not available')
    c.metric('Teacher batches completed', f'{display(done)} / {display(planned)}')
    st.caption('Schools: unique School IDs in School Allocation. Training: Leadership Update 9 Sep; percentage calculated from attended / total HoS. This is the recorded snapshot, not a live weekly feed.')
    table(training)
    if training:
        st.bar_chart(pd.DataFrame(training).set_index('Zone')[['HoS total', 'HoS attended']], stack=False)
    st.subheader('Programme Intelligence Digest')
    st.caption('Zone-level evidence only. Learning scores and school diagnoses are unavailable at this scope.')
    try:
        bundle = json.loads((ROOT / 'verified_zone_briefs.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        bundle = {}
    for z in selected:
        evidence = zone_evidence(data, z)
        brief = bundle.get('zones', {}).get(z, {})
        st.markdown(f'#### {z}')
        if brief.get('source_hash') == fingerprint(evidence):
            for key, label in [('summary', 'Assessment'), ('priority', 'Evidence gap'), ('action', 'Suggested next step')]:
                st.write(f"{label}: {brief['brief'][key]}")
            st.caption(f"Ollama Qwen · {bundle.get('model')} · Generated {brief['generated_at']}")
        else:
            st.write(f"{evidence['school_count']} allocated schools. Training evidence is shown in the table above.")
            st.caption('Verified workbook summary. Qwen brief not generated for this workbook version.')

with tabs[1]:
    st.subheader('School allocation')
    st.metric('Schools in selected allocation', len(school_scope))
    st.info('RAG category, school movement and intensive-support counts: Not available. No school-level classification records are supplied in this workbook.')
    table(school_scope)

with tabs[2]:
    st.subheader('Recorded competency performance')
    st.caption('Programme-level figures from Competency Based Inputs (wip). The sheet does not provide zone-specific results or a measurement date. Duplicate labels are retained because their source rows differ.')
    subject = st.selectbox('Subject', ['All subjects', 'Numeracy', 'Literacy'])
    rows = [r for r in data['competencies'] if subject == 'All subjects' or r['Subject'] == subject]
    table(rows)
    st.info('Zone literacy/numeracy proficiency, student counts and changes over time: Not available from this source.')

with tabs[3]:
    st.subheader('Teacher-practice targets')
    st.caption('Targets and weights from TP adoption KPI and targets. These are planned thresholds, not measured adoption results.')
    table(data['practice_targets'])
    st.info('Observed adoption scores and zone comparisons: Not available. Classroom-observation records are required.')

with tabs[4]:
    st.subheader('Field operations')
    st.caption('Programme-wide records. Separate periods remain separate; blank achievements are not converted into zero. Ambiguous and missing zone assignments are shown as recorded.')
    table(data['visit_reach'])
    periods = list(dict.fromkeys(r['Period'] for r in data['visits']))
    period = st.selectbox('Recorded period', periods)
    visits = [r for r in data['visits'] if r['Period'] == period]
    numeric = [r['Achieved'] for r in visits if isinstance(r['Achieved'], (int, float))]
    st.metric('Sum of reported numeric achievements', display(sum(numeric) if numeric else None))
    st.caption(f"{len(numeric)} of {len(visits)} displayed records have numeric achievements. This is not a count of unique schools.")
    table(visits)

with tabs[5]:
    st.subheader('Competency pack evidence')
    st.info('Pack receipt, engagement, implementation and mastery funnels: Not available. The workbook describes inputs and plans but does not supply the school-level delivery/event records required for these counts.')
    st.write('Available competency performance and targets are shown in Student Learning & SLOs. Pack-level outcomes must not be inferred from these programme-level figures.')

with tabs[6]:
    st.subheader('Results framework')
    st.caption('Source fields are preserved as text, including old/new-zone distinctions and unavailable entries. Baselines and targets are not current measured impact.')
    table(data['framework'])
    st.info('Difference-in-differences, causal impact and zone uplift: Not available. Comparable dated treatment/control assessment records are required.')

with tabs[7]:
    st.subheader('Recorded risks and decisions')
    st.caption('Programme-wide entries from Accountability & Risk, with original dates. No current open/closed status is inferred.')
    severity = st.selectbox('Severity', ['All severities'] + sorted({r['Severity'] for r in data['risks'] if r['Severity']}))
    table([r for r in data['risks'] if severity == 'All severities' or r['Severity'] == severity])

with tabs[8]:
    st.subheader('School evidence brief')
    if school_scope:
        mapping = {s['School ID']: s for s in school_scope}
        school_id = st.selectbox('School', list(mapping), format_func=lambda value: f"{mapping[value]['School']} · {value}")
        table([mapping[school_id]])
        st.info('School-specific mastery, last visit, RAG status and AI diagnosis: Not available. Allocation data alone cannot support a learning diagnosis or a coaching recommendation.')
    else:
        st.info('Select a zone and PoC with school allocations.')

st.divider()
st.caption('Tech Team, Peepul')
