$ErrorActionPreference='Stop'; $root='C:\Users\rando\_MK157'; Set-Location $root
$utf8=[Text.UTF8Encoding]::new($false); $p='_inbox/checkpoint-12'
function Write-Doc($path,$t) { [IO.File]::WriteAllText((Join-Path $root $path),($t -replace "`r`n","`n"),$utf8) }
function Json($obj) { ConvertTo-Json -InputObject $obj -Depth 50 }
function Add-Doc($path,$t) { Write-Doc $path ((Get-Content $path -Raw)+"`n"+$t+"`n") }
function Set-Value($o,$k,$v) { $o | Add-Member -NotePropertyName $k -NotePropertyValue $v -Force }
$baseline=& git -c safe.directory=C:/Users/rando/_MK157 rev-parse HEAD
New-Item -ItemType Directory -Force '_inbox/pricing-12-before','provenance/checkpoint-12-package' | Out-Null
Copy-Item "$p/*" 'provenance/checkpoint-12-package'
$beforeHashes=@{}
foreach($folder in @('bindings','summons','builder','world-clock')) {
 Get-ChildItem $folder -Recurse -File | ForEach-Object { $rel=$_.FullName.Substring($root.Length+1).Replace('\','/'); $beforeHashes[$rel]=(Get-FileHash $_.FullName).Hash }
}
foreach($path in @('live-model/18_CHECKPOINT_11_ECONOMY_CARDS_HANDOFF.md','live-model/01_KIRA.md','live-model/STORY_CLOCK_STATE.md')) { $beforeHashes[$path]=(Get-FileHash $path).Hash }
Write-Doc '_inbox/pricing-12-before/hashes.json' (Json $beforeHashes)
Copy-Item bindings/BINDINGS.json,bindings/BINDINGS.csv,bindings/BINDINGS.jsonl '_inbox/pricing-12-before'
Copy-Item summons/SUMMONED_ENTITIES.json,summons/SUMMONED_ENTITIES.csv,summons/SUMMONED_ENTITIES.jsonl '_inbox/pricing-12-before'
$bindings=Get-Content bindings/BINDINGS.json -Raw | ConvertFrom-Json
$entities=Get-Content summons/SUMMONED_ENTITIES.json -Raw | ConvertFrom-Json
# Read all requested mirrors before mutation; preservation/mirror checks follow in independent validation.
$oldCsv=Import-Csv bindings/BINDINGS.csv
$oldLines=Get-Content bindings/BINDINGS.jsonl | ForEach-Object { $_ | ConvertFrom-Json }
$sCsv=Import-Csv summons/SUMMONED_ENTITIES.csv
$sLines=Get-Content summons/SUMMONED_ENTITIES.jsonl | ForEach-Object { $_ | ConvertFrom-Json }
if($bindings.Count -ne 1016 -or $entities.Count -ne 229 -or $oldCsv.Count -ne 1016 -or $oldLines.Count -ne 1016 -or $sCsv.Count -ne 229 -or $sLines.Count -ne 229) { throw 'Baseline count mismatch' }
$ranks=@('Red','Orange','Yellow','Green','Blue','Violet','White')
$multipliers=@([decimal]1.60,[decimal]1.80,[decimal]2.10,[decimal]2.50,[decimal]3.00,[decimal]4.00)
function Ladder([int]$base) { $ladder=[ordered]@{Red=$base}; $cost=[decimal]$base; for($i=0;$i -lt 6;$i++){ $cost=[decimal]::Round($cost*$multipliers[$i],0,[MidpointRounding]::AwayFromZero); $ladder[$ranks[$i+1]]=[int]$cost }; return $ladder }
function Class([int]$base) { if($base -le 1000){'FOUNDATIONAL'}elseif($base -le 2400){'COMMON_SPECIALIZATION'}elseif($base -le 4900){'ADVANCED'}elseif($base -lt 10000){'POWERFUL'}else{'EXCEPTIONAL'} }
$decisions=[Collections.Generic.List[object]]::new()
function Decision($kind,$key,$name,$base,$reason,$features) { $decisions.Add([pscustomobject]@{registry=$kind;key=$key;name=$name;pricing_class=(Class $base);red_base_cost=$base;rationale=$reason;semantic_features=$features}) }
function Summon-Price($s) {
 if($s.entity_id -match '^PE-'){return @{B=10000;why='Author lock: every Prime has the same Red acquisition price.';features='Prime architecture; author lock'}}
 # Only scale/control/load/role/persistence/mobility metadata; no elemental or basin inputs.
 $base=switch($s.scale){'Tiny'{500} 'Small'{1100} 'Medium'{1700} 'Large'{2400} 'Huge'{4000} 'Variable'{2200} default{throw "Unclassified summon scale $($s.scale)"}}
 $control=switch($s.control_complexity){'low'{0} 'low-to-moderate'{250} 'moderate'{500} 'high'{1400} 'very high'{2000} 'extreme'{2800} default{throw 'Unknown control complexity'}}
 $load=if($s.sustain_load -match '^extreme'){1200}elseif($s.sustain_load -match '^very high'){900}elseif($s.sustain_load -match '^high'){600}elseif($s.sustain_load -match '^moderate'){300}else{0}
 $role=if($s.combat_role -match 'siege|high-output assault'){700}elseif($s.combat_role -match 'screening|area control|lane control|restraint|constriction'){400}elseif($s.combat_role -match 'aerial pursuit'){250}elseif($s.combat_role -match 'charge|extraction|transport|guard|intercept'){150}else{0}
 $distributed=if($s.combat_role -match 'saturation'){800}else{0}
 $persistence=if($s.maximum_practical_persistence -match 'hours' -and $s.control_complexity -eq 'low'){100}else{0}
 $base=[Math]::Min(9900,$base+$control+$load+$role+$distributed+$persistence)
 return @{B=$base;why="Scale $($s.scale); control $($s.control_complexity); sustain $($s.sustain_load); role $($s.combat_role); persistence evaluated. Element identity is excluded.";features="scale=$($s.scale);control=$($s.control_complexity);load=$($s.sustain_load);role=$($s.combat_role);mobility=$($s.mobility);persistence=$($s.maximum_practical_persistence)"}
}
$summonPrices=@(); $byBinding=@{}
foreach($s in $entities) {
 $d=Summon-Price $s; $ladder=Ladder $d.B
 $row=[ordered]@{entity_id=$s.entity_id;name=$s.name;pricing_class=(Class $d.B);red_base_cost=$d.B}
 foreach($rank in $ranks){$row[$rank]=$ladder[$rank]}; $row.pricing_status='LOCKED — Checkpoint 12'
 $summonPrices+=[pscustomobject]$row
 if($s.binding_reference){$byBinding[$s.binding_reference]=$d}
 Decision 'summon' $s.entity_id $s.name $d.B $d.why $d.features
}
$anchors=@{'PT-0002'=600;'PT-0003'=700;'PT-0001'=1800;'GE-0537'=3000;'GE-0043'=5000}
function Binding-Price($b) {
 if($anchors.ContainsKey($b.id)){return @{B=$anchors[$b.id];why='Exact author-locked anchor; overrides semantic classifier.';features=$b.geometry}}
 if($byBinding.ContainsKey($b.name)){return $byBinding[$b.name]}
 $name=$b.name; $g=$b.geometry; $mechanism=$b.physical_mechanism
 $why=[Collections.Generic.List[string]]::new(); $cost=0
 switch($g) {
 'Directed' {$cost=600; $why.Add('direct single-target primitive')}
 'Anchor' {$cost=700; $why.Add('persistent single-target primitive')}
 'Self / biological system' {
  $cost=switch -Regex($name){'^Localized'{800} '^Burst'{1400} '^Persistent'{1800} '^Adaptive'{2800} '^Overdrive'{5000} default{throw 'Unknown augmentation form'}}
  $why.Add('localized/burst/persistent/adaptive/overdrive bodily control scope')
  if($mechanism -match 'neural|cardiac|circulatory|metabolic|sensory|visual|acoustic|coordination'){ $cost+=400; $why.Add('fine physiological/information control') }
  if($mechanism -match 'whole-body|structural resonance|maintain performance deeper|force production'){ $cost+=500; $why.Add('integrated sustain or whole-body output') }
 }
 'Persistent entity' {
  # Unlinked creature/elemental Binding: role and distributed coordination only, never species/element premiums.
  $cost=switch -Regex($mechanism){'large high-output breaker'{7600} 'large mobile assault|high-output assault'{9000} 'transport|extraction'{3200} 'protective interception|guard'{2100} 'aerial/rapid strike'{2150} 'fast pursuit|mobile pursuit'{2050} 'low-output recon|low-output scout'{600} 'distributed many-body'{5300} 'constriction|area-threading'{2900} default{throw "Unknown manifestation role $name"}}
  if($name -match 'Swarm' -and $mechanism -notmatch 'distributed many-body'){ $cost+=1200; $why.Add('distributed swarm control') }
  $why.Add('autonomous manifestation role/load'); $cost=[Math]::Min(9900,$cost)
 }
 'Perception' {
  $cost=if($name -match '^Expanded'){1800}else{800}; $why.Add('local focused versus expanded information geometry')
  if($mechanism -match 'forecast|extrapolate|inspect active|signature|persistent velis'){ $cost+=500; $why.Add('prediction/topology or signature interpretation') }
 }
 'Control relation' {
  $cost=900; $why.Add('single-summon command/control primitive')
  if($mechanism -match 'multiple|group|relay|linked|three or more|independently|transfer|share basic'){ $cost=2600; $why.Add('distributed/concurrent control') }
  elseif($mechanism -match 'condition|priorit|automatic|systematic|compressed|pre-resolve'){ $cost=1700; $why.Add('conditional or information-rich behavior') }
  if($mechanism -match 'high-output|structural depth|remote locus|reform a heavily'){ $cost=5200; $why.Add('deep/high-output/remote reconstruction') }
 }
 'Spatial' {
  $cost=if($name -match '^Expanded'){3000}else{1800}; $why.Add('focused versus expanded spatial constraint')
  if($mechanism -match 'temporarily adjacent|interior usable extent|redirect exits|differential resolution'){ $cost+=1500; $why.Add('adjacency/interior or exclusion topology') }
  if($mechanism -match 'Continuous spatial resolution'){ $cost=7500; $why.Add('continuous free three-dimensional position/orientation/vector integration') }
 }
 'Pattern modifier' {
  $cost=1700; $why.Add('compatible-shaping release modifier')
  if($mechanism -match 'three|four|multiple|division|duplicated|simultaneous|division after'){ $cost+=700; $why.Add('concurrent event copies') }
  if($mechanism -match 'sustained rapid|continuous area|structured area|many releases|intersecting|wide-area'){ $cost+=1600; $why.Add('sustained/area/converging control') }
  if($mechanism -match 'remote|delayed|orbiting'){ $cost+=600; $why.Add('delayed/remote/orbital control') }
 }
 default {
  $cost=switch($g){'Projectile'{1100} 'Jet'{1600} 'Lance'{2100} 'Beam'{2800} 'Arc'{1700} 'Burst'{2000} 'Wave'{2700} 'Ring'{2900} 'Orb'{2200} 'Shard'{1200} 'Field'{2800} 'Plane'{1800} 'Dome'{3000} 'Shield'{3000} 'Bolt'{1600} 'Mark'{1400} 'Pulse'{2300} default{throw "Unclassified geometry $g : $name"}}
  $why.Add("$g delivery/control geometry")
  if($name -match '^(Controlled|Mobile|Channeled)'){ $cost+=700; $why.Add('controlled/mobile/channeled sustain') }
  if($name -match '^(Expanded|Sweeping|Broad|Sustained)'){ $cost+=800; $why.Add('expanded area or sustained throughput') }
  if($mechanism -match 'chiral organization|chirality organization|persistent location/target anchor|active Transduction'){ $cost+=1500; $why.Add('compatible-architecture denial/control') }
  if($name -match '^Sever' -and $g -eq 'Field'){ $cost=10000; $why.Add('exceptional area architecture dismantling') }
 }
 }
 return @{B=$cost;why=($why -join '; ');features="geometry=$g;mechanism=$mechanism;operational_name=$name"}
}
foreach($b in $bindings) {
 $d=Binding-Price $b; $ladder=Ladder $d.B
 Set-Value $b 'pricing_class' (Class $d.B); Set-Value $b 'red_base_cost' $d.B; Set-Value $b 'rank_costs' ([pscustomobject]$ladder)
 foreach($rank in $ranks){Set-Value $b $rank $ladder[$rank]}
 Set-Value $b 'pricing_status' 'LOCKED — Checkpoint 12'
 Decision 'binding' $b.id $b.name $d.B $d.why $d.features
}
Write-Doc 'bindings/BINDINGS.json' ((Json @($bindings))+"`n")
Write-Doc 'bindings/BINDINGS.jsonl' ((($bindings | ForEach-Object { ConvertTo-Json -InputObject $_ -Depth 50 -Compress }) -join "`n")+"`n")
$bindingMap=@{}; foreach($b in $bindings){$bindingMap[$b.id]=$b}
foreach($c in $oldCsv){$b=$bindingMap[$c.id]; Set-Value $c 'pricing_class' $b.pricing_class; $c.red_base_cost=[string]$b.red_base_cost; foreach($rank in $ranks){$c.$rank=[string]$b.rank_costs.$rank}; $c.pricing_status=$b.pricing_status}
Write-Doc 'bindings/BINDINGS.csv' ((($oldCsv | ConvertTo-Csv -NoTypeInformation) -join "`n")+"`n")
function Mirrors($stem,$records,$jsonl=$true){Write-Doc "$stem.json" ((Json @($records))+"`n"); Write-Doc "$stem.csv" ((($records | ConvertTo-Csv -NoTypeInformation) -join "`n")+"`n"); if($jsonl){Write-Doc "$stem.jsonl" ((($records | ForEach-Object { ConvertTo-Json -InputObject $_ -Depth 15 -Compress }) -join "`n")+"`n")}}
Mirrors 'summons/SUMMON_PRICING' $summonPrices
$primePrices=@($summonPrices | Where-Object entity_id -match '^PE-' | ForEach-Object { $o=[ordered]@{prime_id=$_.entity_id}; foreach($prop in $_.PSObject.Properties){if($prop.Name -ne 'entity_id'){$o[$prop.Name]=$prop.Value}}; [pscustomobject]$o })
Mirrors 'summons/PRIME_ELEMENTAL_PRICING' $primePrices $false
Write-Doc 'provenance/CHECKPOINT_12_PRICING_DECISIONS.csv' ((($decisions | ConvertTo-Csv -NoTypeInformation) -join "`n")+"`n")
# Refresh the existing human-readable Binding price mirror, retaining all other content.
$compendium=Get-Content 'bindings/COMPENDIUM.md' -Raw
foreach($b in $bindings){$price=($ranks | ForEach-Object { "$_ $($b.rank_costs.$_.ToString('N0',[Globalization.CultureInfo]::InvariantCulture))" }) -join ', '; $pattern='(?ms)(^## '+[regex]::Escape($b.id)+' — .*?^\*\*Prices:\*\*)[^\r\n]*'; $compendium=[regex]::Replace($compendium,$pattern,{param($m) $m.Groups[1].Value+' '+$price},1)}
foreach($gas in ($bindings | Where-Object family -eq 'Gas')) {
 $price=($ranks | ForEach-Object { "$_ $($gas.rank_costs.$_.ToString('N0',[Globalization.CultureInfo]::InvariantCulture))" }) -join ', '
 $pattern='(?ms)(^## '+[regex]::Escape($gas.id)+' — .*?)Red base cost and all rank costs: OPEN \(no deterministic base-cost convention\)\. Rank development, White expression and basin topology: OPEN\.'
 $compendium=[regex]::Replace($compendium,$pattern,{param($m) $m.Groups[1].Value+'**Prices:** '+$price+"`n`nPricing LOCKED — Checkpoint 12; historical status cost-OPEN wording is superseded. Rank development, White expression and basin topology remain OPEN."})
}
Write-Doc 'bindings/COMPENDIUM.md' ($compendium -replace '(?m)[ \t]+$','')
Write-Doc 'bindings/PRICING_MODEL.md' ((Get-Content "$p/PRICING_POLICY.md" -Raw)+@'

## Reproducible semantic assignment

The operational classifier is preserved in provenance/checkpoint-12-package/SEMANTIC_PRICING.ps1. It examines every record and records its factors/rationale in ../provenance/CHECKPOINT_12_PRICING_DECISIONS.csv. Author anchors override the classifier. Otherwise price uses geometry, focused/expanded scope, sustain, concurrent/distributed control, physiological information precision, spatial constraints, output and autonomous role. Existing price scaffolding and ID sequence never contribute.

Summon scale starts at Tiny 500, Small 1100, Medium 1700, Large 2400, Huge 4000, Variable 2200; control adds 0/250/500/1400/2000/2800 for low through extreme. Moderate/high/very-high/extreme sustain adds 300/600/900/1200. Area/lane control adds 400; aerial pursuit 250; guard/transport/interception 150; siege/high-output assault 700. Distributed saturation adds 800; simple low-control hours-long scouting persistence adds 100. Ordinary prices cap at 9900. Elements, species, visible color and basin data create no price premium. Semantically identical patterns receive equal prices.

Matched summon-Binding names share price decisions; unmatched manifestations use their explicit role and distributed coordination. Ordinary CSR has its own operational registry price and does not overwrite Kira's Black acquisition gate.

ROUND_HALF_UP applies sequentially at every positive-credit transition using decimal arithmetic; the next rank uses the rounded preceding rank. Pricing LOCKED status does not promote an ALPHA mechanism, recipe or topology to canon. Existing status/source strings are preserved even if historical wording mentions OPEN costs; pricing_status and this policy supersede only that price claim.
'@)
Copy-Item '_inbox/pricing-12.ps1' 'provenance/checkpoint-12-package/SEMANTIC_PRICING.ps1'
Write-Doc '_inbox/pricing-12-before/baseline.txt' $baseline
Write-Output 'Priced every Binding and summon; original entity atlas untouched; rank mirrors and decision ledger written.'
