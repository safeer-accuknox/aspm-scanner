import subprocess
import os
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CxScanner:
    def __init__(self, project_name, branch, client_id, client_secret, base_uri, tenant, source_dir, repo_url, repo_branch, repo_commit_sha, repo_commit_ref, repo_name):
        self.project_name = project_name
        self.branch = branch
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_uri = base_uri
        self.tenant = tenant
        self.source_dir = source_dir
        self.repo_url = repo_url
        self.repo_branch = repo_branch
        self.repo_commit_sha = repo_commit_sha
        self.repo_commit_ref = repo_commit_ref
        self.repo_name = repo_name
        self.output_format = "sarif"
        self.output_path = "."
        self.result_file = "cx_result.sarif"
        self.return_file = "cx_result_with_snippets.sarif"

    def run(self):
        """Run the Checkmarx scan."""        
        cx_cmd = [
            "cx", "scan", "create",
            "--project-name", self.project_name,
            "--branch", self.branch,
            "--client-id", self.client_id,
            "--client-secret", self.client_secret,
            "--base-uri", self.base_uri,
            "--tenant", self.tenant,
            "-s", self.source_dir,
            "--report-format", self.output_format,
            "--output-path", self.output_path
        ]

        logger.info(f"Executing command: {' '.join(cx_cmd)}")
        # result = subprocess.run(cx_cmd, capture_output=True, text=True)

        try:
            self.process_sarif_file()
            logger.info("Result file processed successfully.")
        except Exception as e:
            logger.error(f"Error processing result file: {e}")
            raise

        # return result.returncode, self.return_file
        return 0, self.return_file

    def get_code_snippet(self, lines, start_line, start_column, end_column):
        print("get_code_snippetget_code_snippet")

        """Extracts a code snippet from a given file with highlighting."""
        start_line_index = max(start_line - 3, 0)  # Include 2 lines before
        end_line_index = min(start_line + 2, len(lines))  # Include 2 lines after
        snippet_lines = lines[start_line_index:end_line_index]

        highlighted_snippet = []
        for i, line in enumerate(snippet_lines):
            line_number = start_line_index + i + 1
            if line_number == start_line:
                try:
                    highlighted_snippet.append(
                        line[:max(0, start_column - 1)] + "<<<HIGHLIGHT>>>" +
                        line[max(0, start_column - 1):min(len(line), end_column)] + "<<<END_HIGHLIGHT>>>" +
                        line[min(len(line), end_column):]
                    )
                except Exception as e:
                    logger.error(f"Error highlighting line {line_number}: {e}")
                    highlighted_snippet.append(line)
            else:
                highlighted_snippet.append(line)

        return "// Start of snippet\n" + "".join(highlighted_snippet) + "// End of snippet\n"

    def process_sarif_file(self):
        """Reads a SARIF file, extracts code snippets, and embeds them in the SARIF results."""
        source_dir = self.source_dir
        sarif_path = self.result_file

        # Load SARIF data
        with open(sarif_path, "r") as sarif_file:
            sarif_data = json.load(sarif_file)

        for run in sarif_data.get("runs", []):
            for result in run.get("results", []):
                for location in result.get("locations", []):
                    physical_location = location.get("physicalLocation", {})
                    artifact_location = physical_location.get("artifactLocation", {})
                    region = physical_location.get("region", {})

                    uri = artifact_location.get("uri")
                    start_line = region.get("startLine")
                    start_column = region.get("startColumn", 1)  # Default to column 1 if missing
                    end_column = region.get("endColumn", start_column + 10)  # Default range

                    if uri and start_line:
                        file_path = os.path.join(source_dir, uri.lstrip("./"))

                        if not os.path.exists(file_path):
                            logger.warning(f"File not found: {file_path}")
                            continue

                        try:
                            with open(file_path, "r") as source_file:
                                lines = source_file.readlines()
                                region["snippet"] = {"text": self.get_code_snippet(lines, start_line, start_column, end_column)}
                        except Exception as e:
                            logger.error(f"Error processing {file_path}: {e}")

        self.append_github_metadata(sarif_data)
        output_file_path = sarif_path.replace(".sarif", "_with_snippets.sarif")
        with open(output_file_path, "w") as output_file:
            json.dump(sarif_data, output_file, indent=2)

    def append_github_metadata(self, sarif_data):
        metadata = {
            "executionSuccessful": True,
            "toolExecutionNotifications": [],
            "toolConfigurationNotifications": [],
            "properties": {
                "repository": self.repo_name,
                "commit": self.repo_commit_sha,
                "ref": self.repo_commit_ref,
                "workflow_run_id": "",
                "workflow_run_number": "",
                "repository_url": self.repo_url,
                "workflow_run_url": "",
                "source": "GitHub"
            }
        }

        if "runs" in sarif_data and sarif_data["runs"]:
            sarif_data["runs"][0].setdefault("invocations", []).append(metadata)
        else:
            logger.warning("SARIF file does not contain valid runs.")

        logger.info("Git metadata appended to SARIF file.")
