---
layout: page
icon: fas fa-info-circle
order: 4
title: About
---

I'm Deniz Yilmaz. Cloud engineer based in London, focused on AWS.

I came to cloud engineering via the AWS re/Start programme after a previous career as an immigration lawyer. Since then I've worked at QA (formerly Cloud Academy) building AWS and Google Cloud training content. 40+ lessons published, multiple AWS certifications, and an AWS Community Builder.

This site is where I document the cloud work. Bedrock agents, S3 and CloudFront architectures, serverless pipelines, AWS infrastructure builds. Each post is a real project, written as I built it.

For photography, film, and the personal logs, see [denizyilmaz.cloud](https://denizyilmaz.cloud).

---

## Get in touch

The form itself runs on AWS Lambda, API Gateway, Bedrock, and SES — full build [documented here](https://digitalden.cloud/posts/build-serverless-contact-forms-with-generative-ai/){:target="_blank"}.

<form id="contact-form" class="contact-form" novalidate>
  <div class="field">
    <label for="cf-name">Name</label>
    <input type="text" id="cf-name" name="name" required autocomplete="name">
  </div>
  <div class="field">
    <label for="cf-email">Email</label>
    <input type="email" id="cf-email" name="email" required autocomplete="email">
  </div>
  <div class="field">
    <label for="cf-message">Message</label>
    <textarea id="cf-message" name="message" rows="5" required></textarea>
  </div>

  <!-- Honeypot field, hidden from real users. Bots fill it; humans don't. -->
  <div class="field honeypot" aria-hidden="true">
    <label for="cf-website">Website</label>
    <input type="text" id="cf-website" name="website" tabindex="-1" autocomplete="off">
  </div>

  <div class="actions">
    <button type="submit" id="cf-submit" class="btn-send">Send</button>
    <span class="cf-status" id="cf-status" role="status" aria-live="polite"></span>
  </div>
</form>

<style>
.contact-form {
  margin-top: 1rem;
  max-width: 36rem;
}
.contact-form .field {
  margin-bottom: 1rem;
}
.contact-form label {
  display: block;
  margin-bottom: 0.35rem;
  font-size: 0.9rem;
  color: var(--text-color);
  font-weight: 500;
}
.contact-form input,
.contact-form textarea {
  width: 100%;
  padding: 0.6rem 0.75rem;
  background: var(--card-bg);
  border: 1px solid var(--card-border-color, #444);
  border-radius: 6px;
  color: var(--text-color);
  font-family: inherit;
  font-size: 0.95rem;
  box-sizing: border-box;
}
.contact-form input:focus,
.contact-form textarea:focus {
  outline: none;
  border-color: var(--link-color);
}
.contact-form textarea {
  resize: vertical;
  min-height: 6rem;
}
.contact-form .honeypot {
  position: absolute;
  left: -10000px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}
.contact-form .actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
}
.contact-form .btn-send {
  background: transparent;
  color: var(--text-color);
  border: 1px solid var(--card-border-color, #444);
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 400;
  cursor: pointer;
  transition: background 0.15s ease, border-color 0.15s ease;
}
.contact-form .btn-send:hover {
  background: var(--card-bg);
  border-color: var(--text-color);
}
.contact-form .btn-send:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.contact-form .btn-send:hover { opacity: 0.85; }
.contact-form .btn-send:disabled { opacity: 0.5; cursor: not-allowed; }
.contact-form .cf-status { font-size: 0.9rem; }
.contact-form .cf-status.success { color: #4ade80; }
.contact-form .cf-status.error { color: #f87171; }
.contact-form .cf-status.loading { color: var(--text-muted-color); }
</style>

<script src="{{ '/assets/js/contact-form.js' | relative_url }}"></script>