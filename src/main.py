import os
import requests
import logging
from scan import IaCScanner, SecretScanner, CxScanner
from utils import ConfigValidator, upload_results, handle_failure

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_env_vars():
    """Removes surrounding single or double quotes from all environment variables."""
    for key, value in os.environ.items():
        if value and ((value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"'))):
            os.environ[key] = value[1:-1]
clean_env_vars()

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
        input_compact = os.environ.get('INPUT_COMPACT', 'True').lower() == 'true'
        input_quiet = os.environ.get('INPUT_QUIET', 'True').lower() == 'true'
        input_framework = os.environ.get('INPUT_FRAMEWORK', None)
        repo_url = os.environ.get('REPOSITORY_URL', None)
        repo_branch = os.environ.get('REPOSITORY_BRANCH', None)
        ConfigValidatorObj.validate_iac_scan(repo_url, repo_branch, input_file, input_directory, input_compact, input_quiet, input_framework)
        IaCScannerObj = IaCScanner(repo_url, repo_branch, input_file, input_directory, input_compact, input_quiet, input_framework)
        exit_code, result_file = IaCScannerObj.run()
        if(result_file):
            upload_results(result_file, accuknox_endpoint, accuknox_tenant, accuknox_label, accuknox_token, "IAC")
        handle_failure(exit_code, input_soft_fail)
    elif(scan_type == "SECRET"):
        results = os.environ.get('RESULTS', None)
        branch = os.environ.get('BRANCH', None)
        exclude_paths = os.environ.get('EXCLUDE_PATHS', None)
        additional_arguments = os.environ.get('ADDITIONAL_ARGUMENTS', None)
        ConfigValidatorObj.validate_secret_scan(results, branch, exclude_paths, additional_arguments)
        SecretScannerObj = SecretScanner(results, branch, exclude_paths, additional_arguments)
        exit_code, result_file = SecretScannerObj.run()
        if(result_file):
            upload_results(result_file, accuknox_endpoint, accuknox_tenant, accuknox_label, accuknox_token, "TruffleHog")
        handle_failure(exit_code, input_soft_fail)
    elif(scan_type == "CX"):
        project_name = os.environ.get('CX_PROJECT_NAME', None)
        branch = os.environ.get('CX_BRANCH', None)
        client_id = os.environ.get('CX_CLIENT_ID', None)
        client_secret = os.environ.get('CX_CLIENT_SECRET', None)
        base_uri = os.environ.get('CX_BASE_URI', None)
        tenant = os.environ.get('CX_TENANT', None)
        source_dir = os.environ.get('INPUT_DIRECTORY', './')

        repo_url = os.environ.get('REPOSITORY_URL', None)
        repo_branch = os.environ.get('REPOSITORY_BRANCH', None)
        repo_commit_sha = os.environ.get('REPOSITORY_COMMIT_SHA', None)
        repo_commit_ref = os.environ.get('REPOSITORY_COMMIT_REF', None)
        repo_name = os.environ.get('REPOSITORY_NAME', None)

        ConfigValidatorObj.validate_cx_scan(project_name, branch, client_id, client_secret, base_uri, tenant, source_dir, repo_url, repo_branch, repo_commit_sha, repo_commit_ref)
        CxScannerObj = CxScanner(project_name, branch, client_id, client_secret, base_uri, tenant, source_dir, repo_url, repo_branch, repo_commit_sha, repo_commit_ref, repo_name)
        exit_code, result_file = CxScannerObj.run()
        if(result_file):
            upload_results(result_file, accuknox_endpoint, accuknox_tenant, accuknox_label, accuknox_token, "CX")
        handle_failure(exit_code, input_soft_fail)
    else:
        pass

if __name__ == '__main__':
    run_scan()