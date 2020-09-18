# **Python Flask web application for helm releases**

This flask based web application will allow a user to select an existing helm revision to rollback or forward to.

# Basic Requirements
The expectation is that the application will run in a pod on a kubernetes cluster. As such the pod will run with a service account that provides sufficient privileges to perform helm commands based upon the helm releases that it finds.

The initial (front) page should look similar to the image below. For helm version 2, the namespace selector does not require a value, as managing helm 2 revisions does not require a namespace to be provided.
![](https://md.ervine.cloud/uploads/upload_1ebb6880cf0a1f029f96e9b1cdf4be98.png)

The code itself downloads kubectl and helm (version 2.13.1) and will perform commands against these utilities. The tiller namespace dropdown is populated by the following command in the code:
```kubectl get deploy --all-namespaces -l name=tiller```
The Chart dropdown is then filled with the helm charts deployed by the tiller instance that is selected in the Tiller Namespace dropdown. *Some Javascript code is executed to detect that the elementID for the tiller namespace has changed, and the code then populates the Chart dropdown.*

Upon hitting submit the application will then execute a helm history against the selected Chart, and a table is constructed which should look similar to the below image
![](https://md.ervine.cloud/uploads/upload_e91688e8c155e406650fcd887fd8fb59.png)

The Namespace has been added to the usual output that the 'helm history' command would return. A hidden field containing the Chart name is also included.

*At the moment, the namespace field is unnecessary, however wehn/if the application is deployed against a helm  ersion 3 environment, the namespace will be important.*

Each deployment revision is displayed, with the most recent revision displayed at the bottom of the table. Hitting the 'Deploy' button will trigger helm to rollback (or forward) to the revision selected.
