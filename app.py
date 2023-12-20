#!/usr/bin/env python3
import aws_cdk as cdk

from backend.main import OpenSearchStack

app = cdk.App()
OpenSearchStack(app, "OpenSearchStack")
app.synth()                 
