---
title: Getting Hands-On With Vertex AI Agent Builder
date: 2026-03-04 08:00:00 +0000
categories: [Google Cloud]
tags: [Google Cloud, Vertex AI, Agent Builder, ADK, Agent Garden, MCP]
description: After writing five lectures on Vertex AI Agent Builder, I went into the console to get hands-on with everything I'd been teaching. This post documents what I found, what I learned, and what I'm building next.
---

## Theory First, Then Hands-On

This is how I've always learned. When I started with AWS, I'd study the concepts, write about them, then open the console and build. That's why I have a [YouTube channel](https://www.youtube.com/@DigitalDenCloud){:target="_blank"}. The theory gives you the map. The console gives you the territory. They're not the same thing, and the gaps between them are where the real learning happens.

I've now written all five lectures for my Vertex AI Agent Builder course. The services, the architecture, the use cases, the getting started resources. In [Part 1](https://docs.digitalden.cloud/posts/getting-started-with-google-cloud/){:target="_blank"} I set up my Google Cloud account. In [Part 2](https://docs.digitalden.cloud/posts/exploring-vertex-ai-agent-builder/){:target="_blank"} I explored the core services while writing Lecture 2. Now it's time to go deeper. Open every feature I've been teaching about, see how it actually works, and fill in the details that only come from hands-on experience.

---

## Chapter 1: Agent Designer and the ADK Export

In Lecture 3, I taught that Agent Designer provides a low-code canvas for designing agent logic visually, with the ability to export to ADK for further development. I wanted to see that export in action.

I opened Agent Designer and created a basic agent. The configuration page let me set a name, description, instructions, and select a Gemini model. Under tools, Google Search and URL context were enabled by default. I could also add Vertex AI Search data stores and MCP servers.

The Preview tab opened a live chat interface where I could test the agent immediately. I said hello and it responded. A working agent from a few fields and default settings.

Then I clicked **Get code**. It generated a complete ADK Python script. But the structure surprised me. I'd configured one agent with two tools. The exported code created three agents:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

my_agent_google_search_agent = LlmAgent(
  name='My_Agent_google_search_agent',
  model='gemini-2.5-flash',
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[GoogleSearchTool()],
)

my_agent_url_context_agent = LlmAgent(
  name='My_Agent_url_context_agent',
  model='gemini-2.5-flash',
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[url_context],
)

