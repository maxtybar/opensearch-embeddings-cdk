from aws_cdk import aws_iam as iam
from constructs import Construct


class CustomResourceIamRoleConstruct(Construct):

    @property
    def role(self):
        return self._lambda_role
    
    @property
    def role_arn(self):
        return self._lambda_role.role_arn

    def __init__(self, scope: Construct, construct_id: str, props: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda role for a custom construct
        self._lambda_role = iam.Role(self, "LambdaRole",
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com')
        )