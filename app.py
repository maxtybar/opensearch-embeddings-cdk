#!/usr/bin/env python3
import aws_cdk as cdk
import os

from backend.main import OpenSearchEmbeddingsExampleStack

app = cdk.App()
OpenSearchEmbeddingsExampleStack(app, "OpenSearchEmbeddingsExampleStack")
app.synth()                 
