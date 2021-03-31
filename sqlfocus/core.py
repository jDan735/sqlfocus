import logging

from .helpers import all2string

WHERE_SQL = " WHERE {where}"
ORDER_SQL = " ORDER BY {order}"


logger = logging.getLogger("sqlfocus")


class SQLFocus:
    def execute(self, func):
        async def wrapper(table, *args, where=(),
                          order=None, **kwargs):
            query = "".join([
                await func(table, *args, **kwargs),
                self.where(where),
                f" ORDER BY {order}" if order is not None else ""
            ])

            logger.debug(f"sql query: {query}")
            return table, await table.conn.execute(query)

        return wrapper

    def fetch(self, one=False):
        def outer(func):
            async def wrapper(self, *args, **kwargs):
                _, e = await func(self, *args, **kwargs)
                return await e.fetchone() if one else await e.fetchall()

            return wrapper
        return outer

    def where(self, where=()):
        if isinstance(where, str):
            where = [where]

        return WHERE_SQL.format(
            where=" AND ".join(where)
        ) if len(where) > 0 else ""
