This is designed to analyze Infrastructure as Code (IaC) and detect secrets within code repositories. It integrates with AccuKnox's CSPM platform to provide security insights.

## Prerequisites
- Docker installed on the system.
- An AccuKnox account with valid API credentials.
- A `.env` file containing the required environment variables.

## Running the Scan
To initiate a scan, use the following command:

```sh
docker run --rm -ti --env-file .env --entrypoint bash -v $PWD:/src accuknoxaspmscan
```

### Required Environment Variables
The following environment variables must be set in the `.env` file:

```sh
ACCUKNOX_TENANT=1
ACCUKNOX_LABEL=POC
ACCUKNOX_ENDPOINT=cspm.demo.accuknox.com
ACCUKNOX_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9
SCAN_TYPE=IAC
```

| **Input**               | **Description**                                                                 | **Default Value**         |
|--------------------------|---------------------------------------------------------------------------------|---------------------------|
| **INPUT_SOFT_FAIL**      | Do not return an error code if there are failed checks                          | `false` (boolean)          |
| **ACCUKNOX_TENANT**      | The ID of the tenant associated with the CSPM panel                             | N/A (Required)            |
| **ACCUKNOX_ENDPOINT**    | The URL of the CSPM panel to push the scan results to                           | N/A (Required)            |
| **ACCUKNOX_LABEL**       | The label created in AccuKnox SaaS for associating scan results                 | N/A (Required)            |
| **ACCUKNOX_TOKEN**       | The token for authenticating with the CSPM panel                                | N/A (Required)            |
| **SCAN_TYPE**            | This determines the type of scan to be performed, Valid values: IAC, SECRET     | N/A (Required)            |

### Infrastructure as Code (IaC) scanning

The Infrastructure as Code (IaC) scanning is designed to integrate with AccuKnox for scanning infrastructure code files (e.g., Terraform) for security vulnerabilities.

The following optional environment variables can be set:

| **Input**               | **Description**                                                                 | **Default Value**         |
|--------------------------|---------------------------------------------------------------------------------|---------------------------|
| **INPUT_FILE**           | Specify a file for scanning (e.g., ".tf" for Terraform). Cannot be used with directory input. | `""` (empty, optional)    |
| **INPUT_DIRECTORY**      | Directory with infrastructure code and/or package manager files to scan         | `"."` (current directory) |
| **INPUT_COMPACT**        | Do not display code blocks in the output                                        | `true` (boolean)          |
| **INPUT_QUIET**          | Display only failed checks                                                      | `true` (boolean)          |
| **INPUT_FRAMEWORK**      | Run only on a specific infrastructure (e.g., Kubernetes or Terraform)           | `""` (empty, optional)    |

```sh
INPUT_DIRECTORY=./
INPUT_COMPACT=true
INPUT_QUIET=true
SCAN_TYPE=IAC
```

### Secret Scanning

The secret scanning section of the GitLab CI/CD pipeline is designed to integrate with AccuKnox to scan for hardcoded secrets and sensitive information in the git repositories.

Tthe following optional environment variables can be set:


| **Input Value**         | **Description**                                                                                     | **Default Value**                  |
| ------------------------ | --------------------------------------------------------------------------------------------------- | ---------------------------------- |
| **RESULTS**             | Specifies which type(s) of results to output: `verified`, `unknown`, `unverified`, `filtered_unverified`. Defaults to all types. | `""`                               |
| **BRANCH**              | The branch to scan. Use `all-branches` to scan all branches.                                        | `""`                               |
| **EXCLUDE_PATHS**       | Paths to exclude from the scan.                                                                     | `""`                               |
| **ADDITIONAL_ARGUMENTS**| Extra parameters for secret scanning.                                                               | `""`                               |

## **Mounting Repositories**  
Code repositories should be mounted at `/src` to enable scanning. Ensure that your working directory is correctly mapped when running the container.  

## **Example Usage**  
To run the scanner with a mounted repository:  
```sh
docker run --rm -ti --env-file .env -v $PWD:/src accuknoxaspm
```

If you don't have a local repository to mount, you can specify a repository URL using environment variables.  

## **Cloning a Repository**  
If `/src` is not mounted, the scanner will attempt to clone the repository specified in the environment variables.  

### **Environment Variables:**  
- `REPOSITORY_URL` → The Git repository URL to clone. (**Required if not mounting a repository**)  
- `REPOSITORY_BRANCH` → (Optional) The branch to clone. If not provided, the default branch is used.  
- `REPOSITORY_USERNAME` → (Optional) Username for private repositories.  
- `REPOSITORY_ACCESS_TOKEN` → (Optional) Access token for private repositories.  

### **Example Usage for Cloning**  
```sh
docker run --rm -ti --env-file .env accuknoxaspm
```
Ensure `.env` contains:  
```sh
REPOSITORY_URL=https://github.com/safeer-accuknox/aspm-scanner
REPOSITORY_BRANCH=main
REPOSITORY_USERNAME=myusername
REPOSITORY_ACCESS_TOKEN=myaccesstoken
```

### **Authentication for Private Repositories**  
If cloning a private repository, ensure `REPOSITORY_USERNAME` and `REPOSITORY_ACCESS_TOKEN` are provided.  