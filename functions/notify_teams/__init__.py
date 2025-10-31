# functions/notify_teams/__init__.py
import os, json, requests, azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        hook = os.environ["TEAMS_WEBHOOK"]
        data = req.get_json()
        text = data.get("message","Solar wind alert")
        r = requests.post(hook, json={"text": text})
        return func.HttpResponse(r.text, status_code=r.status_code, mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
