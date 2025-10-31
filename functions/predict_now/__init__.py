# functions/predict_now/__init__.py
import os, json, base64, requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        aml_url = os.environ["AML_ENDPOINT"]
        aml_key = os.environ["AML_KEY"]
        body = req.get_json()
        # Pass-through to AML endpoint /score
        r = requests.post(aml_url, headers={"Authorization": f"Bearer {aml_key}","Content-Type":"application/json"}, json=body)
        return func.HttpResponse(r.text, status_code=r.status_code, mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
