# JIRA tickets
To setup Dataflow pipelines using custom Python package along with a Cloud Build CI/CD, here is the list of tasks to be performed:

We assume that each environment has its own dedicated GCP project.

In `develop` GCP project:
1. Enable APIs for: Artifact Registry, Cloud Build, Dataflow
2. Create Artifact Registry Docker repository
3. Create Artifact Registry Python repository
4. Create Cloud Build service account `sa-cloud-build` with following roles:
    - Artifact Registry Writer
    - Cloud Build Editor
    - Logs Writer
    - Service Account User of the default Compute Engine service account of the project (Dataflow uses it)
5. It is recommended to [replace the worker service account with a user-managed service account](https://cloud.google.com/dataflow/docs/concepts/security-and-permissions#permissions)
6. Create Cloud Storage bucket for Dataflow templates and artifacts
7. Create Cloud Build 2nd gen trigger with `push to main branch` event linked to the [custom Python package GitHub repository](https://github.com/gregoireborel/gborelpy) (keep default configuration with `cloudbuild.yaml`). Attach `sa-cloud-build` to the trigger
8. Create Cloud Build 2nd gen trigger with `push to feature/ branch` event linked to Dataflow GitHub repository.  Attach `sa-cloud-build` to the trigger. Apply following configuration:

[<img src="img/develop_trigger_build.png/" width="50%" height="50%" style=" display: block;margin-left: auto;margin-right: auto;">]()

9. Create Cloud Build 2nd gen trigger with `manual invocation` response linked to Dataflow GitHub repository.  Attach `sa-cloud-build` to the trigger. Apply following configuration:

[<img src="img/develop_trigger_run.png/" width="50%" height="50%" style=" display: block;margin-left: auto;margin-right: auto;">]()

In `staging` GCP project:
1. Enable APIs for: Artifact Registry, Cloud Build, Dataflow
2. Create Artifact Registry Docker repository
3. Create Cloud Build service account `sa-cloud-build` with following roles:
    - Artifact Registry Writer
    - Cloud Build Editor
    - Logs Writer
    - Service Account User of the default Compute Engine service account of the project (Dataflow uses it)
    - Artifact Registry Reader access to the `sa-cloud-build` service account in `develop` project (in order to get access to `develop` Artifact Registry)
4. It is recommended to [replace the worker service account with a user-managed service account](https://cloud.google.com/dataflow/docs/concepts/security-and-permissions#permissions)
5. Create Cloud Storage bucket for Dataflow templates and artifacts
6. Create Cloud Build 2nd gen trigger with `push to main branch` event linked to Dataflow GitHub repository. Attach `sa-cloud-build` to the trigger. Apply following configuration:

[<img src="img/staging_trigger_build.png/" width="50%" height="50%" style=" display: block;margin-left: auto;margin-right: auto;">]()

7. Create Cloud Build 2nd gen trigger with `manual invocation` response linked to Dataflow GitHub repository. Attach `sa-cloud-build` to the trigger. Apply following configuration:

[<img src="img/staging_trigger_run.png/" width="50%" height="50%" style=" display: block;margin-left: auto;margin-right: auto;">]()