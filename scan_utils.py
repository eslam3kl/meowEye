from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import json
import requests
from requests.exceptions import ConnectionError
from http.client import RemoteDisconnected
from config import color_tag

def format_as_burp_request(method, url, headers, body):
    parsed = urlparse(url)
    path = parsed.path or "/"
    if parsed.query:
        path += f"?{parsed.query}"
    req = f"{method} {path} HTTP/1.1\n"
    req += f"Host: {parsed.netloc}\n"
    for key, value in headers.items():
        if key.lower() != 'host':
            req += f"{key}: {value}\n"
    req += "\n"
    if body:
        req += body
    return req

def check_response_content(content, attack_choice, payloads):
    if attack_choice == 'lfiLinux':
        return "root:x:" in content
    elif attack_choice == 'lfiWin':
        return "for 16-bit app support" in content
    elif attack_choice == 'ref':
        return any(payload in content for payload in payloads)
    elif attack_choice == 'ssti':
        return "1728394" in content
    return False

def analyze_request(request, attack_choice, payloads, proxies, output_file):
    try:
        headers = dict(request.headers)
        headers.pop('Content-Length', None)
        headers.pop('Host', None)

        if request.method == 'GET':
            parsed_url = urlparse(request.url)
            query_params = parse_qs(parsed_url.query)
            for key in query_params:
                original_value = query_params[key][0]
                for payload in payloads:
                    modified_value = original_value + payload
                    temp_params = query_params.copy()
                    temp_params[key] = modified_value
                    new_query = urlencode(temp_params, doseq=True)
                    new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', new_query, ''))
                    try:
                        res = requests.get(new_url, headers=headers, verify=False, timeout=8, proxies=proxies)
                        if check_response_content(res.text, attack_choice, payloads):
                            burp_req = format_as_burp_request("GET", new_url, headers, None)
                            output_file.write(burp_req + "\n\n")
                            print(f"{color_tag('[Finding]')} Vulnerable parameter: {key} with payload: {payload}")
                    except (ConnectionError, RemoteDisconnected, Exception):
                        pass

        elif request.method == 'POST':
            content_type = request.headers.get('Content-Type', '')
            body = request.body.decode('utf-8', errors='ignore') if request.body else ''

            if 'application/json' in content_type:
                try:
                    json_data = json.loads(body)
                    for key in json_data:
                        original_value = str(json_data[key])
                        for payload in payloads:
                            json_data[key] = original_value + payload
                            try:
                                res = requests.post(request.url, headers=headers, json=json_data, verify=False, timeout=8, proxies=proxies)
                                if check_response_content(res.text, attack_choice, payloads):
                                    burp_req = format_as_burp_request("POST", request.url, headers, json.dumps(json_data))
                                    output_file.write(burp_req + "\n\n")
                                    print(f"{color_tag('[Finding]')} Vulnerable parameter: {key} with payload: {payload}")
                            except (ConnectionError, RemoteDisconnected, Exception):
                                pass
                            json_data[key] = original_value
                except json.JSONDecodeError:
                    pass
            elif 'application/x-www-form-urlencoded' in content_type:
                data = dict(pair.split('=') if '=' in pair else (pair, '') for pair in body.split('&'))
                for key in data:
                    original_value = data[key]
                    for payload in payloads:
                        data[key] = original_value + payload
                        try:
                            res = requests.post(request.url, headers=headers, data=data, verify=False, timeout=8, proxies=proxies)
                            if check_response_content(res.text, attack_choice, payloads):
                                burp_req = format_as_burp_request("POST", request.url, headers, urlencode(data))
                                output_file.write(burp_req + "\n\n")
                                print(f"{color_tag('[Finding]')} Vulnerable parameter: {key} with payload: {payload}")
                        except (ConnectionError, RemoteDisconnected, Exception):
                            pass
                        data[key] = original_value
    except Exception:
        pass
