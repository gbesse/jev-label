# Purpose: Prelabel, select, evaluate and simulate JSONL datasets.
import argparse,json,sys
from pathlib import Path
from .core import *
def rows(path):return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
def main(argv=None):
 p=argparse.ArgumentParser(prog='jev-label');p.add_argument('command',choices=['prelabel','review','evaluate','simulate']);p.add_argument('input');p.add_argument('--out');p.add_argument('--strategy',default='uncertainty');p.add_argument('--budget',type=int,default=20);p.add_argument('--labels');a=p.parse_args(argv)
 try:
  data=rows(a.input)
  if a.command=='prelabel':result=prelabel(data,[{'statement':'primary'},{'statement':'alternate'}],FakeJev())
  elif a.command=='review':result=select(data,a.strategy,a.budget,holdout_ids=[])
  elif a.command=='evaluate':result=evaluate(data,fit_threshold(data))
  else:result=simulate(data,a.strategy.split(','),budget=a.budget)
  text=''.join(json.dumps(x)+'\n' for x in result) if isinstance(result,list) else json.dumps(result,indent=2);Path(a.out).write_text(text) if a.out else print(text)
 except Exception as e:print(f'jev-label: {e}',file=sys.stderr);raise SystemExit(1)
