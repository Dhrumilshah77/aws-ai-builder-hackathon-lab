import pulumi
import pulumi_aws as aws

# Get stack and project info
stack = pulumi.get_stack()
project = pulumi.get_project()
config = pulumi.Config()

agent_type = config.get("agentType") or stack.replace("-agent-dev", "")

# Create S3 bucket for the agent
bucket = aws.s3.Bucket(f"agent-{stack}-bucket",
    tags={
        "Environment": "production",
        "Project": project,
        "AgentType": agent_type,
        "ManagedBy": "Pulumi"
    }
)

# Exports
pulumi.export("stack_name", stack)
pulumi.export("project_name", project)
pulumi.export("agent_type", agent_type)
pulumi.export("bucket_name", bucket.id)
pulumi.export("status", "deployed")
