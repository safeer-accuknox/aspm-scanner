from pydantic import BaseModel, ValidationError, Field, field_validator
import os
import logging
from typing import Optional


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_SCAN_TYPES = {"IAC", "SECRET"}

class Config(BaseModel):
    SCAN_TYPE: str
    ACCUKNOX_ENDPOINT: str
    ACCUKNOX_TENANT: int
    ACCUKNOX_LABEL: str
    ACCUKNOX_TOKEN: str
    INPUT_SOFT_FAIL: bool

    @field_validator("SCAN_TYPE")
    @classmethod
    def validate_scan_type(cls, v):
        if v not in ALLOWED_SCAN_TYPES:
            raise ValueError("Invalid SCAN_TYPE. Allowed values: IAC, SECRET.")
        return v

class IaCScannerConfig(BaseModel):
    REPO_URL: str
    REPO_BRANCH: str
    INPUT_FILE: str
    INPUT_DIRECTORY: str 
    INPUT_COMPACT: bool
    INPUT_QUIET: bool
    INPUT_FRAMEWORK: Optional[str]

class SecretScannerConfig(BaseModel):
    RESULTS: Optional[str]
    BRANCH: Optional[str]
    EXCLUDE_PATHS: Optional[str]
    ADDITIONAL_ARGUMENTS: Optional[str]

class ConfigValidator:
    def __init__(self, scan_type, accuknox_endpoint, accuknox_tenant, accuknox_label, accuknox_token, input_soft_fail):
        try:
            self.config = Config(
                SCAN_TYPE=scan_type,
                ACCUKNOX_ENDPOINT=accuknox_endpoint,
                ACCUKNOX_TENANT=accuknox_tenant,
                ACCUKNOX_LABEL=accuknox_label,
                ACCUKNOX_TOKEN=accuknox_token,
                INPUT_SOFT_FAIL=input_soft_fail
            )
        except ValidationError as e:
            for error in e.errors():
                logger.error(f"{error['loc'][0]}: {error['msg']}")
            exit(1)

    def validate_iac_scan(self, repo_url, repo_branch, input_file, input_directory, input_compact, input_quiet, input_framework):
        try:
            self.config = IaCScannerConfig(
                REPO_URL=repo_url,
                REPO_BRANCH=repo_branch,
                INPUT_FILE=input_file,
                INPUT_DIRECTORY=input_directory,
                INPUT_COMPACT=input_compact,
                INPUT_QUIET=input_quiet,
                INPUT_FRAMEWORK=input_framework
            )
        except ValidationError as e:
            for error in e.errors():
                logger.error(f"{error['loc'][0]}: {error['msg']}")
            exit(1)

    def validate_secret_scan(self, results, branch, exclude_paths, additional_arguments):
        try:
            self.config = SecretScannerConfig(
                RESULTS=results,
                BRANCH=branch,
                EXCLUDE_PATHS=exclude_paths,
                ADDITIONAL_ARGUMENTS=additional_arguments,
            )
        except ValidationError as e:
            for error in e.errors():
                logger.error(f"{error['loc'][0]}: {error['msg']}")
            exit(1)