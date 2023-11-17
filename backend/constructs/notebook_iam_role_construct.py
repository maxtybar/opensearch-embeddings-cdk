from aws_cdk import aws_iam as iam
from constructs import Construct


class SageMakerNotebookRoleConstruct(Construct):

    @property
    def role(self):
        return self._sagemaker_notebook_role
    
    @property
    def role_arn(self):
        return self._sagemaker_notebook_role.role_arn

    def __init__(self, scope: Construct, construct_id: str, props: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs) 

        # Create a role for SageMaker Notebook to assume
        self._sagemaker_notebook_role = iam.Role(self, "SageMakerNotebookRole",
            assumed_by=iam.ServicePrincipal('sagemaker.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
                              iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")])
        