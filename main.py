import os
import requests
import logging
from scan import IaCScanner
from utils import ConfigValidator, upload_results

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


scan_type = os.environ.get('SCAN_TYPE', None)
accuknox_endpoint = os.environ.get('ACCUKNOX_ENDPOINT', None)
accuknox_tenant = os.environ.get('ACCUKNOX_TENANT', None)
accuknox_label = os.environ.get('ACCUKNOX_LABEL', None)
accuknox_token = os.environ.get('ACCUKNOX_TOKEN', None)
input_soft_fail = os.environ.get('INPUT_SOFT_FAIL', 'False').lower() == 'true'
            

def run_scan():
    logger.info('Starting Scan...')
    ConfigValidatorObj = ConfigValidator(scan_type, accuknox_endpoint, accuknox_tenant, accuknox_label, accuknox_token, input_soft_fail)

    if(scan_type == "IAC"):
        input_file = os.environ.get('INPUT_FILE', '')
        input_directory = os.environ.get('INPUT_DIRECTORY', './')
        input_compact = os.environ.get('INPUT_COMPACT', 'False').lower() == 'true'
        input_quiet = os.environ.get('INPUT_QUIET', 'False').lower() == 'true'
        input_framework = os.environ.get('INPUT_FRAMEWORK', None)
        repo_url = os.environ.get('REPO_URL', None)
        repo_branch = os.environ.get('REPO_BRANCH', None)
        ConfigValidatorObj.validate_iac_scan(repo_url, repo_branch, input_file, input_directory, input_compact, input_quiet, input_framework)
        IaCScannerObj = IaCScanner(repo_url, repo_branch, input_file, input_directory, input_compact, input_quiet, input_framework)
        exit_code, result_file = IaCScannerObj.run()
        upload_results(result_file, accuknox_endpoint, accuknox_tenant, accuknox_label, accuknox_token, "IAC")

if __name__ == '__main__':
    run_scan()