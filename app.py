#!/usr/bin/env python3

from aws_cdk import core

from cdk_pipeline_mwe.cdk_pipeline_mwe_stack import CdkPipelineMweStack


app = core.App()
CdkPipelineMweStack(app, "cdk-pipeline-mwe")

app.synth()
