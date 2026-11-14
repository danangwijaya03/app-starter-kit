# Task graph validation

Run `.venv-agent/bin/python tools/validate_plan.py` after installing PyYAML. The registry should contain 156 unique task IDs (156 task setelah 5 task installer-only dihapus) across P00–P16, no missing or cyclical dependencies, 157 cards and 17 phase files. A green graph check validates documentation only, not app behavior.
