import sys


def args_parser():
    args = sys.argv[1:]

    result = {}
    for arg in args:
        comps = arg.split("=")
        if not (len(comps) == 2):
            comps = [arg, True]

        key, value = comps
        key = key.replace("-", "")

        result[key] = value

    return result
