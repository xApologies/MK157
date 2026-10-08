import unittest
from validate_full_repair import check_calendar_audit


class FullRepairGuardTests(unittest.TestCase):
    def test_fresh_audit_only(self):
        expected={'purchase_gates':[{'week':1,'day':3,'balance_after':952}]}
        check_calendar_audit('world-clock/CALENDAR_AUDIT.json',expected,expected)
        with self.assertRaises(ValueError):
            check_calendar_audit('world-clock/CALENDAR_AUDIT.json',expected,{'purchase_gates':[{'week':1,'day':4,'balance_after':952}]})

    def test_never_exempts_calendar_or_other_audit(self):
        for path in ('world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.json','world-clock/ARC7_ECONOMY_AUDIT.json'):
            with self.assertRaises(ValueError):check_calendar_audit(path,{}, {})


if __name__=='__main__':unittest.main()
