---
title: "High-Performance Text Analysis with HuggingFace GPT-2 on AWS Neuron with AWS Inferentia"
date: 2024-04-03 08:00:00 - 0500
categories: [QA Lessons]
tags: [aws, huggingface, neuron, pytorch, inferentia, inf2 instance, jupyter, deep learning, dlami]
image: 
  path: /assets/img/headers/neuron.webp
  lqip: data:image/webp;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAGCAMAAADNLv/0AAAAtFBMVEUQIEAQI08XKVAXKlEWLEoVLFAVLFIVLFMPJlENI0IRKTMNLEAILj4IKz4MLDQVMUMVMUYWMUUXM0caNDgoPj8tSUglREQlRkYnQEIwLSouLCgqKCQnJCElJiaqrK3f5ujW29/0+vyztLYwLzE3ODozMzYsLC8jJCa4uLP49/Dk4Nv///u6ubMiIhwvLignJyEkJB0fHxlVV3pwc55kaJF4eaRWWIIEBTIMDjsLDTkLDToKDDbGR/XUAAAASElEQVQIHQXBgwHAAAwAsM62bdv6/68lAAiK4QRJ0QywHC+IkqyoGuiGadmO6/kBhFGcpFlelBXUTdv1wzjNC6zbfpzX/bzfD5dLButtq3LQAAAAAElFTkSuQmCC
---

Welcome to QA's lesson where you’ll learn how to utilize the AWS deep learning AMI with the Neuron SDK and PyTorch on AWS Inferentia to compile and execute the HuggingFace GPT-2 model. 

This model, built within the PyTorch framework, excels in generating relevant and coherent text.  You'll see how feature extraction on Inf2 instances, powered by AWS Inferentia, accelerates deep learning inference with greater speed and efficiency compared to traditional CPU and GPU setups.

By the end of this lesson, you will have an understanding of how to:
- Request a service quota increase to launch Inferentia instances
- Launch an AWS Deep Learning AMI on an Inf2 instance
- Establish a secure SSH connection to the Inf2 instance
- Activate the Neuron environment, verify installation of key packages, and run Neuron tool commands
- Establish SSH tunneling for secure Jupyter Notebook access
- Launch and configure a Jupyter Notebook environment
- Optimize and deploy HuggingFace GPT-2 model on AWS Inf2 instances
- Conduct performance tests to compare inference times between CPU and Neuron-powered GPU instances

## GitHub Repository
To access the Python scripts and commands for compiling and executing the HuggingFace GPT-2 model, along with additional materials for this lesson, please visit our GitHub repository here:
- <a href="https://github.com/cloudacademy/high-performance-text-analysis-with-huggingface-gpt-2-on-aws-neuron-with-aws-inferentia/tree/main" target="_blank">Cloud Academy Repository</a>

## Intended Audience
This lesson has been created for data scientists, machine learning engineers, and developers with basic knowledge of machine learning.

## Prerequisites
To get the most out of this lesson you should have a familiarity with basic machine learning terms.

## Get Started
[High-Performance Text Analysis with HuggingFace GPT-2 on AWS Neuron with AWS Inferentia](https://cloudacademy.com/course/high-performance-text-analysis-huggingface-gpt-2-aws-neuron-aws-inferentia-5935/){:target="_blank"}