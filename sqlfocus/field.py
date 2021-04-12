class Field:
    WHERE_TEMPLATE = "{option}{operator}{value}"

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self._generate_sql(other, "=")

    def __gt__(self, other):
        return self._generate_sql(other, ">")

    def __lt__(self, other):
        return self._generate_sql(other, "<")

    def __ge__(self, other):
        return self._generate_sql(other, ">=")

    def __le__(self, other):
        return self._generate_sql(other, "<=")

    def _generate_sql(self, other, operator):
        return self.WHERE_TEMPLATE.format(
            option=self.name,
            operator=operator,
            value=self._prepare_value(other)
        )

    def _prepare_value(self, value):
        if isinstance(value, str):
            return self._fix_string(value)

        return value

    def _fix_string(self, string):
        return string.replace('"', '""') \
                     .replace("'", "''")
