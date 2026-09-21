# Purpose: Demonstrate committee selection and holdout exclusion with synthetic data.
from jev_label import select
rows=[{'id':'1','probability':.5,'probabilities':{'a':.5,'b':.5},'committee':[.1,.9]},{'id':'2','probability':.9,'probabilities':{'a':.9,'b':.1},'committee':[.8,.9]}]
print({'source':'synthetic fixture','selected':[x['id'] for x in select(rows,'committee',1,holdout_ids=['2'])]})
