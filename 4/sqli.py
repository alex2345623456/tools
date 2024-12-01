import argparse
import requests
import time
import random
import json

# List of common User-Agent strings
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

def parse_request_file(file_path):
    """Parse the request file to extract URL, HTTP method, headers, and body."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    url = lines[0].strip()
    method = lines[1].split(':')[1].strip().upper()
    http_version = lines[2].split(':')[1].strip()

    headers = {}
    body = None

    for line in lines[3:]:
        if line.startswith("Request Headers:"):
            key, value = line.split("Request Headers:")[1].split(":", 1)
            headers[key.strip()] = value.strip()
        elif line.startswith("Request Body:"):
            body_content = line.split("Request Body:")[1].strip()
            if body_content == "(No body)":
                print("No request body specified. Exiting.")
                exit()
            body = body_content

    # Add random User-Agent to headers
    headers["User-Agent"] = random.choice(USER_AGENTS)

    return url, method, http_version, headers, body

def load_payloads(payload_file):
    """Load the payloads from the specified file."""
    with open(payload_file, 'r') as file:
        return [line.strip() for line in file.readlines()]

def generate_url_encoded_variations(body, payload):
    """Generate variations for URL-encoded body."""
    params = body.split("&")
    payloads = []
    for i, param in enumerate(params):
        key = param.split("=")[0]
        modified_params = params.copy()
        modified_params[i] = f"{key}={payload}"
        payloads.append("&".join(modified_params))
    return payloads

def generate_json_variations(json_obj, payload):
    """Generate variations for JSON body."""
    variations = []
    
    # Recursive function to modify the JSON body
    def recursive_replace(d, path=[]):
        if isinstance(d, dict):
            for k, v in d.items():
                new_path = path + [k]
                if isinstance(v, (dict, list)):
                    recursive_replace(v, new_path)
                else:
                    new_obj = dict(d)  # Copy the dict to avoid mutating it
                    new_obj[k] = payload
                    variations.append((new_path, new_obj))  # Save new variation
    
        elif isinstance(d, list):
            for idx, v in enumerate(d):
                new_path = path + [idx]
                if isinstance(v, (dict, list)):
                    recursive_replace(v, new_path)
                else:
                    new_obj = list(d)  # Copy the list
                    new_obj[idx] = payload
                    variations.append((new_path, new_obj))  # Save new variation
    
    recursive_replace(json_obj)
    return variations

def send_request(url, method, headers, body):
    """Send the HTTP request and return the response and elapsed time."""
    time.sleep(random.uniform(0, 1))  # Introduce random sleep

    start_time = time.time()
    response = None

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=body)
    elif method == "PUT":
        response = requests.put(url, headers=headers, data=body)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, data=body)
    elif method == "PATCH":
        response = requests.patch(url, headers=headers, data=body)
    elif method == "HEAD":
        response = requests.head(url, headers=headers)
    elif method == "OPTIONS":
        response = requests.options(url, headers=headers)
    elif method == "TRACE":
        response = requests.request("TRACE", url, headers=headers, data=body)
    else:
        raise ValueError(f"HTTP method {method} not supported.")

    elapsed_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds
    return response, elapsed_time

def main():
    parser = argparse.ArgumentParser(description="HTTP Request Script")
    parser.add_argument("-l", required=True, help="Path to request file")
    parser.add_argument("-p", required=True, help="Path to payload file")
    args = parser.parse_args()

    url, method, http_version, headers, body = parse_request_file(args.l)
    payloads = load_payloads(args.p)

    try:
        # Process each payload and generate variations
        for payload in payloads:
            if "=" in body:  # URL-encoded body
                payload_variations = generate_url_encoded_variations(body, payload)
            elif body.startswith("{") and body.endswith("}"):  # JSON body
                body_json = json.loads(body)
                payload_variations = generate_json_variations(body_json, payload)
            else:
                print("Unsupported body format. Exiting.")
                exit()

            # Send requests for each variation
            for variation in payload_variations:
                if isinstance(variation, tuple):  # JSON variation
                    new_body = json.dumps(variation[1])  # Get the new JSON body
                else:  # URL-encoded variation
                    new_body = variation

                response, elapsed_time = send_request(url, method, headers, new_body)
                print(url)
                print(f"Method: {method}")
                print(f"Request Body: {new_body}")
                print(f"Status code: {response.status_code}")
                print(f"Time: {elapsed_time}ms")
                if elapsed_time > 10000:
                    print(f"WARNING: Slow response (Payload: {payload})")
                print("--------------------------------------------------")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
