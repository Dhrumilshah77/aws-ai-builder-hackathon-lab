# Step-by-Step Guide: AWS AI Builder Hackathon Lab

## Virtual Pet Store - Complete Build Guide

---

## Why We Built This

We built this project to show how modern AI applications can be deployed to the cloud automatically. Instead of clicking buttons in AWS console for hours, we write code that creates everything for us. This is called **Infrastructure as Code**. It's like having a robot that builds your house exactly the same way every time, instead of hiring different workers who might do things differently.

This project combines three powerful AI agents (Strands, LangGraph, LlamaIndex) with cloud infrastructure (AWS), monitoring tools (Arize), and feature controls (LaunchDarkly). Together, they create a Virtual Pet Store where AI helps customers find and adopt pets.

---

## How This Is Helpful

This approach saves time and prevents mistakes. When you deploy manually, you might forget a step or configure something wrong. With Infrastructure as Code, the same code always creates the same result. If something breaks, you can redeploy in minutes. If you need 10 more environments, you just run the same code 10 times. Companies like Netflix, Airbnb, and Uber use this approach to manage thousands of servers without human error.

For learning, this project teaches you how real companies deploy AI applications. You'll understand AWS services, infrastructure automation, AI observability, and feature management - skills that are in high demand.

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                         VIRTUAL PET STORE ARCHITECTURE                          │
└────────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │   DEVELOPERS    │
                              │  (That's You!)  │
                              └────────┬────────┘
                                       │
                                       │ Write Code
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────┐
│                            CODER WORKSPACE (EC2)                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Pulumi     │  │   AWS CLI    │  │   Python     │  │  MCP Servers │       │
│  │     CLI      │  │              │  │              │  │ Arize/LlamaIndex     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ pulumi up
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────┐
│                              PULUMI CLOUD                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                         │
│  │     ESC      │  │   Policy     │  │ Deployments  │                         │
│  │  (Secrets)   │  │   Packs      │  │   (Drift)    │                         │
│  └──────────────┘  └──────────────┘  └──────────────┘                         │
└────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ Creates Resources
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────┐
│                                    AWS                                          │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                           S3 BUCKETS                                     │  │
│  │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐           │  │
│  │  │ strands-agent   │ │ langgraph-agent │ │ llamaindex-agent│           │  │
│  │  │    bucket       │ │     bucket      │ │     bucket      │           │  │
│  │  └─────────────────┘ └─────────────────┘ └─────────────────┘           │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐               │
│  │   CloudFront    │  │ Secrets Manager │  │      IAM        │               │
│  │   (Website)     │  │  (API Keys)     │  │  (Permissions)  │               │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘               │
└────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ Serves
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────┐
│                              VIRTUAL PET STORE                                  │
│                      https://d15amxqcyx00y1.cloudfront.net                     │
└────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ Monitored By
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────┐
│                             OBSERVABILITY                                       │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐             │
│  │      ARIZE PHOENIX          │  │       LAUNCHDARKLY          │             │
│  │   (Watches AI behavior)     │  │   (Controls features)       │             │
│  └─────────────────────────────┘  └─────────────────────────────┘             │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Workflow Process

```
┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐
│STEP │    │STEP │    │STEP │    │STEP │    │STEP │    │STEP │    │STEP │
│  1  │───▶│  2  │───▶│  3  │───▶│  4  │───▶│  5  │───▶│  6  │───▶│  7  │
└─────┘    └─────┘    └─────┘    └─────┘    └─────┘    └─────┘    └─────┘
   │          │          │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼          ▼          ▼
┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐
│Setup│    │Create│   │Write │   │Create│   │Create│   │Deploy│   │Push │
│Coder│    │Pulumi│   │Infra │   │Stack │   │Policy│   │to    │   │to   │
│Work │    │Project   │Code  │   │Config│   │Pack  │   │AWS   │   │GitHub
│space│    │      │   │      │   │      │   │      │   │      │   │     │
└─────┘    └─────┘    └─────┘    └─────┘    └─────┘    └─────┘    └─────┘
```

---

## Step 1: Set Up Coder Workspace

**What is Coder?**
Coder is a tool that creates development environments in the cloud. Instead of installing tools on your laptop, you get a virtual computer in AWS (EC2 instance) with everything pre-installed. It's like having a fully equipped workshop that you can access from any computer with a browser.

**What I Did:**
I created a Coder template that automatically sets up a workspace with all the tools needed for this project. When someone starts this workspace, they get Python, Pulumi CLI, AWS CLI, and MCP servers for Arize and LlamaIndex already installed.

**How to Connect:**
The Coder workspace runs on an EC2 instance in AWS. When you open the workspace, you're actually connecting to that EC2 instance through your browser. All your code runs there, not on your local computer.

---

## Step 2: Create Pulumi Project

**What is Pulumi?**
Pulumi is an Infrastructure as Code tool. Instead of clicking buttons in AWS console to create resources, you write code (Python, JavaScript, etc.) that describes what you want. Pulumi reads your code and creates all the resources for you. If you delete everything and run the code again, you get the exact same setup.

**What I Did:**
I created a new Pulumi project by making a file called `Pulumi.yaml`. This file tells Pulumi the project name, what programming language we're using (Python), and basic settings.

**The File I Created:**
```yaml
name: virtual-petstore
runtime: python
description: Virtual Pet Store AI Agents
```

**How It Connects:**
This file is the starting point. When you run `pulumi up`, Pulumi looks for this file to understand your project. It then reads your Python code to know what resources to create.

---

## Step 3: Write Infrastructure Code

**What is Infrastructure Code?**
Infrastructure code is Python (or other language) code that describes cloud resources. Instead of saying "go to AWS console, click S3, click create bucket, type a name...", you write code that says "create an S3 bucket with this name and these settings."

**What I Did:**
I created a file called `__main__.py` that creates S3 buckets for each AI agent. The code also adds tags to each bucket for organization.

**The Code I Wrote:**
```python
import pulumi
import pulumi_aws as aws

# Get information about which stack we're deploying
stack = pulumi.get_stack()
project = pulumi.get_project()
config = pulumi.Config()

# Get the agent type from configuration
agent_type = config.get("agentType") or stack.replace("-agent-dev", "")

# Create an S3 bucket for this agent
bucket = aws.s3.Bucket(f"agent-{stack}-bucket",
    tags={
        "Environment": "production",
        "Project": project,
        "AgentType": agent_type,
        "ManagedBy": "Pulumi"
    }
)

# Output the bucket name so we can see it
pulumi.export("bucket_name", bucket.id)
```

**What is Amazon S3?**
S3 (Simple Storage Service) is AWS's storage service. Think of it as a giant hard drive in the cloud where you can store any files - images, documents, data, etc. Each "bucket" is like a folder that can hold unlimited files.

**How It Connects:**
When Pulumi runs this code, it talks to AWS and says "create this S3 bucket with these tags." AWS creates the bucket and Pulumi remembers what it created so it can update or delete it later.

---

## Step 4: Create Stack Configurations

**What is a Stack?**
A stack is one instance of your infrastructure. If you have the same code but want to deploy it three times for three different AI agents, you create three stacks. Each stack has its own configuration and creates its own resources.

**What I Did:**
I created three stack configuration files, one for each AI agent:
- `Pulumi.strands-agent-dev.yaml` - for Strands AI agent
- `Pulumi.langgraph-agent-dev.yaml` - for LangGraph AI agent
- `Pulumi.llamaindex-agent-dev.yaml` - for LlamaIndex AI agent

**Example Configuration File:**
```yaml
config:
  aws:region: us-west-2
  virtual-petstore:environment: production
  virtual-petstore:agentType: strands
environment:
  - default/petstore-env
```

**What are the AI Agents?**
- **Strands Agent**: AWS's AI agent framework that uses Amazon Bedrock to answer questions
- **LangGraph Agent**: Creates AI workflows as graphs - good for multi-step processes
- **LlamaIndex Agent**: Specializes in searching and retrieving data from documents

**How It Connects:**
When you run `pulumi stack select strands-agent-dev`, Pulumi reads the corresponding config file. The settings in that file (like `agentType: strands`) are available in your Python code through `config.get("agentType")`.

---

## Step 5: Set Up Pulumi ESC

**What is Pulumi ESC?**
ESC stands for Environments, Secrets, and Configuration. It's a central place to store settings and secrets that multiple stacks can share. Instead of putting your AWS keys in each config file, you put them in ESC once and all stacks can access them.

**What I Did:**
I created an ESC environment called `default/petstore-env` that stores common configuration:

```yaml
values:
  aws:
    region: us-west-2
  app:
    name: virtual-petstore
  environment: production
pulumiConfig:
  aws:region: us-west-2
  app:name: virtual-petstore
```

**How to Create ESC Environment:**
```bash
pulumi env init default/petstore-env
pulumi env set default/petstore-env values.aws.region us-west-2
pulumi env set default/petstore-env pulumiConfig.aws:region us-west-2
```

**How It Connects:**
In each stack config file, I added `environment: - default/petstore-env`. This tells Pulumi to load settings from that ESC environment before running. All stacks share the same AWS region and app name automatically.

---

## Step 6: Create Policy Pack

**What is a Policy Pack?**
A Policy Pack contains rules that check your infrastructure before it's deployed. For example, "all S3 buckets must have an Environment tag." If your code tries to create a bucket without that tag, the policy blocks it.

**What I Did:**
I created a policy pack in a folder called `policy-pack/` with these files:

**PulumiPolicy.yaml:**
```yaml
name: petstore-policy
runtime: python
description: Policy Pack for Virtual Pet Store
```

**__main__.py (the policy code):**
```python
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
```

**How to Publish the Policy:**
```bash
cd policy-pack
pulumi policy publish
pulumi policy enable Dhrumilshah77-org/petstore-policy latest
```

**How It Connects:**
When you run `pulumi up` or `pulumi preview`, Pulumi checks your resources against all enabled policies. If a resource violates a policy, you see a warning (ADVISORY) or error (MANDATORY).

---

## Step 7: Configure Drift Detection

**What is Drift Detection?**
Drift happens when someone changes infrastructure outside of Pulumi - like manually editing an S3 bucket in AWS console. Drift detection periodically checks if the real infrastructure matches what Pulumi expects.

**What I Did:**
I created deployment configuration files that tell Pulumi to check for drift every 6 hours:

**Pulumi.strands-agent-dev.deploy.yaml:**
```yaml
settings:
  operationType: update
  schedules:
    drift:
      cron: "0 */6 * * *"
      enabled: true
```

**How to Push Deployment Settings:**
```bash
pulumi deployment settings push --stack strands-agent-dev --yes
```

**How It Connects:**
Pulumi Cloud reads these deployment settings and creates scheduled jobs. Every 6 hours, it runs `pulumi refresh` to compare real AWS resources with what's in Pulumi's state. If they differ, you get notified.

---

## Step 8: Deploy to AWS

**What Happens During Deployment?**
When you run `pulumi up`, Pulumi:
1. Reads your Python code
2. Compares desired state with current state
3. Shows you what will change
4. Creates/updates/deletes resources to match your code

**Commands I Ran:**
```bash
# Log into Pulumi Cloud
export PULUMI_ACCESS_TOKEN="your-token-here"
pulumi login

# Select the stack to deploy
pulumi stack select strands-agent-dev

# Preview what will be created
pulumi preview --policy-pack ../policy-pack

# Actually deploy
pulumi up --yes

# Repeat for other stacks
pulumi stack select langgraph-agent-dev
pulumi up --yes

pulumi stack select llamaindex-agent-dev
pulumi up --yes
```

**What Got Created:**
Each stack created:
- 1 S3 bucket with proper tags
- Outputs showing the bucket name

**How It Connects:**
Pulumi talks to AWS using the credentials from ESC. It creates resources and stores the state in Pulumi Cloud. Next time you run `pulumi up`, it compares your code with the stored state to know what changed.

---

## Step 9: Create the Website

**What is CloudFront?**
CloudFront is AWS's Content Delivery Network (CDN). When you host a website on S3, users far from the data center experience slow loading. CloudFront copies your website to servers worldwide, so users always load from a nearby server.

**What I Did:**
I created an S3 bucket for website files and a CloudFront distribution to serve them globally.

**The Website URL:**
```
https://d15amxqcyx00y1.cloudfront.net/
```

**How It Connects:**
1. Website files are stored in S3
2. CloudFront is configured to read from that S3 bucket
3. When users visit the URL, CloudFront serves the files
4. CloudFront caches files at edge locations worldwide

---

## Step 10: Set Up Observability

**What is Arize Phoenix?**
Arize Phoenix is an AI observability platform. It watches your AI agents and records everything they do - what questions they received, what answers they gave, how long it took, and if there were errors.

**What is LaunchDarkly?**
LaunchDarkly is a feature flag service. Feature flags let you turn features on/off without deploying new code. For example, if a new AI feature has bugs, you can disable it instantly while you fix it.

**What I Did:**
I added MCP (Model Context Protocol) servers for both tools in the Coder template:

```terraform
env = {
  ARIZE_API_KEY     = data.aws_secretsmanager_secret_version.arize.secret_string
  LAUNCHDARKLY_KEY  = data.aws_secretsmanager_secret_version.launchdarkly.secret_string
}
```

**How It Connects:**
1. API keys are stored in AWS Secrets Manager
2. Coder workspace loads the keys at startup
3. MCP servers connect to Arize and LaunchDarkly
4. AI agents send traces to Arize automatically
5. Feature flags from LaunchDarkly control agent behavior

---

## Step 11: Push to GitHub

**What is GitHub?**
GitHub is a platform for storing and sharing code. It tracks every change you make (version control), lets multiple people work together, and serves as a backup of your project.

**What I Did:**
I created a GitHub repository and pushed all the code:

```bash
# Initialize git in the project folder
git init
git branch -m main

# Connect to GitHub (using a personal access token)
git remote add origin https://github.com/Dhrumilshah77/aws-ai-builder-hackathon-lab.git

# Add all files
git add -A

# Commit with a message
git commit -m "Initial commit: Virtual Pet Store infrastructure"

# Push to GitHub
git push -u origin main
```

**What's in the Repository:**
```
aws-ai-builder-hackathon-lab/
├── __main__.py                    # Infrastructure code
├── Pulumi.yaml                    # Project config
├── Pulumi.strands-agent-dev.yaml  # Strands stack config
├── Pulumi.langgraph-agent-dev.yaml
├── Pulumi.llamaindex-agent-dev.yaml
├── requirements.txt               # Python dependencies
├── policy-pack/                   # Compliance policies
├── screenshots/                   # Project images
├── docs/                          # Documentation
└── README.md                      # Project overview
```

**How It Connects:**
GitHub stores the code, but doesn't run it. The actual infrastructure lives in AWS. Pulumi Cloud stores the state (what resources exist). GitHub is for collaboration and backup.

---

## Complete Connection Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        HOW EVERYTHING CONNECTS                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   [Your Computer]                                                       │
│        │                                                                │
│        │ Browser                                                        │
│        ▼                                                                │
│   [Coder Workspace] ◄─── Runs on AWS EC2                               │
│        │                                                                │
│        │ You write code here                                           │
│        ▼                                                                │
│   [Pulumi CLI]                                                         │
│        │                                                                │
│        ├──────────────────┬──────────────────┐                         │
│        ▼                  ▼                  ▼                         │
│   [Pulumi Cloud]    [Policy Pack]      [ESC Environment]               │
│   (stores state)    (checks rules)     (provides secrets)              │
│        │                  │                  │                         │
│        └──────────────────┴──────────────────┘                         │
│                           │                                            │
│                           ▼                                            │
│                    [AWS Account]                                       │
│                           │                                            │
│        ┌──────────────────┼──────────────────┐                         │
│        ▼                  ▼                  ▼                         │
│   [S3 Buckets]      [CloudFront]     [Secrets Manager]                 │
│   (storage)         (website CDN)    (API keys)                        │
│        │                  │                  │                         │
│        └──────────────────┼──────────────────┘                         │
│                           │                                            │
│                           ▼                                            │
│                    [AI Agents]                                         │
│        ┌──────────────────┼──────────────────┐                         │
│        ▼                  ▼                  ▼                         │
│   [Strands]         [LangGraph]       [LlamaIndex]                     │
│        │                  │                  │                         │
│        └──────────────────┼──────────────────┘                         │
│                           │                                            │
│                           ▼                                            │
│              [Arize Phoenix + LaunchDarkly]                            │
│              (monitoring + feature control)                            │
│                           │                                            │
│                           ▼                                            │
│                    [End Users]                                         │
│              (visit the pet store website)                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Summary: What We Built

| Component | Tool Used | Purpose |
|-----------|-----------|---------|
| Development Environment | Coder + EC2 | Write and run code in the cloud |
| Infrastructure Code | Pulumi + Python | Define AWS resources as code |
| Storage | Amazon S3 | Store data for each AI agent |
| Website Hosting | CloudFront | Serve website globally fast |
| Secret Management | AWS Secrets Manager + Pulumi ESC | Keep API keys safe |
| Access Control | AWS IAM | Control who can do what |
| Compliance | Pulumi Policy Packs | Enforce security rules |
| Monitoring | Pulumi Deployments | Detect infrastructure changes |
| AI Observability | Arize Phoenix | Watch AI agent behavior |
| Feature Control | LaunchDarkly | Toggle features on/off |
| Version Control | GitHub | Store and share code |

---

## How to Rebuild This Project

1. **Get a Coder workspace** with Pulumi and AWS CLI installed
2. **Create Pulumi.yaml** with your project name
3. **Write __main__.py** with your infrastructure code
4. **Create stack configs** for each environment you need
5. **Set up Pulumi ESC** for shared secrets
6. **Create a Policy Pack** for compliance rules
7. **Run `pulumi up`** to deploy to AWS
8. **Push to GitHub** for version control

The same pattern works for any cloud project - write code, run Pulumi, get infrastructure.

---

**Built at AWS AI Builder Hackathon | February 2026**
