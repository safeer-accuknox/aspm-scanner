import subprocess
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

RESULT_FILE = "results.json"

class SecretScanner:
    def __init__(self, results=None, branch=None, exclude_paths=None, additional_args=None):
        self.results = results
        self.branch = branch
        self.exclude_paths = exclude_paths
        self.additional_args = additional_args

    def run(self):
        """Run the secret scan and return the exit code and result file (if applicable)."""
        logger.info("Starting Secret Scan...")
        
        exit_code = self.run_secret_scan()

        if os.path.exists(RESULT_FILE) and os.stat(RESULT_FILE).st_size > 0:
            return exit_code, RESULT_FILE
        else:
            logger.info("No secrets found. Skipping API upload.")
            return exit_code, None

    def run_secret_scan(self):
        """Execute TruffleHog for secret scanning."""
        trufflehog_cmd = [
            "trufflehog", 
            "git", f"file://{os.getcwd()}",
            "--json", "--no-update", "--fail"
        ]

        if self.results:
            trufflehog_cmd.extend(["--results", self.results])
        if self.exclude_paths:
            trufflehog_cmd.extend(["-x", self.exclude_paths])

        branch_flag = self.get_branch_flag()
        if branch_flag:
            trufflehog_cmd.append(branch_flag)

        if self.additional_args:
            trufflehog_cmd.append(self.additional_args)

        logger.info(f"Executing command: {' '.join(trufflehog_cmd)}")
        result = subprocess.run(trufflehog_cmd, capture_output=True, text=True)

        logger.info(result.stdout)
        logger.error(result.stderr)
        logger.info(f"Exit code: {result.returncode}")

        with open(RESULT_FILE, "w") as f:
            f.write(result.stdout)

        return result.returncode

    def get_branch_flag(self):
        """Determine the correct branch flag for TruffleHog."""
        if self.branch == "all-branches":
            return ""
        elif self.branch:
            return f"--branch={self.branch}"
        elif os.getenv("REPOSITORY_COMMIT_SHA"):
            return f"--branch={os.getenv('REPOSITORY_COMMIT_SHA')}"
        return ""