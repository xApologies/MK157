import csv
import io
import unittest

from validate_clock_promotion import OLD, NEW, check_clock_bytes, check_prose_bytes
from validate_clock_promotion import check_calendar_annotation, REPAIR_CALENDAR_PROSE


class ClockPromotionTests(unittest.TestCase):
    def fixture(self):
        stream = io.StringIO(newline='')
        writer = csv.writer(stream)
        writer.writerow(['season', 'week', 'nightly_highlights', 'kira_clock'])
        for season in ('Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Violet', 'White'):
            for week in range(1, 8):
                writer.writerow([season, week, OLD, 'preserved character overlay'])
        return stream.getvalue().encode()

    def test_clock_accepts_only_full_timestamp_correction(self):
        old = self.fixture()
        check_clock_bytes(old, old.replace(OLD.encode(), NEW.encode()))
        for changed in (old, old.replace(b'25:00', b'27:00', 48),
                        old.replace(b'25:00', b'28:00'),
                        old.replace(b'25:00', b'27:00').replace(b'preserved', b'changed')):
            with self.subTest(changed=changed[:40]), self.assertRaises(ValueError):
                check_clock_bytes(old, changed)

    def test_clock_rejects_reordered_rows(self):
        old = self.fixture()
        rows = old.replace(b'25:00', b'27:00').splitlines(keepends=True)
        rows[1], rows[2] = rows[2], rows[1]
        with self.assertRaises(ValueError):
            check_clock_bytes(old, b''.join(rows))

    def test_prose_does_not_exempt_existing_content(self):
        for path in ('live-model/PRISM.md', 'builder/COMMUNITY.md'):
            check_prose_bytes(path, b'old source\r\n', b'old source\r\nnew detail\r\n')
            with self.assertRaises(ValueError):
                check_prose_bytes(path, b'old source\r\n', b'changed source\r\nnew detail\r\n')
        path = 'world-clock/ARC5_DIRECTOR_CALENDAR.md'
        check_prose_bytes(path, b'25:00; fixed combat', b'27:00; fixed combat')
        with self.assertRaises(ValueError):
            check_prose_bytes(path, b'25:00; fixed combat', b'27:00; moved combat')
        with self.assertRaises(ValueError):
            check_prose_bytes('combat-rewards/RAID_BOSS_REWARDS.csv', b'old', b'old new')

    def test_repair_cannot_rewrite_prior_calendar_prose(self):
        before = b'Minimum balance 952; purchase 25705\r\n'
        for path in REPAIR_CALENDAR_PROSE:
            check_calendar_annotation(path, before, before + b'Explicit later annotation\r\n')
            for after in (before, before.replace(b'952', b'3452') + b'annotation',
                          before.replace(b'\r\n', b'\n') + b'annotation'):
                with self.subTest(path=path, after=after), self.assertRaises(ValueError):
                    check_calendar_annotation(path, before, after)

    def test_repair_does_not_exempt_calendar_data_or_other_prose(self):
        for path in ('world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.csv',
                     'world-clock/ARC3_ORANGE_CALENDAR.json',
                     'world-clock/ARC6_DIRECTOR_CALENDAR.md'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                check_calendar_annotation(path, b'original', b'original annotation')


if __name__ == '__main__':
    unittest.main()
