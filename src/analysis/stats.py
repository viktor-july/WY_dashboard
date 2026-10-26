def stats(s):
    s = s.dropna()
    q1, q3 = s.quantile([0.25, 0.75])
    return dict(mean=s.mean(), std=s.std(ddof=1), median=s.median(), iqr=q3 - q1, n=len(s))