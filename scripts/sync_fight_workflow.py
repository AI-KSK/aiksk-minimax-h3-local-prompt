#!/usr/bin/env python3
"""Export preset-consistent MiniMax H3 T2VA/R2VA Veda workflow + prompts.

Pure Python stdlib; no ComfyUI runtime/network calls. Does not overwrite input.
"""
import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'references/playbooks/fight-lora-presets.json'
DEFAULT_WORKFLOW=ROOT/'integrations/AIKSK_H3_JOKER141_九预设_T2VA_R2VA_Veda_单阶段.json'

STORY={
 'unarmed': ("Two adult fighters exchange a tightly choreographed unarmed martial-arts combination in a clean stone courtyard with one stable screen axis.",
             "At 0.0-1.0 s, both settle into guarded full-body stances. At 1.0-2.2 s, A steps from screen left and throws a controlled right-hand strike; B redirects it with the left forearm, visible forearm-to-forearm contact. At 2.2-3.65 s, B pivots and counters with one readable palm strike; A slips back, transfers weight onto the rear foot and recovers the guard. At 3.65-5.17 s, they separate and stabilize without changing identities or clothing.",
             "Footfalls and cloth swishes track every step; the parry has a single short contact sound, followed by breath and a soft landing."),
 'weapon': ("Two adult wuxia duelists cross matching but distinct practice swords in a sunlit stone courtyard; each has exactly one sword and keeps the same owner and grip.",
            "At 0.0-1.0 s, A stands on screen left holding one steel practice sword in the right hand and B faces A on screen right holding one sword in the right hand. At 1.0-2.2 s, A draws one clear horizontal arc; B meets the flat of A's blade with a controlled parry. At 2.2-3.65 s, their blades slide apart; B rotates the wrist and makes one reply cut while A steps diagonally aside. At 3.65-5.17 s, both lower their blades into visible guard positions, with each weapon still in its original owner's hand; no duplicated blades.",
            "A clean metallic sword contact exactly at the parry, footsteps and cloth movement, followed by separated steel resonance and a final steady room ambience."),
 'gunfu': ("Two adult performers act out a fictional cinematic gun-fu exchange on a controlled movie set; the scene emphasizes continuity and readable dramatic blocking rather than actionable tactical instruction.",
           "At 0.0-1.0 s, the two figures face each other in a medium-wide shot, clearly separated; one prop firearm belongs to each character. At 1.0-2.2 s, A makes a short dramatic feint and B turns defensively, their positions remaining clear. At 2.2-3.65 s, B shifts direction in a single stylized counter-movement, A staggers back and recovers balance, with no abrupt disappearance or swapping of props. At 3.65-5.17 s, both settle into a visibly separated final pose with consistent hands, wardrobes, and prop ownership.",
           "Cinematic prop movement, footsteps, fabric movement, a restrained stage-impact cue and room reflections synchronized to visible beats."),
 'motion': ("Two adult performers demonstrate continuous high-difficulty acrobatic movement across a clean studio floor, focusing on physically readable transitions.",
           "At 0.0-1.0 s, A establishes a grounded stance at screen left and B watches from the right. At 1.0-2.2 s, A steps into one controlled turning leap; B stays physically distinct. At 2.2-3.65 s, A completes a continuous rotation with a single stable body orientation and lands on the marked floor. At 3.65-5.17 s, A regains the guard and B steps into position, with no discontinuous limbs, impossible teleport or pose reset.",
           "Approach steps, controlled fabric motion, one landing sound and light studio ambience aligned to the visible action."),
}

def load_cfg():return json.loads(CONFIG.read_text(encoding='utf-8'))
def row_for(cfg,preset):
 if preset=='BASE':return {**cfg['baseline'],'style':'unarmed','prompt_strategy':{'scene':'unarmed'}}
 for row in cfg['presets']:
  if row['id']==preset:return row
 raise ValueError(f'Unknown preset {preset}')

