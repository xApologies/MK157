"""Read-only, bounded validation of the October 8 Red/Orange author correction.

Historical checkpoint packages remain exact. Only the listed current owners can
change, with every current data row compared to an explicit transform of the
pre-integration Git revision. Later seasons and fixed reward tables are untouched.
"""
from copy import deepcopy
import csv
import io
import json
import subprocess

BASELINE = 'd2e6a9eded93b0cc4061952a8e381875f06d86c9'
PREFIX = 'provenance/diplomatic-pouch-2026-10-08/'
SOURCE = PREFIX + 'package/red-orange-reconciliation/package/'
STEMS = ('RED_TO_ORANGE_COMBAT_CALENDAR', 'ARC3_ORANGE_CALENDAR',
         'ILLI_AUTHOR_PROGRESSION_LEDGER', 'ILLI_PROGRESSION_SKELETON')
DATA_PATHS = {f'world-clock/{s}.{e}' for s in STEMS for e in ('csv', 'json')} | {
    'world-clock/WORLD_CLOCK_TEMPLATE.csv', 'world-clock/ARC4_HANDOFF.json'}
PROSE_PATHS = {'world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.md',
               'world-clock/ARC3_ORANGE_CALENDAR.md', 'world-clock/ARC4_HANDOFF.md'}
NUMERIC = {
    'RED_TO_ORANGE_COMBAT_CALENDAR': ('week','day','illi_credits_earned','purchase_cost','illi_running_balance'),
    'ARC3_ORANGE_CALENDAR': ('week','day','illi_credit','kira_credit'),
    'ILLI_AUTHOR_PROGRESSION_LEDGER': ('week','day','cost','cumulative_progression_spend'),
    'ILLI_PROGRESSION_SKELETON': ('week','day'),
}


def reconcile_dates(rows):
    """Move precisely PC Blue/Legacy and Absorption; retain all other fields."""
    result = deepcopy(rows)
    for row in result:
        if row['season'] != 'Orange':
            continue
        key = row.get('purchase_or_upgrade', row.get('binding'))
        if row['week'] == 1 and key in ('Persistent Coherence → Blue','Accept White Legacy','Persistent Coherence','White Legacy'):
            if row['day'] != 4: raise ValueError('Unexpected prior PC/Legacy date')
            row['day'] = 3
        elif row['week'] == 2 and key in ('Absorption Shield → Red','Absorption Shield'):
            if row['day'] != 3: raise ValueError('Unexpected prior Absorption date')
            row['day'] = 2
            if 'note' in row:
                row['note'] = 'Immediate same-day purchase after Duo W10; White Legacy celebration.'
    return result


