from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')

required = [
    'integrated_multimodal_description',
    'overall_soundscape',
    'non_diegetic_music',
    'subject_definitions',
    'retention_analysis',
    'detailed_description',
    '<Subject N>', '<Picture N>', '<Video N>', '<Audio N>',
    'fully_preserved', 'partially_preserved', 'attribute_transfer', 'weak_reference',
    'fully_copy', 'partially_copy', 'reference',
]

for item in required:
    assert item in skill, item

for path in [
    ROOT/'references/official/base-en.txt',
    ROOT/'references/official/ref-en.txt',
    ROOT/'references/playbooks/use-case-catalog.md',
    ROOT/'references/CROSS_VALIDATION.md',
]:
    assert path.exists(), path

print('OK')
