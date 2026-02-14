from pulumi_policy import PolicyPack, ResourceValidationPolicy, EnforcementLevel

def validate_tags(args, report_violation):
    if args.resource_type == "aws:s3/bucket:Bucket":
        tags = args.props.get("tags", {})
        if not tags.get("Environment"):
            report_violation("All S3 buckets must have an Environment tag")

PolicyPack(
    name="petstore-policy",
    enforcement_level=EnforcementLevel.ADVISORY,
    policies=[
        ResourceValidationPolicy(
            name="require-environment-tag",
            description="Requires Environment tag on resources",
            validate=validate_tags,
        ),
    ],
)
