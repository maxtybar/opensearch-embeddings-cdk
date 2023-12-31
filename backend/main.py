from aws_cdk import Stack
from constructs import Construct

from backend.constructs.opensearch_serverless_construct import OpenSearchCollectionConstruct
from backend.constructs.sagemaker_notebook_construct import SageMakerNotebookConstruct
from backend.constructs.notebook_iam_role_construct import SageMakerNotebookRoleConstruct


class OpenSearchEmbeddingsExampleStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs) 

        self.collection_name = 'bedrock-workshop-rag'
        self.sagemaker_notebook_instance_type = 'ml.t3.medium'
        self.git_repo = "https://github.com/maxtybar/opensearch-embeddings-cdk.git"
        self.current_user_arn = self.node.try_get_context("current_user_arn")

        sagemaker_notebook_role = SageMakerNotebookRoleConstruct(self, "SageMakerNotebookRoleConstruct", {})
        opensearch_collection = OpenSearchCollectionConstruct(self, "OpensearchCollectionConstruct", {
            "collection_name": self.collection_name,
            "notebook_role_arn": sagemaker_notebook_role.role_arn,
            "current_user_arn": self.current_user_arn
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
