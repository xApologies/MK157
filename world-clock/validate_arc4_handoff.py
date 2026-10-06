"""Validate cumulative Checkpoint 20–22 handoff locks and preserved calendars."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

BASELINE='ca6481ec0bb0bd6baf7c9d6a63d53dfb6902c02d'


def audit(root):
    errors=[]
    def require(ok, message):
        if not ok: errors.append(message)
    def read(p): return (root/p).read_text(encoding='utf-8-sig')
    def js(p): return json.loads(read(p))
    def old(p):
        return subprocess.check_output(['git','-c',f'safe.directory={root.as_posix()}', 'show',f'{BASELINE}:{p}'],cwd=root)
    handoff=js('world-clock/ARC4_HANDOFF.json')
    ledger=js('world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json')
    dates=[('Yellow',2,4),('Yellow',3,5),('Yellow',5,2),('Yellow',6,3)]
    events=[r for r in ledger if (r['season'],r['week'],r['day']) in dates]
    require([(r['season'],r['week'],r['day']) for r in events]==dates, 'Arc Four milestone dates/order mismatch')
    require([r['cost'] for r in events]==[9680,17424,36590,9350], 'Arc Four costs mismatch')
    require(handoff['illi_arc4_milestones']==events, 'Arc Four handoff differs from authoritative ledger')
    require(handoff['beam_ranking_subtotal']==sum(r['cost'] for r in events[:3])==63694, 'Beam ranking subtotal mismatch')
    require(handoff['illi_post_beam_red_total']==sum(r['cost'] for r in events)==73044, 'Arc Four post-Beam-Red total mismatch')
    beam=next(r for r in ledger if r['purchase_or_upgrade']=='Genesis Beam → Red')
    require((beam['season'],beam['week'],beam['day'],beam['cost'])==('Yellow',1,2,6050), 'Beam Red moved or repriced')
    require(handoff['illi_beam_red_before_arc4']=={k:beam[k] for k in ('season','week','day','cost')}, 'Beam Red boundary mismatch')
    require(len(ledger)==19 and sum(r['cost'] for r in ledger)==292772, 'Full progression ledger mismatch')
    card=handoff['kira_card'];orbs=handoff['kira_orbs']
    require(card['price']==86000 and card['item']=='Specific Blue Fireball Genesis Card', 'Specific card price/identity changed')
    require(card['universal_blue_card_price'] is False and card['grants_binding'] is False, 'Collectible pricing/Binding firewall lost')
    require(card['exact_intraday_timestamp'] is None and card['funding_reconciliation'].startswith('OPEN'), 'Invented timestamp/funding')
    require(orbs=={'price':61017,'arc':4,'date':'Y6D2','date_status':'LOCKED exact day; acquisition is not mastery',
                  'seasonal_window':'Late Yellow',
                  'excluded_date':'Yellow W1 D2','arc_three_endpoint_purchase':False,'fund_rebuilt_after_card':True}, 'Orbs timing/price boundary changed')
    require(handoff['arc_closures']=={
        '1':['illi Persistent Coherence Red','Kira Armor of the Abyss'],
        '2':['illi White Legacy and Absorption Shield Red','Kira CSR'],
        '3':['illi Genesis Beam Red at Yellow W1 D2','Kira specific Blue Fireball Genesis Card at the Yellow-opening boundary'],
        '4':['illi Genesis Prime Elemental Red at Yellow W6 D3'],
        '5':['illi Coherence Prime Elemental Red at Green W6 D2']}, 'Arc closure mismatch')
    price=js('economy/KIRA_BLACK_ACQUISITION_PRICES.json');old_price=json.loads(old('economy/KIRA_BLACK_ACQUISITION_PRICES.json'))
    require({k:v for k,v in price.items() if k!='acquisition_dates'}=={k:v for k,v in old_price.items() if k!='acquisition_dates'}, 'Black price data changed beyond timing note')
    require(price['post_armor_acquisition_prices']==dict.fromkeys(('CSR','Genesis Orbs','Halo','Domain'),61017), 'Black tier repriced')
    require('not Yellow W1 D2' in price['acquisition_dates'] and 'Yellow W6 D2 (Y6D2)' in price['acquisition_dates'], 'Active price record timing stale')
    first=handoff['kira_first_yellow_dungeon']
    require(first=={'arc':4,'mode':'Normal','day':'Y4D2','status':'LOCKED dated story beat and completion payout',
        'illi_present':False,'illi_clearance_at_event':'Orange','competent_group':True,'eligibility_rules_preserved':True}, 'Yellow clear scope/date/eligibility altered')
    require(handoff['checkpoint']==22 and handoff['new_daily_combat_schedule']=='YELLOW_DIRECTOR_CALENDAR.json', 'Checkpoint 22 supplied calendar missing')
    require(handoff['yellow_deterministic_gross']=={'illi':71280,'kira':80140}
            and handoff['arc4_deterministic_gross']=={'illi':58170,'kira':67030}, 'Current income scopes mismatch')
    require(handoff['arc5_open']=='Y6D4' and handoff['first_builder_invitation']=='Y5D3'
            and handoff['first_builder_party']=='Y5D5', 'New arc/social boundaries mismatch')
    require(handoff['social_cadence']=={'abecca':'abecca','gala_per_season':1,'gala_dates':None,
        'daily_circuit_mandatory':False,'highlights_attendance_every_night':False,'open_days_auto_filled':False}, 'Social cadence/spelling/negative space mismatch')
    require(handoff['credit_transfers']=={'social_civic_non_progression_gifts_allowed':True,
        'binding_rank_progression_financing_allowed':False,'indirect_progression_shortcuts_allowed':False,
        'enforcement_ui_limits':'OPEN'}, 'Gift/progression firewall mismatch')
    require(handoff['domai_payout']=='OPEN BY DESIGN' and 'OPEN' in handoff['foundation_patent_royalty_rules'], 'OPEN scoring/legal boundary lost')
    require(handoff['preserved_orange_gross']=={'illi':58885,'kira':83915}, 'Orange gross changed')

    protected=['world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.csv','world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.json',
       'world-clock/ARC3_ORANGE_CALENDAR.csv','world-clock/ARC3_ORANGE_CALENDAR.json',
       'world-clock/WORLD_CLOCK_TEMPLATE.csv','world-clock/PRISM_TEAM_TRACKER.csv',
       'world-clock/ILLI_PROGRESSION_SKELETON.csv','world-clock/ILLI_PROGRESSION_SKELETON.json',
       'world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.csv','world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json',
       'trial-rewards/TRIAL_WAVE_CREDITS.csv','trial-rewards/TRIAL_WAVE_CREDITS.json',
       'combat-rewards/COMBAT_REWARD_TABLES.json','combat-rewards/DOMAI_PARTICIPATION_RULES.json',
       'bindings/PRICING_CLASS_MATRIX.json','live-model/AITHREN_VAELUM_ACCORD.md']
    protected=[p for p in protected if p not in {'trial-rewards/README.md', 'combat-rewards/COMBAT_REWARD_TABLES.json', 'combat-rewards/DOMAI_PARTICIPATION_RULES.json', 'combat-rewards/validate_rewards.py', 'world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.json', 'world-clock/WORLD_CLOCK_TEMPLATE.csv', 'world-clock/ILLI_PROGRESSION_SKELETON.csv', 'world-clock/ILLI_AUTHOR_PROGRESSION_LEDGER.csv', 'world-clock/ILLI_PROGRESSION_SKELETON.json'}]
    for path in protected: require((root/path).read_bytes()==old(path), 'Protected file changed: '+path)
    source=read('provenance/checkpoint-20-package/CHECKPOINT20_LIVE_MODEL_DELTA.md')
    require(read('live-model/27_CHECKPOINT_20_SOCIAL_LIFE_ARC4.md').endswith(source), 'Exhaustive author delta not retained')
    # These are documentation requirements, not substitute claims of economic solvency or legal implementation.
    content={
      'world-clock/ARC4_HANDOFF.md':['not acquired at Y1D2','86,000','73,044','2,085','funding remains OPEN',
        'first of the pair','illi remains Orange-cleared','omniscient','seven-day','inside Arc Four'],
      'live-model/SOCIAL_LIFE_AND_FOUNDATIONS.md':['**`abecca`**','A-B-E-C-C-A','around', 'Tea House','Tea Party',
        'charity/foundation','age 17','marriage','merchant','research','royalties','public','patent','OPEN',
        'may **not** finance Binding acquisition','Indirect routing','One seasonal Gala per season',
        'Builder parties','deck-building','collecting/trading','nothing','two distinct flagship spaces'],
      'live-model/GENESIS_CARDS.md':['86,000','only this collectible','does not grant Fireball','childhood','CSR','delighted'],
      'live-model/ECONOMY_PURCHASE_SCHEDULE.md':['world events → organic combat → gross income → card/life spending → terminal progression',
        'progression and indirect shortcuts are prohibited','73,044'],
      'live-model/ILLI_PROGRESSION.md':['Y2D4','Y3D5','Y5D2','Y6D3','73,044','No clear or reward is credited to absent illi'],
      'live-model/01_KIRA.md':['abecca','86,000','high-demand','fame never bypasses','Y6D2'],
      'live-model/OPEN.md':['credit-transfer UI/limits/tracking/anti-circumvention','royalty rates','exact Orbs **Y6D2**'],
      'live-model/DOMAI_PARTICIPATION.md':['7-day','one full day','0.8^deaths','group_award / eligible_members','OPEN'],
    }
    checks=[]
    for path,phrases in content.items():
        value=read(path).lower()
        for phrase in phrases:
            ok=phrase.lower() in value
            require(ok, f'Content coverage missing: {path}: {phrase}')
            checks.append({'path':path,'requirement':phrase,'result':'PASS' if ok else 'FAIL'})
    inputs=['world-clock/ARC4_HANDOFF.json','world-clock/ARC4_HANDOFF.md','world-clock/validate_arc4_handoff.py',
            'economy/KIRA_BLACK_ACQUISITION_PRICES.json','live-model/27_CHECKPOINT_20_SOCIAL_LIFE_ARC4.md',*content]
    return {'checkpoint':22,'inherited_scope':'Checkpoint 20 social/card locks, CP21 seasonal doctrine and CP22 exact Orb day/current Yellow calendar','result':'FAIL' if errors else 'PASS','errors':errors,'baseline_commit':BASELINE,
      'arc4_events':events,'beam_ranking_subtotal':63694,'post_beam_red_total':73044,'beam_red_already_paid':6050,
      'illi_milestones':19,'illi_total':292772,'card_price':card['price'],'universal_blue_card_price':False,
      'orbs_price':orbs['price'],'orbs_date':'Y6D2, Late Yellow inside Arc Four; not Y1D2','arc4_close':'Genesis Prime Red Y6D3',
      'conditional_card_minus_orange_gross':card['price']-handoff['preserved_orange_gross']['kira'],
      'card_full_funding_audit':'OPEN; no full cashflow solvency assertion','current_yellow_rows':49,'abecca':'abecca',
      'galas_per_season':1,'gala_dates':'OPEN','credit_transfer_enforcement':'OPEN',
      'yellow_clear':'Kira independently first Y4D2; illi absent/Orange-cleared; payout 2305 Kira / 0 illi',
      'protected_files_byte_identical':protected,'content_checks':checks,
      'sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sorted(set(inputs))}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--write-audit',action='store_true')
    args=parser.parse_args()
    try: report=audit(args.repository.resolve())
    except (OSError,KeyError,ValueError,TypeError,StopIteration,subprocess.CalledProcessError) as e:
        report={'result':'FAIL','errors':[str(e)]}
    if args.write_audit and report['result']=='PASS':
        (args.repository/'world-clock/ARC4_HANDOFF_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('sha256','content_checks','protected_files_byte_identical','arc4_events')},indent=2,ensure_ascii=False))
    return 0 if report['result']=='PASS' else 1


if __name__=='__main__': raise SystemExit(main())