def triggers(cfg,row,scene,combat_trigger='default',motion_trigger=False):
 weights=row['weights']; cards=cfg['model_cards']; out=[]
 if weights['Weapon Combat V1']>0:out.append(cards['Weapon Combat V1']['default_trigger'])
 if weights['GunFu']>0:out.append(cards['GunFu']['default_trigger'])
 if weights['Combat V2']>0 and combat_trigger in ('intense','finisher'):
  out.extend(cards['Combat V2']['variants'][combat_trigger])
 if weights['Motion Repair V2']>0 and motion_trigger:out.append(cards['Motion Repair V2']['optional_trigger'])
 if weights['Fight Flow V1']>0:out.append(cards['Fight Flow V1']['trigger_by_scene'][scene])
 # Preserve model-card order while removing shared BUNNY duplicates.
 return list(dict.fromkeys(out))

def compose(cfg,preset,mode,fighter_a='',fighter_b='',combat_trigger='default',motion_trigger=False):
 row=row_for(cfg,preset);scene=row['prompt_strategy']['scene']; intro,beats,sound=STORY[scene]
 tags=triggers(cfg,row,scene,combat_trigger,motion_trigger)
 tagtext=(' '.join(f'{t}.' for t in tags)+' ') if tags else ''
 if mode=='T2VA':
  ids=(f'Fighter A: {fighter_a.strip() or "adult performer in dark practice clothing"}. '
       f'Fighter B: {fighter_b.strip() or "adult performer in contrasting light practice clothing"}. ')
  return (f'integrated_multimodal_description:\n[Shot 1] {tagtext}{intro} {ids}'
          'Keep both faces, wardrobe and screen-left/screen-right assignments consistent; '
          'a medium-wide full-body shot with one slow lateral tracking motion. '
          f'{beats} No subtitles, overlays or extra fighters.\n\n'
          f'overall_soundscape:\n{sound} No dialogue.\n\n'
          'non_diegetic_music:\nN/A\n')
 if mode!='R2VA':raise ValueError('mode must be T2VA or R2VA')
 # Reference images are identities; their unknown visual properties must not be guessed.
 a=fighter_a.strip() or 'appearance, outfit and proportions exactly as shown in <Picture 1>'
 b=fighter_b.strip() or 'appearance, outfit and proportions exactly as shown in <Picture 2>'
 return (f'subject_definitions:\n<Subject 1> is Fighter A, preserving {a}; referenced by <Picture 1>.\n'
         f'<Subject 2> is Fighter B, preserving {b}; referenced by <Picture 2>.\n\n'
         f'summary:\n[reference generation] A single continuous cinematic action exchange between <Subject 1> '
         f'and <Subject 2>, retaining their separate reference identities; the images are identity references, not two sequential shots.\n\n'
         f'retention_analysis:\n<Subject 1> (appears in [Shot 1]): fully_preserved - identity, facial structure, hairstyle, outfit and proportions as shown in <Picture 1>.\n'
         f'<Subject 2> (appears in [Shot 1]): fully_preserved - identity, facial structure, hairstyle, outfit and proportions as shown in <Picture 2>.\n\n'
         f'detailed_description:\n[Shot 1] {tagtext}{intro} <Subject 1> starts on screen left and '
         f'<Subject 2> starts on screen right, using exactly the faces, clothing, accessories and body shapes in their input images. '
         'Medium-wide full-body framing, one stable camera axis and minimal side tracking. '
         f'{re.sub(r"\bB\b", "<Subject 2>", re.sub(r"\bA\b", "<Subject 1>", beats))} Track each move as <Subject 1> versus <Subject 2> without replacing their faces, '
         'duplicate weapons or swapping clothing. No new speakers or characters.\n\n'
         f'overall_soundscape:\n{sound} No dialogue or invented audio references.\n\n'
         'non_diegetic_music:\nN/A\n')

def set_widgets(n,index,value):
 w=n.get('widgets_values');
 if isinstance(w,list):w[index]=value
 names=n.get('widgets_values_named')
 if isinstance(names,dict):
  # These types expose one meaningful first scalar field.
  k={'PrimitiveInt':'value','PrimitiveBoolean':'value','PrimitiveFloat':'value','PrimitiveStringMultiline':'value'}.get(n['type'])
  if k and index==0 and k in names:names[k]=value

