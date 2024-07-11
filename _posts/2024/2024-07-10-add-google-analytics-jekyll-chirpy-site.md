---
title: "Set Up Google Analytics in Your Jekyll Chirpy Site"
date: 2024-06-19 08:00:00 - 0500
categories: [Web Development, Jekyll]
tags: [jekyll, chirpy, lqip, webp]
image: 
  path: /assets/img/headers/google-jekyll.webp
  lqip: data:image/webp;base64,UklGRlIAAABXRUJQVlA4IEYAAACQAwCdASoUAAwAPzmGulOvKSWisAgB4CcJaQAAUqcyf8QgjPAAAP3Sdf++BUC7J8gpEDjOZulNrffdweivL0HvR8CeQAAA
---

Integrate Google Analytics into your Jekyll Chirpy site to gain insights into your website's traffic and user behavior. This documentation will walk you through the process of setting up Google Analytics and implementing it in your Jekyll Chirpy site, allowing you to make data-driven decisions to improve your content and user experience.

## Create a Google Analytics Account

1. **Sign up for Google Analytics:**
   - Visit the [Get started with Analytics](https://analytics.google.com/){:target="_blank"} page.
   - Click on `Start measuring`

2. **Account Creation:**
   - Account Name: Provide an account name ( blog or website name)
   - Data Sharing Settings: Leave the default data sharing settings selected.
   - Click `Next`

3. **Property Creation:**
   - Property Name: Choose a descriptive name, such as Blog Analytics or Chirpy Site Analytics.
   - Reporting Time Zone: Select your local timezone.
   - Currency: Select your preferred currency.
   - Click `Next`

4. **Business Details:**
   - Industry Category: For a tech blog select `Computers & Electroncis`
   - Business Size: Choose the size of the business.
   - Business Objectives: Select the objectives that best match your goals. For a technical blog, consider:
     - Generate leads
     - Raise brand awareness
     - Examine user behavior
   - Click `Create`

5. **Agree to Terms of Service:**
   - Review and accept the Google Analytics terms of service.

6. **Start Collecting Data:**
   - Choose Data Collection Source: Select `Web`

7. **Set Up Web Data Collection:**
   - Website URL: Enter your website URL.
   - Stream Name: Suggest a descriptive name for your stream, such as My Blog Stream or Chirpy Site Stream.
   - to generate the tracking ID and global site tag click `Create Stream`

8. **Copy the Measurement ID:**
   - After the stream is created, note down your Measurement ID (it looks like G-XXXXXXXX).

## Set Up Google Analytics in Your Jekyll Chirpy Site

1. **Update _config.yml with Your Google Analytics ID:**
   - Open your `_config.yml` file and add or update the Google Analytics section:

   ```yaml
   google_analytics:
     id: "G-XXXXXXXX" # replace with your actual Google Analytics Measurement ID
   ```
   {: .nolineno }

2. **Ensure the _includes Directory Exists:**
   ```bash
   mkdir -p _includes
   ```
    {: .nolineno }

   This command creates the **_includes** directory if it doesn't already exist. This directory is a standard Jekyll folder used for storing reusable content snippets, like our Google Analytics code. Creating it ensures proper Jekyll structure and prevents potential build errors.

3. **Create the analytics.html File:**
   : Create **analytics.html** in the **_includes directory** to isolate the Google Analytics tracking code, making it easier to manage and include across multiple pages in our Jekyll site.

        - Create a file named `analytics.html` in the `_includes` directory.
        - Add the following code into the file:

   ```html
   <!-- Global site tag (gtag.js) - Google Analytics -->
   <script async src="https://www.googletagmanager.com/gtag/js?id={% raw %}{{ site.google_analytics.id }}{% endraw %}"></script>
   <script>
     /* global dataLayer */
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', '{% raw %}{{ site.google_analytics.id }}{% endraw %}');
   </script>
   ```
    {: .nolineno }

    - The `/* global dataLayer */` tells the text editor or linter that dataLayer is a global variable, preventing it from showing warnings about dataLayer being undefined.
    - The use of `{% raw %}{{ site.google_analytics.id }}{% endraw %}` instead of a hardcoded ID allows you to set the Google Analytics ID in your _config.yml file, making it easier to update or change in the future.

3. **Modify default.html in the _layouts Directory:**
   : Modify the **default.html** file to include the Google Analytics code on all pages while ensuring it only loads in the production environment. This approach prevents tracking during development and testing.

        - Add the following lines into `default.html` just above the closing `</head>` tag to include the `analytics.html` file conditionally:

   ``` html
   <head>
     {% raw %}{% if jekyll.environment == 'production' and site.google_analytics %}
       {% include analytics.html %}
     {% endif %}{% endraw %}
   </head>
   ```
    {: .nolineno }

   This placement ensures that the Google Analytics code is included within the **<head>** section of your HTML document, which is the recommended location for such scripts. Placing it just before the closing **</head>** tag, ensures it's one of the last things loaded in the head, which can help with page load performance.
   - To see an example of how this looks in a real `default.html` file, you can check out [my default.html on GitHub](https://github.com/DigitalDenCloud/digitaldencloud.github.io/blob/main/_layouts/default.html){:target="_blank"}.

## Build and Deploy Your Site

1. **Build the Site:**
   : Run the build command with the production environment variable to ensure Google Analytics is included:

   ```bash
   JEKYLL_ENV=production bundle exec jekyll build -d "_site"
   ```
    {: .nolineno }

   > The `JEKYLL_ENV=production` environment variable tells Jekyll to build the site in production mode, enabling features like Google Analytics that are meant only for the live site.

2. **Commit and Push the Changes:**
   : Stage, commit, and push your changes to your repository:

    ```bash
    git add .
    git commit -m "Add Google Analytics tracking to the site"
    git push
    ```
    {: .nolineno }

## Verify Google Analytics Integration

1. **Check Real-Time Report:**
   Verify that your site is sending data to Google Analytics:

   - Visit the [Google Analytics Dashboard](https://analytics.google.com/){:target="_blank"}.
   - Select your Jekyll Chirpy site's property.
   - Select `Realtime`
   - Open your website in a separate browser tab or window.
   - Navigate through your site and watch for activity in the Real-Time report.

   > It may take a few hours before data starts appearing in your Google Analytics dashboard.
   {: .prompt-tip }
   
2. **Inspect Your Site's Source Code:**
   Confirm that the Google Analytics code is properly embedded in your site:

   - Open your live website in any browser.
   - Right-click and select `View Page Source`
   - Search for the Google Analytics tracking code in the **<head>** section. It should look similar to this:

     ```html
     <!-- Global site tag (gtag.js) - Google Analytics -->
     <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXX"></script>
     <script>
       window.dataLayer = window.dataLayer || [];
       function gtag(){dataLayer.push(arguments);}
       gtag('js', new Date());
       gtag('config', 'G-XXXXXXXX');
     </script>
     ```
        {: .nolineno }