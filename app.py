from flask import Flask, request, jsonify, send_file # type: ignore
from urllib3.poolmanager import PoolManager # type: ignore
from requests.adapters import HTTPAdapter # type: ignore
from urllib.parse import urljoin # type: ignore
from bs4 import BeautifulSoup # type: ignore
from flask_cors import CORS # type: ignore
import requests # type: ignore
import ssl # type: ignore
import os # type: ignore

app = Flask(__name__)
CORS(app)

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers('ALL')
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SSLAdapter())

def load_payloads(filepath = "payloads.txt"):
    """Load SQL injection payloads from a file."""
    with open(filepath, "r") as file:
        payloads = [line.strip() for line in file if line.strip()]
    return payloads

def get_forms(url):
    soup = BeautifulSoup(session.get(url).content, "html.parser")
    return soup.find_all("form")

def form_details(form):
    detailsOfForm = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get")
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({
            "type": input_type,
            "name": input_name,
            "value": input_value,
        })

    detailsOfForm['action'] = action
    detailsOfForm['method'] = method
    detailsOfForm['inputs'] = inputs
    return detailsOfForm

def vulnerable(response, payload):
    errors = {
        "quoted string not properly terminated",
        "unclosed quotation mark after the character string",
        "you have an error in your SQL syntax",
        "mysql_fetch_array()",
        "sql syntax",
        "syntax error",
        "warning: mysql",
        "sql error",
        "you have an error in your sql syntax",
        "invalid query",
    }

    for error in errors:
        if error in response.content.decode().lower():
            return True

    if response.status_code == 500:
        return True

    if "admin" in response.text.lower():
        return True

    if "Welcome, admin" in response.text:
        return True

    if payload in response.text:
        return True

    return False

def sql_injection_scan(url):
    forms = get_forms(url)
    result = []
    payloads = load_payloads()

    for form in forms:
        details = form_details(form)

        for payload in payloads:
            data = {}
            for input_tag in details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    data[input_tag['name']] = input_tag["value"] + payload
                elif input_tag["type"] != "submit":
                    data[input_tag["name"]] = f"test{payload}"

            action_url = urljoin(url, details["action"])

            if details["method"].lower() == "post":
                res = session.post(action_url, data = data)
            elif details["method"].lower() == "get":
                res = session.get(action_url, params = data)

            if vulnerable(res, payload):
                result.append({
                    "url": action_url,
                    "payload": payload,
                    "vulnerability": "SQL Injection Detected",
                    "description": f"SQL Injection vulnerability detected using the payload\n'{payload}'.\nThis attack can manipulate the SQL query to bypass authentication or access sensitive data.\n\n"
                })
            else:
                result.append({
                    "url": action_url,
                    "payload": payload,
                    "vulnerability": "No Vulnerability Detected",
                    "description": "No SQL injection vulnerability detected with this payload.\nThe system appears to be protected against this attack vector."
                })
    
    return result

def generate_report(results):
    report_filename = "sql_injection_report.html"
    with open(report_filename, "w") as f:
        f.write("<html><body>")
        f.write("<h1>SQL Injection Vulnerability Report</h1>")
        f.write("<ul>")
        for result in results:
            f.write(f"<li>{result['url']}: {result['vulnerability']} - {result['description']}</li>")
        f.write("</ul>")
        f.write("</body></html>")
    return report_filename

@app.route('/', methods = ['POST'])
def scan_url():
    url = request.get_json().get('url')
    if not url:
        return jsonify({"message": "URL is required"}), 400

    results = sql_injection_scan(url)

    return jsonify({"results": results})

@app.route('/download_report')
def download_report():
    return send_file("sql_injection_report.html", as_attachment = True)

if __name__ == '__main__':
    app.run(debug = True)