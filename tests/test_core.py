# Purpose: Verify strategy order, call packing, holdout isolation, durability and evaluation.
import tempfile,unittest
from pathlib import Path
from jev_label import *
ROWS=[{'id':'a','probability':.49,'probabilities':{'x':.51,'y':.49},'committee':[.1,.9],'label':1},{'id':'b','probability':.9,'probabilities':{'x':.9,'y':.1},'committee':[.8,.9],'label':1},{'id':'c','probability':.2,'probabilities':{'x':.6,'y':.4},'committee':[.2,.2],'label':0}]
class Tests(unittest.TestCase):
 def test_strategies(self):
  self.assertEqual(select(ROWS,'uncertainty',1)[0]['id'],'a');self.assertEqual(select(ROWS,'margin',1)[0]['id'],'a');self.assertEqual(select(ROWS,'entropy',1)[0]['id'],'a');self.assertEqual(select(ROWS,'committee',1)[0]['id'],'a');self.assertEqual(select(ROWS,'random',3,seed=2),select(ROWS,'random',3,seed=2))
 def test_committee_single_call(self):
  f=FakeJev();r=prelabel([{'id':'x','text':'t'}],[{},{}],f);self.assertEqual(len(f.calls),1);self.assertEqual(len(r[0]['committee']),2)
 def test_holdout_excluded(self):self.assertNotIn('a',[r['id'] for r in select(ROWS,'uncertainty',3,holdout_ids=['a'])])
 def test_durable_resume(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'labels.jsonl';write_label(p,ROWS[0],1,'reviewer');self.assertEqual(resume_ids(p),{'a'})
 def test_threshold_and_wilson(self):
  t=fit_threshold(ROWS);self.assertIn(t,[.2,.49,.9]);self.assertGreater(wilson(0,10)[1],0);self.assertIn('accuracy_interval',evaluate(ROWS,t))
 def test_simulation_fixed(self):self.assertEqual(simulate(ROWS,['random'],step=1,seed=3),simulate(ROWS,['random'],step=1,seed=3))
if __name__=='__main__':unittest.main()
