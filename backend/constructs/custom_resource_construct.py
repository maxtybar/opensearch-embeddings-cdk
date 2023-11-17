from aws_cdk import (
    Duration,
    custom_resources as cr,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_logs as logs,
    CustomResource
)
from constructs import Construct


class CustomResourceConstruct(Construct):

    def __init__(self, scope: Construct, construct_id: str, props: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.custom_resource_role = props['custom_resource_role']
        self.collection_arn = props['collection_arn']
        self.collection_endpoint = props['collection_endpoint']
        self.vector_field_name = props['vector_field_name']
        self.vector_index_name = props['vector_index_name']
        self.text_field = props['text_field']
        self.metadata_filed = props['metadata_field']

        # Create a policy to allow access from Lambda to OpenSearch Data Plane
        self.custom_resource_role.add_to_policy(iam.PolicyStatement(
            resources=[f"{self.collection_arn}"],
            actions=["aoss:APIAccessAll"]
        ))

        # Lambda Layer with required dependencies
        layer = lambda_.LayerVersion(self, "OpenSearchLayer",
            code=lambda_.Code.from_asset("backend/lambda_layer/dependencies.zip"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_9],
            description="Lambda Layer with opensearch.py and other dependencies."
        )

        # Custom lambda to provision vector index
        on_event = lambda_.Function(self, "OpenSearchCustomResourceFunction",
            runtime=lambda_.Runtime.PYTHON_3_9, 
            handler="custom_resource.on_event",
            code=lambda_.Code.from_asset("backend/function"),
            layers=[layer],
            timeout=Duration.seconds(600),
            environment={
                "COLLECTION_ENDPOINT": self.collection_endpoint,
                "VECTOR_FIELD_NAME": self.vector_field_name,
                "VECTOR_INDEX_NAME": self.vector_index_name,
                "TEXT_FIELD": self.text_field,
                "METADATA_FIELD": self.metadata_filed
            },
            role=self.custom_resource_role
        )

        provider = cr.Provider(self, "CustomResourceProvider",
            on_event_handler=on_event,
            log_retention=logs.RetentionDays.ONE_DAY,
        )

        CustomResource(self, "CustomResource",
            service_token=provider.service_token
        ).node.add_dependency(self.custom_resource_role)
