# Selection and evaluation

Uncertainty uses distance to threshold, margin uses the top-two probability gap, entropy uses the whole distribution, committee uses variance between same-request phrasings, and random is the baseline. A random holdout is removed before selection. Thresholds fit only on tuning labels; evaluation uses Wilson intervals on the untouched holdout.
