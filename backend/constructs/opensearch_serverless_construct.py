from aws_cdk import (
    CfnOutput,
    aws_opensearchserverless as opensearchserverless
)
from constructs import Construct


class OpenSearchCollectionConstruct(Construct):

    @property
    def collection_arn(self):
        return self._collection.attr_arn
    
    @property
    def collection_endpoint(self):
        return self._collection.attr_collection_endpoint

    def __init__(self, scope: Construct, construct_id: str, props: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.collection_name = props['collection_name']
        self.notebook_role_arn = props['notebook_role_arn']
        self.custom_resource_role_arn = props['custom_resource_role_arn']

        # Encryption policy for opensearch collection
        encryption_policy = opensearchserverless.CfnSecurityPolicy(
            self, "EncryptionPolicy",
            name="embeddings-encryption-policy",
            type="encryption",
            description=f"Encryption policy for {self.collection_name} collection.",
            policy="""
            {
                \"Rules\": [
                    {
                        \"ResourceType\": \"collection\",
                        \"Resource\": [
                            \"collection\/""" + self.collection_name + """*\"
                        ]
                    }
                ],
                \"AWSOwnedKey\": true
            }"""
        )

        # Network policy for opensearch collection
        network_policy = opensearchserverless.CfnSecurityPolicy(
            self, "NetworkPolicy",
            name="embeddings-network-policy",
            type="network",
            description=f"Network policy for {self.collection_name} collection.",
            policy="""
            [{
                \"Rules\": [
                    {
                        \"ResourceType\": \"collection\",
                        \"Resource\": [\"collection\/""" + self.collection_name + """*\"]
                    },
                    {
                        \"ResourceType\": \"dashboard\",
                        \"Resource\": [\"collection\/""" + self.collection_name + """*\"]
                    }],
                \"AllowFromPublic\": true
            }]"""
        )

        # Data access policy for opensearch collection
        data_access_policy = opensearchserverless.CfnAccessPolicy(
            self, "DataAccessPolicy",
            name="embeddings-access-policy",
            type="data",
            description=f"Data access policy for {self.collection_name} collection.",
            policy="""
            [{
                \"Rules\": [{
                    \"ResourceType\": \"collection\",
                    \"Resource\": [\"collection\/""" + self.collection_name + """*\"],
                    \"Permission\": [\"aoss:CreateCollectionItems\",
                                     \"aoss:DescribeCollectionItems\",
                                     \"aoss:DeleteCollectionItems\",
                                     \"aoss:UpdateCollectionItems\"
                                   ]
                    }, 
                    {
                    \"ResourceType\": \"index\",
                    \"Resource\": [\"index\/""" + self.collection_name + """*\/*\"],
                    \"Permission\": [\"aoss:CreateIndex\",
                                     \"aoss:DeleteIndex\",
                                     \"aoss:UpdateIndex\",
                                     \"aoss:DescribeIndex\",
                                     \"aoss:ReadDocument\",
                                     \"aoss:WriteDocument\"
                                  ]
                    }
                ],
                \"Principal\": [
                    \"""" + self.notebook_role_arn + """\",
                    \"""" + self.custom_resource_role_arn + """\"
                ]
            }]"""
        )   

        # Create opensearch collection
        self._collection = opensearchserverless.CfnCollection(
            self,
            "MyCfnCollection",
            name="embeddings-collection",
            description="Collection created by CDK to explore vector embeddings.",
            type="VECTORSEARCH"
        )
        
        self._collection.node.add_dependency(encryption_policy)
        self._collection.node.add_dependency(network_policy)
        self._collection.node.add_dependency(data_access_policy)
        
        # Output collection endpoint
        CfnOutput(self, "OpenSearchCollectionEndpoint", 
                          value=self._collection.attr_collection_endpoint,
                          export_name="OpenSearchCollectionEndpoint")
