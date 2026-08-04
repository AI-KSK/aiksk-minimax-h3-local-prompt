import json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from h3_refmap import build_manifest_from_manual, build_manifest_from_workflow

class RefMapTests(unittest.TestCase):
    def test_video_soundtrack_then_standalone(self):
        m=build_manifest_from_manual({"connected":{"ref_images":[0],"ref_videos":[0],"ref_video_audios":[0],"ref_audios":[0]}})
        self.assertEqual([x['label'] for x in m['audios']],['<Audio 1>','<Audio 2>'])
        self.assertEqual(m['audios'][0]['kind'],'video_soundtrack')
        self.assertEqual(m['audios'][1]['kind'],'standalone_audio')
        self.assertEqual(m['videos'][0]['label'],'<Video 1>')
    def test_no_soundtrack_standalone_is_audio1(self):
        m=build_manifest_from_manual({"connected":{"ref_videos":[0],"ref_audios":[0]}})
        self.assertEqual(m['audios'][0]['label'],'<Audio 1>')
    def test_orphan_soundtrack_errors_and_is_ignored(self):
        m=build_manifest_from_manual({"connected":{"ref_images":[0],"ref_video_audios":[0]}})
        self.assertTrue(any('will not register' in x for x in m['errors']))
        self.assertEqual(m['audios'],[])
    def test_two_video_soundtracks_then_voice(self):
        m=build_manifest_from_manual({"connected":{"ref_images":[0],"ref_videos":[0,1],"ref_video_audios":[0,1],"ref_audios":[0]}})
        self.assertEqual([x['label'] for x in m['audios']],['<Audio 1>','<Audio 2>','<Audio 3>'])
        self.assertEqual([x['label'] for x in m['videos']],['<Video 1>','<Video 2>'])
    def test_holes_are_compacted(self):
        m=build_manifest_from_manual({"connected":{"ref_images":[2],"ref_videos":[1],"ref_audio_0" if False else "ref_audios":[2]}})
        self.assertEqual(m['pictures'][0]['label'],'<Picture 1>')
        self.assertEqual(m['videos'][0]['label'],'<Video 1>')
        self.assertEqual(m['audios'][0]['label'],'<Audio 1>')
    def test_audio_only_rejected(self):
        m=build_manifest_from_manual({"connected":{"ref_audios":[0]}})
        self.assertTrue(any('sole input' in x for x in m['errors']))
    def test_official_uploaded_workflow_has_two_pictures_only(self):
        p=Path('/mnt/data/video_minimax_h3_r2v.json')
        if not p.exists(): self.skipTest('uploaded official workflow unavailable')
        ms=build_manifest_from_workflow(p)
        self.assertTrue(ms)
        m=ms[0]
        self.assertEqual(len(m['pictures']),2)
        self.assertEqual(len(m['videos']),0)
        self.assertEqual(len(m['audios']),0)

if __name__=='__main__':unittest.main()
