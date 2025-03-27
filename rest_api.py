import _snowflake
import logging
import json
import requests
import base64

SECRET_NAMES = ['aqs_url', 'aqs_sas_token']

def main(job_name: str):
    logging.info(f"Triggered procedure for {job_name}")
    
    secrets_data = {secret_name: _snowflake.get_generic_secret_string(secret_name) for secret_name in SECRET_NAMES}
    logging.info("Fetched secrets")
    
    url = f"{secrets_data['aqs_url']}/messages?{secrets_data['aqs_sas_token']}"

    data = {
        "group": "EDW",
        "project": "EDW",
        "version": "default",
        "environment": "Test",
        "job": job_name,
        "variables": {}
    }

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/xml'}
    

    encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    payload = f'<QueueMessage><MessageText>{encoded_data}</MessageText></QueueMessage>'

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        logging.info(f"Response: {response.text}")
        return 1
    except requests.RequestException as e:
        logging.error(f"Error when sending POST request to {url}: {e}")
        return 0