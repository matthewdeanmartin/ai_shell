# Bug Trail

This is a workstation logger to capture bugs encountered while you are writing code.

## Installation

```bash
pip install bug-trail
```

## Usage

```python
import bug_trail
import logging 

db_path = "error_log.db"
handler = bug_trail.ErrorLogSQLiteHandler(db_path)
logging.basicConfig(handlers=[handler], level=logging.ERROR)

logger = logging.getLogger(__name__)
logger.error("This is an error message")
```

To generate to the log folder relative to the current working directory:

```bash
bug_trail --output logs --db error_log.db
```

## Security
None. Do not publish your error log to the internet. Add the log folder to your .gitignore file.

## Prior Art
Inspired by elmah. Much less ambitious, as this is just a browsable, static HTML report.