def reconcile_red(rows):
    result=deepcopy(rows);lookup={(r['season'],r['week'],r['day']):r for r in result}
    def r(s,w,d):return lookup[(s,w,d)]
    r('Red',2,5)['author_notes'] += ' Intentional bad run, not capability ceiling; healing tunnel vision/missed flank/death, then abecca/raeon decompression. Booked W2 remains140.'
    r('Red',3,2).update(result='Fire Dragon Red-A CLEAR; Shardfield Orange-B repeated FAIL',author_notes='Group dissolves after failed Shardfield pulls; booked Red first-clear2500 retained.')
    r('Red',4,1)['author_notes'] += ' Old W3 is minimum accounting, not a capability ceiling; variable Solo frontier and any actual excess reward remain OPEN.'
    r('Red',4,5)['author_notes'] += ' Authored BONUS Burrower Red-B CLEAR:2500 each actual/discretionary surplus, excluded from this minimum progression ledger.'
    r('Red',5,4).update(kira_combat='OPEN / recovery-social',illi_combat='OPEN / recovery-social',author_notes='OPEN; prior seasonal raeon participation/elimination removed by explicit October8 correction. Daily10:00 raeon remains separate.')
    r('Red',6,4)['author_notes'] += ' PC Green followed by bookstore007; optional Solo/top-off credits OPEN.'
    r('Red',6,6).update(result='Red repeat: no major reward; Coherence Twins Orange-A CLEAR',author_notes='Repeated failures; overlapping mutual coherence requires working5/5 separation. Existing3750 minimum reward retained.')
    r('Red',7,6)['author_notes'] += ' 10:00 SEASONAL raeon entry and EARLY KNOCKOUT, then the existing same-day Duo W10 clear;1950 and running balance unchanged. No global tournament cadence inferred.'
    for week,old_day,new_day in ((1,4,3),(2,3,2)):
        old,new=r('Orange',week,old_day),r('Orange',week,new_day)
        assert new['purchase_cost']==0
        new['purchase'],new['purchase_cost']=old['purchase'],old['purchase_cost']
        old['purchase'],old['purchase_cost']='',0
    r('Orange',1,3)['author_notes']='Duo W10 then IMMEDIATE PC Blue/White Legacy same day:24707+1950=26657; minus25705 leaves952.'
    r('Orange',1,4).update(kira_combat='OPEN / recognition-social',illi_combat='OPEN / recognition-social',author_notes='No required purchase/combat. White-Legacy recognition/royal aftermath after O1D3 acceptance.')
    r('Orange',1,5)['author_notes']='Girls day Elara+Kira+illi+Naira+Laina; no required combat.'
    r('Orange',1,6).update(result='Sixfold CLEAR; Triumvirate CLEAR; Black Orchard FAIL; Weaver/Wayfarer/Bloom NOT ATTEMPTED',author_notes='Two Red first-clears5000 each actual total; Sixfold2500 booked here, Triumvirate2500 actual/discretionary surplus outside minimum. ZERO Orange reward. No Red reward again O4D2.')
    r('Orange',2,2)['author_notes']='Duo W10 then IMMEDIATE Absorption Red same day:7442+1950=9392; minus9350 leaves42. Major White-Legacy celebration.'
    r('Orange',2,3).update(kira_combat='CSR purchase61017 later; family-smithy/social',illi_combat='Optional early Solo W7 CLEAR/W8 FAIL; reward OPEN',author_notes='CSR exact purchase day O2D3 LOCKED;61017 Kira-specific cost, not charged to illi ledger. Early illi Solo milestone explicit but optional credits remain OPEN and unbooked.')
    balance=2000
    for row in result:
        balance+=row['illi_credits_earned']-row['purchase_cost'];row['illi_running_balance']=balance
    return result


def reconcile_arc3(rows):
    result=deepcopy(rows);lookup={(r['week'],r['day']):r for r in result}
    lookup[(2,5)]['notes']='Optional failed Black Orchard daytime Raid/no reward; Kira late Solo W13 remains3305 Kira-only.'
    lookup[(3,3)]['notes']='About4 Yellow Dungeon attempts, all FAIL; group fizzles. No invented partial/completion reward.'
    lookup[(3,4)]['notes']='illi independent Solo frontier, no new validated milestone or guessed credits. Kira leisure then late-night Solo W14 CLEAR;3855 Kira-only unchanged.'
    lookup[(4,2)].update(event='Normal Raid: Black Orchard Orange-A; optional Red repeats',status='ORANGE CLEAR / RED REPEAT UNPAID',illi_credit=3750,kira_credit=3750,notes='Both Orange-season Normal Reds already claimed O1D6. NO Red reward. Black Orchard first-clear3750 each ONLY; no third Red. Earlier second-Red2500 remains actual/discretionary income.')
    for date in ((5,1),(5,6)):
        lookup[date].update(event='OPEN — social / independent life / recovery',kind='OPEN',duration='',status='',notes='Prior seasonal qualification/elimination removed. Daily10:00 raeon is separate; no required combat.')
    lookup[(6,5)]['notes']='First Hard Raid: same seasonal bosses as Normal, continuous hostile environment, no systemic fatigue reset, locked roster/no re-entry or replacement. Existing Red clear3750/Orange fail retained; no extra boss clearance inferred.'
    lookup[(6,6)]['notes']='OPEN; optional/WORKING DAILY10:00 raeon, not seasonal. No required combat.'
    lookup[(7,5)].update(event='Mandatory post-domai recovery / otherwise OPEN',kind='Recovery',notes='Full mandatory recovery; prior championship viewing removed. No combat.')
    lookup[(7,6)]['notes']='10:00 SEASONAL raeon entry -> EARLY KNOCKOUT -> later same-day Duo W17 CLEAR5805. Recovery lock has elapsed; no global tournament cadence inferred.'
    return result


