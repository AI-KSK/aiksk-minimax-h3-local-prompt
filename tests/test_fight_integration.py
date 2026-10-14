"""Regression + smoke checks for H3 fight preset compiler (no GPU inference)."""
import hashlib
import importlib.util
import json
import re
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'scripts/sync_fight_workflow.py'
spec=importlib.util.spec_from_file_location('h3_fight_sync',F)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

cfg=m.load_cfg()
wf=m.DEFAULT_WORKFLOW
assert wf.is_file()
original_bytes=wf.read_bytes()
original_hash=hashlib.sha256(original_bytes).hexdigest()
workflow=json.loads(original_bytes)
orig_links=workflow['links']
orig_nodes={n['id']:n for n in workflow['nodes']}
assert len(cfg['presets'])==9
assert set(cfg['baseline']['weights'])==set(cfg['lora_order'])
assert all(v==0 for v in cfg['baseline']['weights'].values())
assert [x['id'] for x in cfg['presets']]==[f'A{i}' for i in range(9)]
assert len(cfg['model_cards'])==5
assert all(cfg['lora_files'][k] in [n.get('widgets_values',[''])[0] for n in workflow['nodes'] if n['type']=='LoraLoaderModelOnly'] for k in cfg['lora_files'])
assert all(n['id'] in orig_nodes for n in workflow['nodes'])
# Every source/target reference must exist, and each linked input points to its link record.
link_by_id={x[0]:x for x in orig_links}
assert len(link_by_id)==len(orig_links)
for link in orig_links:
    assert link[1] in orig_nodes and link[3] in orig_nodes,link
    destination=orig_nodes[link[3]]
    assert destination['inputs'][link[4]]['link']==link[0],(link,destination['inputs'])

scenes={'A0':'unarmed','A1':'unarmed','A2':'unarmed','A3':'unarmed','A4':'weapon','A5':'gunfu','A6':'gunfu','A7':'gunfu','A8':'motion','BASE':'unarmed'}
for preset,scene in scenes.items():
    assert m.row_for(cfg,preset)['prompt_strategy']['scene']==scene
    tg=m.triggers(cfg,m.row_for(cfg,preset),scene)
    assert len(tg)==len(set(tg))
    if preset=='A4':assert tg==['BUNNY']
    if preset in ['A5','A6','A7']:assert tg==['BUNNY']
    if preset in ('A2','A3'):assert tg==['Unarmed combat interaction']
    if preset=='BASE':assert tg==[]
    for mode in ('T2VA','R2VA'):
        prompt=m.compose(cfg,preset,mode)
        if mode=='T2VA':
            required=['integrated_multimodal_description:','overall_soundscape:','non_diegetic_music:']
            assert not re.search(r'^subject_definitions:',prompt,re.M)
            assert '<Picture 1>' not in prompt
        else:
            required=['subject_definitions:','summary:','retention_analysis:','detailed_description:','overall_soundscape:','non_diegetic_music:']
            assert '<Picture 1>' in prompt and '<Picture 2>' in prompt
            assert '<Subject 1>' in prompt and '<Subject 2>' in prompt
            assert '<Audio 1>' not in prompt and 'video editing' not in prompt
        positions=[]
        for s in required:
            assert prompt.count(s)==1,(preset,mode,s)
            positions.append(prompt.index(s))
        assert positions==sorted(positions)
        assert any(word in prompt for word in {'contact','parry','counter','rotation'}),(preset,mode)
        assert not any(x in prompt for x in ('strength_model:','generated_sparsity:','fight_lora:'))
        if scene=='weapon':assert 'sword' in prompt.lower() and 'BUNNY' in prompt
        if scene=='gunfu':assert 'gun-fu' in prompt.lower() and 'BUNNY' in prompt
        if preset=='BASE':assert 'BUNNY' not in prompt and 'interaction.' not in prompt.lower()

