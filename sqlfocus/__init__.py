from .table import SQLTable

__version__ = "0.1.4"


class SQLFocus:
    def __init__(self, module, db_name="sqlite"):
        self.conn = module.connect(db_name)
        self.table = SQLTable
