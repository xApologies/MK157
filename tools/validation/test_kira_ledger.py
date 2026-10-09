import unittest
from validate_kira_ledger import earned_for_event, coverage_report, row_differences, check_armor_only_rows


class KiraLedgerTests(unittest.TestCase):
    tables=({5:565,8:1275}, {'Red':395,'Orange':1020}, {'Red':2500,'Orange':3750})

    def row(self,event,kira,**kw):
        return dict(season='Red',week='1',day='2',combat_event=event,kira_combat=kira,
                    illi_credits_earned='999999',**kw)

    def test_duo_ignores_illi_amount(self):
        self.assertEqual(earned_for_event(self.row('Duo Trial W5','Duo Trial'),self.tables)[0],565)

    def test_kira_solo_and_illi_exclusion(self):
        self.assertEqual(earned_for_event(self.row('Kira Solo Trial','Solo Trial W8'),self.tables)[0],1275)
        self.assertEqual(earned_for_event(self.row('illi Solo Trial W2','OPEN / rest'),self.tables)[0],0)

    def test_dungeon_count(self):
        self.assertEqual(earned_for_event(self.row('Orange Dungeon ×2','Orange Dungeons ×2'),self.tables)[0],2040)

    def test_unknown_event_fails(self):
        with self.assertRaises(ValueError):earned_for_event(self.row('Unplaced bonus Raid','Normal Raid'),self.tables)

    def test_locked_spend_can_fail_affordability(self):
        report=coverage_report(63705,2000,5000,61017)
        self.assertEqual(report['result'],'FAIL')
        self.assertEqual(report['known_transaction_balance_after_CSR'],-312)
        self.assertIn('shortfall 312',report['failure_detail'])

    def test_exact_armor_consumes_grant(self):
        report=coverage_report(63705,2000,2000,61017)
        self.assertEqual(report['actual_pre_CSR_balance'],63705)
        self.assertEqual(report['actual_post_CSR_balance'],2688)

    def test_armor_fix_cannot_change_reward_or_csr(self):
        before=[{'event':'Entry grant','kira_progression_spend':0,'kira_known_running_balance':2000,'notes':''},
                {'event':'Armor of the Abyss old','source_kind':'old','kira_progression_spend':None,'kira_known_running_balance':2000,'notes':''},
                {'event':'CSR','kira_credits_earned':0,'kira_progression_spend':61017,'kira_known_running_balance':4688,'notes':''}]
        after=[dict(x) for x in before]
        after[1].update(event='Armor of the Abyss — initial acquisition',source_kind='Locked progression spend',kira_progression_spend=2000,kira_known_running_balance=0)
        after[2]['kira_known_running_balance']=2688
        check_armor_only_rows(before,after)
        for field,value in [('kira_credits_earned',1),('kira_progression_spend',61016)]:
            bad=[dict(x) for x in after];bad[2][field]=value
            with self.assertRaises(ValueError):check_armor_only_rows(before,bad)

    def test_row_diff_reports_added_missing_and_tampered_rewards(self):
        source=[{'event':'source clear','earned':2500}]
        self.assertEqual(row_differences(source,[{'event':'source clear','earned':5000}])[0]['source_expected'],source[0])
        self.assertEqual(len(row_differences(source,[])),1)
        self.assertEqual(len(row_differences([],source)),1)


if __name__=='__main__':unittest.main()
