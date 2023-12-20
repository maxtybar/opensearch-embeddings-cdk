
# OpenSearch Serverless Python CDK project

Resources to be provisioned within your account:

* OpenSearch Serverless collection
* SageMaker Jupyter Notebook instance
* IAM role with ``AmazonS3FullAccess`` and ``AmazonSageMakerFullAccess``, Bedrock full access, and access to the OpenSearch collection that was provisioned for SageMaker Jupyter Notebook

**Impotant Note:** Jupyter notebook as well as assets related to it (like images and dependencies) that are included and being used in this repository (found in [this](./notebook/) folder) were cloned and modified from the oficial aws-samples repository (see original notebook [here](https://github.com/aws-samples/amazon-bedrock-workshop/blob/main/03_QuestionAnswering/02_qa_w_rag_claude_opensearch.ipynb)).

# Prerequisites

Deployment has been tested on MacOS and Linux machines. Installation guide assumes you have AWS account and Administrator Access to provision all the resources. 

Due to lengthy time it takes to spin up OpenSearch collection and Notebook Instance, the whole deployment can take anywhere around 10-15 minutes.

=============

* [node](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) >= 16.0.0
* [Python](https://www.python.org/) >= 3.11
* [pip](https://pypi.org/project/pip/) >= 23.3.1
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) >= 2.0.0
* [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) >= 2.66.1

# Before you start

All of the commands are to be executed from the project's root folder.

Recommended: Create a Python virtual environemnt. To manually create a virtualenv on MacOS and Linux:

```
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

**Note: This command is for MacOS/Linux machines only.** 
If you are using MacOS/Linux machine run the following command:

```
source .venv/bin/activate
```

**Note: This command is for Windows machines only.** 
If you are using a Windows platform, you would activate the virtualenv like this:

```
.venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
pip install -r requirements.txt
```

After that bootstrap your account if this your first time using cdk in this account. 
You only need to do that once for an account per region.

```
cdk bootstrap
```

To deploy the application run the following command:

```
cdk deploy -c current_user_arn=$(aws sts get-caller-identity --query Arn --output text) --require-approval never
```

Current repository was also cloned to the Jupyter Notebook Instance and you can access it in ``/home/ec2-user/SageMaker/`` notebook directory in your Amazon SageMaker Notebook Instance.

# How to delete

From within the root project folder (``opensearch-embeddings-cdk``), run the following command:

```
cdk destroy -c current_user_arn=$(aws sts get-caller-identity --query Arn --output text) --force
```