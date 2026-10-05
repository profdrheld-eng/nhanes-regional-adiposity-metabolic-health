"""Aggregate revision evidence and figures; no alteration of raw files."""
from pathlib import Path
import os, tarfile, io, json, platform
ROOT=Path(__file__).resolve().parents[2]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'03_analysis/environment/matplotlib-cache'))
os.environ.setdefault('MPLBACKEND','Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
R=ROOT/'04_outputs/results'; F=ROOT/'04_outputs/figures'
d=pd.read_csv(ROOT/'02_data/derived/harmonized_analysis_data.csv',low_memory=False)
def yes(x): return x.astype(str).str.lower().eq('true')
p=d[yes(d.primary_domain)].copy(); p['event']=yes(p.metabolic_dysfunction).astype(int)
pre=d[yes(d.eligible)&(d.pooled_fasting_weight>0)&d.leg_trunk_ratio.notna()].copy()
vars=['LBXTR','LBDHDD','mean_sbp','mean_dbp','LBXGLU','antihypertensive_med','lipid_med_proxy','high_tg','low_hdl','high_bp','high_glucose','education','INDFMPIR','smoking']
pd.DataFrame([{'variable':v,'denominator':len(pre),'missing_n':pre[v].isna().sum()} for v in vars]).to_csv(R/'missingness_before_selection.csv',index=False)
rows=[]
for c,g in pre.groupby('cycle'):
    for name,h,t,r,med in [('Blood pressure','BPQ020','BPQ050A','BPQ040A','antihypertensive_med'),('Lipids','BPQ080','BPQ100D','BPQ090D','lipid_med_proxy')]:
        skip=g[h].eq(1)&g[r].eq(2)&g[t].isna()
        rows.append(dict(cycle=c,component=name,negative_skip_n=int(skip.sum()),remaining_unknown_n=int(g.loc[skip,med].isna().sum())))
pd.DataFrame(rows).to_csv(R/'skip_rule_verification.csv',index=False)
# Historical revision_population_comparison.csv is supplied as aggregate provenance.
# It is not regenerated because the superseded individual-level archive is not distributed.
rows=[]
for label,g in [('Development 2011–2016',p[p.cycle.ne('2017-2018')]),('Test 2017–2018',p[p.cycle.eq('2017-2018')])]:
    w=g.pooled_fasting_weight
    rows.extend([dict(sample=label,characteristic='Participants / cases',value=f'{len(g)} / {g.event.sum()}'),dict(sample=label,characteristic='Weighted outcome prevalence, %',value=f'{100*np.average(g.event,weights=w):.1f}'),dict(sample=label,characteristic='Female participants, n (weighted %)',value=f'{g.sex.eq("Women").sum()} ({100*np.average(g.sex.eq("Women"),weights=w):.1f})')])
    for v in ['RIDAGEYR','BMXBMI','BMXWAIST','INDFMPIR','total_fmi','log_leg_trunk_ratio','ag_ratio','vat_kg']:
        known=g[v].notna(); x=g.loc[known,v]; wt=w[known]; mu=np.average(x,weights=wt); sd=np.sqrt(np.average((x-mu)**2,weights=wt))
        rows.append(dict(sample=label,characteristic=v,value=f'{mu:.2f} ({sd:.2f}); missing {int((~known).sum())}'))
    for v in ['race_ethnicity','education','smoking']:
        for level in sorted(g[v].dropna().unique(),key=str): rows.append(dict(sample=label,characteristic=f'{v}: {level}',value=f'{g[v].eq(level).sum()} ({100*np.average(g[v].eq(level),weights=w):.1f}%)'))
pd.DataFrame(rows).to_csv(R/'development_test_description.csv',index=False)
# Weighted empirical quantiles describe exposure support, not clinical thresholds.
def wq(x,w,q):
    idx=np.argsort(x); x=np.asarray(x)[idx]; w=np.asarray(w)[idx]
    return np.interp(q,(np.cumsum(w)-.5*w)/sum(w),x)
q=[]
for sex,g in p.groupby('sex'):
    vals=wq(g.log_ltr_z,g.pooled_fasting_weight,[.05,.5,.95]);q.append(dict(sex=sex,p05=vals[0],p50=vals[1],p95=vals[2],n=len(g)))
support=pd.DataFrame(q); support.to_csv(R/'exposure_support.csv',index=False)
lo=support.p05.max();hi=support.p95.min()
curve=pd.read_csv(R/'nonlinear_prediction_curve.csv')
fig,axes=plt.subplots(2,1,figsize=(7,7),sharex=True,gridspec_kw={'height_ratios':[2,1]})
for sex,color in [('Men','#0072B2'),('Women','#CC79A7')]:
    g=curve[curve.sex.eq(sex)];axes[0].plot(g.log_ltr_z,g.predicted_prevalence,label=sex,color=color);axes[0].fill_between(g.log_ltr_z,g.ci_low,g.ci_high,color=color,alpha=.17)
    g=p[p.sex.eq(sex)]; axes[1].hist(g.log_ltr_z,bins=np.linspace(-2,2,25),weights=g.pooled_fasting_weight/g.pooled_fasting_weight.sum(),histtype='step',color=color,label=sex)
for ax in axes:
    ax.axvspan(lo,hi,color='grey',alpha=.1);ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Fitted mean (95% CI)');axes[0].legend(frameon=False)
axes[1].set(xlabel='Log leg-to-trunk fat ratio, pooled SD units',ylabel='Weighted proportion',xlim=(-2,2))
fig.tight_layout();fig.savefig(F/'figure_s1_nonlinearity.png',dpi=250);plt.close(fig)
# Bins are descriptive; fitted calibration is not a model update.
pred=pd.read_csv(ROOT/'02_data/derived/protected_test_predictions.csv');rows=[]
fig,ax=plt.subplots(figsize=(6,5))
for model,color in [('penalized_logistic','#0072B2'),('spline_logistic','#009E73'),('xgboost','#D55E00')]:
    prob=pred['D_dxa__'+model]; bins=pd.qcut(prob,10,duplicates='drop')
    tmp=[]
    for _,idx in pred.groupby(bins,observed=True).groups.items():
        g=pred.loc[idx];w=g.pooled_fasting_weight
        row=dict(model=model,n=len(g),predicted=np.average(prob.loc[idx],weights=w),observed=np.average(g.outcome,weights=w));rows.append(row);tmp.append(row)
    z=pd.DataFrame(tmp);ax.plot(z.predicted,z.observed,'o-',label=model.replace('_',' '),color=color,markersize=4)
ax.plot([0,1],[0,1],'k--',linewidth=1);ax.set(xlabel='Mean predicted probability',ylabel='Observed weighted proportion',xlim=(0,1),ylim=(0,1));ax.legend(frameon=False);ax.spines[['top','right']].set_visible(False);fig.tight_layout();fig.savefig(F/'figure_s2_calibration.png',dpi=250);plt.close(fig)
pd.DataFrame(rows).to_csv(R/'calibration_bins.csv',index=False)
import sklearn,xgboost,statsmodels,scipy
(ROOT/'03_analysis/environment/revision-runtime.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,sklearn=sklearn.__version__,xgboost=xgboost.__version__,statsmodels=statsmodels.__version__,scipy=scipy.__version__),indent=2))
print('Revision aggregate evidence and figures built.')
