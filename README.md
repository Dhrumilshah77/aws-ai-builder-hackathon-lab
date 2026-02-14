# AWS AI BUILDER LAB: CRAFT WITH AI AND BUILD WITH AI

## Virtual Pet Store - AI-Powered Infrastructure

This project demonstrates a comprehensive AI-powered infrastructure deployment using modern cloud-native tools and best practices.

![Virtual Pet Store](screenshots/virtual-petstore-website.png)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AWS AI BUILDER LAB PIPELINE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│   │   STRANDS    │     │  LANGGRAPH   │     │  LLAMAINDEX  │               │
│   │    AGENT     │     │    AGENT     │     │    AGENT     │               │
│   └──────┬───────┘     └──────┬───────┘     └──────┬───────┘               │
│          │                    │                    │                        │
│          └────────────────────┼────────────────────┘                        │
│                               ▼                                             │
│                    ┌──────────────────┐                                     │
│                    │   PULUMI IaC     │                                     │
│                    │  (Python SDK)    │                                     │
│                    └────────┬─────────┘                                     │
│                             │                                               │
│          ┌──────────────────┼──────────────────┐                            │
│          ▼                  ▼                  ▼                            │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                   │
│   │  Pulumi ESC  │   │   Pulumi     │   │   Pulumi     │                   │
│   │ (Secrets &   │   │   Policy     │   │ Deployments  │                   │
│   │   Config)    │   │   Packs      │   │(Drift Detect)│                   │
│   └──────────────┘   └──────────────┘   └──────────────┘                   │
│                             │                                               │
│                             ▼                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                         AWS SERVICES                                 │  │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │  │
│   │  │   S3    │  │CloudFront│  │ Secrets │  │   IAM   │  │   EC2   │   │  │
│   │  │ Buckets │  │   CDN   │  │ Manager │  │  Roles  │  │(Coder)  │   │  │
│   │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                             │                                               │
│                             ▼                                               │
│                    ┌──────────────────┐                                     │
│                    │  OBSERVABILITY   │                                     │
│                    │  ┌────────────┐  │                                     │
│                    │  │   Arize    │  │                                     │
│                    │  │  Tracing   │  │                                     │
│                    │  └────────────┘  │                                     │
│                    │  ┌────────────┐  │                                     │
│                    │  │LaunchDarkly│  │                                     │
│                    │  │  Feature   │  │                                     │
│                    │  │   Flags    │  │                                     │
│                    │  └────────────┘  │                                     │
│                    └──────────────────┘                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## AWS Services Used

| Service | Purpose |
|---------|---------|
| **Amazon S3** | Storage buckets for each AI agent (strands, langgraph, llamaindex) |
| **Amazon CloudFront** | CDN for hosting the Virtual Pet Store website |
| **AWS Secrets Manager** | Secure storage for API keys (Pulumi, LaunchDarkly) |
| **Amazon EC2** | Coder workspace hosting for development |
| **AWS IAM** | Identity and access management for services |

---

## Project Components

### 1. Pulumi Infrastructure as Code
- **Organization**: `Dhrumilshah77-org`
- **Project**: `virtual-petstore`
- **Runtime**: Python

### 2. AI Agent Stacks
| Stack | Agent Type | Resources |
|-------|------------|-----------|
| `strands-agent-dev` | Strands | S3 Bucket with tags |
| `langgraph-agent-dev` | LangGraph | S3 Bucket with tags |
| `llamaindex-agent-dev` | LlamaIndex | S3 Bucket with tags |

### 3. Pulumi Features Implemented
- **ESC (Environments, Secrets, Configuration)**: `default/petstore-env`
- **Policy Packs**: `petstore-policy` - Enforces Environment tags on S3 buckets
- **Drift Detection**: Scheduled refresh every 6 hours
- **Stack Configuration**: Per-stack config values for agent types

### 4. Coder Templates
- `petstore-pulumi-launchdarkly` - Pulumi + LaunchDarkly integration
- `petstore-arize-llamaindex` - Arize + LlamaIndex MCP servers

---

## Hosted Website

**Virtual Pet Store**: https://d15amxqcyx00y1.cloudfront.net/

---

## Screenshots

### Virtual Pet Store Website
![Website](screenshots/virtual-petstore-website.png)

### Pulumi Stack Overview
![Pulumi](screenshots/pulumi-stack-overview.png)

---

## Tech Stack

| Category | Technology |
|----------|------------|
| **Infrastructure** | Pulumi (Python SDK) |
| **Cloud Provider** | AWS |
| **AI Frameworks** | LlamaIndex, LangGraph, Strands |
| **Observability** | Arize Phoenix |
| **Feature Flags** | LaunchDarkly |
| **Development** | Coder Workspaces |
| **MCP Servers** | Arize, LlamaIndex |

---

## Quick Start

```bash
# Install dependencies
pip install pulumi pulumi-aws

# Select a stack
pulumi stack select strands-agent-dev

# Preview changes
pulumi preview --policy-pack ../policy-pack

# Deploy
pulumi up --yes
```

---

## Project Structure

```
pulumi-petstore/
├── __main__.py                          # Main Pulumi program
├── Pulumi.yaml                          # Project configuration
├── Pulumi.strands-agent-dev.yaml        # Strands stack config
├── Pulumi.langgraph-agent-dev.yaml      # LangGraph stack config
├── Pulumi.llamaindex-agent-dev.yaml     # LlamaIndex stack config
├── Pulumi.*.deploy.yaml                 # Deployment settings
├── requirements.txt                     # Python dependencies
├── screenshots/                         # Project screenshots
│   ├── virtual-petstore-website.png
│   └── pulumi-stack-overview.png
└── README.md                            # This file

policy-pack/
├── __main__.py                          # Policy definitions
├── PulumiPolicy.yaml                    # Policy pack config
└── requirements.txt                     # Policy dependencies
```

---

## Author

Built with AI assistance during the **AWS AI Builder Lab** hackathon.

**Date**: February 2026
