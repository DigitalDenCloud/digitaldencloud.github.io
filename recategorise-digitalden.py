#!/usr/bin/env python3
# Recategorise digitalden into four flat buckets: Builds, Lessons, Guides, Architecture.
# Google Cloud becomes a tag, not a category. Run from the digitalden repo root.
import re, glob, os

# filename -> new single category
MAP = {
    "2023-10-05-terraform-remote-backend-bash-script": "Guides",
    "2024-01-28-creating-terraform-module-s3-remote-backend": "Guides",
    "2024-02-18-particles-js-integration-tutorial-html5up-site-template": "Guides",
    "2024-02-21-building-and-running-serverless-applications-using-the-sam-cli": "Lessons",
    "2024-03-26-set-up-and-deploy-a-documentation-site-with-jekyll-and-chirpy-on-aws-cloud9": "Guides",
    "2024-04-03-high-performance-text-analysis-with-huggingface-gpt-2-on-aws-neuron-with-aws-inferentia": "Lessons",
    "2024-04-27-animating-the-cloud": "Guides",
    "2024-04-29-create-web-applications-using-aws-amplify": "Lessons",
    "2024-05-07-setting-up-adobe-creative-cloud-after-effects-on-aws-ec2-with-nvidia-gpus": "Guides",
    "2024-05-10-scaling-gpus-with-ec2-ultraclusters": "Lessons",
    "2024-05-22-aws-security-best-practices-for-developers": "Lessons",
    "2024-06-14-amazon-sagemaker-machine-learning-workflows": "Lessons",
    "2024-06-19-create-fast-loading-images-with-lqip-webp-in-your-jekyll-chirpy-site": "Guides",
    "2024-07-10-add-google-analytics-jekyll-chirpy-site": "Guides",
    "2024-07-16-running-deep-learning-workloads-with-the-aws-neuron-sdk": "Lessons",
    "2024-07-30-implementing-text-to-speech-with-amazon-polly": "Lessons",
    "2024-09-07-working-with-amazon-rekognition-for-video-and-image-analysis": "Lessons",
    "2024-09-12-build-genai-integrated-serverless-contact-forms-for-static-websites-with-aws-lambda-api-gateway-bedrock-and-ses": "Lessons",
    "2024-10-08-detecting-abnormal-operating-patterns-using-amazon-devops-guru": "Lessons",
    "2024-10-21-getting-started-with-amazon-bedrock": "Lessons",
    "2024-10-24-using-amazon-lex-to-create-conversational-ai-interfaces": "Lessons",
    "2024-10-29-monitoring-and-analyzing-data-quality-for-xgboost-churn-models-with-amazon-sagemaker-model-monitor": "Lessons",
    "2024-10-30-extracting-text-handwriting-and-layout-elements-using-amazon-textract": "Lessons",
    "2024-11-12-optimize-machine-learning-models-for-inference-with-sagemaker-neo": "Lessons",
    "2024-11-19-monitoring-model-inference-with-amazon-sagemaker": "Lessons",
    "2024-11-22-configuring-and-launching-hyperparameter-tuning-jobs-with-amazon-sageMaker-amt": "Lessons",
    "2025-01-16-training-and-fine-tuning-machine-learning-and-foundation-models-with-amazon-sagemaker": "Lessons",
    "2025-01-28-managing-database-access-permissions-in-aws": "Lessons",
    "2025-02-05-build-serverless-contact-forms-with-generative-ai": "Builds",
    "2025-04-23-deployment-orchestration-with-elastic-beanstalk": "Lessons",
    "2025-04-27-serverless-etl-pipeline-for-weather-data": "Builds",
    "2025-06-11-aws-relational-databases": "Lessons",
    "2025-07-21-aws-non-relational-databases": "Lessons",
    "2025-07-31-cost-and-sustainability-optimization-for-aws-storage-and-databases": "Lessons",
    "2025-11-05-automating-cost-and-sustainability-optimization-in-aws": "Lessons",
    "2025-12-12-fixing-rss-feed-limits-in-jekyll-chirpy": "Guides",
    "2025-12-14-building-my-first-bedrock-agent": "Builds",
    "2025-12-23-aws-console-demos-with-camtasia-and-after-effects-for-youtube": "Guides",
    "2025-12-30-building-a-bedrock-agent-with-aws-news-search": "Builds",
    "2026-01-02-adding-observability-to-my-bedrock-agent": "Builds",
    "2026-01-11-protecting-api-gateway-endpoints": "Builds",
    "2026-01-13-introduction-to-agentic-ai-systems-on-aws": "Lessons",
    "2026-01-18-tracking-amazon-bedrock-agent-costs-wit-allocation-tags-for-bedrock-agents": "Builds",
    "2026-02-01-getting-started-with-google-cloud": "Guides",
    "2026-02-22-extracting-a-recipe-from-youtube-with-aws-transcribe": "Builds",
    "2026-04-13-vertex-ai-search-vs-rag-engine": "Builds",
    "2026-04-15-extending-agents-with-aws-lambda-and-step-functions": "Lessons",
    "2026-04-25-how-my-domain-got-hijacked-through-a-dangling-dns": "Architecture",
    "2026-05-12-the-four-domain-portfolio": "Architecture",
    "2026-06-02-translating-youtube-subtitles-aws-transcribe-bedrock": "Builds",
    "2026-06-12-one-site-two-clouds": "Builds",
    "2026-06-13-cinematic-portfolio-infrastructure": "Builds",
}

# Posts that should carry a Google Cloud tag (GCP content)
GCP = {
    "2026-02-01-getting-started-with-google-cloud",
    "2026-04-13-vertex-ai-search-vs-rag-engine",
    "2026-06-12-one-site-two-clouds",
}

def slug(path):
    return os.path.basename(path)[:-3]

changed = 0
for path in glob.glob("_posts/*.md"):
    s = slug(path)
    if s not in MAP:
        print(f"SKIP (unmapped): {s}")
        continue
    src = open(path).read()
    new_cat = MAP[s]

    # Replace the categories line
    src2 = re.sub(r'^categories:.*$', f'categories: [{new_cat}]', src, count=1, flags=re.M)

    # Ensure Google Cloud tag on GCP posts
    if s in GCP:
        m = re.search(r'^tags:\s*\[(.*?)\]', src2, flags=re.M)
        if m and "Google Cloud" not in m.group(1):
            src2 = src2[:m.start()] + f'tags: [Google Cloud, {m.group(1)}]' + src2[m.end():]

    if src2 != src:
        open(path, "w").write(src2)
        changed += 1

print(f"\nDone. {changed} posts updated.")
