# Static Code Analysis — Issues and Fixes

| # | Issue | Tool | Severity | Line | Description | Fix Applied | Evidence |
|---|--------|------|----------|------|--------------|--------------|-----------|
| 1 | Mutable default argument | pylint | Medium | add_item | Used `logs=[]` which shares the same list across calls | Changed to `logs=None` and created new list inside function | Warning removed in `pylint_report_after.txt` |
| 2 | Bare except | pylint / bandit | High | remove_item | Used `except:` with `pass`, hiding all errors | Changed to `except KeyError:` and added proper log message | No Bandit B110 warning after fix |
| 3 | Use of eval() | bandit | High | main() | `eval("print('eval used')")` could execute arbitrary code | Removed `eval()` completely | Bandit report clear of B307 |
| 4 | File not closed properly | pylint | Medium | load_data / save_data | Used `open()` and `close()` manually | Replaced with `with open(...)` context managers | Resource warning gone |
| 5 | No input validation | pylint | Medium | add_item / remove_item | Allowed wrong types (e.g. `addItem(123, "ten")`) causing crash | Added type checking and error logs | No runtime errors, handled gracefully |
