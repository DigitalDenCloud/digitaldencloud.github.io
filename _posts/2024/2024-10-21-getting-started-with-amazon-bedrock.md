---
title: "Getting Started With Amazon Bedrock"
date: 2024-10-21 08:00:00 - 0500
categories: [aws, genai]
tags: [aws, amazon bedrock, generative ai, foundation models, aws cli, boto3, aws cloudshell, inference,]
image: 
  path: /assets/img/headers/amazon-bedrock2.webp
  lqip: data:image/webp;base64,UklGRlYAAABXRUJQVlA4IEoAAABwAwCdASoUAAwAPzmGuVOvKSWisAgB4CcJZQDImBtPgh4gCEAA/udAwu7682t9feJZUv/0SeNWTlH0FKSBvQBRtusP3xfYykwAAA==
---

In this lesson, you will explore Amazon Bedrock, a fully managed service in AWS's generative AI layer. You will learn about its core concepts, capabilities, and how to interact with it using the Bedrock Playground, AWS CLI, and SDKs.

You will be guided through setting up model access and using the Bedrock console. In the playground, you will experiment with inference, prompts, and parameters to better understand AI model interactions.

> Through hands-on exercises, you will learn how to invoke Bedrock models using CloudShell with AWS CLI and Python (Boto3), gaining practical experience to integrate AI services into your cloud-based applications.
{: .prompt-tip }


## Learning Objectives
By the end of this lesson, you will have an understanding of Amazon Bedrock including:
- Understand foundation models and Amazon Bedrock's unified API.
- Set up model access and explore the Bedrock console.
- Learn about inference and AI model interactions.
- Experiment with prompts and inference parameters in the Bedrock playground.
- Invoke Bedrock models using CloudShell with AWS CLI and Python (Boto3).

## Who should attend this lesson?
This lesson is designed for you if you are just getting started with Amazon Bedrock, whether you are a cloud practitioner, developer, data scientist, or someone interested in AWS’s generative AI capabilities.

## Get Started
{% include embed/youtube.html id='YsnipGh22Gw' %}

## Code Examples for Amazon Bedrock
To help you get hands-on with Amazon Bedrock, here are two practical examples: one using the AWS CLI and another using the Python SDK (Boto3). These examples will show you how to invoke a Bedrock model and customize the AI-generated outputs based on your prompts and parameters.

### CLI Example
You can invoke a model using the AWS CLI with the following command:

```bash
aws bedrock-runtime invoke-model \
    --model-id anthropic.claude-v2 \
    --body '{"prompt": "\n\nHuman: story of two dogs\n\nAssistant:", "max_tokens_to_sample" : 300}' \
    --cli-binary-format raw-in-base64-out \
    invoke-model-output.txt
```
{: .nolineno }

This command can also be found in the [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-invoke.html){:target="_blank"}

### Python SDK (Boto3) Example
You can also use the AWS SDK for Python (Boto3) to programmatically invoke Bedrock models. Here's an example:

```python
import boto3
import json

# Create a Bedrock runtime client
client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Prepare request body
request_body = {
    "prompt": "Describe the purpose of a 'hello world' program in one line.",
    "max_tokens": 50,
    "temperature": 0.5
}

# Invoke the model
response = client.invoke_model(
    modelId='anthropic.claude-v2',
    body=json.dumps(request_body)
)

# Process and print the response
response_body = json.loads(response['body'])
print(response_body['completions'][0]['text'])
```
{: .nolineno }

This example can also be found in the [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModel_AnthropicClaude_section.html){:target="_blank"}