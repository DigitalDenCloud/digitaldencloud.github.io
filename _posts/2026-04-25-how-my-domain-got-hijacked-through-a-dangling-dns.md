---
title: "How My Domain Got Hijacked Through a Dangling DNS"
date: 2026-04-25
categories: [Cloud, Security]
tags: [DNS, Route 53, GitHub Pages, Security, Subdomain Takeover, Search Console]
description: "I made a GitHub repo private and within 12 hours an automated bot took over my domain and was serving gambling spam to Google's crawler. Here is how dangling DNS works, what the attacker actually did, and the cleanup playbook I ran to shut it down."
---

I have a personal journal site that I keep separate from this blog. It runs on Jekyll Chirpy, hosted on GitHub Pages, with the domain registered through AWS Route 53. Standard architecture. I have used the same kind of setup across several of my sites for over a year without issue.

Last week I decided I did not want my journal entries sitting in a public GitHub repo anymore. I flipped the repo from public to private with the plan of moving the site to S3 and CloudFront over the weekend. I never got round to the migration. Within 12 hours, an automated bot had taken over my domain and was serving Indonesian gambling spam to Google's crawler under my URLs.

The site itself never moved. My AWS account was never touched. My GitHub account was never touched. My DNS records were never edited by anyone other than me. Despite all of that, someone managed to serve their content under my domain name to Googlebot, while I saw blank white pages in my browser.

This post breaks down exactly how that happened, what the attacker actually did, why I saw nothing while Google saw spam, and the cleanup playbook I ran to shut it down. If you have ever pointed a domain at GitHub Pages, Heroku, Netlify, S3, or any third party hosting, you should understand this attack pattern.

<!--more-->

---

## The Architecture Before Anything Went Wrong

The site had been live for about six months. The infrastructure was a typical Jekyll Chirpy on GitHub Pages flow.

1. Markdown posts in a GitHub repo
2. GitHub Pages building and serving the site at `username.github.io`
3. A custom domain configured in the repo settings, with a `CNAME` file in the repo root containing `mysite.cloud`
4. DNS records in Route 53 pointing the domain at GitHub's servers

The two DNS records doing the actual work were an A record on the apex domain pointing to GitHub Pages IPs, and a CNAME on the www subdomain pointing to the GitHub Pages hostname.

```
mysite.cloud         A      185.199.108.153
                            185.199.109.153
                            185.199.110.153
                            185.199.111.153
www.mysite.cloud     CNAME  username.github.io
```

Those four IPs are GitHub Pages servers. Every site hosted on GitHub Pages with a custom domain points at the exact same IPs. GitHub then figures out which repo to serve based on the incoming domain name in the HTTP request. This is called virtual hosting.

That detail is the foundation of the entire attack. Hold onto it.

---

## What I Did Wrong

I made the GitHub repo private without thinking about what that does to the GitHub Pages deployment.

GitHub Pages on a free account does not serve from private repos. The moment you flip a repo to private on the free plan, GitHub Pages stops serving the site. The repo is private, the domain still has DNS pointing at GitHub, but GitHub no longer has any active deployment to map that domain to.

> **The dangling part of dangling DNS**  
> When DNS still points at a service, but that service no longer hosts your content, you have a dangling record. The DNS resolves correctly, the request reaches the destination, but the destination has no idea who owns the domain anymore. That gap is the security hole.
{: .prompt-warning }

GitHub actually documents this exact scenario in their own Pages documentation. Their guidance is that if your Pages site is disabled but the custom domain is still configured in your DNS, you should immediately remove the DNS records or verify your domain on GitHub. I had done neither.

I assumed the worst case was that my site would just be down until I migrated it. I was wrong by a wide margin.

---

## How the Attack Actually Works

GitHub Pages assigns custom domains based on a configuration field inside repos. When you set `mysite.cloud` as the custom domain in your repo's Pages settings, GitHub records that mapping internally. When a request comes in for `mysite.cloud`, GitHub looks up the mapping and serves your content.

When I made my repo private on a free plan, that mapping was effectively released. The `CNAME` file still sat in my repo with `mysite.cloud` written inside it, but GitHub no longer had a valid claim on the domain because the repo it pointed at could no longer serve via Pages.

Here is what the attacker did. None of it required access to anything I owned.

