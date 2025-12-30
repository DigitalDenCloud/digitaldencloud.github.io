---
title: "Fixing RSS Feed Limits in Jekyll Chirpy"
date: 2025-12-12 08:00:00 - 0500
categories: [Jekyll, Chirpy]
tags: [Jekyll, Chirpy, RSS]
description: "How to customize the RSS feed in Jekyll Chirpy. The theme limits feeds to 5 posts and truncates summaries to 400 characters by default, which works for typical blogs but not for AI agents or integrations that need full content. The solution: override the feed template and use the description field in front matter for full control."
image: 
  path: /assets/img/headers/jekyll-chirpy.webp
  lqip: data:image/webp;base64,UklGRnIAAABXRUJQVlA4IGYAAAAQBACdASoUAAwAPzmKu1SvKaYjMAgB4CcJbACdMoMYAEmaev8vi4/RgAD+2MDAB/6U3XCMCNwfY8TuqrcSy8dheSqs6J98VvnhAOf0PbFlh5c5xC1hJTIOfaBHX4QZcZifVA+4OAA=
---

## The Problem

If you're using RSS feeds for anything beyond basic blog subscriptions, you might run into issues with Jekyll Chirpy. This could affect AI agents that search your content, feed readers that display full summaries, or any integration that relies on complete RSS data.

By default, Chirpy limits the feed to 5 posts and truncates summaries to 400 characters. This makes sense for typical blog feeds where readers only need recent posts and short previews. However, for use cases that need full context or access to all content, these limits become a problem.

For example, if you have 35 posts, only 5 appear in the feed, and summaries may get cut off like this:
```
...This course is desi...
```

Not helpful for anything trying to understand what the post is about.

## The Cause

Jekyll Chirpy's feed template has two hardcoded limits:
```liquid
{% raw %}{% for post in site.posts limit: 5 %}{% endraw %}
```
{: .nolineno }
```liquid
{% raw %}<summary>{% include post-summary.html max_length=400 %}</summary>{% endraw %}
```
{: .nolineno }

This limits the RSS feed to 5 posts and truncates summaries to 400 characters. This is fine for blog preview cards on a website, but not for use cases that need full context.

The template lives inside the Chirpy gem and cannot be edited directly:
```
~/.rbenv/versions/3.2.2/lib/ruby/gems/3.2.0/gems/jekyll-theme-chirpy-7.4.1/assets/feed.xml
```

## Finding the Template

To locate the feed template in the gem, use:
```bash
find $(bundle show jekyll-theme-chirpy) -name "*.xml"
```
{: .nolineno }

To see where the truncation is happening:
```bash
grep -r "truncate\|excerpt\|summary" $(bundle show jekyll-theme-chirpy)/_includes
```
{: .nolineno }

## The Fix

Copy the template to your project to override the gem version:
```bash
cp $(bundle show jekyll-theme-chirpy)/assets/feed.xml assets/feed.xml
```
{: .nolineno }

Make two changes to `assets/feed.xml`

Change `limit: 5` to `limit: 100`:

```liquid
{% raw %}{% for post in site.posts limit: 100 %}{% endraw %}
```
{: .nolineno }

Or remove the limit entirely to include all posts:

```liquid
{% raw %}{% for post in site.posts %}{% endraw %}
```
{: .nolineno }

Change the summary line from:

```liquid
{% raw %}<summary>{% include post-summary.html max_length=400 %}</summary>{% endraw %}
```
{: .nolineno }

to:

```liquid
{% raw %}<summary>{{ post.description | default: post.excerpt | strip_html | xml_escape }}</summary>{% endraw %}
```
{: .nolineno }

This removes the 400 character truncation and increases the post limit. The summary now uses `description` from front matter if it exists, otherwise falls back to `excerpt` (the content above `<!--more-->` in your post, or the first paragraph if `<!--more-->` is not used).

## Controlling the Summary

There are two approaches:

**Option 1: Use `description` in front matter (recommended)**

Best when your intro has multiple paragraphs you want to keep for readability:
```markdown
---
title: "My Post"
description: "Full summary for the RSS feed. Write as much as you need here. No truncation."
---

Intro with paragraphs for readability on the website.

More text here.

## The Rest of the Post
```

The `description` controls the RSS summary. Your paragraphs stay readable on the website.

**Option 2: Use `<!--more-->`**

Best when your intro is a single block of text and you want the RSS summary to match exactly what's on the page:
```markdown
---
title: "My Post"
---
Single block intro that becomes the RSS summary. It needs to be one block without blank lines, otherwise Jekyll only uses the first paragraph.

<! --more-->

## The Rest of the Post
```

For most cases, `description` is cleaner because it gives full control and allows paragraphs in the intro for readability.

Use `<!--more-->` when you want the RSS summary to match exactly what appears on the page and your intro is a single block of text. This avoids duplicating content between the front matter and the body.