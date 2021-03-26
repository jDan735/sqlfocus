from .table import SQLTable, SQLTableBase

__version__ = "0.1.9"


class SQLFocus:
    def __init__(self, module, db_name="sqlite"):
        self.conn = module.connect(db_name)
        self.table = SQLTable