1. They created their own GitHub account
2. They created a new repo on that account
3. They put gambling spam HTML pages inside it
4. They configured the custom domain field as `mysite.cloud`
5. GitHub accepted the claim because no other active Pages deployment held the domain
6. My DNS still pointed at GitHub's servers
7. Googlebot crawled my domain and got served their content

> **Subdomain takeover**  
> The industry term for this attack pattern. The name is misleading because it works on apex domains too. The core idea is that DNS points at a third party service, the service no longer has your content registered, and someone else registers the domain on the service from their own account. The attacker takes over the destination, not the domain itself.
{: .prompt-info }

I want to be clear about what was not compromised. My domain registration was untouched. My Route 53 hosted zone was untouched. My AWS account was untouched. My GitHub account, my email, my SSL certs, my other sites, all untouched. The attacker never logged into anything that belonged to me.

What they did was hijack the destination that my DNS was pointing at. From Googlebot's perspective the result was the same as if I had been hosting that content myself. My DNS resolved to GitHub Pages, GitHub Pages served the attacker's content, Google indexed it under my domain. The fix lived entirely in DNS because that was the only link in the chain I still controlled.

---

## How They Found Me So Fast

The 12 hour window between flipping the repo private and the takeover landing is not a coincidence. This whole thing is automated.

There is a documented industry of subdomain takeover scanners. Tools like `subjack`, `subzy`, and various nuclei templates run continuously across the internet looking for exactly this configuration. They work like this.

1. Pull DNS records from public datasets like Certificate Transparency logs, passive DNS feeds, or zone files
2. Filter for domains pointing at known hijackable services like GitHub Pages, Heroku, S3, Netlify, Azure, and dozens of others
3. Probe each candidate to detect the fingerprint of an inactive deployment, for GitHub Pages this is the response "There isn't a GitHub Pages site here"
4. Auto-claim the matching slot on the target service from a rotating pool of accounts
5. Drop pre-built spam content onto the claimed deployment
6. Move on to the next target

A single bot running this loop can claim dozens of dangling domains per hour. The attacker who got my domain was almost certainly running infrastructure like this at scale. The Gmail address that appeared in Search Console (`ciyacila6@gmail.com`) is a throwaway from a rotating pool. There is nothing personal about being targeted, my domain is just a row in their pipeline.

> **Why automation makes this worse**  
> Manual subdomain takeovers used to be the work of bug bounty hunters scanning for one domain at a time. Modern automated tooling has industrialised the attack. The window between a domain becoming vulnerable and being claimed is now measured in hours, not days. There is no realistic safety margin for "I will fix this tomorrow."
{: .prompt-warning }

A security researcher writing about a similar incident found a single GitHub account running 87 active subdomain takeovers in parallel, all serving SEO spam to drive search traffic to malicious destinations. This is the scale these networks operate at.

---

## Why I Saw a Blank Page and Google Saw Gambling

Here is the part that confused me at first. When I visited my own domain during the takeover, I got a blank white page. No content, no errors, just a white page. I assumed the site was just down because the repo was private. The Search Console email was the first signal that something else was happening.

When the second Search Console email arrived showing structured data errors on URLs under my domain, the page titles were Indonesian gambling spam.

```
URL                                       Item Name
mysite.cloud/tags/some-real-tag/          BOMSLOT Situs Mahjong Slot Gacor
mysite.cloud/tags/another-real-tag/       BIGSLOT Slot Mahjong Legendaris
```

Googlebot was clearly being served real gambling content while I was getting a blank page. The technique that explains this is called user-agent cloaking.

> **User-agent cloaking**  
> Serving different content to search engine crawlers than to regular browsers. The server reads the User-Agent header on each incoming request. If the request comes from Googlebot, Bingbot, or another crawler, it returns spam content stuffed with target keywords. If the request comes from a normal browser, it returns either nothing, a redirect, or a blank page. This lets the attacker poison search results without the domain owner noticing through casual visits.
{: .prompt-info }

Cloaking is widespread in SEO spam operations. Google explicitly bans it in their spam policies, but detection is non-trivial because Googlebot has to actually receive the spam content in order for it to get indexed in the first place. By the time Google's spam team flags the site, the SEO benefit has already been extracted.

This is why I could not just open my domain in a browser and see what was wrong. The attacker's setup was deliberately designed to be invisible to me. The only signal I got was Google reporting the indexed URLs back to me through Search Console, which only happened because I was still the verified owner of the property.

---

## The Multi-Platform Fingerprint

