from .core import SQLFocus, logger
from .field import Field
from .helpers import all2string

INSERT_INTO_SQL = "INSERT INTO {name} VALUES ({values});"
CREATE_SQL = "CREATE TABLE {exists}{name} ({vars});"
SELECT_SQL = "SELECT * FROM {name}"
DELETE_SQL = "DELETE FROM {name}"
UPDATE_SQL = "UPDATE {name} SET {vars}"


sqlfocus = SQLFocus()


class SQLTableBase:
    def __init__(self, conn=None, quote='"'):
        self._name = self.__class__.__name__.lower()
        self._conn, self.conn = conn, conn
        self._quote = quote

    async def load(self):
        if self.__dict__.get("colums") is None:
            master = SQLTable("sqlite_master", self._conn)
            this = await master.select(where=f'name="{self._name}"')
            sql = this[-1][-1]

            self._colums = sql[sql.find("(") + 1:-1].split(", ")

        self.__load()

    def __load(self):
        for column in self._colums:
            name = column.split()[0]
            self.__dict__[name] = Field(name)

    async def create(self, schema, exists):
        self._colums = [" ".join(var) for var in schema]
        self.__load()

        return await self.execute(CREATE_SQL.format(
            name=self._name,
            exists="IF NOT EXISTS " if exists else "",
            vars=", ".join(self._colums)
        ))

    async def execute(self, sql):
        logger.debug(sql)
        return await self._conn.execute(sql)

    async def commit(self):
        return await self._conn.commit()

    @sqlfocus.fetch(one=True)
    @sqlfocus.execute
    async def selectone(self):
        return SELECT_SQL.format(name=self._name)

    @sqlfocus.fetch(one=False)
    @sqlfocus.execute
    async def select(self):
        return SELECT_SQL.format(name=self._name)

    @sqlfocus.execute
    async def delete(self):
        return DELETE_SQL.format(name=self._name)

    @sqlfocus.execute
    async def update(self, exists=False, **kwargs):
        return UPDATE_SQL.format(
            vars=" AND ".join(all2string(kwargs)),
            name=self._name
        )

    @sqlfocus.execute
    async def insert(self, *args):
        return INSERT_INTO_SQL.format(
            name=self._name,
            values=", ".join(all2string(args, self._quote))
        )


class SQLTable(SQLTableBase):
    def __init__(self, name, conn, quote='"'):
        self._name = name
        self._conn, self.conn = conn, conn
        self._quote = quote