CLOCK_OVERLAY = {
    ('Red','5'): ('D1-D2 domai; D3 recovery; D4 OPEN/no seasonal tournament.',)*2,
    ('Red','7'): ('D6 10:00 seasonal raeon entry/early knockout -> same-day Duo W10 clear1950; D7 Orange x2 unchanged2040. Daily raeon separate.',)*2,
    ('Orange','1'): (None,'D3 Duo W10 -> immediate Persistent Coherence Blue/White Legacy acceptance; cost25705; minimum952. D4 recognition/royal aftermath; no required purchase/combat.'),
    ('Orange','2'): ('D3 CSR purchase61017 LOCKED; D4 Green Duo W13; D5 late Solo W13 with optional daytime Black Orchard FAIL/no reward; D6 Orange x2; D7 social.', 'D2 Duo W10 -> immediate Absorption Red9350; minimum42. D3 optional early Solo W7 clear/W8 fail, credits OPEN. D4 Duo W13; D6 Orange x2; D7 social.'),
    ('Orange','3'): (None,'D1/D7 Duo W14; D3 Yellow Dungeon FAIL; D4 optional Solo frontier/no validated milestone or guessed reward; D5 Orange Dungeon; D2 girls day/D6 royal family.'),
    ('Orange','4'): ('D1 late Solo W14; D2 Black Orchard clear3750 only, Red repeats unpaid; D4 Duo W15; D6 Orange x2; D7 formalwear/private gala.', 'D2 Black Orchard clear3750 only, Red repeats unpaid; D4 Duo W15; D6 Orange x2; D7 formalwear/private gala.'),
    ('Orange','5'): ('D1/D6 OPEN, no seasonal qualification/elimination; D2 Duo W15; D3 late Solo W15; D4 Yellow FAIL; D5/D7 OPEN.', 'D1/D6 OPEN, no seasonal qualification/elimination; D2 Duo W15; D4 Yellow FAIL; D5/D7 OPEN.'),
    ('Orange','7'): ('D1/D6 Duo W17; D2 late Solo W16; D3-D4 domai/exit; D5 full recovery/otherwise OPEN, no championship viewing; D6 10:00 seasonal entry/early knockout before Duo5805; D7 Orange Dungeon1020. Actual card funding OPEN.', 'D1/D6 Duo W17; D3-D4 domai/exit; D5 full recovery/otherwise OPEN, no championship viewing; D6 10:00 seasonal entry/early knockout before Duo5805; D7 Orange Dungeon1020; Y1D2 Beam reserve6050.'),
}


def reconcile_clock(rows):
    result=deepcopy(rows)
    for row in result:
        pair=CLOCK_OVERLAY.get((row['season'],row['week']))
        if pair:
            for key,value in zip(('kira_clock','illi_clock'),pair):
                if value is not None:row[key]=value
    return result


def expected_data(path,before):
    if path.endswith('WORLD_CLOCK_TEMPLATE.csv'):
        return reconcile_clock(list(csv.DictReader(io.StringIO(before.decode('utf-8-sig')))))
    data=json.loads(before)
    if path.endswith('RED_TO_ORANGE_COMBAT_CALENDAR.json'):return reconcile_red(data)
    if path.endswith('ARC3_ORANGE_CALENDAR.json'):return reconcile_arc3(data)
    if 'ILLI_' in path:return reconcile_dates(data)
    if path.endswith('ARC4_HANDOFF.json'):
        data['preserved_orange_gross']={'illi':56385,'kira':81415};return data
    raise ValueError('Unapproved reconciliation path:'+path)