A few days after the initial takeover I got a third Search Console notification, this time about AMP page domain mismatch errors. The URLs flagged in the email were not on my domain at all.

```
https://amp-tess-maen-cantek.pages.dev/
https://amp-tess-maen-cantek.pages.dev/mahjong
```

That `pages.dev` subdomain is Cloudflare Pages, which is Cloudflare's equivalent of GitHub Pages. The attacker had a parallel deployment running there, serving AMP versions of the same gambling spam content. Visiting the Cloudflare URL directly shows the actual gambling site, fully rendered, no cloaking, because that domain is theirs and they have no reason to hide on it.

> **AMP and canonical URLs**  
> AMP (Accelerated Mobile Pages) is a Google-backed framework for serving stripped-down mobile pages that load fast in search results. Every AMP page declares a canonical URL pointing at the non-AMP version of the same content. Search Console reports AMP errors to whoever owns the canonical domain, not the AMP host. The attacker's AMP pages on Cloudflare were declaring their canonical URL as my domain, which is why Google emailed me about errors on a domain I had never heard of.
{: .prompt-info }

This was the moment the operation came into focus. The attacker was running a coordinated multi-platform spam network. GitHub Pages handled the cloaked pages served under hijacked custom domains. Cloudflare Pages handled the AMP versions for mobile search results. The two layers were stitched together through canonical URL declarations to pass search ranking benefit between platforms while using the trust of established domains like mine as the foundation.

Each platform on its own would get flagged and shut down quickly. Wired together across platforms with takeover infrastructure on top, the whole network can run for weeks before any single piece gets caught. This is the architecture of industrialised SEO spam.

---

## What the Attacker Actually Wanted

A reasonable question is why anyone would bother hijacking a small personal blog with no traffic. The answer is they did not target me specifically. They targeted my domain's reputation.

Domains accumulate trust over time with search engines. Age, clean history, working email authentication, HTTPS, real content all signal to Google that a domain is legitimate. A fresh gambling site on a random new domain gets flagged within hours. Gambling content served under an established personal blog gets indexed first and flagged later. That delay window is the entire business model.

The attacker wanted to use my domain's trust to get gambling spam pages indexed in Google. Those indexed pages then link to their actual gambling properties, passing search ranking benefit through to the sites they care about. This is automated SEO link laundering at scale. They run thousands of these takeovers in parallel because each one only needs to last a few days to be profitable.

The Indonesian keywords give away which network was running it. "Situs Mahjong Slot Gacor" translates roughly to "popular Mahjong slot site" and is one of the most heavily promoted gambling spam patterns coming out of that region.

> **Why hosted services let this happen**  
> GitHub Pages, Heroku, Netlify, AWS S3 with static hosting, and similar services accept custom domain claims based on whoever sets the configuration field first when no other active deployment is claiming it. They cannot reliably tell the difference between a legitimate user moving between accounts and an attacker claiming an abandoned domain. The responsibility for keeping DNS aligned with active services sits entirely with the domain owner.
{: .prompt-warning }

---

## The Cleanup Playbook

Here is exactly what I did, in the order I did it, with the reasoning for each step. If you ever find yourself in this situation, this is the playbook.

### Step 1, Kill the DNS records pointing at the hijacked service

This is the most important action and it should happen first. Everything else is downstream of breaking the DNS link.

In Route 53, I deleted two records.

```
mysite.cloud         A      (deleted)
www.mysite.cloud     CNAME  (deleted)
```

I kept everything else. The MX records, SPF, DKIM, DMARC, ACM cert validation records, NS, SOA, all stayed. Email kept working, certs stayed valid, the only thing that broke was the resolution of the apex domain and www subdomain.

Verifying the deletion took two `dig` commands.

```bash
dig mysite.cloud
dig www.mysite.cloud
```

The apex returned `ANSWER: 0` and www returned `NXDOMAIN`. At that moment the takeover was effectively dead. The attacker's GitHub Pages deployment still existed on their account, but no DNS resolution meant no visitors and no Googlebot hits.

### Step 2, Submit a URL removal request in Search Console

Google had already indexed the spam pages under my domain. Even with DNS killed, those entries would sit in the Google index until the crawler refetched them and noticed they were gone. That could take weeks.

I used the Search Console Removals tool with a prefix removal.

```
URL: https://mysite.cloud/
Option: Remove all URLs with this prefix
```

