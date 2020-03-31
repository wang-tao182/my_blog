from django.http import JsonResponse


class HttpCode(object):
    # 一切正常
    ok = 200
    # 参数错误,比如账号密码
    paramserror = 400
    # 没有授权
    unauth = 401
    # 请求方法错误
    methoderror = 405
    # 服务器内部错误
    servererror = 500


def result(code=HttpCode.ok, message="", data={},kwargs=None):
        json_dict = {"code": code, "message": message, "data": data}
        if kwargs and isinstance(kwargs, dict) and kwargs.keys():
            json_dict.update(kwargs)
        return JsonResponse(json_dict)


def params_error(message="", data={}):
    return result(code=HttpCode.paramserror, message=message, data=data)


def unauth(message="", data={},):
    return result(code=HttpCode.unauth, message=message, data=data)


def method_error(message="", data={},):
    return result(code=HttpCode.methoderror, message=message, data=data)


def server_error(message="", data={}):
    return result(code=HttpCode.servererror, message=message, data=data)


def ok():
    return result()