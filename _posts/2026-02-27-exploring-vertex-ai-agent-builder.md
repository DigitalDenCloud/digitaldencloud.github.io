---
title: Exploring Vertex AI Agent Builder. Writing My First Google Cloud Lecture
date: 2026-02-23 08:00:00 +0000
categories: [Google Cloud]
tags: [Google Cloud, Vertex AI, Agent Builder, Gemini, Grounding, ADK]
description: With my Google Cloud environment set up, I started exploring Vertex AI Agent Builder while writing Lecture 2 of my first Google Cloud course. This post documents what I found in Model Garden, Vertex AI Studio, grounding with Google Search, and the services that make up the agent building stack.
mermaid: true
image:
  path: /assets/img/headers/vertex-ai.webp
  lqip: data:image/webp;base64,UklGRj4AAABXRUJQVlA4IDIAAABwAwCdASoUABQAPxGCuVWsKKWjKAgBgCIJZwDNhBEcyPaJrAAA/u5yLgtZWvbSA4AAAA==
---

## Picking Up Where I Left Off

In [Part 1](https://docs.digitalden.cloud/posts/getting-started-with-google-cloud/){:target="_blank"}, I documented setting up my Google Cloud account for the first time. The project, the IAM roles, the 180 organisation policies, the 22 pre-enabled APIs. Foundation work.

Now I needed to actually look at what I'm building a course about. The course is called *Empowering Intelligence: Building Agentic Systems on Google Cloud*, and I'm starting with the Lecture *Google Cloud Services for Agentic AI*, which goes through each Google Cloud service that supports agent development and maps it to the agentic capabilities I defined in the previous lecture.

Writing the lecture and exploring the console happened at the same time. I'd open a service, see what was there, then check the Google Cloud documentation to fill in the gaps and verify what I was seeing. Coming from AWS, my instinct is to get hands on first and compare what I see to what I already know. The docs answer questions I already have, rather than teaching theory without context. This post documents that process.

---

## Chapter 1: Model Garden

Model Garden was my first stop. It's Vertex AI's model library, and the scale is immediately obvious. The sidebar organises models into three collections: 125 Google models, 50 partner models, and 18 self-deploy partner models.

What caught my attention was the task-based filtering. You can filter by what you want to do, thats text generation (88 models), image generation (38), multimodal generation (26), translation (43), video generation (16). In Bedrock, the model catalog (219 models at the time of writing) is organised by provider. You pick a provider, then a model. Model Garden gives you a second axis, what task are you solving.

The provider list includes names I recognise from Bedrock. Anthropic (9 models), Meta (21), Mistral (9), and providers I haven't seen on AWS: Salesforce, MongoDB, NVIDIA, CSM, Qodo. The fact that both clouds offer Claude and Llama means the model itself isn't the differentiator. The platform around it is.

One feature I liked include 116 models support one-click deployment, and 41 integrate directly with Vertex AI Studio. Model Garden isn't just a catalog, it connects to the rest of the platform.

---

## Chapter 2: Vertex AI Studio. My First Prompt on Google Cloud

Vertex AI Studio is the prompt testing interface. On first launch, the landing page presents four quick-start options: Gemini 3.1 Pro, Nano Banana Pro (image generation), Veo 3.1 (video generation), and **Build an app (Preview)**, which generates an application from a prompt or screenshot.

The prompt bar includes built-in **Tools** and **Agents** controls. In contrast to the Bedrock Playground, where these are configured in separate sections, Vertex AI Studio integrates them directly into the prompt interface.

I selected **Gemini 3.1 Pro** and asked:

*"What are the core components of an AI agent?"*

The response included a *“Thought for 8 seconds”* indicator, followed by a visible reasoning trace showing how the model structured its answer:

### Gemini Thinking Trace

1. **Analyzing User Intent**  
2. **Defining Agent Components**  
3. **Refining the Framework**  
4. **Synthesizing the Response**

---

### Components Identified

- **Brain** → reasoning and decision-making  
- **Memory** → storing context and past interactions  
- **Planning** → breaking tasks into steps  
- **Tools** → interacting with external systems  

This closely aligns with the agent capabilities introduced in Lecture 1, although the mapping is not exact.

### Preview and Code

The interface has two modes at the top: **Preview** and **Code**. Preview is the interactive chat. Code generates the equivalent API call. I clicked Code and saw a ready-to-use Python script:

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True)
model = "gemini-3.1-pro-preview"
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text(text="What are the core components of an AI agent?")]
    ),
]
tools = [
    types.Tool(google_search=types.GoogleSearch()),
]
```

Two things stood out. First, the SDK is `google-genai`, compared to `boto3` for AWS. Different syntax, same concept. Second, **Google Search is included as a tool by default**. The playground added grounding automatically. In Bedrock, you'd need to configure a knowledge base or build a Lambda action group to add search capability. Google integrates it directly.

The Code view also has a **Deploy** button and an **Open notebook** option for Colab. Bedrock doesn't offer one-click deployment from the playground.

---

## Chapter 3: Grounding. The Feature That Surprised Me

Grounding was the standout discovery. I knew about it from my research for Lecture 1, but seeing it work made it real.

In the Vertex AI Studio settings, grounding is enabled by default with two options:

- **Google Search** for public web data
- **Your data** for RAG using Vertex AI Search or RAG Engine

I tested it with a simple prompt: *"What is the current weather in London?"*

**With grounding off:** Gemini refused to answer. It said it has no access to real-time data and suggested I check a weather app.

**With grounding on:** Gemini returned live temperature (53-55°F / 12-13°C), humidity (72-80%), forecast conditions, and cited sources from weather sites.

Same model, same prompt. Completely different results. Without grounding, Gemini can't answer. With grounding, it pulls live data and cites its sources. This is exactly what I covered in Lecture 1 about hallucinations. Grounding didn't just improve the answer. It made the answer possible.

In AWS, there's no equivalent to this. Bedrock has Knowledge Bases for enterprise data grounding (similar to Vertex AI Search), but there's no "toggle on web search" feature built into the model call. On AWS, you'd need to build that yourself with a Lambda action group that calls a search API. On Google Cloud, it's one line in the API: `types.Tool(google_search=types.GoogleSearch())`.

---

## Chapter 4: Trying to Use Claude on Google Cloud

I wanted to test Claude Opus 4.6 with grounding enabled. Model Garden had it listed, and I could see the model card with all the details. I clicked Enable, agreed to the terms, and then hit a wall:

> *Action required: Choose different billing account. This product cannot be purchased using a billing account currently associated with a free trial.*

Partner models like Claude are offered as managed APIs (Model as a Service) through Model Garden. They require accepting the publisher's terms and using a paid billing account. The free trial can't be used for partner models. Pricing for Claude Opus 4.6 on Vertex AI is $5.00 per 1M input tokens and $25.00 per 1M output tokens for context windows up to 200K tokens, with higher rates for longer contexts and separate pricing for batch and prompt caching.

This is different from how Bedrock handles model access. In Bedrock, many third‑party serverless models are effectively ‘available by default’—and on first invocation Bedrock can auto‑initiate the AWS Marketplace subscription/enablement in the background (given Marketplace permissions and prerequisites). On Google Cloud, partner models require accepting publisher terms and enabling/deploying via Model Garden before use.

I went back to Gemini. For learning and course development, it's the right choice anyway. It's free trial eligible, grounding works the same way, and it's the primary model for the course. When I need Claude, I use it directly through claude.ai rather than through a cloud provider.

---

## Chapter 5: Agent Engine and Cloud Run Functions

Two more services I checked in the console.

1. **Agent Engine** is where deployed agents live. My page was empty because I haven't deployed anything yet. The columns show Name, Resource name, Identity, Telemetry collection, Created, and Framework. That last column is interesting. Agent Engine supports agents built with ADK, LangChain, LangGraph, AG2, and LlamaIndex. You're not locked into one framework.

2. **Cloud Run functions** (formerly Cloud Functions) is the serverless compute for tool execution. When I searched for Cloud Functions, the console took me to Cloud Run instead. Google merged the two services in 2024. Functions, containers, and source code all deploy from the same console now. The top bar shows three options: "Deploy container", "Connect repo", "Write a function". In AWS, Lambda (functions) and Fargate (containers) are separate services. Google unified them.

---

## What I've Learned Writing Lecture 2

- **Model Garden is a marketplace, not just a catalog.**  
  Task-based filtering, one-click deployment, and notebook integration. Bedrock’s model catalog is simpler and more direct.

- **Vertex AI Studio integrates tools into the prompt interface.**  
  Search and agents are configured within the same view. There is no need to switch between console sections.

- **Grounding with Google Search is a key differentiator.**  
  A single toggle enables access to live web data with citations. There is no direct equivalent in Bedrock without building it.

- **Partner models require a paid account.**  
  Claude and other marketplace models are not included in the free trial. Gemini models are available within the free credit.

- **Cloud Functions are integrated into Cloud Run.**  
  Functions and containers are deployed through the same service. AWS separates Lambda and Fargate.

- **Agent Engine is framework-agnostic.**  
  Supports LangChain, LangGraph, AG2, and LlamaIndex. Not limited to ADK.

---

## What's Next

Lecture 2 is written. Since then, I've also written and verified Lectures 3, 4, and 5 by going back into the console and checking everything against the Google Cloud documentation. That verification process uncovered a few things I didn't expect, like Agent Designer exporting directly to ADK code, pre-built MCP servers for BigQuery and Firestore on the Tools page, and GenAI Evaluation sitting as its own service rather than inside Agent Engine.

I also noticed a YouTube Analytics connector in the Integration Connectors list. I have a YouTube channel. The next post will cover the verification process, what I discovered, and building my first agent on Google Cloud, one that connects to my own YouTube Analytics data.

---

*This is Part 2 of a series documenting my journey into Google Cloud as an AWS engineer. [Part 1](https://docs.digitalden.cloud/posts/getting-started-with-google-cloud/) covered account setup, IAM, and first impressions. Part 3 will cover verifying the architecture and building my first agent.*