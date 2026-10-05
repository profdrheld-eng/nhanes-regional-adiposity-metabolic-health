"""Draw participant selection from aggregate, sequential counts only."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parents[2]
f=pd.read_csv(ROOT/'04_outputs/results/participant_flow.csv')
stages=['MEC adults 20-59, not pregnant','Positive fasting weight','Valid required DXA','All outcome components','Primary complete']
n=f.groupby('stage').n.sum().reindex(stages).astype(int).tolist()
labels=['Examined adults aged 20–59 years\nwithout recorded pregnancy','Positive fasting-subsample weight','Valid required DXA measurements','All four metabolic components classifiable','Primary complete-case analysis']
exclusions=['No positive fasting-subsample weight','Required DXA measures invalid or missing','At least one component unclassifiable','Incomplete primary covariates']
fig,ax=plt.subplots(figsize=(9,9));ax.set(xlim=(0,10),ylim=(0,10));ax.axis('off')
ys=[9,7.3,5.6,3.9,2.2]
def box(x,y,w,h,label):
 ax.add_patch(FancyBboxPatch((x,y-h/2),w,h,boxstyle='round,pad=0.06',facecolor='#f5f5f5',edgecolor='#444444',linewidth=1))
 ax.text(x+w/2,y,label,ha='center',va='center',fontsize=10,color='black')
for i,(y,label,count) in enumerate(zip(ys,labels,n)):
 box(.15,y,5.4,1.05,f'{label}\nn = {count:,}')
 if i<4:
  mid=(ys[i]+ys[i+1])/2
  ax.annotate('',xy=(2.85,ys[i+1]+.57),xytext=(2.85,y-.57),arrowprops=dict(arrowstyle='->',color='#444444'))
  ax.annotate('',xy=(6.0,mid),xytext=(2.85,mid),arrowprops=dict(arrowstyle='->',color='#444444'))
  reason=exclusions[i].replace('fasting-subsample','fasting-subsample\n').replace('invalid or missing','\ninvalid or missing').replace('unclassifiable','\nunclassifiable')
  box(6.1,mid,3.65,1.15,f'Excluded: {n[i]-n[i+1]:,}\n{reason}')
ax.text(2.85,.85,'Development 2011–2016: n = 3,220\nTemporal test 2017–2018: n = 751',ha='center',va='center',fontsize=10)
ax.annotate('',xy=(2.85,1.25),xytext=(2.85,1.63),arrowprops=dict(arrowstyle='->',color='#444444'))
fig.tight_layout()
for ext in ['png','svg']:fig.savefig(ROOT/f'04_outputs/figures/figure_s3_participant_flow.{ext}',dpi=200,bbox_inches='tight')
print(dict(zip(stages,n)))
