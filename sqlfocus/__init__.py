__version__ = "0.1.3"

from .table import SQLTable


class SQLFocus:
    def __init__(self, module, db_name="sqlite"):
        self.conn = module.connect(db_name)
        self.table = SQLTable
