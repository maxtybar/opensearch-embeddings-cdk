from aws_cdk import Stack
from constructs import Construct

from backend.constructs.opensearch_serverless_construct import OpenSearchCollectionConstruct
from backend.constructs.sagemaker_notebook_construct import SageMakerNotebookConstruct
from backend.constructs.notebook_iam_role_construct import SageMakerNotebookRoleConstruct
from backend.constructs.custom_resource_iam_role import CustomResourceIamRoleConstruct
from backend.constructs.custom_resource_construct import CustomResourceConstruct


class OpenSearchStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs) 

        self.collection_name = 'embeddings-collection'
        self.sagemaker_notebook_instance_type = 'ml.m5.xlarge'
        self.vector_field_name = 'test-embeddings'
        self.vector_index_name = 'test-vector'
        self.text_field = 'text-field'
        self.metadata_filed = 'metadata-field'
        self.git_repo = "https://github.com/aws-samples/amazon-bedrock-workshop.git"


        custom_resource_iam_role = CustomResourceIamRoleConstruct(self, "CustomResourceIamRoleConstruct", {})
        sagemaker_notebook_role = SageMakerNotebookRoleConstruct(self, "SageMakerNotebookRoleConstruct", {})
        opensearch_collection = OpenSearchCollectionConstruct(self, "OpensearchCollectionConstruct", {
            "collection_name": self.collection_name,
            "notebook_role_arn": sagemaker_notebook_role.role_arn,
            "custom_resource_role_arn": custom_resource_iam_role.role_arn
        })

        custom_resource = CustomResourceConstruct(self, "CustomResourceConstruct", {
            "custom_resource_role_arn": custom_resource_iam_role.role_arn,
            "custom_resource_role": custom_resource_iam_role.role,
            "collection_arn": opensearch_collection.collection_arn,
            "collection_endpoint": opensearch_collection.collection_endpoint,
            "vector_field_name": self.vector_field_name,
            "vector_index_name": self.vector_index_name,
            "text_field": self.text_field,
            "metadata_field": self.metadata_filed
        })

        sagemaker_notebook = SageMakerNotebookConstruct(self, "SagemakerNotebookConstruct", {
            "collection_arn": opensearch_collection.collection_arn,
            "notebook_instance_type": self.sagemaker_notebook_instance_type,
            "notebook_role": sagemaker_notebook_role.role,
            "notebook_role_arn": sagemaker_notebook_role.role_arn,
            "git_repo": self.git_repo
        })
        
        sagemaker_notebook.node.add_dependency(sagemaker_notebook_role)
        sagemaker_notebook.node.add_dependency(opensearch_collection)
        custom_resource.node.add_dependency(opensearch_collection)
        custom_resource.node.add_dependency(custom_resource_iam_role)
