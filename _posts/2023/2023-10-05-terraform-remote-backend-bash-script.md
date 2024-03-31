---
title: "Setting Up Terraform Remote Backend With AWS Using A Bash Script"
date: 2023-10-05 08:00:00 - 0500
categories: [AWS, Terraform]
tags: [terraform, bash script, aws, s3, dynamodb, state management]
image:
  path: /assets/img/headers/bash-script.webp
  lqip: data:image/webp;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAGCAMAAADNLv/0AAAAmVBMVEW6wsiOnqmNnKqNnaqNnKmwucJjeIoMLkoIK0QHK0QHLEQGKkQEJ0IEJkMAIkBIXnFkeYsaOVMUNk0PMUoNMEoKLUgGKEQAIT9GXHBfdIcPM0gQNUgQM0wPMEwJK0YFJkQBI0AAID5fdIYKMEMJMUMJLkUGLUUDKEEHKEUFJ0RFW2+gq7RmeYVleYVleIVkdoZldoZjdYWNmaMIZDnWAAAAR0lEQVQIHWNgYGQCAWYWVgY2dg5OLm4eXj5+BgFBIWERUTFecQkGSSlpGVk5eQVFCQYlZRVVNXUNTUUtBm0dHV09fX0DQyMAdocFpbQkwGsAAAAASUVORK5CYII=
---

When it comes to managing Terraform state on AWS, it often feels like a chicken-and-egg problem. While Terraform allows you to define and deploy your infrastructure as code, configuring the remote backend can present a challenge. There are various methods to achieve this goal, each with its unique nuances and complexities.

Now, imagine you’re just beginning your'e getting started with Terraform, and you’ve chosen to utilize an S3 bucket and DynamoDB table for efficient state management. Typically, you’d define your backend configuration like this:

```hcl
terraform {
  backend "s3" {
    bucket         = "tf-remote-bucket"
    key            = "tf-remote-bucket/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-lock-table"
  }
}
```
  {: .nolineno }

However, it makes sense to set up the supporting infrastructure for your S3 bucket, IAM (Identity and Access Management) groups, and policies with Terraform. The real challenge arises when you want to configure your Terraform backend using Terraform itself while ensuring that your backend state remains tracked by Terraform. It’s akin to solving a nested dolls problem within your infrastructure management process.

The post provides a practical solution to this conundrum. Deploying AWS backend resources using a bash script, enables you to establish a robust and automated infrastructure management workflow. Using this approach, you can simplify the process, and significantly speed up the initialization of your infrastructure with Terraform on a remote state.

## Objectives

- **Prepare AWS Environment:** Ensure your local development environment has AWS CLI, Terraform CLI, and essential tools. Organize your project by creating dedicated folders for AWS bash scripts and Terraform configurations, including a primary configuration file.
- **Create Custom AWS S3 Policy:** Establish a custom AWS S3 policy to grant Terraform permissions for secure state file management. The policy template offers flexibility to adapt to your AWS environment.
- **Automate Terraform Backend Setup:** Automate the creation of AWS resources required for Terraform’s remote backend using a Bash script. This simplifies IAM user, S3 bucket, DynamoDB table, and policy setup for smooth infrastructure provisioning.
- **Set Up Terraform Backend with AWS S3 and DynamoDB:** Configure Terraform to manage its state using AWS S3 for storage and DynamoDB for state locking. Enhance your main.tf file with AWS provider details, version constraints, and backend configuration for secure state management.
- **Initialize Terraform Configuration:** After configuring the Terraform backend, run terraform init to prepare the environment. This command initializes providers, downloads plugins, and configures the backend, ensuring Terraform is ready to manage infrastructure resources.

## Solution Overview

**a) Bash Script**
- You use a Bash script to create these AWS backend resources. The Bash script contains the necessary AWS CLI commands to create the IAM user, S3 bucket, and DynamoDB table, as well as configure bucket policies.

**b) Execution Order**
- You execute the Bash script before configuring your Terraform backend in the main.tf file. By doing so, you ensure that the AWS backend resources are created before Terraform attempts to use them.

**c) Terraform Configuration**
- You have a Terraform configuration file (typically named main.tf) where you define your AWS backend resources, such as the S3 bucket for storing the Terraform state file and the DynamoDB table for state locking. These resources are specified as part of your Terraform configuration.

**d) Resource Creation**
- When the Bash script runs, it creates the IAM user, S3 bucket, and DynamoDB table with the specified configurations. It also applies the necessary bucket policy. These resources are created within your AWS account based on your Terraform configuration.

**e) Terraform State File**
- After the resources are created, Terraform is ready to use them as its backend. When you run terraform init, Terraform initializes the backend configuration as defined in your main.tf file. This includes setting up the S3 bucket and DynamoDB table as the backend for storing Terraform state. Terraform also generates its initial state file and stores it in the configured S3 bucket.

By following this sequence of steps, you ensure that your Terraform backend resources are created independently of Terraform using the Bash script. Terraform’s backend configuration is then set to use these pre-existing AWS resources. This approach guarantees that Terraform is aware of and can effectively manage its state using the specified AWS backend resources. Your Terraform backend configuration aligns seamlessly with the actual AWS resources you created, ensuring consistency and effective tracking.

## Prerequisites

To follow this tutorial, you will need:

- AWS account
- AWS CLI
- Terraform CLI installed.
- JQ

## Watch Tutorial

{% include embed/youtube.html id='-qTvkOolvQc' %}

## Read More

- [https://blog.digital.cloud](https://aws.plainenglish.io/setting-up-terraform-remote-backend-with-aws-using-a-bash-script-6549d8e62a6)