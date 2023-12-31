
# OpenSearch Serverless Vector Store Python CDK project

This code repository is associated with the [following](https://medium.com/@maxtybar/use-amazon-opensearch-serverless-for-rag-184dd12355a0) Medium post.

Resources to be provisioned within your account:

* OpenSearch Serverless collection
* SageMaker Jupyter Notebook instance
* IAM role with ``AmazonS3FullAccess`` and ``AmazonSageMakerFullAccess``, Bedrock full access, access to the OpenSearch collection that was provisioned for SageMaker Jupyter Notebook and ``BatchGetCollection`` API call against OpenSearch Serverless collections.

**Impotant Note:** Jupyter notebook as well as assets related to it (like images and dependencies) that are included and being used in this repository (found in [this](./notebook/) folder) were cloned and modified from the official aws-samples repository (see original notebook [here](https://github.com/aws-samples/amazon-bedrock-workshop/blob/main/03_QuestionAnswering/02_qa_w_rag_claude_opensearch.ipynb)).

# Prerequisites

Deployment has been tested on MacOS, Windowsa and Linux machines. Installation guide assumes you have AWS account and Administrator Access to provision all the resources. 

Due to lengthy time it takes to spin up OpenSearch collection and Notebook Instance, the whole deployment can take anywhere around 10-15 minutes.

=============

* [node](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) >= 16.0.0
* [Python](https://www.python.org/) >= 3.11
* [pip](https://pypi.org/project/pip/) >= 23.3.1
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) >= 2.0.0
* [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) >= 2.66.1

# Before you start

Clone current repository:

```
git clone https://github.com/maxtybar/opensearch-embeddings-cdk.git
```

Navigate to the cloned repository in your terminal/shell. All of the commands are to be executed from the project's root folder/repo that you just cloned.

Recommended: Create a Python virtual environment. To manually create a virtualenv run the following command:

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
python3 -m pip install -r requirements.txt
```

After that bootstrap your account if this your first time using cdk in this account. 
You only need to do that once for an account per region.

```
cdk bootstrap -c current_user_arn=$(aws sts get-caller-identity --query Arn --output text) --require-approval never
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