CREATE_SQL = "CREATE TABLE {exists}{name} ({vars});"
SELECT_SQL = "SELECT * FROM {name}"
SELECT_WHERE_SQL = "SELECT * FROM {name} WHERE {where};"
INSERT_INTO_SQL = "INSERT INTO {name} VALUES ({values})"


class SQLTable:
    def __init__(self, name, conn=None):
        self.name = name
        self.conn = conn

    async def create(self, schema, exists=True):
        cur = await self.conn.cursor()
        colums = []

        for var in schema:
            colums.append(" ".join(var))

        await cur.execute(CREATE_SQL.format(
            name=self.name,
            exists="IF NOT EXISTS " if exists else "",
            vars=", ".join(colums)
        ))

    async def selectall(self, where=()):
        cur = await self.conn.cursor()

        if len(where) > 0:
            return await cur.execute(SELECT_WHERE_SQL.format(
                name=self.name,
                where=" AND ".join(where)
            ))
        else:
            return await cur.execute(SELECT_SQL.format(
                name=self.name
            ))

    async def insert(self, *args):
        cur = await self.conn.cursor()

        return await cur.execute(INSERT_INTO_SQL.format(
            name=self.name,
            values=", ".join(all2string(args))
        ))


def all2string(args):
    params = []

    for arg in args:
        if arg.__class__ != str:
            arg = str(arg)
        else:
            arg = f'"{arg}"'

        params.append(arg)

    return params
