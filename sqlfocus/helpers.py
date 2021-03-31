def sstr(text):
    return text.replace("\\", "\\\\")\
               .replace('"', '\\"')\
               .replace("'", '\\"')


def all2string(args, q="'"):
    if args.__class__ == list or args.__class__ == tuple:
        return [str(_) if _.__class__ != str else f"{q}{_}{q}" for _ in args]
    else:
        return [f"{_}={args[_]}" if args[_].__class__ != str
                else f"{_}={q}{args[_]}{q}" for _ in args]
