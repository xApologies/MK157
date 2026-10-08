"""Reject unapproved payouts, dates and later-season edits in the new overlay."""
from copy import deepcopy
from pathlib import Path
import subprocess
import unittest

from validate_red_orange_reconciliation import BASELINE, expected_data, check_data


class ReconciliationFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[2]
        git=['git','-c',f'safe.directory={root.as_posix()}','-C',str(root)]
        paths=('world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.json',
               'world-clock/ARC3_ORANGE_CALENDAR.json',
               'world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json',
               'world-clock/WORLD_CLOCK_TEMPLATE.csv')
        cls.before={p:subprocess.check_output(git+['show',BASELINE+':'+p]) for p in paths}

    def test_immediate_purchases_preserve_costs_and_end_balances(self):
        p='world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.json'
        data=expected_data(p,self.before[p]);lookup={(r['season'],r['week'],r['day']):r for r in data}
        self.assertEqual((lookup[('Orange',1,3)]['purchase_cost'],lookup[('Orange',1,3)]['illi_running_balance']),(25705,952))
        self.assertEqual((lookup[('Orange',2,2)]['purchase_cost'],lookup[('Orange',2,2)]['illi_running_balance']),(9350,42))
        check_data(p,self.before[p],data)
        for date in (('Orange',2,3),('Red',4,5)):
            changed=deepcopy(data);next(r for r in changed if (r['season'],r['week'],r['day'])==date)['illi_credits_earned']+=2500
            with self.assertRaises(ValueError):check_data(p,self.before[p],changed)

    def test_duplicate_raid_reward_and_lost_duo_are_rejected(self):
        p='world-clock/ARC3_ORANGE_CALENDAR.json';data=expected_data(p,self.before[p])
        self.assertEqual(sum(r['illi_credit'] for r in data),56385)
        self.assertEqual(sum(r['kira_credit'] for r in data),81415)
        for date,field,value in (((4,2),'illi_credit',6250),((7,6),'kira_credit',0),((3,4),'event','OPEN')):
            changed=deepcopy(data);next(r for r in changed if (r['week'],r['day'])==date)[field]=value
            with self.assertRaises(ValueError):check_data(p,self.before[p],changed)

    def test_later_milestone_and_cost_changes_are_rejected(self):
        p='world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json';data=expected_data(p,self.before[p])
        for index,field in ((7,'day'),(4,'cost'),(18,'cumulative_progression_spend')):
            changed=deepcopy(data);changed[index][field]+=1
            with self.assertRaises(ValueError):check_data(p,self.before[p],changed)

    def test_no_global_tournament_rewrite_or_row_reorder(self):
        p='world-clock/WORLD_CLOCK_TEMPLATE.csv';data=expected_data(p,self.before[p])
        for index,field in ((0,'raeon_tournament'),(14,'kira_clock'),(48,'raeon_tournament')):
            changed=deepcopy(data);changed[index][field]='rewritten'
            with self.assertRaises(ValueError):check_data(p,self.before[p],changed)
        changed=deepcopy(data);changed[0],changed[1]=changed[1],changed[0]
        with self.assertRaises(ValueError):check_data(p,self.before[p],changed)


if __name__=='__main__':unittest.main()
