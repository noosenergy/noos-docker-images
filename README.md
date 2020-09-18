[![CircleCI](https://circleci.com/gh/noosenergy/neptune-aws-cloud.svg?style=svg&circle-token=96776f9688a883a3a6a5055efbd2a293437d483e)](https://circleci.com/gh/noosenergy/noos-forge)

# Noos Forge
Developer tools for working with the Kubernetes platform.

## Quickstart
To install the stack via `docker-compose` on a Mac.


### Clone the repositories
Copy the codebase for:
* the quantitative analytics [`octoquant`](https://github.com/octoenergy/octoquant)
* the [`octotrade`](https://github.com/octoenergy/octotrade) trade capture service
* the [`octocurve`](https://github.com/octoenergy/octocurve) curve engine service
* and their python clients [`octoclient`](https://github.com/octoenergy/octoclient)
* the [`octohub`](https://github.com/octoenergy/octohub) platform
* and its mounted volume [`octohub-volume`](https://github.com/octoenergy/octohub-volume)

And follow their individual installation guidelines.

### Add env variables
:warning: Copy the project `dotenv` file and amend the variables to adapt your local file system.

```dotenv
# Github token to install first party libraries (Docker image build stage)
GITHUB_TOKEN=

# AWS credentials to access remote resources (S3, Athena, etc)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# Secret store for resource URLs (FTPs, DBs, etc)
TENTACLIO_SECRETS_FILE=

# Procurement lib repositories
OCTOQUANT_REPO_PATH=
OCTOCLIENT_REPO_PATH=

# Procurement app repositories
OCTOTRADE_REPO_PATH=
OCTOCURVE_REPO_PATH=
OCTOHUB_REPO_PATH=

# Procurement app volumes
OCTOHUB_VOLUME_REPO_PATH=
```

## Extras
The repository implements as well a set of utilities with their associated Docker images:
* backing up service databases into local / remote storage