This blocks every URL under the domain from Google search results for about six months. It is a temporary block, not a permanent index removal, but six months is plenty of time for the dead site to fall out of the index naturally and for the eventual S3 and CloudFront rebuild to repopulate with real content.

### Step 3, Pause or delete the Vertex AI Search datastore

This step is specific to my setup. I had a Vertex AI Search datastore configured to crawl the domain as a data source for grounded LLM queries. Recent crawls would have ingested the gambling spam content into the datastore alongside my real posts.

I deleted the datastore entirely. Cheaper to rebuild it later from a clean site than to try and surgically remove polluted documents.

If you have any system that crawls or syncs from your domain (RSS readers, search indexes, archive services, AI training pipelines), assume they have ingested the spam during the takeover window. Audit and clean each one.

### Step 4, Remove or correct the Search Console property

This is optional. The property itself is not actively harmful, but if you want to start fresh when you rebuild, removing it cleans up any lingering verification tokens or settings. I left mine in place because the URL removal request was tied to it.

### Step 5, Confirm the GitHub side is clean

In the original GitHub repo, I checked the Pages settings. Because the repo is private on a free plan, Pages was already disabled and there was no custom domain field shown. The `CNAME` file in the repo root still contained `mysite.cloud`, which is fine because without DNS pointing at GitHub, that file is just a string in a private repo with no real-world effect.

The attacker's repo on their own account is something I cannot see or delete. That is fine. Without my DNS pointing at GitHub's servers, their custom domain configuration is just a string in a database that resolves to nothing.

---

## What I Should Have Done

The mistake was making the GitHub repo private without first removing the DNS records that pointed at GitHub Pages. The clean order would have been the opposite.

1. Remove the DNS A record and CNAME pointing at GitHub
2. Confirm the domain no longer resolves
3. Then make the repo private

Or if I was migrating to a new host, the order would have been to set up the new hosting first, repoint DNS at the new hosting, verify the new site works, and only then decommission the old GitHub setup.

There is also a GitHub-specific protection I had never enabled. Verifying the domain on GitHub itself (a separate process from Google Search Console verification) prevents anyone else's GitHub repo from claiming the domain. With domain verification active, even if my DNS pointed at GitHub Pages and my repo was inactive, no other GitHub user could claim the domain on their own account. Worth setting up in advance for any custom domain pointed at GitHub.

The general rule is that DNS should never point at a service you are no longer actively using. The moment you stop using a hosting service, remove the DNS records before you stop the service. That single habit closes the entire class of subdomain takeover attacks.

> **DNS hygiene rule**  
> Always remove DNS records pointing at a third party service before you stop using that service. Never the other way round. If your DNS points at a destination that no longer claims the domain, anyone who can host on that platform can claim it.
{: .prompt-tip }

---

## How Bad Was the Damage

The damage was limited. The attacker had access to my domain for somewhere between a few hours and roughly a day. In that window they served gambling spam pages to Googlebot and got an unknown number of them indexed by Google. Once I killed the DNS, the spam pages stopped resolving. The URL removal request blocked them from search results within hours of submission.

No data was stolen. The attacker never had access to my AWS, GitHub, email, or any other account. The site itself contained no sensitive information because the journal entries were already private (which is why I made the repo private in the first place). My other domains and other sites were entirely unaffected.

The recovery cost was about an hour of cleanup work and a temporarily empty domain. The domain reputation hit will take a few weeks to wash out as Google reindexes the dead site. When I rebuild on S3 and CloudFront, the real content will repopulate the index and the gambling spam will fade out of search history.

---

## What This Taught Me

Three things stuck with me.

The attack surface for personal sites is wider than it looks. I had thought of GitHub Pages as a simple static host. The mental model I was missing is that GitHub Pages is a multi-tenant platform where domain claims are first-come-first-served on inactive deployments, and the platform cannot tell the difference between you and someone else when no active claim exists. Any multi-tenant platform you point DNS at has this property.

Dangling DNS is a process problem, not a technical problem. The fix is not a new tool or a security service. It is a checklist. When decommissioning anything, remove DNS first. When migrating, set up the new host before tearing down the old. These are habits, not configurations.

Monitoring DNS is worth a tiny amount of effort. A simple cron job that runs `dig` against your domains daily and alerts on unexpected changes would have caught the takeover within hours. I did not have one. I do now.

---

*Documented April 2026.*
