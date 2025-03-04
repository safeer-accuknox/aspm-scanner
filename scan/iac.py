import subprocess
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IaCScanner:
    output_format = 'json'
    output_file_path = './results'
    result_file = f'{output_file_path}/results_json.json'

    def __init__(self, repo_url=None, repo_branch=None, input_file=None, input_directory='./', compact=False, quiet=False, framework=None):
        self.input_file = input_file
        self.input_directory = input_directory
        self.compact = compact
        self.quiet = quiet
        self.framework = framework
        self.repo_url = repo_url
        self.repo_branch = repo_branch

    def run(self):
        """Run the IaC scan using Checkov."""
        checkov_cmd = ["checkov"]

        if self.input_file:
            checkov_cmd.extend(["-f", self.input_file])
        if self.input_directory:
            checkov_cmd.extend(["-d", self.input_directory])
        if self.compact:
            checkov_cmd.append("--compact")
        if self.quiet:
            checkov_cmd.append("--quiet")
        checkov_cmd.extend(["-o", self.output_format, "--output-file-path", self.output_file_path])
        if self.framework:
            checkov_cmd.extend(["--framework", self.framework])

        logger.info(f"Executing command: {' '.join(checkov_cmd)}")
        result = subprocess.run(checkov_cmd, capture_output=True, text=True)

        logger.info(result.stdout)
        logger.error(result.stderr)

        self.process_result_file()
        return result.returncode, self.result_file

    def process_result_file(self):
        """Process the result JSON file to ensure it is an array and append additional metadata."""
        try:
            with open(self.result_file, 'r') as file:
                data = json.load(file)

            if isinstance(data, dict):
                data = [data]

            repo_link = os.getenv('REPO_URL', 'unknown_repo')
            branch = os.getenv('REPO_BRANCH', 'unknown_branch')
            data.append({
                "details": {
                    "repo":   self.repo_url,
                    "branch":  self.repo_branch
                }
            })

            with open(self.result_file, 'w') as file:
                json.dump(data, file, indent=2)

            logger.info("Result file processed successfully.")
        except Exception as e:
            logger.error(f"Error processing result file: {e}")
            raise