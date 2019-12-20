#!/usr/bin/env python3

from aws_cdk import core

from cdk_pipeline_mwe.asg import AutoScaling
from cdk_pipeline_mwe.pipeline import Pipeline


app = core.App()
asg_stack = AutoScaling(app, "asg-stack")
pipe_stack = Pipeline(app, "pipeline-stack", asg_stack.asg)
pipe_stack.add_dependency(asg_stack)

app.synth()
