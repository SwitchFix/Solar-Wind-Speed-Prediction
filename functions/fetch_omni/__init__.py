# functions/fetch_omni/__init__.py
import json
import azure.functions as func
from ..shared.hv_omni import get_omni_window

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        hours = int(req.params.get("hours", "24"))
        df = get_omni_window(hours=hours)
        return func.HttpResponse(df.to_json(orient="records"), status_code=200, mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
