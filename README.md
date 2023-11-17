
# OpenSearch Serverless Python CDK project

Resources to be provisioned within your account:

* OpenSearch Serverless collection
* SageMaker Jupyter Notebook instance
* Lambda Custom Resource that will run once on deployment and create a vector index
* IAM role with ``AmazonS3FullAccess`` and ``AmazonSageMakerFullAccess`` and access to the OpenSearch collection that was provisioned for SageMaker Jupyter Notebook
* IAM role with access to the OpenSearch collection that was provisioned for SageMaker Jupyter Notebook


Due to lengthy time it takes to spin up OpenSearch collection, the whole deployment will take around 15-20 minutes.

# Before you start
All of the commands are to be executed from the project's root folder.

Recommended: Create a Python virtual environemnt. To manually create a virtualenv on MacOS and Linux:

```
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
.venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
pip install -r requirements.txt
```

After that bootstrap your account. You only need to do that once for an account per region.

```
cdk bootstrap
```

To deploy the application run the following command:

```
cdk deploy --require-approval never
```

After that clone the following repo ``https://github.com/aws-samples/amazon-bedrock-workshop.git`` in your Jupyter Notebook instance. 