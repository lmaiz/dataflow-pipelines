# flex-pokemon-pubsub-dataflow-biqquery
## What is it?
flex-pokemon-pubsub-dataflow-biqquery is batch pipeline designed to : 
- Read Pokemon files from GCS
- Process the data
- Write processed data to the BigQuery table

## Run
- In local, simply use `directrunner.sh` [with batch or streaming parameter to define the mode] 
- In `develop` GCP project, from your branch, push your commits. It will trigger the CI and build the Docker image. Then use the `dataflow-flex-template-run ` trigger to run your pipeline

## Update the Docker dependencies
You probably don't have any reason to amend the Dockerfile. However, if you have new dependencies, you will need to inject them in the Docker image:
1. Update `requirements.in`
2. `pip-compile requirements.in` will regenerate `requirements.txt`
