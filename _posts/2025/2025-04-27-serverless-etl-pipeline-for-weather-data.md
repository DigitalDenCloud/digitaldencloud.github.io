---
title: "Serverless ETL Pipeline for Weather Data"
date: 2025-04-23 08:00:00 - 0500
mermaid: true
categories: [AWS, Data Engineering]
tags: [AWS, Serverless, ETL, AWS Lambda, Amazon Data Firehose, Amazon S3, AWS Glue, Amazon Aurora, AWS Secrets Manager, VPC Endpoints, Amazon EventBridge, Amazon Athena]
image: 
  path: /assets/img/headers/serverless-etl.webp
  lqip: data:image/webp;base64,UklGRiYBAABXRUJQVlA4IBoBAADQBgCdASoyABwAPsFMn0unpCKht/qoAPAYCWYAyhUALsAI9VW1Bwwjml3JF8ZTMiQ1kAFeoX29KF66Tkqo0qAA/vd5Yagh2hMl/m7b7aRx2yhj9H2XknUCaWpJZ7q4WZaSB17KLuZfBLREBp+jai6yMDZZFRV/DNP/HgvHaKhF89V4EpwYUUDh3x4L7asgGPo/Rkqu4N2LyDOY/CWGyc7il3GJ5vKksIA10CyXT+NqmDMJCh+MJbEJ/Yvma5DdKgq64QPIYuaCcU41sNtM6fx0Yy/Q5/1Hq4CIlh5l0dY57dQMc5dgbL1e0DSybIOraXDiOYRiRC71Ik38KTEbmCuSA+Y8AdE/pMhg76ZE9PV1IMccOxgGrctAAAA=
---

This solution builds a serverless data pipeline that collects, processes, and analyzes global weather data using:
- OpenWeatherMap API as the data source
- Lambda function for data ingestion
- Kinesis Data Firehose for streaming
- S3 for data lake storage with time-based partitioning
- AWS Glue Crawler & Data Catalog for automated schema discovery
- Amazon Athena for SQL query capabilities against raw data
- VPC Endpoints for secure data access
- AWS Secrets Manager for credential management
- AWS Glue ETL for data transformation
- Aurora Serverless v2 for structured data storage and analysis
- EventBridge Rules for workflow orchestration

The pipeline delivers a complete solution with minimal operational overhead, providing both raw data in S3 and structured data in Aurora for comprehensive weather insights.

## Intended audience  
This video is designed for beginners interested in AWS data engineering seeking hands-on experience with ETL pipelines. It's suitable for those preparing for the AWS Data Engineering certification or anyone wanting to develop practical cloud data skills through a real-world project.

## Learning Objectives    
- Create a Lambda function to process weather data from the OpenWeatherMap API
- Set up Kinesis Firehose to store data in S3 with dynamic partitioning
- Implement AWS Secrets Manager for secure credential management
- Configure a Glue Crawler to catalog the S3 data
- Set up Amazon Athena for querying the raw data via the Glue Data Catalog
- Deploy Amazon Aurora Serverless v2 database to store transformed data
- Establish VPC endpoints for S3 and Secrets Manager for enhanced security
- Build a Glue ETL pipeline using visual ETL and script mode for data transformation
- Configure automated triggers using EventBridge for Lambda and Glue triggers for the crawler and ETL job
- Run SQL queries via Aurora's built-in Query Editor

This hands-on demonstration will show you how to deploy directly from the command line while Elastic Beanstalk automatically handles the infrastructure provisioning and management. 

## Get Started
[Solution Overview](https://www.youtube.com/watch?v=aKEC8z9_UA4&t=1s&ab_channel=Hands-OnWithDigitalDen){:target="_blank"}