#!/bin/sh

# syncing data from s3 bucket of https://mf-models-on-aws.org/
aws s3 sync s3://mf-nwp-models/arpege-europe s3://noos-prod-neptune-services/Raw/METEOFRANCE/arpege-europe --exclude "*" --include "*TMP/2m/*" --exclude "v1/*" --include "static/*"
aws s3 sync s3://mf-nwp-models/arome-france-hd s3://noos-prod-neptune-services/Raw/METEOFRANCE/arome-france-hd --exclude "*" --include "*TMP/2m/*" --exclude "v1/*" --include "static/*"
