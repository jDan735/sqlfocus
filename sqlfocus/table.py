import logging

INSERT_INTO_SQL = "INSERT INTO {name} VALUES ({values});"
CREATE_SQL = "CREATE TABLE {exists}{name} ({vars});"
SELECT_SQL = "SELECT * FROM {name}"
DELETE_SQL = "DELETE FROM {name}"
UPDATE_SQL = "UPDATE {name} SET {vars}"
WHERE_SQL = " WHERE {where};"


logger = logging.getLogger("sqlfocus")


class SQLTableBase:
    def __init__(self, conn=None, quote='"'):
        self.name = self.__class__.__name__.lower()
        self.conn = conn
        self.quote = quote

    async def create(self, schema, exists=True):
        colums = []

        for var in schema:
            colums.append(" ".join(var))

        await self.execute(CREATE_SQL.format(
            name=self.name,
            exists="IF NOT EXISTS " if exists else "",
            vars=", ".join(colums)
        ))

    async def select(self, one_line=False, where=()):
        e = await self._where(where, SELECT_SQL)

        if one_line:
            return await e.fetchone()
        else:
            return await e.fetchall()

    async def delete(self, one_line=False, where=()):
        e = await self._where(where, DELETE_SQL)

        if one_line:
            return await e.fetchone()
        else:
            return await e.fetchall()

    async def update(self, where=(), **kwargs):
        return await self._where(where, UPDATE_SQL.format(
            vars=" AND ".join(all2string(kwargs)),
            name="{name}"
        ))

    async def insert(self, *args):
        return await self.execute(INSERT_INTO_SQL.format(
            name=self.name,
            values=", ".join(all2string(args, self.quote))
        ))

    async def execute(self, sql):
        logger.debug(sql)

        cur = await self.conn.cursor()
        return await cur.execute(sql)

    async def _where(self, where, sql):
        if where.__class__ == str:
            where = [where]

        if len(where) > 0:
            return await self.execute((sql + WHERE_SQL).format(
                name=self.name,
                where=" AND ".join(where)
            ))
        else:
            return await self.execute(sql.format(
                name=self.name
            ))


class SQLTable(SQLTableBase):
    def __init__(self, name=None, conn=None, quote='"'):
        self.name = name
        self.conn = conn
        self.quote = quote


def all2string(args, q='"'):
    if args.__class__ == list:
        return [str(_) if _.__class__ != str else f"{q}{_}{q}" for _ in args]
    else:
        return ["=".join([_, f"{q}{args[_]}{q}"]) if args[_].__class__ != str
                else "=".join([_, args[_]]) for _ in args]
