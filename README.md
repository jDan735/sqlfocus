# sqlfocus
Simple wrapper for sql

## Example of usage (sqlite3)

```python
import sqlite3

from sqlfocus import SQLTable

sql = (
    ("id", "INTEGER"),
    ("name", "TEXT")
)

conn = sqlite3.connect("test.db")
table = SQLTable("test", conn)


"CREATE TABLE IF NOT EXISTS test (id INTEGER, name TEXT);"
table.create(exists=True, schema=sql)


'SELECT * FROM test WHERE id = 23455 AND name = "None"'
table.select()
table.select(where=["id = 23455", 'name = "None"'])


'INSERT INTO test VALUES (23455, "None")'
table.insert(23455, "None")

conn.commit()
```
