# jev-label

**Choose the human labels that teach the most, preserve every review action, and measure the gain on a clean holdout.**

[![Tests](https://github.com/gbesse/jev-label/actions/workflows/test.yml/badge.svg)](https://github.com/gbesse/jev-label/actions/workflows/test.yml) ![MIT](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.11%2B-blue) ![Public alpha](https://img.shields.io/badge/status-public_alpha-orange)

## 30-second offline quick start
`git clone https://github.com/gbesse/jev-label.git && cd jev-label && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements-dev.txt && python -m examples.offline_demo`

## Call real Jev
Set `TYPESAFE_API_KEY` before a reviewed prelabel adapter sends paid requests to `api.typesafe.ai`. The alpha transport is unwired; `python scripts/live_smoke.py` makes zero calls. Demo probabilities are synthetic.

## Library and integration
Use `split_holdout`, `prelabel`, `select`, `write_label`, `resume_ids`, `fit_threshold`, `evaluate`, and `simulate`. CLI supports `prelabel`, `review`, `evaluate`, and `simulate`; browser UI and CSV export remain future work.

## How it decides
Uncertainty, margin, entropy, committee variance and seeded random selection are pure stored-probability functions. Committee phrasings share one request. The random holdout is identified before selection and its ids are rejected by every selector. Labels append immediately with identity, time and original model answer.

## Boundaries
This alpha provides the durable terminal/library primitives, not the loopback browser UI. Simulation curves currently expose selected-set positive rate rather than retrained-model accuracy because Jev is not retrained. Thresholds are illustrative and require representative human labels. No label-saving benchmark is claimed.

## Validation
Run `python -m compileall -q src tests && python -m unittest discover -s tests && python -m examples.offline_demo`; CI uses Python 3.11 and 3.13.

## Related projects
[Question Forge](https://github.com/gbesse/question-forge), [DecisionPacks](https://github.com/gbesse/decisionpacks), and [jev-codebook](https://github.com/gbesse/jev-codebook).

Independent project; not affiliated with TypeSafe AI. [API docs](https://docs.typesafe.ai/api) · [model notes](https://docs.typesafe.ai/model-jaggedness/jev-1.13/)
