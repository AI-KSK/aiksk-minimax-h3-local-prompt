from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
base = (ROOT / 'references/official/base-en.txt').read_text(encoding='utf-8')
ref = (ROOT / 'references/official/ref-en.txt').read_text(encoding='utf-8')
director = (ROOT / 'references/director/AIMIXER_DIRECTOR_RULES.md').read_text(encoding='utf-8')

# Version
assert 'version: "1.8.1-2026.10.13"' in skill

# Base exact fields and first-line patterns
for item in ['integrated_multimodal_description:', 'overall_soundscape:', 'non_diegetic_music:']:
    assert item in skill and item in base, item
assert 'For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.' in skill
assert 'How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.' in skill
assert 'How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.' in skill

# Ref2VA six-section order in skill
sections = ['subject_definitions:', 'summary:', 'retention_analysis:', 'detailed_description:', 'overall_soundscape:', 'non_diegetic_music:']
block = skill.split('### Ref2VA hard section order',1)[1].split('---',1)[0]
pos = [block.index(s) for s in sections]
assert pos == sorted(pos), pos

# Reference semantics
for item in ['<Subject N>', '<Picture N>', '<Video N>', '<Audio N>']:
    assert item in skill and item in ref, item
assert 'Picture = which file/frame. Subject = who/what this reusable thing is.' in skill

# Official task types
for item in ['keyframe completion','reference generation','video editing','video continuation','audio reuse','audio reference']:
    assert item in skill and item in ref, item

# Retention markers
for item in ['fully_preserved','partially_preserved','attribute_transfer','weak_reference','fully_copy','partially_copy']:
    assert item in skill and item in ref, item

# Director-specific requirements
for item in ['`r2v`','`v2v`','`rv2v`','`@` picker','common prompt','<Video 1>']:
    assert item in director, item

# Narrative production rules
for item in ['Causal bridges','causal bridges','350–500 English words','[Shot 1]']:
    assert item in skill or item in director, item

# Speaker syntax
assert '(S1)' in skill
assert '<d>[Language]' in skill

# Required files
required_paths = [
    ROOT/'references/official/base-en.txt',
    ROOT/'references/official/ref-en.txt',
    ROOT/'references/director/AIMIXER_DIRECTOR_RULES.md',
    ROOT/'references/director/DIRECTOR_PROMPT_LOGIC_ZH.md',
    ROOT/'references/CROSS_VALIDATION.md',
    ROOT/'references/SOURCE_REGISTER.md',
    ROOT/'templates/director_r2v_master.txt',
    ROOT/'examples/director_r2v_10s_three_image_story.txt',
    ROOT/'CODEX_INSTALL.md',
]
for path in required_paths:
    assert path.exists(), path

# Ensure example has one six-section sequence and three story shots
example = (ROOT/'examples/director_r2v_10s_three_image_story.txt').read_text(encoding='utf-8')
for section in sections:
    assert example.count(section) == 1, (section, example.count(section))
assert '[Shot 1]' in example and '[Shot 2]' in example and '[Shot 3]' in example
assert 'At 00:03.300' in example and 'At 00:06.900' in example

# Martial-arts extension invariants (additive to v1.7)
import json
import hashlib
fight = (ROOT/'references/playbooks/fight-choreography.md').read_text(encoding='utf-8')
for word in ['Fighter A', 'Fighter B', '5.17s', '15s', '<Subject 1>', 'Veda', 'A0', 'A8', '接触']:
    assert word in fight, word
assert 'references/playbooks/fight-choreography.md' in skill
preset = json.loads((ROOT/'references/playbooks/fight-lora-presets.json').read_text(encoding='utf-8'))
assert len(preset['presets']) == 9
assert [p['id'] for p in preset['presets']] == [f'A{i}' for i in range(9)]
assert len(preset['lora_order']) == 5
assert set(preset['lora_order']) == set(preset['lora_files'])
for i,p in enumerate(preset['presets']):
    assert set(p['weights']) == set(preset['lora_order'])
    assert all(isinstance(v,(float,int)) and 0 <= v <= 1.5 for v in p['weights'].values())
    if i == 4:
        assert p['weights']['Weapon Combat V1'] > 0
        assert all(v == 0 for k,v in p['weights'].items() if k != 'Weapon Combat V1')

for fp in ['templates/fight_t2va_5s_master.txt','templates/fight_ref2va_5s_master.txt',
           'examples/fight_t2va_5s_unarmed.txt','examples/fight_ref2va_5s_two_person.txt']:
    assert (ROOT/fp).is_file(), fp
fbase=(ROOT/'examples/fight_t2va_5s_unarmed.txt').read_text(encoding='utf-8')
assert fbase.startswith('integrated_multimodal_description:')
assert fbase.count('overall_soundscape:') == 1 and fbase.count('non_diegetic_music:') == 1
fref=(ROOT/'examples/fight_ref2va_5s_two_person.txt').read_text(encoding='utf-8')
for sec in sections: assert fref.count(sec) == 1, (sec,fref.count(sec))
assert 'subject_definitions:' in fref and fref.index('subject_definitions:') < fref.index('summary:')
assert 'video editing' not in fref and '<Audio 1>' not in fref

# Official references from source package must remain byte-identical to v1.7 manifest.
source_manifest_hashes={
 'references/official/base-en.txt':'088fb632fa3cbb18c9821024fb689e6f0f356f824c8f2e6b8e43a33239b137c7',
 'references/official/ref-en.txt':'b621067b41988c4d92be715b7a98ba48338f4076ab6041d95fcf463ea7c8ccdd',
}
for path,sha in source_manifest_hashes.items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == sha,path

# Verify every file hash in the versioned MANIFEST, and that no delivered file is omitted.
manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf-8'))
actual={p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('*') if p.is_file() and p.name != 'MANIFEST.json' and '__pycache__' not in p.parts}
recorded={f['path']:f for f in manifest['files']}
assert set(recorded)==set(actual), (set(recorded)-set(actual),set(actual)-set(recorded))
for name,p in actual.items():
    assert recorded[name]['sha256']==hashlib.sha256(p.read_bytes()).hexdigest(),name
    assert recorded[name]['bytes']==len(p.read_bytes()),name

print('OK v1.8.1')
