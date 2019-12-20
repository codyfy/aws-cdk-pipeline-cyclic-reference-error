from aws_cdk import (
    core,
    aws_codecommit as codecommit,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_autoscaling as autoscaling,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codedeploy as codedeploy
)


class Pipeline(core.Stack):

    def __init__(self, scope: core.Construct, id: str, props: autoscaling.AutoScalingGroup, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

         #---------- CodeCommit Repository ----------#
        repository = codecommit.Repository(self, "Repository", repository_name="repo")
        
        #---------- CodePipeline ----------#
        pipeline = codepipeline.Pipeline(self, "CodePipeline")

        #---------- Source ----------#
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name="Source",
            repository=repository,
            output=source_output
        )
        
        pipeline.add_stage(stage_name="Source", actions=[source_action])

        #---------- Build ----------#
        
        build_output = codepipeline.Artifact()
        build_project = codebuild.PipelineProject(self, "CodeBuildProject",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml")
        )
        build_action = codepipeline_actions.CodeBuildAction(
            action_name="Build",
            input=source_output,
            project=build_project,
            outputs=[ build_output ]
        )

        pipeline.add_stage(stage_name="Build", actions=[build_action])

        #---------- Deploy ----------#
        deploy_application = codedeploy.ServerApplication(self, "CodeDeployApplication", application_name="application")
        deployment_group = codedeploy.ServerDeploymentGroup(self, "DeploymentGroup",
            application=deploy_application,
            auto_scaling_groups=[ props ]
        )
        print(deployment_group)
        deploy_action = codepipeline_actions.CodeDeployServerDeployAction(
            action_name="DeployToASG",
            input=source_output,
            deployment_group=deployment_group
        )
        pipeline.add_stage(stage_name="Deploy", actions=[ deploy_action ])