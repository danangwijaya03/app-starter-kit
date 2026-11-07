# Task graph validation

Run `.venv-agent/bin/python tools/validate_plan.py` after installing PyYAML. The registry should contain 161 unique task IDs (157 preserved + P01-08, P01-09, P02-07, P03-09) across P00–P16, no missing or cyclical dependencies, 157 cards and 17 phase files. A green graph check validates documentation only, not app behavior.