def check_data(path, before, after):
    if after != expected_data(path, before):
        raise ValueError('Unapproved reconciliation data:' + path)


def audit(root, require_promotion=True):
    git=['git','-c',f'safe.directory={root.as_posix()}','-C',str(root)]
    def old(path):return subprocess.check_output(git+['show',BASELINE+':'+path])
    def require(ok,msg):
        if not ok:raise ValueError(msg)
    if require_promotion:
        from validate_promotions import audit_promotions
        promotions=audit_promotions(root,git,require,lambda p:require((root/p.split('#',1)[0]).exists(),'Missing target:'+p))
        required={SOURCE+n for n in ('CORE_AND_RED.md','ORANGE_W1_W4.md','ORANGE_W5_W7.md','ORANGE_NORMAL_RAID_ROSTER.md','HARD_RAID_DOCTRINE.md','VERIFY_AFTER.md')}
        require(required<=promotions['source_paths'],'Missing reconciliation source accounting')
        require(DATA_PATHS|PROSE_PATHS <= promotions['changed'],'Unaccounted reconciliation owner')
    for stem in STEMS:
        path=f'world-clock/{stem}.json'; expected=expected_data(path,old(path))
        actual=json.loads((root/path).read_text(encoding='utf-8-sig'))
        check_data(path,old(path),actual)
        with (root/f'world-clock/{stem}.csv').open(encoding='utf-8-sig',newline='') as f:mirror=list(csv.DictReader(f))
        for row in mirror:
            for key in NUMERIC[stem]:row[key]=int(row[key])
        require(mirror==expected,'CSV mirror differs:'+stem)
    for path in ('world-clock/WORLD_CLOCK_TEMPLATE.csv','world-clock/ARC4_HANDOFF.json'):
        expected=expected_data(path,old(path))
        if path.endswith('.csv'):
            with (root/path).open(encoding='utf-8-sig',newline='') as f:actual=list(csv.DictReader(f))
        else:actual=json.loads((root/path).read_text(encoding='utf-8-sig'))
        check_data(path,old(path),actual)
    for path in ('combat-rewards/COMBAT_REWARD_TABLES.json',
                 'trial-rewards/TRIAL_WAVE_CREDITS.json'):
        require((root/path).read_bytes()==old(path),'Fixed reward table changed:'+path)
    return {'result':'PASS','source':SOURCE,'baseline':BASELINE,'data_files':len(DATA_PATHS),
            'arc3_gross':{'illi':56385,'kira':81415},'PC_Blue':'O1D3','Absorption_Red':'O2D2',
            'CSR':'O2D3','later_clock_rows_unchanged':35,'fixed_reward_tables_unchanged_by_correction':True}


def validated_replacements(root):
    audit(root)
    return DATA_PATHS | PROSE_PATHS


def historical_clock_view(root, rows):
    """Only after validating current data, restore scoped cells for old audits."""
    audit(root)
    git=['git','-c',f'safe.directory={root.as_posix()}','-C',str(root)]
    before=list(csv.DictReader(io.StringIO(subprocess.check_output(git+['show',BASELINE+':world-clock/WORLD_CLOCK_TEMPLATE.csv']).decode('utf-8-sig'))))
    lookup={(r['season'],r['week']):r for r in before};result=deepcopy(rows)
    for row in result:
        key=(row['season'],row['week'])
        if key in CLOCK_OVERLAY:
            for field,value in zip(('kira_clock','illi_clock'),CLOCK_OVERLAY[key]):
                if value is not None:row[field]=lookup[key][field]
    return result


if __name__=='__main__':
    from pathlib import Path
    print(json.dumps(audit(Path(__file__).resolve().parents[2]),indent=2))
