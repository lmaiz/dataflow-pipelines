# gcp_pipelines/dataflow-pipelines

## What are Dataflow and Apache Beam
Google Cloud Dataflow is a fully managed service for executing Apache Beam pipelines within the Google Cloud Platform ecosystem.

Apache Beam is an open source, unified model for defining both batch and streaming data-parallel processing pipelines. Using one of the open source Beam SDKs (Java, Python, Go), you build a program that defines the pipeline.

[<img src="https://beam.apache.org/images/learner_graph.png" width="75%" height="75%" style=" display: block;margin-left: auto;margin-right: auto;">](https://beam.apache.org/get-started/beam-overview/)

**Remember**: you code a streaming or batch pipeline. You package it as a template. You deploy it by running a job of said template.

### Types of data pipelines
Dataflow has two data pipeline types, streaming (unbounded data) and batch (bounded data). Both types of pipeline run jobs that are defined in Dataflow templates (Classic or Flex).

Streamings jobs are typically run continously where as batch jobs are run on a schedule (e.g. daily).

```
Use case: you need to ingest historical and incremental data. The transformation logic is the same for both cases, but the size of the data differs.

We could create:
- one batch pipeline running once per day ingesting huge chunks of historical data (e.g. one file)
- one streaming pipeline running continously and ingesting small updates (e.g. thousands of files)

Yet, both pipelines share most of the source code because they process the same data. Only the data input and data size change.
```

However, streaming pipelines are more complex to manage. Specific concepts such as [windowing](https://beam.apache.org/documentation/programming-guide/index.html#windowing) and [triggers](https://beam.apache.org/documentation/programming-guide/index.html#triggers) need to be learned in order to address the unbounded nature of streaming data.

### Types of Dataflow templates: Classic vs Flex
Dataflow templates allow you to package a Dataflow pipeline for deployment. Old way is to use Classic template, new way is Flex template. Both have pros and cons:

| Feature              | Dataflow Classic Templates       | Dataflow Flex Templates                                                                                          |
|----------------------|----------------------------------|------------------------------------------------------------------------------------------------------------------|
| Job graph            | Static                           | Dynamic (the graph is built based on input parameters)                                                           |
| Input parameters     | Requires ValueProvider interface | Can use any type of input parameter                                                                              |
| Preprocessing        | Not supported                    | Supported                                                                                                        |
| Customization        | More limited                     | More flexible                                                                                                    |
| Packaging            | Template loaded in GCS           | Docker image in Artifact Registry with a template specification in GCS, containing a pointer to the Docker image |
| Recommended          | For old pipelines                | For new pipelines                                                                                                |

## How to develop Dataflow pipelines
Three ways:
- Local environment
- Cloud Shell
- [Dataflow notebooks](https://cloud.google.com/dataflow/docs/guides/interactive-pipeline-development)

We'll focus on the first one as it is the most permissive and flexible.

## Local environment
You need to install:
- [vscode](https://code.visualstudio.com/) (with the following extensions: Python, Pylance, Ruff, Git Graph and Remote Development if you're on Windows)
- WSL 2 with Ubuntu 22.04 if you're on Windows
- [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) (to easily handle Python versions)
- [gcloud](https://cloud.google.com/sdk/docs/install)


Useful Ruff commands in vscode:
- Format imports
- Format documents
- Fix all auto-fixable problems

### Initialization
Given the numerous bugs we can find on Apache Beam, it's important to keep track of the latest updates and use the most recent versions.
As for this project, we use Python 3.11 and Apache Beam 2.57.0.

More info about the SDK version support status [here](https://cloud.google.com/dataflow/docs/support/sdk-version-support-status).

1. Install and use Python 3.11 in a virtual environment for the `dataflow-pipelines` folder

Using pyenv:
```bash
pyenv install 3.11
pyenv virtualenv 3.11 dataflow-pipelines-env
cd ~/gcp_pipelines/dataflow-pipelines
pyenv local dataflow-pipelines-env
pyenv versions
```
You can find a good pyenv tutorial [here](https://realpython.com/intro-to-pyenv).

Using virtualenv:
```bash
pip install virtualenv
cd ~/gcp_pipelines/dataflow-pipelines
virtualenv -p python3.11 dataflow-pipelines-env
source dataflow-pipelines-env/bin/activate  # On macOS/Linux
dataflow-pipelines-env\Scripts\activate # On Windows
python --version
```
2. Install Python dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
``` 
This will install Apache Beam 2.57.0, some Google packages, our private package from Artifact Registry and `pip-tools`.

3. Initialize gcloud
```bash
gcloud auth login
gcloud auth application-default login
```

:point_up: When you turn on your computer, you may need to reactivate your virtual environment.
```bash
cd ~/gcp_pipelines/dataflow-pipelines
pyenv local dataflow-pipelines-env
```

## Workflow:

1. `git checkout -b feature/GIA-XXX-my-branch`
2. Create your pipeline folder (lowercase, beginning with "flex"). Copy-pasting from anoter pipeline is handy
3. Run your code locally with `directrunner.sh`, with the `DirectRunner`
4. Add all necessary tests scripts to the `tests/` folder
5. Commit and push your work on your branch. This will trigger the Cloud Build CI in the `develop` project
6. Raise a draft PR
7. Once the PR is merged to main, the Cloud Build CI in the `staging` project will be triggered
8. From the `staging` project, run the `dataflow-flex-template-run` manual trigger to run your pipeline (replace `_PIPELINE_NAME` value)
9. Clean up. Temporary topics, buckets, etc. need to be deleted. Scripts could be handy so that the reviewer can do the same

# FAQ
- _I got weird import/pickling errors_

Use `--save_main_session` when building the template. More info on dependencies [here](https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/).

- _valueError: Expected a table reference (PROJECT:DATASET.TABLE or DATASET.TABLE)_

Check for any typos in your dataset, table or project variables.

- _I encounter errors while inserting data into a BigQuery table through the native Beam function 'WriteToBigQuery'_

These errors are not very explicit as they don't explain why the data can't be inserted (on which columns, for which row, etc.). There is a trick for having a better understanding of the reason. Here is the process:

1. In the Dataflow Job Logs, you may encounter a message such as: "Please look into the errors[] collection for more details. File: gs://[BUCKET-NAME]/path/bq_load/97f6ac09aa914ff5b5f9c01346dc728d/[PROJECT_ID.DATASET/TABLE_NAME]/fbec71d0-a311-4ab0-8ec9-f0681faa080a". Follow this path and download the final file. It contains all the rows being inserted into the BigQuery table, thus it contains the row(s) that generate the error.

2. Go to the BigQuery UI console and click "Add" in the Toggle Panel Explorer.

3. Click "Local File": Choose the appropriate file format (should be JSONL). Create a new table and browse the file with all rows that you downloaded in step number 1. Give a name to the table and associate it with a dataset (in a staging or temporary dataset). **Very important step: Edit the schema as text and copy-paste the exact schema you have when inserting data through the Dataflow job.**

4. Click "Create Table": This will create a job.

5. Click "Go to job": This will open the Load Job Details panel and should explain more explicitly the error you encountered when inserting the data, giving you a better understanding of the error.

# Additional resources
Dataflow:
- [Guides](https://cloud.google.com/dataflow/docs/overview)
- [Dataflow pipeline options](https://cloud.google.com/dataflow/docs/reference/pipeline-options)
- [Guide to common Dataflow use case patterns](https://cloud.google.com/blog/products/data-analytics/guide-to-common-cloud-dataflow-use-case-patterns-part-1?hl=en)
- [Perform fast insert and upsert to BQ with protobuff and Storage Write API](https://cloud.google.com/blog/products/data-analytics/bigquery-gains-change-data-capture-functionality)

Apache Beam:
- [Tour of Beam](https://tour.beam.apache.org/)
- [Documentation](https://beam.apache.org/documentation/)
- [Windows, late-data and triggers](https://medium.com/@shlomisderot/apache-beam-windows-late-data-and-triggers-e2e856c502b9)
- [Beam college](https://github.com/griscz/beam-college/tree/main) (lots of use cases)
- [Perform a Left Join](https://github.com/HocLengChung/Apache-Beam-Dataflow-for-public/tree/master)
- [Fast Joins in streaming](https://www.ahalbert.com/technology/2023/07/08/fast_beam_joins.html)
