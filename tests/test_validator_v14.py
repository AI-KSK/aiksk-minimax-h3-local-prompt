import argparse,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_h3_prompt import validate

class ValidatorV14Tests(unittest.TestCase):
    def args(self,manifest,profile='direct'):
        return argparse.Namespace(mode='ref2va',profile=profile,duration=5.0,manifest=manifest,workflow=None,node_index=0,pictures=0,videos=0,audios=0,allow_placeholders=False,strict=False)
    def test_wrong_audio_number_fails(self):
        m=ROOT/'examples/ref2va/video-soundtrack-plus-voice-manifest.json'
        text='Use <Picture 1>, <Video 1>, and <Audio 3> for the target.'
        e,w=validate(self.args(m),text)
        self.assertTrue(any('unavailable Audio' in x for x in e))
    def test_port_names_fail(self):
        m=ROOT/'examples/ref2va/video-soundtrack-plus-voice-manifest.json'
        e,w=validate(self.args(m),'Use ref_audio_0 as the voice and <Picture 1> for identity.')
        self.assertTrue(any('port names' in x for x in e))
    def test_voice_needs_speaker_binding(self):
        m=ROOT/'examples/ref2va/video-soundtrack-plus-voice-manifest.json'
        e,w=validate(self.args(m),'Use <Picture 1> for identity and use the voice timbre from <Audio 2>.')
        self.assertTrue(any('speaker binding' in x for x in e))
    def test_valid_direct_example(self):
        m=ROOT/'examples/ref2va/video-soundtrack-plus-voice-manifest.json'
        text=(ROOT/'examples/ref2va/direct-video-soundtrack-plus-voice.txt').read_text(encoding='utf-8')
        e,w=validate(self.args(m),text)
        self.assertEqual(e,[])
    def test_context_ir_retention_speaker_forbidden(self):
        m=ROOT/'examples/ref2va/video-soundtrack-plus-voice-manifest.json'
        text=('subject_definitions:\n<Audio 1> is a soundtrack.\nsummary:\n[reference generation] x\n'
              'retention_analysis:\n<Audio 1> (S1): reference - x\n'
              'detailed_description:\n[Shot 1] x\noverall_soundscape:\nx\nnon_diegetic_music:\nN/A')
        a=self.args(m,'context_ir_emulation');a.allow_placeholders=True
        e,w=validate(a,text)
        self.assertTrue(any('retention_analysis' in x for x in e))

if __name__=='__main__':unittest.main()