root_agent = LlmAgent(
  name='My_Agent',
  model='gemini-2.5-flash',
  sub_agents=[],
  instruction='',
  tools=[
    agent_tool.AgentTool(agent=my_agent_google_search_agent),
    agent_tool.AgentTool(agent=my_agent_url_context_agent)
  ],
)
```

A root agent with two sub-agents, one for each tool. Google Search and URL context are each wrapped as their own agent using `AgentTool`. That's a multi-agent pattern generated automatically from what looked like a simple single-agent setup. This is the kind of detail you only discover by clicking the button.

---

## Chapter 2: Pre-Built MCP Servers

In Lecture 5, I taught about MCP (Model Context Protocol) as an open standard for connecting agents to external systems. I described it conceptually. Then I went to **Vertex AI → Agent Builder → Tools** and found it already built into the console.

After enabling the Cloud API Registry API, a table appeared with pre-built MCP servers for Google Cloud services:

| MCP Server | Service |
|---|---|
| bigtableadmin.googleapis.com | Bigtable Admin |
| firestore.googleapis.com | Firestore |
| compute.googleapis.com | Compute Engine |
| container.googleapis.com | Google Kubernetes Engine |
| bigquery.googleapis.com | BigQuery |
| discoveryengine.googleapis.com | Discovery Engine |
| mapstools.googleapis.com | Maps Grounding Lite |

All disabled by default, but one click to enable. I'd taught MCP as a concept. Here it was, pre-configured for major Google Cloud services. Enable the BigQuery MCP server and your agent can query BigQuery. Enable Firestore and your agent can read and write documents. No custom integration code needed.

In AWS, if you want a Bedrock agent to interact with AWS services, you build custom Lambda action groups for each one. Google is providing these connections out of the box.

---

## Chapter 3: Agent Garden

I opened **Agent Garden** in the console expecting a few sample agents. The page had significantly more than that.

The description says "Pre-built, customisable blueprints with source code, configuration files and best practice examples." The samples include working agents for Data Science, RAG, Financial Advisor, Marketing Agency, Customer Service, Deep Search, Academic Research, Software Bug Assistant, and Travel Concierge. All built with ADK and Python.

The left sidebar has filter categories that reflect how you'd actually think about building agents:

- **Tools & Integrations:** Google Search, Agent tool, Custom tool, Function tool
- **Core AI Capabilities:** NL2SQL, Multimodal, Human-in-the-Loop, PDF parsing, RAG
- **Architecture & Design Patterns:** Multi-agent, Single-agent, Dynamic instructions
- **Use Cases:** Bug Tracking, IT Support Tool, Business Intelligence, E-commerce, Shopping assistant

The use case tags map directly to the patterns I covered in Lecture 4. Customer Service is the support agent pattern. Data Science and RAG are enterprise Q&A. Deep Search is research and brief writing. In the lecture, these are descriptions. In Agent Garden, they're working code you can deploy and adapt.

In Lecture 5, I described Agent Garden as "a collection of ready-to-use samples and tools." Having seen it, "customisable blueprints with source code" is more accurate and more useful.

---

## Chapter 4: GenAI Evaluation

In Lecture 3, I'd written that Agent Engine "supports evaluation capabilities (including an integrated Gen AI evaluation service)." When I looked at the Vertex AI sidebar, GenAI Evaluation is its own service at the same level as Model Garden and Vertex AI Studio. It's not inside Agent Engine.

The service lets you build evaluation datasets, run prompts through models, and measure quality using adaptive rubrics (tailored pass/fail tests for each prompt), static rubrics, computation-based metrics, or custom Python functions. It also supports agent evaluation with agent-specific metrics like traces and response quality.

The distinction matters for how you think about the architecture. Agent Engine handles the runtime: deployment, scaling, sessions, memory. GenAI Evaluation is a separate tool you use alongside it to measure quality before and after deployment. I updated Lectures 3 and 4 to reference it correctly.

This is exactly the kind of thing that changes when you move from reading documentation to navigating the actual console. The docs mention evaluation in the context of Agent Engine. The console shows you it's a standalone service.

---

## Chapter 5: Sessions and Memory Bank

I checked the Sessions and Memory Bank descriptions from Lecture 3 against the Google Cloud documentation to make sure the details were right.

**Sessions** maintain interaction history within a single conversation. Each message and action, including function calls, is recorded as events. The docs also describe **State**, which holds temporary data relevant only during the current conversation. When you deploy an ADK agent to Agent Engine, session management is handled automatically.

**Memory Bank** is a separate service that works across sessions. What stood out in the docs was how it works. Memory Bank uses an LLM to automatically extract and consolidate memories from conversations. It's not storing raw conversation logs. It's generating meaningful facts about the user that evolve as new information comes in. A customer service agent could remember key details from previous support tickets without the user repeating themselves.

The docs also flag memory poisoning as a security risk, where false information gets stored and affects future sessions. Google recommends Model Armor, adversarial testing, and sandbox execution as mitigations. Good to know for when I build something that uses long-term memory.

---

## Chapter 6: Integration Connectors and a YouTube Discovery

In Lecture 5, I mentioned "100+ pre-built connectors for connecting to enterprise systems." I pulled up the full list in the docs: roughly 35 Google service connectors and 120+ third-party connectors covering Salesforce, SAP, ServiceNow, Jira, Slack, and dozens more.

Scrolling through the Google service connectors, I spotted **YouTube Analytics**. I have a [YouTube channel](https://www.youtube.com/@DigitalDenCloud){:target="_blank"}. An agent that connects to my own YouTube Analytics data and answers questions about video performance, subscriber growth, and watch time. That's not a hypothetical use case. That's something I can build with my own data.

---

## Refinements From Getting Hands-On

Two things I refined in the lectures after the console experience:

1. **GenAI Evaluation location.** I originally placed it inside Agent Engine. It's a separate Vertex AI service. Updated Lectures 3 and 4 to reflect the correct architecture.

2. **ReAct naming.** In Lecture 5, I'd written "React" when describing Agent Starter Pack templates. The correct term is "ReAct" (Reasoning and Acting), a pattern where the agent thinks step by step and decides which tools to use. Not the JavaScript framework.

Small refinements. The kind you only catch when you go from writing about something to working with it directly.

---

## What's Next

Five lectures written. Every feature explored in the console. Documentation verified. Now I build.

The YouTube Analytics connector gave me an idea for my first agent on Google Cloud: one that connects to my own channel data and answers questions about video performance. It's a real use case with real data, and it uses the concepts I've been teaching: tools, connectors, grounding, and Agent Engine.

That build will be the final chapter of this post.

---

*This is Part 3 of a series documenting my journey into Google Cloud as an AWS engineer. [Part 1](https://docs.digitalden.cloud/posts/getting-started-with-google-cloud/) covered account setup and first impressions. [Part 2](https://docs.digitalden.cloud/posts/exploring-vertex-ai-agent-builder/) covered exploring services and writing Lecture 2.*
