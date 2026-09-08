"""SQLite storage for parsed flat files.

Table schemas mirror the columns actually present in the downloaded files
(Block 0 Step 6h), plus a session_date column. Not populated until the file
columns have been observed.
"""

from __future__ import annotations
