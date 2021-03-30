from .core import SQLFocus, logger

INSERT_INTO_SQL = "INSERT INTO {name} VALUES ({values});"
CREATE_SQL = "CREATE TABLE {exists}{name} ({vars});"
SELECT_SQL = "SELECT * FROM {name}"
DELETE_SQL = "DELETE FROM {name}"
UPDATE_SQL = "UPDATE {name} SET {vars}"


sqlfocus = SQLFocus()


class SQLTableBase:
    def __init__(self, conn=None, quote='"'):
        self.name = self.__class__.__name__.lower()
        self.conn = conn
        self.quote = quote

    async def create(self, schema, exists):
        colums = [" ".join(var) for var in schema]

        return self.execute(CREATE_SQL.format(
            name=self.name,
            exists="IF NOT EXISTS " if exists else "",
            vars=", ".join(colums)
        ))

    async def execute(self, sql):
        logger.debug(sql)
        return await self.conn.execute(sql)

    async def commit(self):
        return await self.conn.commit()

    @sqlfocus.fetch(one=True)
    @sqlfocus.execute
    async def selectone(self):
        return SELECT_SQL.format(name=self.name)

    @sqlfocus.fetch(one=False)
    @sqlfocus.execute
    async def select(self):
        return SELECT_SQL.format(name=self.name)

    @sqlfocus.execute
    async def delete(self):
        return DELETE_SQL.format(name=self.name)

    @sqlfocus.execute
    async def update(self, exists=False, **kwargs):
        return UPDATE_SQL.format(
            vars=" AND ".join(all2string(kwargs)),
            name=self.name
        )

    @sqlfocus.execute
    async def insert(self, *args):
        return INSERT_INTO_SQL.format(
            name=self.name,
            values=", ".join(all2string(args, self.quote))
        )


class SQLTable(SQLTableBase):
    def __init__(self, name, conn, quote='"'):
        self.name = name
        self.conn = conn
        self.quote = quote


def all2string(args, q='"'):
    if args.__class__ == list or args.__class__ == tuple:
        return [str(_) if _.__class__ != str else f"{q}{_}{q}" for _ in args]
    else:
        return [f"{_}={args[_]}" if args[_].__class__ != str
                else f"{_}={q}{args[_]}{q}" for _ in args]
