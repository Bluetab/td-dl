from flask import jsonify


def findIndexInList(array, condition):
    for i, item in enumerate(array):
        if condition(item):
            return i


def make_error(status_code, message):
    response = jsonify({
        'status': status_code,
        'message': message,
    })
    response.status_code = status_code
    return response

def checkparams(params, request):
    if not request.json:
        return "Error body json not found"
    for param in params:
        if not param in request.json:
            return "Error {} not found".format(param)
    return False

def checkonlyone(params, request):
    if not request.json:
        return "Error body json not found", None
    total = []
    for param in params:
        if param in request.json:
            total.append(param)
    if len(total) > 1:
        return "Error, multiple params founds: {}. You can use only one".format(",".join(total)), None
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
