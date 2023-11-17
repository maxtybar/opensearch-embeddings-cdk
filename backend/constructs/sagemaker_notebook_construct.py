from aws_cdk import (
    aws_sagemaker as sagemaker,
    aws_iam as iam,
    Fn
)
from constructs import Construct

class SageMakerNotebookConstruct(Construct):

    def __init__(self, scope: Construct, construct_id: str, props: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.sagemaker_notebook_role = props['notebook_role']
        self.sagemaker_notebook_role_arn = props['notebook_role_arn']
        self.sagemaker_notebook_instance_type = props['notebook_instance_type']
        self.collection_arn = props['collection_arn']
        self.git_repo = props['git_repo']

        # Create a lifecylce config to clone git repo
        notebook_instance_lifecycle_config = sagemaker.CfnNotebookInstanceLifecycleConfig(self, "MyCfnNotebookInstanceLifecycleConfig",
            notebook_instance_lifecycle_config_name="notebookInstanceLifecycleConfigName",
            on_create=[sagemaker.CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty(
                content=Fn.base64("""cd /home/ec2-user/SageMaker/ && git clone {}""".format(self.git_repo))
            )]
        )

        # Create a SageMaker Notebook Instance
        sagemaker.CfnNotebookInstance(self, "MyCfnNotebookInstance",
            instance_type=self.sagemaker_notebook_instance_type,
            role_arn=self.sagemaker_notebook_role_arn,
            lifecycle_config_name=notebook_instance_lifecycle_config.attr_notebook_instance_lifecycle_config_name
        )

        # Create a policy to allow access to OpenSearch Data Plane and 
        # add it to SageMaker Notebook role
        self.sagemaker_notebook_role.add_to_policy(iam.PolicyStatement(
            resources=[f"{self.collection_arn}"],
            actions=["aoss:APIAccessAll"]
        ))

        # Attach Bedrock access to invoke models
        self.sagemaker_notebook_role.add_to_policy(iam.PolicyStatement(
            resources=["*"],
            actions=["bedrock:*"]
        ))

