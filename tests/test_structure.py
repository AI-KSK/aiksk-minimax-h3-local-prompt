from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
base = (ROOT / 'references/official/base-en.txt').read_text(encoding='utf-8')
ref = (ROOT / 'references/official/ref-en.txt').read_text(encoding='utf-8')
director = (ROOT / 'references/director/AIMIXER_DIRECTOR_RULES.md').read_text(encoding='utf-8')

# Version
assert 'version: "1.7.0-2026.08.29"' in skill

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

print('OK v1.7')
