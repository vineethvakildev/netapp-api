from .serializers import DataSerializer


def validate_api(content):
    res = {"success": True, "errors": None, "details": None}
    validation = DataSerializer(data=content)
    if validation.is_valid():
        res["success"] = True
    else:
        res["success"] = False
        res["details"] = "Bad Request Body"
        res["errors"] = validation.errors
    return res