$ErrorActionPreference='Stop'; $root='C:\Users\rando\_MK157'; Set-Location $root; $utf8=[Text.UTF8Encoding]::new($false)
function Write-Doc($path,$t){[IO.File]::WriteAllText((Join-Path $root $path),($t -replace "`r`n","`n"),$utf8)}
function Assert($c,$m){if(-not $c){throw $m}}
function Canon($o){ConvertTo-Json -InputObject $o -Depth 50 -Compress}
$b=Get-Content bindings/BINDINGS.json -Raw | ConvertFrom-Json
$old=Get-Content '_inbox/pricing-12-before/BINDINGS.json' -Raw | ConvertFrom-Json
$s=Get-Content summons/SUMMON_PRICING.json -Raw | ConvertFrom-Json
$entities=Get-Content summons/SUMMONED_ENTITIES.json -Raw | ConvertFrom-Json
$ranks=@('Red','Orange','Yellow','Green','Blue','Violet','White'); $mult=@([decimal]1.6,[decimal]1.8,[decimal]2.1,[decimal]2.5,[decimal]3,[decimal]4)
$allowed=@('red_base_cost','rank_costs','pricing_class','pricing_status')+$ranks
Assert ($b.Count -eq 1016 -and $s.Count -eq 229) 'Wrong counts'
Assert (@($b.id | Sort-Object -Unique).Count -eq 1016 -and @($s.entity_id | Sort-Object -Unique).Count -eq 229) 'Duplicate IDs'
for($i=0;$i -lt $old.Count;$i++) {
 $a=[ordered]@{}; $z=[ordered]@{}
 foreach($prop in $old[$i].PSObject.Properties){if($prop.Name -notin $allowed){$a[$prop.Name]=$prop.Value}}
 foreach($prop in $b[$i].PSObject.Properties){if($prop.Name -notin $allowed){$z[$prop.Name]=$prop.Value}}
 Assert ((Canon $a) -eq (Canon $z)) "Non-price data changed $($b[$i].id)"
}
$hashes=Get-Content '_inbox/pricing-12-before/hashes.json' -Raw | ConvertFrom-Json
$allowedChanged=@('bindings/BINDINGS.json','bindings/BINDINGS.jsonl','bindings/BINDINGS.csv','bindings/COMPENDIUM.md','bindings/PRICING_MODEL.md','bindings/README.md','summons/README.md')
foreach($prop in $hashes.PSObject.Properties){if($prop.Name -notin $allowedChanged){Assert ((Get-FileHash $prop.Name).Hash -eq $prop.Value) "Protected file changed $($prop.Name)"}}
foreach($row in @($b)+@($s)) {
 Assert ($row.red_base_cost -ge 500 -and $row.red_base_cost -le 10000 -and $row.red_base_cost % 50 -eq 0) 'Base band/increment invalid'
 Assert ($row.pricing_status -eq 'LOCKED — Checkpoint 12') 'Pricing status invalid'
 $value=[decimal]$row.red_base_cost
 for($i=0;$i -lt 7;$i++){
  if($i -gt 0){$value=[decimal]::Round($value*$mult[$i-1],0,[MidpointRounding]::AwayFromZero)}
  Assert ($row.($ranks[$i]) -eq $value) "Ladder invalid $($row.name) $($ranks[$i])"
  if($row.id){Assert ($row.rank_costs.($ranks[$i]) -eq $value) 'Nested ladder differs'}
 }
 $expected=if($row.red_base_cost -le 1000){'FOUNDATIONAL'}elseif($row.red_base_cost -le 2400){'COMMON_SPECIALIZATION'}elseif($row.red_base_cost -le 4900){'ADVANCED'}elseif($row.red_base_cost -lt 10000){'POWERFUL'}else{'EXCEPTIONAL'}
 Assert ($row.pricing_class -eq $expected) 'Class and band disagree'
}
$anchors=@{'PT-0002'=600;'PT-0003'=700;'PT-0001'=1800;'GE-0537'=3000;'GE-0043'=5000}
$anchorChecks=@(); foreach($key in $anchors.Keys){$row=$b | Where-Object id -eq $key; Assert ($row.red_base_cost -eq $anchors[$key]) "Anchor wrong $key"; $anchorChecks+=@{id=$key;red_base_cost=$row.red_base_cost;pass=$true}}
$prime=Get-Content summons/PRIME_ELEMENTAL_PRICING.json -Raw | ConvertFrom-Json
Assert ($prime.Count -eq 9) 'Prime count'
foreach($row in $prime){Assert ($row.red_base_cost -eq 10000 -and $row.White -eq 1814400 -and (($ranks | ForEach-Object {$row.$_} | Measure-Object -Sum).Sum -eq 2534480)) 'Prime ladder wrong'; $sr=$s | Where-Object entity_id -eq $row.prime_id; foreach($field in @('name','pricing_class','red_base_cost','pricing_status')+$ranks){Assert ($sr.$field -eq $row.$field) 'Prime atlas inconsistency'}}
Assert (@($s | Where-Object { $_.entity_id -notmatch '^PE-' -and $_.red_base_cost -ge 10000 }).Count -eq 0) 'Ordinary summon reaches Prime price'
Assert (@($s.entity_id | Sort-Object) -join '|' -eq (@($entities.entity_id | Sort-Object) -join '|')) 'Entity pricing IDs differ'
# JSONL equality preserves every serialized field; CSV compares original non-price columns plus all price columns.
$lines=Get-Content bindings/BINDINGS.jsonl | ForEach-Object {$_ | ConvertFrom-Json}
$csv=Import-Csv bindings/BINDINGS.csv; $oldCsv=Import-Csv '_inbox/pricing-12-before/BINDINGS.csv'
for($i=0;$i -lt $b.Count;$i++){
 Assert ((Canon $b[$i]) -eq (Canon $lines[$i])) 'Binding JSONL mismatch'
 foreach($prop in $oldCsv[$i].PSObject.Properties){if($prop.Name -notin $allowed){Assert ([string]$csv[$i].($prop.Name) -eq [string]$prop.Value) "CSV field lost $($prop.Name)"}}
 foreach($field in @('id','name','pricing_class','red_base_cost','pricing_status')+$ranks){Assert ([string]$csv[$i].$field -eq [string]$b[$i].$field) "Binding CSV price mismatch $field"}
}
foreach($stem in @('SUMMON_PRICING','PRIME_ELEMENTAL_PRICING')){
 $j=Get-Content "summons/$stem.json" -Raw | ConvertFrom-Json; $c=Import-Csv "summons/$stem.csv"
 Assert ($j.Count -eq $c.Count) 'CSV pricing count'
 for($i=0;$i -lt $j.Count;$i++){foreach($prop in $j[$i].PSObject.Properties){Assert ([string]$prop.Value -eq [string]$c[$i].($prop.Name)) "Pricing CSV mismatch $stem"}}
 if($stem -eq 'SUMMON_PRICING'){$l=Get-Content "summons/$stem.jsonl" | ForEach-Object {$_ | ConvertFrom-Json}; for($i=0;$i -lt $j.Count;$i++){Assert ((Canon $j[$i]) -eq (Canon $l[$i])) 'Summon JSONL mismatch'}}
}
$decisions=Import-Csv provenance/CHECKPOINT_12_PRICING_DECISIONS.csv
Assert ($decisions.Count -eq 1245 -and @($decisions | Where-Object rationale -eq '').Count -eq 0) 'Missing row-level decisions'
$compendium=Get-Content bindings/COMPENDIUM.md -Raw
$blocks=[regex]::Matches($compendium,'(?ms)^## ([A-Z]+-\d+) — .*?(?=^## |\z)')
Assert ($blocks.Count -eq 1016) 'Compendium count'
$bm=@{}; foreach($row in $b){$bm[$row.id]=$row}
foreach($block in $blocks){$row=$bm[$block.Groups[1].Value]; $price=($ranks | ForEach-Object { "$_ $($row.rank_costs.$_.ToString('N0',[Globalization.CultureInfo]::InvariantCulture))" }) -join ', '; Assert ($block.Value.Contains('**Prices:** '+$price)) "Compendium price mismatch $($row.id)"}
$coverage=Import-Csv provenance/CHECKPOINT_12_COVERAGE_MANIFEST.csv
Assert ($coverage.Count -eq 8 -and @($coverage | Where-Object status -ne INTEGRATED).Count -eq 0) 'Coverage incomplete'
foreach($r in $coverage){foreach($dest in $r.actual_destination -split '; '){Assert (Test-Path $dest) "Coverage missing $dest"}}
$economic=Get-Content live-model/ECONOMY_PURCHASE_SCHEDULE.md -Raw
Assert ($economic.Contains('18,655') -and $economic.Contains('61,000 each') -and $economic.Contains('BLUE')) 'Economic integration incomplete'
foreach($path in @('README.md','THREAD_DEVELOPMENT_CONSTITUTION.md','live-model/INDEX.md','live-model/19_CHECKPOINT_12_COMPLETE_PRICING.md','bindings/README.md','summons/README.md')){foreach($match in [regex]::Matches((Get-Content $path -Raw),'\[[^\]]+\]\(([^)]+)\)')){$target=$match.Groups[1].Value; if($target -match '^https?://'){continue}; if($target -match 'CHECKPOINT_12_AUDIT.json$'){continue}; Assert (Test-Path (Join-Path (Split-Path (Join-Path $root $path)) $target)) "Broken link $path -> $target"}}
function Stats($records){$v=@($records.red_base_cost | Sort-Object); $n=$v.Count; $med=if($n%2){$v[[int][Math]::Floor($n/2)]}else{($v[$n/2-1]+$v[$n/2])/2}; return @{min=$v[0];median=$med;max=$v[-1]}}
function Distribution($records,$key){$o=[ordered]@{}; foreach($g in ($records | Group-Object $key | Sort-Object Name)){$o[$g.Name]=$g.Count}; return $o}
$bindingFlags=@('Generated families often share templates; same semantic geometry/control factors intentionally share prices across elemental names. Review repeated-price clusters when mechanisms gain substantive detail.','Gas record historical status strings still say costs OPEN; pricing_status supersedes costs only, preserving rank-expression/basin OPENs.','Exceptional ordinary Sever Field price reflects area architecture dismantling; review alongside evolving topology canon.')
$summonFlags=@('Elemental variants and numbered Pattern variants with identical scale/control/role metadata have equal Red prices; no element-name premium or pattern-number premium.','Some ordinary entity records have no exact Binding-name counterpart; entity atlas remains independently keyed and no registry records were invented.')
$ba=[ordered]@{checkpoint='12';result='PASS';records=1016;priced=1016;counts_by_pricing_class=(Distribution $b 'pricing_class');red_base_statistics=(Stats $b);counts_by_domain=(Distribution $b 'primary_domain');anchor_checks=$anchorChecks;null_price_count=0;arithmetic_checks='PASS — decimal sequential ROUND_HALF_UP';mirror_equality='PASS — JSON/JSONL all fields; CSV existing fields and full price fields';preserved_checks='PASS — IDs, six domains, basin fields/OPENs, mechanisms, White expressions, statuses, lineage, recipes/gates';suspicious_distributions_for_review=$bindingFlags}
$sa=[ordered]@{checkpoint='12';result='PASS';records=229;priced=229;ordinary=220;primes=9;counts_by_pricing_class=(Distribution $s 'pricing_class');red_base_statistics=(Stats $s);ordinary_red_statistics=(Stats @($s | Where-Object entity_id -notmatch '^PE-'));counts_by_entity_type=(Distribution $entities 'entity_type');prime_checks=@{count=9;red=10000;ladder=@(10000,16000,28800,60480,151200,453600,1814400);cumulative=2534480;all_pass=$true};null_price_count=0;ordinary_at_or_above_10000=0;arithmetic_checks='PASS';mirror_equality='PASS';preserved_checks='Entity atlas and every original summon file except README byte unchanged; recipes and illi gates byte unchanged';suspicious_distributions_for_review=$summonFlags}
Write-Doc 'bindings/PRICING_AUDIT.json' ((ConvertTo-Json -InputObject $ba -Depth 15)+"`n")
Write-Doc 'summons/PRICING_AUDIT.json' ((ConvertTo-Json -InputObject $sa -Depth 15)+"`n")
$packageHashes=@(); Get-ChildItem provenance/checkpoint-12-package -File | ForEach-Object {$packageHashes+=@{path=$_.Name;sha256=(Get-FileHash $_.FullName).Hash.ToLower()}}
$changed=@(& git -c safe.directory=C:/Users/rando/_MK157 diff --name-only)+@(& git -c safe.directory=C:/Users/rando/_MK157 diff --cached --name-only)+@(& git -c safe.directory=C:/Users/rando/_MK157 ls-files --others --exclude-standard)+@('provenance/CHECKPOINT_12_AUDIT.json')
$audit=[ordered]@{checkpoint='12';result='PASS';baseline_commit=(Get-Content '_inbox/pricing-12-before/baseline.txt').Trim();final_commit_note='Integration commit hash reported after commit; not embedded self-referentially.';authority_chain='12 > 11 > 10 > 09 > 08 > 07B/07 > 06 > 05 > 04 > 03 > 02 > 01';changed_files=@($changed | Sort-Object -Unique);before_hashes=$hashes;package_hashes=$packageHashes;bindings=$ba;summons=$sa;row_decisions=1245;no_id_sequence_or_basin_pricing=$true;kira_gates_unchanged=$true;checkpoint_11_calendar_unchanged=$true;existing_legacy_registry_unchanged=$true;warnings=@($bindingFlags)+@($summonFlags);open_items_retained=@('Purchase dates','Credit reward/income tables','Discretionary prices','Topology-derived basin assignments','ALPHA/WORKING recipe choices','White-expression development where already OPEN','Planetary month reconciliation')}
Write-Doc 'provenance/CHECKPOINT_12_AUDIT.json' ((ConvertTo-Json -InputObject $audit -Depth 20)+"`n")
Write-Output (ConvertTo-Json -InputObject @{binding_classes=$ba.counts_by_pricing_class;binding_red=$ba.red_base_statistics;summon_classes=$sa.counts_by_pricing_class;summon_red=$sa.red_base_statistics;ordinary_summon_red=$sa.ordinary_red_statistics;status='PASS'} -Depth 5)
