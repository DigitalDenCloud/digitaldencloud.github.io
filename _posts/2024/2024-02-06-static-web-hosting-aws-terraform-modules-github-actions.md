---
title: "Static Web Hosting on AWS Series: Terraform Modules & GitHub Actions"
date: 2024-02-06 08:00:00 - 0500
categories: [AWS, Terraform]
tags: [terraform, aws, s3, dynamodb, state management, acm, route 53, cloudfront, github actions, devops]
image:
  path: /assets/img/headers/static-web-hosting.webp
  lqip: data:image/webp;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAGCAMAAADNLv/0AAAArlBMVEX6+Pz5+Pv19Pb6+fv7+/zt7/j39/f6+/z39/j9+vv5+fn9/Pzi1fH18Ob29vD49/329vzy9vXs8env6vfX0eHs5+H08vH4+Pr49/r09/fy9fL08vju7fP17+D28er35ebr6+T08/Ds7Pbc3N/38tz17937/P789PX15OT9/f38/P3g4eP18uv49O37+/zr5/Pq4vHq7Ovx8+3m5+j38+n6+PT9/v749vv3+Pf5+fgfQaB1AAAADHRSTlPrueu567nrueu567kHUO/PAAAASUlEQVQIHQXBAwKAQBAAwM027rJt1/8/1gyArKiabpgWAaTtuAh7fkABHUYxStIsZ4Atyqpu2q7ngB/GaV7WbRdAPM7rxs/7ST+sOQals5rUoAAAAABJRU5ErkJggg==
---

## Introduction

Immerse yourself in a detailed, six-part tutorial series that simplifies the process of automating cloud infrastructure deployment and website hosting with Terraform, GitHub Actions, and AWS. The series is designed to walk you through a progressive build-up of your web hosting environment, showcasing advanced DevOps techniques for setting up a secure, scalable, and efficient web hosting environment.

In six parts, you'll learn how to write efficient Terraform code, exploring variables, outputs, and modules. Each of the four key modules builds on the fundamentals of web infrastructure management and demonstrates their interconnectedness to boost your infrastructure. Modules include:

- S3 Remote Backend
- DNS settings with Route 53 & AWS ACM
- S3 Website Hosting
- CloudFront distribution

You'll learn how to implement a CI/CD pipeline using GitHub Actions. You'll create a workflow with the following jobs:

- Deploying your infrastructure with Terraform
- Syncing your files to an S3 bucket
- Invalidating your CloudFront cache

> Whenever you make changes to your website, simply update your content and commit the changes to your repository. The CI/CD pipeline, integrated into this Terraform-managed infrastructure, automatically kicks in. It syncs the new content to the S3 bucket and triggers a CloudFront cache invalidation, ensuring that your website reflects the latest updates promptly.
{: .prompt-info }

## Project Steps Overview

1. **Initialize GitHub Repository and Local Setup:**

   - Set up a development environment with Visual Studio Code after cloning the GitHub repository to my local workstation.

2. **Terraform Remote Backend Setup:**

   - Configured a remote backend on AWS using a custom Terraform module, involving resources like an IAM user, S3 bucket, and DynamoDB table.

3. **CI/CD Pipeline with GitHub Actions:**

   - Automated infrastructure deployment through a GitHub Actions pipeline, triggered by git push events.

4. **DNS and SSL Certificate Management Module:**

   - Managed DNS with AWS Route 53 and automated SSL certificate provisioning with AWS Certificate Manager.

5. **AWS S3 Static Website Hosting Module:**

   - Set up an AWS S3 bucket to serve a static website, managing the bucket creation, versioning, and public access configurations.

6. **CI/CD Pipeline Enhancement for S3 Sync:**

   - Updated the CI/CD pipeline to include a job for synchronizing website files to the S3 bucket.

7. **AWS CloudFront Distribution Module for S3:**

   - Created a CloudFront distribution for the S3 bucket to deliver content globally, with optimized distribution settings.

8. **CI/CD Pipeline Enhancement for CloudFront Cache Invalidation:**

   - Enhanced the pipeline to invalidate the CloudFront cache whenever the S3 bucket is synchronized.

9. **Live Website Update:**
   - Commits to the repository trigger the automated pipeline, syncing changes to the S3 bucket and invalidating the CloudFront cache, reflecting updates on the live website.

![Pipeline](/assets/img/posts/pipeline.webp)
_CI/CD Pipeline_

## AWS Well-Architected Framework Alignment

This project aligns with the AWS Well-Architected Framework, ensuring best practices across the following pillars:

- **Operational Excellence:** CI/CD pipelines facilitate automated deployments and iterative improvements.
- **Security:** AWS IAM, Certificate Manager, and S3 bucket policies provide secure access management and data encryption.
- **Reliability:** AWS S3, DynamoDB, and Route 53 enhance system availability and fault tolerance.
- **Performance Efficiency:** AWS CloudFront ensures efficient content delivery with low latency.
- **Cost Optimization:** Precise resource provisioning through Terraform minimizes costs.
- **Sustainability:** Automation and efficient AWS services reduce the environmental impact.

## Tech Stack

- Terraform
- GitHub Actions
- AWS
  - IAM 
  - S3 
  - DynamoDB
  - ACM 
  - Route 53 
  - CloudFront
  
## The Series
- Watch The Intro & Framework Overview
{% include embed/youtube.html id='sBPo_60Mzxc' %}

- [The 6 Part Playlist](https://www.youtube.com/playlist?list=PLfmMgg_VrrlAz4s0UxLCdgZlcw2iCqVrD)

## GitHub
- [GitHub Codebase](https://github.com/digitalden3/AWS-Static-Web-Hosting-Series-Codebase)
  -  The central hub for all Terraform module templates and GitHub Action YAML files needed to complete this extensive six-part project.
- [GitHub](https://github.com/digitalden3/Static-Web-Hosting-on-AWS-Terraform-Modules-GitHub-Actions)
  - The Complete GitHub Repository for the full project and all the complete code for the series.