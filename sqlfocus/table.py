import logging

CREATE_SQL = "CREATE TABLE {exists}{name} ({vars});"
SELECT_SQL = "SELECT * FROM {name}"
SELECT_WHERE_SQL = "SELECT * FROM {name} WHERE ({where});"
DELETE_SQL = "DELETE FROM {name}"
DELETE_WHERE_SQL = "DELETE FROM {name} WHERE ({where});"
INSERT_INTO_SQL = "INSERT INTO {name} VALUES ({values});"

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
        e = await self._where(where, SELECT_WHERE_SQL, SELECT_SQL)

        if one_line:
            return await e.fetchone()
        else:
            return await e.fetchall()

    async def delete(self, one_line=False, where=()):
        e = await self._where(where, DELETE_WHERE_SQL, DELETE_SQL)

        if one_line:
            return await e.fetchone()
        else:
            return await e.fetchall()

    async def insert(self, *args):
        return await self.execute(INSERT_INTO_SQL.format(
            name=self.name,
            values=", ".join(all2string(args, self.quote))
        ))

    async def execute(self, sql):
        logger.debug(sql)

        cur = await self.conn.cursor()
        return await cur.execute(sql)

    async def _where(self, where, sql, sql2):
        if where.__class__ == str:
            where = [where]

        if len(where) > 0:
            return await self.execute(sql.format(
                name=self.name,
                where=" AND ".join(where)
            ))
        else:
            return await self.execute(sql2.format(
                name=self.name
            ))


class SQLTable(SQLTableBase):
    def __init__(self, name=None, conn=None, quote='"'):
        self.name = name
        self.conn = conn
        self.quote = quote


def all2string(args, quote='"'):
    params = []

    for arg in args:
        if arg.__class__ != str:
            arg = str(arg)
        else:
            arg = f"{quote}{arg}{quote}"

        params.append(arg)

    return params
