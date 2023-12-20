#!/usr/bin/env python3
import aws_cdk as cdk

from backend.main import OpenSearchEmbeddingsExampleStack

app = cdk.App()
OpenSearchEmbeddingsExampleStack(app, "OpenSearchEmbeddingsExampleStack")
app.synth()                 