def export(workflow,cfg,preset,mode,out,fighter_a='',fighter_b='',combat_trigger='default',motion_trigger=False):
 if workflow.resolve()==out.resolve():raise ValueError('Input and output paths must differ: source workflow is immutable.')
 data=json.loads(workflow.read_text(encoding='utf-8'))
 nodes={n['id']:n for n in data['nodes']}
 checks={17:'PrimitiveStringMultiline',25:'PrimitiveStringMultiline',35:'PrimitiveBoolean',39:'PrimitiveInt',40:'PrimitiveBoolean',41:'PrimitiveFloat',43:'PrimitiveFloat',45:'PrimitiveFloat',47:'PrimitiveFloat',49:'PrimitiveFloat'}
 for k,t in checks.items():
  if k not in nodes or nodes[k]['type']!=t:raise ValueError(f'Workflow incompatible: expected node {k}={t}. No output written.')
 row=row_for(cfg,preset)
 # For BASE, current 9 preset numerics stay the same. BASE uses manual zeros.
 if preset=='BASE':
  set_widgets(nodes[40],0,True)
  for n in (41,43,45,47,49):set_widgets(nodes[n],0,0)
 else:
  set_widgets(nodes[39],0,int(preset[1:]))
  set_widgets(nodes[40],0,False)
 mode_r2va=(mode=='R2VA')
 set_widgets(nodes[35],0,mode_r2va)
 # Preexisting module routes have a shared Boolean input; local values retained in case link is removed.
 for n in data['nodes']:
  if n['type']=='ComfySwitchNode' and n['id'] in (29,30,31,32):set_widgets(n,0,mode_r2va)
 pt=compose(cfg,preset,'T2VA',fighter_a,fighter_b,combat_trigger,motion_trigger)
 pr=compose(cfg,preset,'R2VA',fighter_a,fighter_b,combat_trigger,motion_trigger)
 set_widgets(nodes[17],0,pt);set_widgets(nodes[25],0,pr)
 # Present contextual titles that do not interfere with node execution.
 nodes[17]['title']=f'T2VA {preset} | '+row['prompt_strategy']['scene']
 nodes[25]['title']=f'R2VA {preset} | '+row['prompt_strategy']['scene']
 for n in data['nodes']:
  if n['type']=='LoraLoaderModelOnly' and n['id']>=37:
   name=next((key for key,v in cfg['lora_files'].items() if v==n['widgets_values'][0]),None)
   if name is not None and len(n['widgets_values'])>1:
    n['widgets_values'][1]=row['weights'][name]
    if isinstance(n.get('widgets_values_named'),dict): n['widgets_values_named']['strength_model']=row['weights'][name]
 # Not all values are static when linked; the preset formula/manual control is source of truth.
 out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 audit={'preset':preset,'mode':mode,'scene':row['prompt_strategy']['scene'],'weights':row['weights'],
        'trigger_words':triggers(cfg,row,row['prompt_strategy']['scene'],combat_trigger,motion_trigger),
        'turbo_and_veda_kept':True,'r2va_4step_veda_status':'out-of-main-8step-training-conditions; validate empirically' if mode_r2va else None,
        'output':out.name,'input':workflow.name,'runtime_UI_switching_changes_prompt_automatically':False,
        'warning':'If changing preset inside ComfyUI later, rerun the exporter or edit prompt to match.'}
 aud=out.with_suffix('.audit.json');aud.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return audit

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--preset',choices=['BASE']+[f'A{i}' for i in range(9)],default='A2')
 parser.add_argument('--mode',choices=['T2VA','R2VA'],default='T2VA')
 parser.add_argument('--workflow',type=Path,default=DEFAULT_WORKFLOW)
 parser.add_argument('--output',type=Path,required=True)
 parser.add_argument('--fighter-a',default='')
 parser.add_argument('--fighter-b',default='')
 parser.add_argument('--combat-trigger',choices=['default','intense','finisher'],default='default')
 parser.add_argument('--motion-trigger',action='store_true')
 args=parser.parse_args()
 data=export(args.workflow,load_cfg(),args.preset,args.mode,args.output,args.fighter_a,args.fighter_b,args.combat_trigger,args.motion_trigger)
 print(json.dumps(data,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
