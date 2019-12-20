from aws_cdk import (
    core,
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2
)


class AutoScaling(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(self, "VPC")

        self.asg = autoscaling.AutoScalingGroup(self, "AutoScalingGroup",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MEDIUM),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2)
        )