assert m.triggers(cfg,m.row_for(cfg,'A0'),'unarmed','finisher')==['prfight2','prfin1']
assert m.triggers(cfg,m.row_for(cfg,'A0'),'unarmed','intense')==['prfight2']
assert m.triggers(cfg,m.row_for(cfg,'A1'),'unarmed',motion_trigger=True)==['bunny_crisp_motion']
assert m.triggers(cfg,m.row_for(cfg,'BASE'),'unarmed','finisher',True)==[]
assert '<Subject 1>' in m.compose(cfg,'A4','R2VA',fighter_a='adult actor with silver hair')
assert 'adult actor with silver hair' in m.compose(cfg,'A4','R2VA',fighter_a='adult actor with silver hair')
assert not ('in dark practice clothing' in m.compose(cfg,'A4','R2VA'))

# Cross-file human-readable and source documentation checks.
triggers_doc=(ROOT/'references/playbooks/fight-trigger-policy.md').read_text(encoding='utf-8')
for term in ['prfight2','prfin1','BUNNY','bunny_crisp_motion','Unarmed combat interaction','Melee weapon interaction','Gun-fu interaction']:
    assert term in triggers_doc,term
for term in ('A4','A7','BASE','R2VA','4 步','8 步'):
    assert term in (ROOT/'references/playbooks/fight-prompt-mapping.md').read_text(encoding='utf-8') or term in (ROOT/'references/playbooks/fight-choreography.md').read_text(encoding='utf-8')

# Running offline exporter with each preset and both modes produces valid, aligned workflow JSON.
with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    for preset in ['BASE']+[f'A{i}' for i in range(9)]:
        for mode in ('T2VA','R2VA'):
            out=td/f'{preset}_{mode}.json'
            audit=m.export(wf,cfg,preset,mode,out)
            data=json.loads(out.read_text(encoding='utf-8'))
            nodes={n['id']:n for n in data['nodes']}
            assert len(data['nodes'])==len(workflow['nodes'])
            assert data['links']==orig_links
            assert len(data['links'])==len(orig_links)
            assert audit['mode']==mode and audit['preset']==preset
            assert audit['runtime_UI_switching_changes_prompt_automatically'] is False
            assert nodes[35]['widgets_values'][0]==(mode=='R2VA')
            assert nodes[17]['widgets_values'][0]==m.compose(cfg,preset,'T2VA')
            assert nodes[25]['widgets_values'][0]==m.compose(cfg,preset,'R2VA')
            assert len([n for n in nodes.values() if n['type']=='VedaSparseAttention'])==2
            assert len([n for n in nodes.values() if n['type']=='LoraLoaderModelOnly'])==12
            for n in [n for n in nodes.values() if n['type']=='LoraLoaderModelOnly' and n['id']>=37]:
                lora=next(k for k,v in cfg['lora_files'].items() if v==n['widgets_values'][0])
                assert n['widgets_values'][1]==m.row_for(cfg,preset)['weights'][lora]
                assert n['widgets_values_named']['strength_model']==m.row_for(cfg,preset)['weights'][lora]
            if preset=='BASE':
                assert nodes[40]['widgets_values'][0] is True
                assert [nodes[i]['widgets_values'][0] for i in (41,43,45,47,49)]==[0]*5
            else:
                assert nodes[40]['widgets_values'][0] is False
                assert nodes[39]['widgets_values'][0]==int(preset[1:])
            audit_on_disk=json.loads(out.with_suffix('.audit.json').read_text(encoding='utf-8'))
            assert audit_on_disk['preset']==preset
    try:
        m.export(wf,cfg,'A4','R2VA',wf)
        assert False,'Should refuse overwriting source'
    except ValueError:pass
    # Hard guard against differing workflow node layouts.
    bad=td/'bad.json'
    broken=json.loads(original_bytes)
    broken['nodes']=[n for n in broken['nodes'] if n['id']!=39]
    bad.write_text(json.dumps(broken),encoding='utf-8')
    try:
        m.export(bad,cfg,'A4','R2VA',td/'badoutput.json')
        assert False,'Should refuse mismatched node layout'
    except ValueError:pass
    assert not (td/'badoutput.json').exists()
assert wf.read_bytes()==original_bytes and hashlib.sha256(wf.read_bytes()).hexdigest()==original_hash
print('OK v1.8.1 integration: 20 workflow variants and trigger/prompt/base/source regression checks')
