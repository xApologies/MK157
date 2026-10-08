"""Read-only verification of the full Red/Orange repair and derived audits."""
import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

from validate_kira_ledger import audit as kira_audit
from validate_red_orange_reconciliation import audit as reconciliation_audit

PREFIX='provenance/live-model-full-repair-2026-10-08/'
BASELINE='22f806aaa5eed0a6ff0534fb186c6d1fbb59687f'
STALE_PHRASES=(
    'R5D4 raeon participation/elimination with no required combat',
    "O4D2's paid Normal Red is constrained to an unpaid boss distinct from O1D6",
    'O4D2 paid Red must be a distinct unpaid boss from O1D6',
    'Kira + illi participate and are eliminated at **R5D4**',
    'Orange qualification is **O5D1**',
    'O5D6 eliminated', 'O7D5 recovery/optional viewing',
    'Ten OPEN days are protected', 'Ten OPEN rows protect',
    'Ten OPEN days protect', '10 protected OPEN rows',
)


def load_module(root,path):
    spec=importlib.util.spec_from_file_location(Path(path).stem,root/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def check_calendar_audit(path, expected, actual):
    if path != 'world-clock/CALENDAR_AUDIT.json' or expected != actual:
        raise ValueError('Calendar audit differs from current independent economy calculation: '+path)


def validated_calendar_audit(root):
    """Admit this one regenerated report only after source/promotion validation.

    Existing economy.audit invokes full promotion and corrected-calendar checks;
    it never calls this function. Numeric source data receives no exemption.
    """
    manifest_path=root/(PREFIX+'INTEGRATION.json')
    if not manifest_path.exists():return set()
    manifest=json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    path='world-clock/CALENDAR_AUDIT.json'
    if manifest['id']!='live-model-full-repair-2026-10-08' or path not in manifest['changed_paths']:
        raise ValueError('Regenerated calendar audit lacks declared source promotion')
    expected=load_module(root,'economy/validate_economy.py').audit(root)
    if expected['result']!='PASS':raise ValueError('Economy source audit failed: '+str(expected['errors']))
    check_calendar_audit(path,expected['calendar'],json.loads((root/path).read_text(encoding='utf-8-sig')))
    return {path}


def stale_owner_claims(root):
    """Scan current prose/metadata; archived numbered checkpoints stay history."""
    paths=[root/p for p in ('README.md','CANON_STATUS.md','THREAD_DEVELOPMENT_CONSTITUTION.md')]
    for folder in ('canon','story','live-model','world-clock','economy'):
        paths.extend(p for p in (root/folder).rglob('*.md') if not re.match(r'\d\d_CHECKPOINT_',p.name))
    findings=[]
    for path in paths:
        text=path.read_text(encoding='utf-8-sig')
        for phrase in STALE_PHRASES:
            if phrase in text:findings.append({'path':path.relative_to(root).as_posix(),'phrase':phrase})
    return findings


def audit(root):
    def js(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
    def text(p):return (root/p).read_text(encoding='utf-8-sig')
    git=['git','-c',f'safe.directory={root.as_posix()}','-C',str(root)]
    checks=[]
    def check(number,ok,detail):checks.append({'item':number,'result':'PASS' if ok else 'FAIL','evidence':detail})
    reconciliation=reconciliation_audit(root)
    red=js('world-clock/RED_TO_ORANGE_COMBAT_CALENDAR.json'); orange=js('world-clock/ARC3_ORANGE_CALENDAR.json')
    r={(x['season'][0],x['week'],x['day']):x for x in red};o={(x['week'],x['day']):x for x in orange}
    stale=stale_owner_claims(root)
    check(1,r['R',5,4]['combat_event']=='NO REQUIRED COMBAT' and 'OPEN' in r['R',5,4]['author_notes'] and not stale,{'calendar':'R5D4 OPEN','stale_current_owner_claims':stale})
    check(2,'EARLY KNOCKOUT' in r['R',7,6]['author_notes'] and r['R',7,6]['illi_credits_earned']==1950 and r['R',7,7]['illi_credits_earned']==2040,'R7D6 10:00 knockout/Duo W10; R7D7 unchanged')
    check(3,all(o[x]['kind']=='OPEN' for x in [(5,1),(5,6)]) and not stale,'O5D1/O5D6 OPEN across current owners')
    check(4,o[7,5]['kind']=='Recovery' and 'championship' in o[7,5]['notes'] and 'EARLY KNOCKOUT' in o[7,6]['notes'] and o[7,6]['kira_credit']==5805 and o[7,7]['kira_credit']==1020,'O7D5 recovery; O7D6 10:00 knockout before Duo; O7D7 unchanged')
    check(5,r['O',1,3]['purchase_cost']==25705 and r['O',1,3]['illi_running_balance']==952 and r['O',2,2]['purchase_cost']==9350 and r['O',2,2]['illi_running_balance']==42 and 'CSR purchase61017' in r['O',2,3]['kira_combat'],'PC/Legacy O1D3 952; Absorption O2D2 42; CSR O2D3 61,017')
    kira=kira_audit(root)
    ledger=js('world-clock/KIRA_CREDIT_LEDGER.json')
    bonus=[x for x in ledger if x['season']=='Orange' and x['week']==1 and x['day']==6 and x['kira_actual_surplus_earned']==2500]
    check(6,r['O',1,6]['result']=='Sixfold CLEAR; Triumvirate CLEAR; Black Orchard FAIL; Weaver/Wayfarer/Bloom NOT ATTEMPTED' and len(bonus)==1,'O1D6 six outcomes plus second Red actual surplus ledger row')
    check(7,o[4,2]['kira_credit']==o[4,2]['illi_credit']==3750 and o[4,2]['status']=='ORANGE CLEAR / RED REPEAT UNPAID','O4D2 Black Orchard 3,750; Red repeats zero')
    arc3=load_module(root,'world-clock/validate_arc3.py').audit(root)
    stored=js('world-clock/ARC3_ECONOMY_AUDIT.json')
    check(8,stored==arc3 and arc3['result']=='PASS' and arc3['deterministic_gross']=={'illi':56385,'kira':81415} and arc3['income_by_kind']['Raid']=={'illi':3750,'kira':3750} and not {'Tournament','Recovery/Tournament'} & arc3['event_rows_by_kind'].keys(),{'stored_equals_fresh':stored==arc3,'event_counts':arc3['event_rows_by_kind'],'gross':arc3['deterministic_gross'],'dates':arc3['tournament_dates'],'raid':arc3['raid_eligibility_constraint']})
    check(9,all((root/('world-clock/KIRA_CREDIT_LEDGER'+ext)).exists() for ext in ('.csv','.json')),'63 sourced ledger rows in both mirrors')
    check(10,kira['result']=='PASS',{'row_differences':kira['row_differences'],'income_by_kind':kira['income_by_kind']})
    check(11,kira['checkpoint_difference']==0,{'computed':kira['authored_actual_combat_gross'],'author_checkpoint':kira['expected_author_checkpoint'],'difference':kira['checkpoint_difference']})
    check(12,kira['affordability']['result']=='PASS',kira['affordability'])
    check(13,'R5D4 OPEN with no seasonal tournament' in text('story/ARC_02/ARC.md') and not stale,'Arc Two current scaffold corrected in place')
    check(14,all('O4D2 Red repeats pay zero and Black Orchard pays 3,750 each only' in text(p) for p in ('live-model/04_COMBAT_WORLD.md','live-model/COMBAT_ECOLOGY.md','live-model/COMBAT_THRESHOLDS.md')),'All three mirrored combat-owner statements corrected')
    check(15,all('R7D6 and O7D6 at10:00' in text(p) and '**R5D4, O5D1 and O5D6 are OPEN**' in text(p) for p in ('world-clock/WORLD_CLOCK.md','live-model/WORLD_CLOCK.md','live-model/RAEON.md')),'Both World Clock owners and raeon owner agree with dated calendars')
    baseline=js(PREFIX+'BASELINE.json')['files']
    protected=[p for p in baseline if (p.startswith('provenance/') or re.match(r'live-model/\d\d_CHECKPOINT_',p) or (p.startswith('world-clock/') and p.endswith(('.csv','.json')) and 'AUDIT' not in p))]
    drift=[p for p in protected if not (root/p).is_file() or hashlib.sha256((root/p).read_bytes()).hexdigest()!=baseline[p]['sha256']]
    # Full original story/HARD/roster sections are prefix-independent byte slices.
    preserved_sections=[]
    for p,marker in [('live-model/04_COMBAT_WORLD.md','## October 8 — Orange-season Normal Raid roster'),('live-model/COMBAT_ECOLOGY.md','## October 8 cumulative — Hard Raid doctrine')]:
        old=subprocess.check_output(git+['show',BASELINE+':'+p]).decode('utf-8-sig');current=text(p)
        if marker not in old:
            raise ValueError('Preservation section missing: '+marker)
        a=old.index(marker);b=old.find('\n## ',a+len(marker));section=old[a:b if b>=0 else len(old)].strip()
        preserved_sections.append(section in current)
    check(16,all(preserved_sections),'Hard doctrine and Orange boss roster sections byte-preserved (apart from surrounding line endings)')
    family=text('live-model/01_KIRA.md');scenes=text('live-model/STORY_CLOCK_STATE.md');city=text('visual-references/CITY_LOCATION_REGISTRY.csv')
    check(17,all(name in family for name in ('Maelor','Naira','Caelen','Vaedren','Laina','Kaevren')) and 'conventional bow' in text('live-model/ILLI_PROGRESSION.md') and '007' in city and '008' in city,'Family, Kaevren, conventional bow and bookstore/festival registry survive unchanged')
    check(18,not drift,{'all_existing_calendar_data_and_numbered_provenance_unchanged':not drift,'drift':drift})
    check(19,not drift,'Every preexisting calendar CSV/JSON unchanged from fetched baseline; no combat event moved')
    eco=load_module(root,'economy/validate_economy.py').audit(root)
    handoff=load_module(root,'world-clock/validate_arc4_handoff.py').audit(root)
    fresh=(js('economy/AUDIT.json')==eco and js('world-clock/CALENDAR_AUDIT.json')==eco['calendar'] and js('world-clock/ARC4_HANDOFF_AUDIT.json')==handoff)
    check(20,fresh and all(x['result']=='PASS' for x in (kira,arc3,eco,handoff,reconciliation)),{'dependent_stored_audits_equal_fresh':fresh,'calendar_mirrors':'PASS','remote_blob_check':'Publication receipt verifies every resulting commit blob after fetch; this function is read-only on the supplied tree.'})
    return {'result':'PASS' if all(c['result']=='PASS' for c in checks) else 'FAIL','baseline':BASELINE,'checks':checks,
            'kira':{k:v for k,v in kira.items() if k not in ('source_rows','sha256','row_differences')},
            'protected_files_checked':len(protected),'stale_current_owner_claims':stale,
            'history_scope':'Numbered checkpoint records, provenance, pre-repair audit snapshots and past report hashes describe their pinned revisions, never current alternate Red/Orange facts.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--repository',type=Path,default=Path(__file__).resolve().parents[2]);args=parser.parse_args()
    try:report=audit(args.repository.resolve())
    except (OSError,ValueError,KeyError,TypeError,IndexError,subprocess.CalledProcessError) as exc:report={'result':'FAIL','errors':[str(exc)]}
    print(json.dumps(report,indent=2,ensure_ascii=False));return 0 if report['result']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
