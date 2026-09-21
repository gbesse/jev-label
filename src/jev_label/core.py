# Purpose: Selection strategies, holdout isolation, durable review and evaluation.
import json,math,random
from datetime import datetime,timezone
from pathlib import Path
from statistics import NormalDist
def split_holdout(rows,fraction=.2,seed=7):
 ids=list(range(len(rows)));random.Random(seed).shuffle(ids);n=round(len(rows)*fraction);held=set(ids[:n]);return [r for i,r in enumerate(rows) if i not in held],[r for i,r in enumerate(rows) if i in held]
def _entropy(dist):return -sum(p*math.log(p,2) for p in dist.values() if p>0)
def score(row,strategy,threshold=.5):
 probs=row.get('probabilities',{})
 if strategy=='uncertainty':return -abs(row['probability']-threshold)
 if strategy=='margin':
  values=sorted(probs.values(),reverse=True);return -(values[0]-values[1])
 if strategy=='entropy':return _entropy(probs)
 if strategy=='committee':
  votes=row['committee'];mean=sum(votes)/len(votes);return sum((x-mean)**2 for x in votes)/len(votes)
 if strategy=='random':return 0
 raise ValueError('Unknown strategy')
def select(rows,strategy,budget,*,holdout_ids=(),seed=7,threshold=.5):
 eligible=[r for r in rows if r['id'] not in set(holdout_ids)]
 if strategy=='random':eligible=list(eligible);random.Random(seed).shuffle(eligible);return eligible[:budget]
 return sorted(eligible,key=lambda r:(-score(r,strategy,threshold),str(r['id'])))[:budget]
class FakeJev:
 def __init__(self):self.calls=[]
 def judge(self,state,questions):self.calls.append((state,questions));return [state.get('fixture',.5+i*.1) for i in range(len(questions))]
def prelabel(rows,questions,provider):
 output=[]
 for row in rows:
  answers=provider.judge({'text':row['text'],'fixture':row.get('fixture',.5)},questions);output.append({**row,'committee':answers,'probability':answers[0]})
 return output
def write_label(path,row,label,labeler):
 record={'id':row['id'],'label':label,'labeler':labeler,'timestamp':datetime.now(timezone.utc).isoformat(),'model_answer':row.get('probability')}
 with Path(path).open('a') as h:h.write(json.dumps(record)+'\n')
 return record
def resume_ids(path):
 p=Path(path);return {json.loads(x)['id'] for x in p.read_text().splitlines()} if p.exists() else set()
def wilson(k,n,confidence=.95):
 z=NormalDist().inv_cdf((1+confidence)/2);p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return max(0,c-h),min(1,c+h)
def fit_threshold(tuning):
 candidates=sorted({r['probability'] for r in tuning});return max(candidates,key=lambda t:sum((r['probability']>=t)==bool(r['label']) for r in tuning))
def evaluate(rows,threshold=.5):
 classes=sorted({r['label'] for r in rows});correct=sum((r['probability']>=threshold)==bool(r['label']) for r in rows);metrics={}
 for c in classes:
  tp=sum(r['label']==c and (r['probability']>=threshold)==bool(c) for r in rows);pred=sum((r['probability']>=threshold)==bool(c) for r in rows);actual=sum(r['label']==c for r in rows);metrics[str(c)]={'precision':tp/pred if pred else None,'recall':tp/actual if actual else None,'recall_interval':wilson(tp,actual) if actual else None}
 return {'accuracy':correct/len(rows),'accuracy_interval':wilson(correct,len(rows)),'classes':metrics}
def simulate(rows,strategies,step=20,budget=None,seed=7):
 budget=budget or len(rows);curves={}
 for strategy in strategies:
  order=select(rows,strategy,budget,seed=seed);curves[strategy]=[{'labels':n,'mean_positive':sum(bool(r['label']) for r in order[:n])/n} for n in range(step,len(order)+1,step)]
 return curves
