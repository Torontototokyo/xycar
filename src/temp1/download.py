
"""Simple HTTP request simulator.

Provides a small helper to perform HTTP requests for testing or download
purposes. Uses the `requests` library if available, otherwise falls back to
urllib.
"""
from typing import Optional, Dict, Any
from http.cookiejar import CookieJar

import requests
def simulate_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, data: Optional[Any] = None, timeout: int = 10,cookies:CookieJar = None) -> dict:
	"""Perform an HTTP request and return a dictionary with status, headers and content.

	Args:
		url: Request URL.
		method: HTTP method, e.g. 'GET' or 'POST'.
		headers: Optional request headers.
		data: Optional request body for POST/PUT.
		timeout: Timeout in seconds.

	Returns:
		dict with keys: status_code (int), headers (dict), content (bytes), text (str).
	"""
	try:
		

		resp = requests.request(method, url, headers=headers, data=data, timeout=timeout,cookies=cookies)
		return {
			"status_code": resp.status_code,
			"headers": dict(resp.headers),
			"content": resp.content,
			"text": resp.text,
		}
	except Exception:
		# Fallback to urllib
		from urllib import request as _request
		from urllib.error import HTTPError, URLError

		req = _request.Request(url, data=data if isinstance(data, (bytes, type(None))) else str(data).encode(), headers=(headers or {}), method=method)
		try:
			with _request.urlopen(req, timeout=timeout) as resp:
				content = resp.read()
				return {
					"status_code": getattr(resp, 'status', 200),
					"headers": dict(resp.getheaders()),
					"content": content,
					"text": content.decode(errors='replace'),
				}
		except HTTPError as e:
			body = e.read() if hasattr(e, 'read') else b''
			return {"status_code": e.code, "headers": dict(e.headers or {}), "content": body, "text": body.decode(errors='replace')}
		except URLError as e:
			return {"status_code": 0, "headers": {}, "content": b"", "text": str(e)}



# Example usage
# import sys

# if len(sys.argv) < 2:
# 	print("Usage: python download.py <url>")
# 	sys.exit(1)
data = {
    "carNo": "湘-K71068",
    "orgPath": "",
    "startTime": "2026-07-15 00:00:00",
    "endTime": "2026-07-15 23:59:59",
    "subsystemCodeList": [
        "p210839100",
        "p240167951",
        "p210839104",
        "p240167745"
    ],
    "personName": "",
    "tcType": "",
    "timeType": 2,
    "inPassageId": "",
    "outPassageId": "",
    "parkId": "",
    "tcName": "",
    "vehicleType": 0,
    "identityList": [],
    "inDealWayList": [],
    "inOperateSourceList": [],
    "dealWayList": [],
    "operateSourceList": [],
    "passWayList": [],
    "parkStartTime": "",
    "parkEndTime": "",
    "sidx": "",
    "sord": "desc",
    "pageIndex": 1,
    "pageSize": 10
}
headers = {
    "Jstoken":"JSaeb5ced3172d4b3cae544ee61c9f0072",
    "jscuraccno":"xy13420789366",
    "Host":"jzgk.jslife.com.cn",
    "Env":"g",
    "customerid":"22006",
	"Orgcode":"O88923512709",
	"Origin":"https://jzgk.jslife.com.cn",
	"Personid":"640016",
	"Personname":"%E9%BB%8E%E5%BB%BA%E6%B6%9B",
	"Source":"jzgk"
}

jar = CookieJar()
#env=g; UC_ID=3A2ADA4200994C9EB3A754512E4FD8E4
cookie_obj = {"env":"g","UC_ID":"3A2ADA4200994C9EB3A754512E4FD8E4"}

url = "https://jzgk.jslife.com.cn/jpark-center-mgr/api/excel/parkOut/exportExcel?env=g"
url = "https://jzgk.jslife.com.cn/jpark-center-mgr/api/statistical/vehicleTrafficMgt/getParkOutList?env=g"
result = simulate_request(url=url,method="POST",headers=headers,data= data,cookies=cookie_obj)
print(f"Status: {result['status_code']}")
print("Headers:")
for k, v in result['headers'].items():
    print(f"{k}: {v}")
print()
print(result['text'][:1000])
