# functions/fetch_euv/__init__.py
import json
import azure.functions as func
from ..shared.hv_omni import get_euv_sequence

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        hours = int(req.params.get("hours", "12"))
        seq = get_euv_sequence(hours=hours)
        return func.HttpResponse(json.dumps({"frames": seq}), status_code=200, mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
