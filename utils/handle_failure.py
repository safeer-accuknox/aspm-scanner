import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_failure(exit_code, soft_fail):
    """Handle pipeline success or failure based on soft fail flag."""
    if exit_code != 0:
        if soft_fail:
            logger.warning("Scan failed, but soft fail is enabled. Continuing...")
        else:
            logger.error("Scan failed and soft fail is disabled. Exiting with failure.")
            self.fail(message="Scan failed!")
    else:
        logger.info("Scan completed successfully.")