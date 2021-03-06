from flask import make_response, jsonify


def findIndexInList(array, condition):
    for i, item in enumerate(array):
        if condition(item):
            return i


def abort(status_code, body=None):
    return make_response(jsonify(body), status_code)


def checkparams(params, request):
    if not request.json:
        return "Error body json not found"
    for param in params:
        if param not in request.json:
            return "Error {} not found".format(param)
    return False


def format_levels(levels):
    format_levels = "*" if levels == -1 \
        else "*1..{levels}".format(levels=levels)
    return format_levels


def checkonlyone(params, request):
    if not request.json:
        return "Error body json not found", None
    total = []
    for param in params:
        if param in request.json:
            total.append(param)
    if len(total) > 1:
        return "Error, multiple params founds: {}. \
                You can use only one".format(",".join(total)), None
    if len(total) == 0:
        return "Error, params {} not founds".format(" or ".join(params)), None
    return False, total[0]


def findInArgs(default, args):
    arg = ""
    value = ""
    for key, value in args.items():
        if key == default:
            arg = default
            value = value
    if arg == "":
        return "Error, '{}' not found in args".format(default), None
    return False, [arg, value]


def docstring_parameter(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec
