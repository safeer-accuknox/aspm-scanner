import requests

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_results(result_file, endpoint, tenant_id, label, token, data_type):
    """Upload the result JSON to the specified endpoint."""
    logger.info("Uploading results...")
    try:
        with open(result_file, 'rb') as file:
            response = requests.post(
                f"https://{endpoint}/api/v1/artifact/",
                headers={
                    "Tenant-Id": tenant_id,
                    "Authorization": f"Bearer {token}"
                },
                params={
                    "tenant_id": tenant_id,
                    "data_type": data_type,
                    "label_id": label,
                    "save_to_s3": "true"
                },
                files={"file": file}
            )
        response.raise_for_status()
        logger.info(f"Upload successful. Response: {response.status_code}")
    except Exception as e:
        logger.error(f"Error uploading results: {e}")
        raise