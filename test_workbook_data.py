import io
import json
from pathlib import Path
import unittest
from workbook_data import read_workbook, zone_evidence


class SnapshotChecks(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path(__file__).with_name('workbook_snapshot.json').read_text(encoding='utf-8'))

    def test_source_reconciliation(self):
        self.assertEqual(len(self.data['schools']), 479)
        self.assertEqual(len({s['School ID'] for s in self.data['schools']}), 479)
        self.assertEqual(sum(t['HoS attended'] for t in self.data['training']), 408)
        self.assertEqual(sum(t['Teacher batches completed'] for t in self.data['training']), 16)
        self.assertEqual(sum(t['Teacher batches planned'] for t in self.data['training']), 20)

    def test_visit_period_and_missing_values(self):
        first = [r for r in self.data['visits'] if r['Period'] == '11th September 2026']
        megha = next(r for r in first if r['Team member'] == 'Megha')
        self.assertEqual((megha['Planned'], megha['Achieved']), (1, 1))
        geeta = next(r for r in first if r['Team member'] == 'Geeta')
        self.assertEqual((geeta['Planned'], geeta['Achieved']), (2, 2))
        self.assertEqual(geeta['Zone as recorded'], 'Civil Lines')
        self.assertEqual(sum(r['Achieved'] for r in first if r['Achieved'] is not None), 19)
        later = [r for r in self.data['visits'] if r['Period'] != '11th September 2026']
        self.assertTrue(any(r['Achieved'] is None for r in later))

    def test_brief_has_only_verified_zone_evidence(self):
        evidence = zone_evidence(self.data, 'West')
        self.assertEqual(evidence['school_count'], 127)
        self.assertNotIn('lit_prof', evidence)
        self.assertNotIn('red_schools', evidence)
        self.assertEqual(evidence['training']['Teacher batches completed'], 4)

    def test_contact_fields_excluded(self):
        for school in self.data['schools']:
            self.assertNotIn('Phone Number', school)
            self.assertNotIn('Principal/School Incharge Name', school)


if __name__ == '__main__':
    unittest.main()
