---
title: "Adding Cost Protection to My Bedrock Agent"
date: 2026-01-11 08:00:00 -0500
categories: [AWS, Generative AI]
tags: [AWS, Generative AI, Bedrock Agents, Serverless, Amazon Bedrock, Amazon API Gateway, Cost Optimization, Security]
description: "Protect public API Gateway endpoints from abuse using usage plans and budget alerts. This post covers practical strategies to limit requests, monitor costs, and explores when AWS WAF or authentication might be needed."
image:
  path: /assets/img/headers/api-gateway-protection.webp
  lqip: data:image/webp;base64,UklGRmQAAABXRUJQVlA4IFgAAAAwBACdASoUABQAPxFws1MsJaSisBgIAYAiCWUAx+WJ/hgaqYDjjc56pwAA/uwSHwgMm1AcEzHDjbMnpu7bX4NYC9pe4/bUTIZAlO21u4NTx+HG+Ch80AAA
---

## The Problem

I recorded a demo video for my [AWS News Search agent](https://awsnews.digitalden.cloud){:target="_blank"} and realised my API Gateway endpoint was visible on screen. My first thought was to regenerate the URL so the one in the video no longer worked.

Then I realised it doesn't matter.

Anyone can open browser dev tools, go to the Network tab, and see the exact endpoint the frontend is calling. Hiding the URL in a video provides no real protection. If someone wants the endpoint, they can get it in seconds.

The actual risk is cost. Every request to the API invokes a Lambda function, which calls a Bedrock agent. Bedrock charges per token. If someone decides to spam the endpoint, my AWS bill goes up.

![Architecture Diagram](/assets/img/posts/aws-bill.webp){: .w-50 .rounded-10 .shadow }

## Protection Options

Rather than trying to hide the endpoint, focus on limiting what can be done with it.

### Amazon API Gateway Usage Plans

API Gateway usage plans let you set throttling limits and quotas. You can restrict requests per second and cap the total number of requests per day or month.

For a demo project, a low daily quota works well. Set it to 100-500 requests per day. That's enough for legitimate use but prevents someone from running thousands of requests overnight.

To create a usage plan:

1. Open the API Gateway console
2. Select **Usage Plans** from the navigation pane
3. Select **Create usage plan**

Configure the usage plan details:

- **Name**: `aws-news-agent-plan`
- **Throttling**: Enabled
  - **Rate**: `1` (requests per second)
  - **Burst**: `5` (allows short spikes)
- **Quota**: Enabled
  - **Requests**: `100`
  - **Period**: `Per day`

Create the usage plan.

#### Associate the API Stage

After creating the plan, associate it with your API:

1. In the usage plan details, select **Add Stage**
2. Select your API (`aws-news-agent-api`)
3. Select the stage (`prod`)
4. Select **Add to usage plan**

#### Create an API Key

An API key is a string that API Gateway generates. Clients include it in requests to identify themselves. The key links requests to your usage plan, which enforces the throttling and quota limits.

1. In the API Gateway console, select **API Keys** from the navigation pane
2. Select **Create API key**
3. Enter a name (e.g. `aws-news-agent-key`)
4. Select **Save**

Copy the API key value. You will need it for the frontend.

> The API key is not a security mechanism on its own. Anyone with the key can use it. The protection comes from the usage plan limits attached to it.
{: .prompt-info }

#### Attach the Key to the Usage Plan

1. Open your usage plan (`aws-news-agent-plan`)
2. Select the **Associated API keys** tab
3. Select **Add API key**
4. Select the key you created
5. Select **Add API key**

#### Require the API Key on the Method

1. In the API Gateway console, select your API
2. Select the `/agent` resource and the `POST` method
3. Select the **Method request** tab
4. Select **Edit**
5. Select the **API key required** checkbox
6. Select **Save**
7. Select **Deploy API** and deploy to the `prod` stage

> After enabling API key required, requests without a valid key receive a `403 Forbidden` response. Test your endpoint to confirm the key is working before updating the frontend.
{: .prompt-tip }

Test without the API key:
```bash
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/agent \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

Expected response:
```json
{"message":"Forbidden"}
```

Test with the API key:
```bash
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/agent \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-api-key-here" \
  -d '{"message": "What is Lambda?"}'
```

Expected response: A valid response from the agent.

#### Update the Frontend

The frontend now needs to include the API key in the `x-api-key` header:

```javascript
const response = await fetch(API_ENDPOINT, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'x-api-key': 'your-api-key-here'
    },
    body: JSON.stringify({ message: message, sessionId: sessionId })
});
```

The key is visible in browser dev tools, but combined with the usage plan quota, the damage from abuse is limited to 100 requests per day.

### AWS WAF

AWS WAF can block or rate limit requests based on IP address. If a single IP sends too many requests in a short period, WAF blocks that IP while allowing others through.

The difference between WAF and usage plans:

- **Usage plans** limit total requests across all users. One person could consume the entire quota.
- **WAF rate limiting** limits requests per IP. One abusive user gets blocked, but others can still access the API.

WAF matters when you have multiple users and want to protect against one bad actor consuming the entire quota. For a demo project where you're the main user, usage plans are sufficient.

#### Pricing

WAF pricing in eu-west-2 (London):

| Resource | Cost |
|----------|------|
| Web ACL | $5.00/month |
| Rule | $1.00/month per rule |
| Requests | $0.60 per 1 million |

A basic WAF setup with one rate limit rule costs around $6/month. For a low-traffic demo already protected by usage plans, the added cost doesn't justify the benefit.

For production APIs with multiple users or higher traffic, WAF provides an extra layer of protection worth considering.

### AWS Budgets

Even with usage plans, a budget alert provides a final safety net.

I already have a general budget that tracks overall AWS spend. For this project, I wanted a separate budget that only tracks costs from the AWS News agent.

My first thought was to filter by service - create a budget scoped to Amazon Bedrock and Amazon API Gateway. However, I use those services for other projects too. A service filter would include costs from everything, not just this agent.

The solution is to use cost allocation tags. Tag the resources in this project, then create a budget filtered by that tag.

#### Tag Your Resources

First, add a project tag to each resource:

- `search-aws-news` (Lambda)
- `invoke-agent` (Lambda)
- `aws-news-agent-api` (API Gateway)
- `aws-news-agent` (Bedrock agent)

For each resource:

1. Open the resource in the AWS console
2. Select the **Tags** tab
3. Add a tag:
   - **Key**: `Project`
   - **Value**: `aws-news-agent`

#### Activate Cost Allocation Tags

Cost allocation tags must be activated before they appear in Budgets:

1. Open the **Billing and Cost Management** console
2. Select **Cost allocation tags** from the navigation pane
3. Find your `Project` tag under **User-defined cost allocation tags**
4. Select the tag and select **Activate**

> Tags can take up to 24 hours to appear in cost allocation tags after tagging resources, and another 24 hours to appear in Budgets after activation. This is because AWS processes billing data in batches rather than real-time. Plan for up to 48 hours from tagging resources to being able to filter by tag in Budgets.
{: .prompt-info }

#### Create the Budget

1. Open the AWS Budgets console
2. Select **Create budget**
3. Select **Customize (advanced)**
4. Select **Cost budget** and select **Next**
5. Enter a budget name (e.g. `aws-news-agent-budget`)
6. For **Period**, select **Monthly**
7. For **Budget renewal type**, select **Recurring budget**
8. Set the budgeted amount (e.g. `$10`)
9. Under **Budget scope**, select **Filter specific AWS cost dimensions**
10. Select **Tag** from the dimension dropdown
11. Select your `Project` tag and the value `aws-news-agent`
12. Select **Next**
13. Set an alert threshold (e.g. 80% of budget)
14. Enter your email for notifications
15. Select **Create budget**

This tracks only the costs from resources tagged with this project, separate from your other AWS usage.

## Summary

Hiding API endpoints in videos or source code does not provide real protection. The endpoint is visible in browser network requests.

For this demo agent, I configured a usage plan with a daily quota of 100 requests and a budget alert filtered by project tag. The endpoint remains public, but abuse is limited and any unusual spending triggers a notification.

I explored AWS WAF as an option for rate limiting individual IP addresses, but for a low-traffic demo already protected by usage plans, the additional cost did not justify the benefit.

The protections covered in this post - usage plans, WAF, and budget alerts - limit and monitor requests but do not restrict who can access the API. For production APIs handling sensitive data, consider adding authentication:

- **Amazon Cognito** - Users sign in and receive a token. API Gateway validates the token before allowing requests.
- **IAM Authorization** - Requests must be signed with AWS credentials. Only users or roles you explicitly grant can call the API.
- **Lambda Authorizers** - Custom authentication logic to validate tokens from your own auth system.
- **Private APIs** - API Gateway can be configured as private, accessible only from within a VPC.

Usage plans and budget alerts provide sufficient protection for a demo. Authentication ensures only authorized users can access the API at all.