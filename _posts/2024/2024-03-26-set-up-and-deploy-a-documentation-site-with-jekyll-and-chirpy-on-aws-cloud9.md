---
title: "Set Up and Deploy a Documentation Site With Jekyll & Chirpy on AWS Cloud9"
date: 2024-03-26 08:00:00 - 0500
categories: [Web Development, Jekyll]
tags: [aws, cloud9, jekyll, chirpy, ruby, git, route 53, cname]
image: 
  path: /assets/img/headers/jekyll.webp
  lqip: data:image/webp;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAGCAMAAADNLv/0AAAAilBMVEWrq6uxsbF1dHVYV1pVVllXV1paWlyJiYrv7+/6+vqvr69SUVYeISguLjMrKzAZHSZZWVvt7e2wsLBNTU0eISdfTTZPQzIXHCZbW13u7u5QUFAfHyErKiooJygbGx1fX2B9fX1hYmFgYWBdXl6BgoHi4uKsrKyqqqqur6+wsbGxsrKys7PKy8v4+PiSJDQPAAAARElEQVQIHWNgYGRiZmFlY+fgZGDg4ubh5eMXEAQyhYRFRMXEJSSBTEYpaRlZOXmQAkYFRUUlZRVVIFNNXU1DU0tbRxcAZiwEgRfNpoYAAAAASUVORK5CYII=
---

 This documentation outlines the steps for setting up and deploying a documentation site using Jekyll, a popular static site generator, and the Chirpy theme using GitHub Actions on AWS Cloud9 IDE. It includes instructions for configuring a custom subdomain, such as `https://docs.example.com`, through AWS Route 53 and integrating it with GitHub Pages.
 
## Objectives

- Launch and prepare the AWS Cloud9 environment
- Set up the development environment for Jekyll with Chirpy on Cloud9
- Configure Git and SSH for GitHub integration
- Set up the Chirpy theme with the Chirpy starter template
- Create and run a start script to preview your site in Cloud9
- Deploy the site to GitHub Pages using GitHub Actions
- Personalize the Jekyll site configuration and the about me page
- Write your first post with Chirpy using Markdown syntax
- (Optional) Map a custom domain to your GitHub Pages site

By the end of this post, you will have your own documentation site hosted on GitHub Pages, a free hosting solution. The site will be set up with the Chirpy theme, which provides a beautifully structured layout and various features automatically. You can then focus on writing your content in Markdown, committing it to a Git repository, and let Chirpy and GitHub Actions handle the rest.

## Prerequisites
- AWS Account
- GitHub Account
- (Optional) Registered domain on Amazon Route 53 (if you want to use a custom domain like docs)

## Launch and Prepare the AWS Cloud9 Environment

> This documentation will utilize AWS Cloud9 running on Amazon Linux to set up Jekyll and the Chirpy theme. The Git panel extension for AWS Cloud9 will be used to provide convenient user interface access to core Git commands.

#### **a) Benefits of Using Cloud9**

   - **Cloud-Based Content Management:**  
   Cloud9's cloud-based setup enables bloggers and writers to remotely update their Jekyll/Chirpy site, perfect for regular content updates.

   - **Uniform Starting Point:**  
   Using Cloud9 ensures that everyone, especially for tutorial purposes, begins with a blank Linux instance, allowing learners to follow along precisely without environment discrepancies.

   - **Version Control Integration:**  
   Git integration with Cloud9 simplifies version control, useful for managing updates, and theme modifications.

> The AWS Free Tier provides 750 monthly hours of EC2 t2.micro usage and 5GB EBS storage for one year. This demo, run on a t2.micro instance using less than 1GB storage, incurs no additional costs under the Free Tier. Without it, the cost is approximately $0.11 per hour.
{: .prompt-warning }

#### **b) Set Up the Cloud9 Environment**

   - Navigate to the AWS Cloud9 console.
   - Create a new environment named `JekyllChirpyEnv` (or any name you prefer).
   - Configure the environment as needed, `t2.micro` will suit the requirements.
   - Once your environment is ready, open the terminal within the Cloud9 IDE.
   - Update your package manager to ensure you have the latest packages.

   ```bash
sudo yum update -y
   ```
   {: .nolineno }
   
   - The -y flag automatically answers 'yes' to any prompts during the update process, allowing it to run without manual intervention.

## Set Up the Development Environment for Jekyll with Chirpy on AWS Cloud9

To set up your development environment for Jekyll with Chirpy on AWS Cloud9, you'll go through a series of steps involving the installation of Ruby, necessary development tools, configuring the Ruby Gems environment, and installing Jekyll along with Bundler. These steps ensure your AWS Cloud9 environment is fully prepared for Jekyll Chirpy development.

> If you prefer using your own text editor like VS Code, macOS users can apply the same Linux commands in the Terminal for setting up Jekyll, Ruby, and Chirpy.
 {: .prompt-tip }

#### **a) Install Ruby and Development Tools**  
Execute the following commands in the Cloud9 terminal:
   
   ```bash
sudo yum install -y ruby ruby-devel
sudo yum groupinstall -y "Development Tools"
   ```
   {: .nolineno }

#### **b) Configure Ruby Gems Environment**  
Set up a specific directory for RubyGems to streamline gem management. This setup:
   - Enables user-level gem installations, reducing security risks.
   - Creates an isolated environment for gems, preventing version conflicts.
   - Simplifies the process of managing, updating, and uninstalling gems.
   - Prevents permission-related problems common with system-wide installations.
   - Enhances the portability of the development environment across different machines.
   
   ```bash
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
   ```
   {: .nolineno }

#### **c) Install Jekyll and Bundler**  
With the RubyGems environment now configured, proceed to install Jekyll and Bundler:

   ```bash
gem install jekyll bundler
   ```
   {: .nolineno }

#### **d) Update RubyGems if Necessary**  
Should there be a new release of RubyGems available, update to the latest version:
   ```bash
gem update --system 3.5.6
   ```
   {: .nolineno }

#### **e) Verify Jekyll Installation**  
Ensure Jekyll is correctly installed by checking its version:

   ```bash
jekyll -v
   ```
   {: .nolineno }

   - The JekyllChirpy environment on AWS Cloud9 is now fully set up and ready for development.

## Configure Git and SSH for GitHub Integration
Before you start using Git, configure it with your personal information which will be associated with your commits.

#### **a) Configure Git with Your User Information**
   ```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"
   ```
   {: .nolineno }

   - Replace "`Your Name`" and "`youremail@example.com`" with your actual name and email associated with your GitHub account.
   
   > The new name you set will be visible in any future commits you push to GitHub from the command line. If you'd like to keep your real name private, you can use any text as your Git username.
   {: .prompt-tip }

#### **b) Generate an SSH Key Pair** 
SSH key pairs facilitate secure, passwordless authentication with GitHub, linking commits to your account and ensuring only authorized users can access repositories:

   ```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```
   {: .nolineno }

   - Press Enter to accept the default file locations.
   - Press Enter twice on passphrase prompts (entering a passphrase is optional).

#### **c) Start the ssh-agent & Add Your SSH Key**
   ```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
   ```
   {: .nolineno }

#### **d) Display and Copy your SSH public key**
   
   ```bash
cat ~/.ssh/id_rsa.pub
   ```
   {: .nolineno }

#### **e) Add Your SSH Public Key to Your GitHub Account**
`GitHub` → `Settings` → `SSH & GPG Keys` → `New SSH key` → `Paste Key`

#### **f) Verify SSH Connection to GitHub**
   ```bash
ssh -T git@github.com
   ```
   {: .nolineno }

   - You should see a message confirming successful authentication.
   - Your AWS Cloud9 environment will be fully configured to interact with GitHub using SSH.

## Set Up the Chirpy theme with the Chirpy Starter template

Creating a new site with the Chirpy theme is straightforward using the Chirpy Starter. This method is preferred for its simplicity and maintenance ease, ideal for AWS cloud engineers and technical writers who wish to focus on their content rather than the technical aspects of website setup.

#### **a) Use the Chirpy Starter Template**
   - Visit the [Chirpy Starter Repository](https://github.com/cotes2020/chirpy-starter) on GitHub.**
   - Click on the `Use this template` button at the repository page.
   - Name the new repository `USERNAME.github.io`, where `USERNAME` is your GitHub username. This naming is crucial for GitHub Pages to automatically host the site.
   - Ensure the repository is set to `public`. GitHub Pages requires the repository to be public to serve the website unless you are on a GitHub plan that supports private repositories for GitHub Pages.
   - Click `Create repository from template` to initiate the new repository setup.

> Your site will be available at `https://USERNAME.github.io`
{: .prompt-tip }

#### **b) Clone your New Repository Using Cloud9:**
   - Obtain the SSH link from your GitHub repository
   - In the Cloud9 environment, locate the Git panel window and select `Clone Repository`
   - Enter the SSH Link. 
     - This will be in the format `https://github.com/USERNAME/USERNAME.github.io.git`
   - After entering the URL, press `Return`
   - A dialog box will appear prompting you to select a workspace folder for the cloned repository. Choose your desired location and click `Select Repository Location` to finalize the cloning process.

#### **c) Install Jekyll and Other Dependencies:**
   ```bash
bundle install
   ```
   {: .nolineno }

   - This will install all the Ruby gems needed for your Jekyll site, as specified in the Gemfile, which includes Jekyll itself and any plugins or themes you're using.

## Preview the Jekyll Site

To preview a Jekyll site locally, the command `bundle exec jekyll serve` is used, which starts a server and makes the site accessible at `http://localhost:4000`.  When moving to AWS Cloud9, a cloud-based development environment, adjustments are necessary: `127.0.0.1:4000` won't work due to Cloud9's remote nature. 

Instead, Cloud9 requires using its environment URL and supports web traffic on ports `8080`, `8081`, and `8082`, necessitating a change in server settings to make your site accessible.

> `127.0.0.1:4000` and `http://localhost:4000` both direct you to the same location: your local development server running on port 4000. The term "localhost" is a hostname that translates to the IP address 127.0.0.1, which represents your own computer.
{: .prompt-tip }

The adjusted command to run Jekyll in Cloud9, accommodating its supported ports and making your site accessible, would be:

``` bash
bundle exec jekyll serve --host 0.0.0.0 --port 8080 --baseurl ''
```
{: .nolineno }

### **a) Create and Run a Start Script to preview the site in Cloud9**
Entering the command bundle exec `jekyll serve --host 0.0.0.0 --port 8080 --baseurl ''` every time you want to preview your site can be time-consuming. Instead, creating a start script in Cloud9 can automate the server launch process. Here's how to set it up:

- **Open Cloud9 Terminal:**
   - Navigate to your project directory within the Cloud9 IDE.

-  **Create a New File for the Start Script:**
   - Within the file explorer under your project directory, create a new file named `start_jekyll.sh`.

-  **Edit the Start Script:**
   - Open `start_jekyll.sh` in the Cloud9 editor and input the following line to configure Jekyll for Cloud9:
   ```bash
   bundle exec jekyll serve --host 0.0.0.0 --port 8080 --baseurl ''
   ```
   {: .nolineno }

   - Use `--host 0.0.0.0` to make the server accessible from any IP address, `--port 8080` to comply with Cloud9's allowed web traffic ports, and `--baseurl ''` to correctly reference resources.
   - Save the changes to the script.

-  **Run the Start Script:**
   - Press the `Run` button in Cloud9.
   - This command initiates the Jekyll server on Cloud9's specified ports, making your site accessible.

-  **Access Your Site:**
   - Your site can be viewed at Cloud9's environment URL, formatted as:
     - `https://<workspace-name>-<username>.vfs.cloud9.<region>.amazonaws.com:8080`

This setup allows you to run and preview your Jekyll site directly from the AWS Cloud9 environment, adapting the local development workflow to the cloud.

## Deploy the Jekyll Site to GitHub Pages using GitHub Actions

Deploying your Jekyll site through GitHub Actions automates the process, establishing a CI/CD pipeline that automatically builds your site and deploys it to GitHub Pages upon any push to your repository. This is particularly beneficial for Jekyll Chirpy theme users, as it includes a pre-configured GitHub Actions workflow suitable for this purpose.

 - To  make the `.github` directory visible, and access the GitHub Actions workflow configurations make sure your AWS Cloud9 environment is correctly set up to show hidden files:
   - Click on the `gear` icon (Preferences).
   - Select `Show Hidden Files`

### **a) The GitHub Actions Workflow**

The GitHub Actions workflow, specifically tailored for Jekyll deployments, is structured to facilitate seamless builds and deployments. Here’s a breakdown of its components:

- **Navigate to Workflow:** 
   - Access the `workflows` folder within the .github directory.
   - Open the `pages-deploy.yaml` file to examine the workflow details.

-  **Workflow Overview:**
   - The workflow is named Build and Deploy.
   - It activates on pushes to both the main and master branches, with exceptions for changes to .gitignore, README.md, and LICENSE files. Manual triggers are also supported.
   - It's configured with read permissions for contents and write permissions for pages and ID tokens, ensuring secure and authorized operations.
   - Designed to run a single deployment at a time, it cancels any in-progress deployments upon new pushes to streamline the update process.

-  **Jobs Detail:**
   - Utilizes the latest Ubuntu runner for operations like checking out the code, setting up GitHub Pages, configuring Ruby, building the site via Jekyll, performing tests with htmlproofer, and uploading the site as an artifact for deployment.
   - Focuses on deploying the built site to GitHub Pages and providing a URL to the deployed site.

### **b) Configure GitHub Pages Deployment**

To ensure your site deploys via GitHub Actions to GitHub Pages, a few configuration steps are necessary within your GitHub repository settings:

-  **Access Repository Settings:** 
   - Navigate to your GitHub repository online and enter the settings menu.

- **Locate Pages Section:** 
   - Within the settings, find and click on the Pages option on the left navigation bar to access GitHub Pages settings.

-  **Deployment Source Setup:**
   - In the Build and deployment section, find the Source setting.
   - Choose `GitHub Actions` from the dropdown menu to enable deployments through GitHub Actions.

This setup ensures that every push to your repository triggers the GitHub Actions workflow, automatically building your Jekyll site and deploying it to GitHub Pages. It's a streamlined process that simplifies site updates, allowing you to focus more on content creation and less on manual deployment tasks.

> **Tip:** For users of GitHub's free tier, keep your repository public to utilize GitHub Pages without any costs.
{: .prompt-tip}

### **c) Set the Site URL for GitHub Pages**

Before pushing your Jekyll site to GitHub, configure the `_config.yml` file to set your site's URL and personalize various settings.

> GitHub Pages requires the correct base URL to serve your site. This is a critical step for your site's accessibility and functionality.
{: .prompt-warning }

-  Open the `_config.yml` file and find the `url` field, which sets the base URL for your site. 
   For example, if your GitHub   username is digitalden3, your url would be:

   ```yaml
url: "https://digitalden3.github.io"
   ```
   {: .nolineno }

   - By setting the url, you enable GitHub Pages to host your site at a predictable address based on your username.

### **d) Personalize the Jekyll Site Configuration**

With the URL set, continue to personalize your site by updating these important fields in the `_config.yml` file:

- **title tagline and description**: 
  - Define your site's title and description to improve search engine optimization (SEO).

- **timezone**:
  - Set the correct timezone to ensure your posts have accurate timestamps. 
  - Use a [Time Zone Picker](https://kevinnovak.github.io/Time-Zone-Picker) to find your timezone string.

- **username**: 
  - Enter your social media usernames (github.username, twitter.username...).

- **name and email**: 
  - Provide your full name and email address under the social section for use in site elements like the footer.

- **theme_mode**: 
  - Choose your theme preference. Light, dark, or automatic.

- **avatar**: 
   - Add a profile picture.
     - Store your images in an organized directory, such as assets/images/.
     - Upload your preferred image to this directory.
     - Reference your avatar in the avatar field:

   ```yaml
avatar: "/assets/images/your-image.jpg"
   ```
   {: .nolineno }

> To ensure your site loads quickly, optimize your images! Use efficient image formats, such as WebP.
{: .prompt-tip }

### e)Deploy the Jekyll Site with GitHub Actions

Deploying your Jekyll site to GitHub Pages using GitHub Actions automates the build and publish process, making site updates seamless with every push. In the AWS Cloud9 interface, select to the `Source Control` panel.

-  **Stage Your Changes**:
    - Go to the Git panel menu and choose Stage All Changes.
    - Choose Stage All Changes.

-  **Commit Your Changes**:
    - In the Source Control panel, you should see a text box where you can enter a commit message.
    - Enter Deploying Jekyll Site.
    - Go to the Git panel menu and choose Commit All.

-  **Push Changes to GitHub**:
    - Go to the Git panel menu and choose Push. This action will push your commits to the GitHub repository, triggering the GitHub Actions workflow.

-  **Deployment via GitHub Actions:**
    - Navigate to your GitHub repository in a web browser.
    - Click on the `Actions` tab near the top of the repository page. This is where all the automated workflows are listed.
    - Inside the Actions tab, you'll see a list of all the workflow runs. Each run corresponds to a push you've made to the repository.
    - Click on the latest run to see the details of the workflow execution, including setup, build, and deployment steps.
    - After the GitHub Actions workflow completes, your site will be live. GitHub will provide a URL where your site is hosted, which will typically follow this format:
      - `https://<username>.github.io`

## Personalize the About Me Page

Update your About Me page on your Jekyll site to reflect your personality, professional journey, hobbies, and more. You can also add images.

-  **Edit the About Me Page**:
    - Navigate to `_tabs/about.md` in your project files within Cloud9. This file is where you'll introduce yourself and share your story.

-  **Incorporate Your Personal Story**:
    - Begin by writing about yourself. You might include your background, what you do professionally, your passions, and the purpose of your site.

-  **Upload Images**:
    - To add images, go to the `assets/img` directory in the Cloud9 file tree.
    - Select File → Upload Local Files.

-  **Insert an Image in Your About Me Page**:
    - Add the following line of markdown to `_tabs/about.md` to include an image. Ensure to replace `profileimage.jpg` with the actual name of your uploaded image file.

    ```markdown
![About](/assets/img/profileimage.jpg)
    ```
    {: .nolineno }

-  **Save Your Changes**:
    - After editing and adding images, save the`about.md file.

-  **Preview Your Site**:
    - Use Cloud9's built-in server to preview your site and see how the changes appear in real-time.

-  **Deploying Changes to GitHub**
    - Stage All Changes in the Git panel → Enter a message and commit → Push changes to deploy via GitHub Actions.

## Write the First Post with Chirpy Using Markdown Syntax

Creating a new post in Jekyll using the Chirpy theme is straightforward. Chirpy enhances Jekyll with unique features and requires specific variables in posts.

> Markdown is a lightweight markup language with plain text formatting syntax that is designed to be converted to HTML and other formats. It's very simple to use and allows you to write rich content with plain text.
{: .prompt-info }

For better management, organize posts within the `_posts` folder by year (2023, 2024...). This helps keep your directory structured without affecting post processing.

-  **File Naming:**
   - Place your post in the correct year folder within `_posts`, naming it `YYYY-MM-DD-TITLE.MD`

-  **Front Matter**
   - Use the following template at the start of your post:

```yaml
---
title: "Your Post Title"
date: YYYY-MM-DD HH:MM:SS +/-TTTT
categories: [Primary Category, Subcategory]
tags: [tag1, tag2, tag3]
image: /path/to/image
alt: "Image alt text"
---
```
{: .nolineno }

- **title:** The title of your post.
- **date:** The publication date and time of your post, including the timezone.
- **categories:** Categories for organizing your post, limited to two.
- **tags:** Keywords associated with your post for tagging purposes.
- **image:** An optional path to a preview image for your post.
- **alt:** Descriptive text for the preview image, used for accessibility and SEO.

Following these initial steps sets up an empty post scaffold. To fill your post with content, you'll write in Markdown, a straightforward yet powerful syntax for creating web content. For detailed guidance, including Markdown syntax and advanced Chirpy features, consult the:
- [Chirpy documentation on writing a new post](https://chirpy.cotes.page/posts/write-a-new-post/)

> The Jekyll Chirpy theme automatically transforms your Markdown content into a visually appealing website. By applying CSS for styling, HTML templates for structure, and JavaScript for interactivity, Chirpy ensures your content is readable, engaging and professionally presented.
{: .prompt-tip }

**Workflow:** 
: `Write Post` → `Preview` → `Stage New Post` → `Commit` → `Push to GitHub` → `Deployment`

## Map a Custom Domain to GitHub Pages (Optional)

GitHub Pages offers free hosting for websites, allowing the use of custom domains to improve brand identity, SEO, and more. This guide explains the process of mapping a custom domain to GitHub Pages, taking advantage of GitHub's secure hosting.

When opting for a subdomain, such as `docs.example.com`, over the primary domain (example.com), you strategically organize and differentiate content. A subdomain like docs specifically earmarks this section for documentation, facilitating centralized content management.
 - For implementation, replace example.com with your own domain.

### a) Create a CNAME File in Cloud9
   - In Cloud9, go to your repository's root directory.
   - Right-click, choose New File, and name it `CNAME`—no file extension.
   - Open CNAME, input `docs.example.com`, and save.

### b) Push the CNAME File to GitHub
   - Follow the sequence: `Stage CNAME` → `Commit` → `Push to GitHub` → `Deployment`.

### c) Set Custom Domain in GitHub Pages Settings
   - In your GitHub repository settings, select `Pages`
   - Under Custom domain, enter `docs.example.com` and save.

   > A DNS record error may initially appear—this resolves after proper DNS setup.
   {: .prompt-warning }

### d) Create a CNAME Record in AWS Route 53
   - Access `Route 53` in the AWS Management Console.
   - In your hosted zone, add a CNAME record:
     - **Record Name:** docs
     - **Type:** CNAME
     - **Value:** `USERNAME.github.io` (replace USERNAME).

### e) Verify DNS Configuration
   - Confirm DNS setup with:
     ```
     dig docs.example.com +nostats +nocomments +nocmd
     ```

      - GitHub Pages will show DNS checks in progress after correct DNS setup.
      - Post-DNS verification, enable `Enforce HTTPS` in GitHub Pages settings.
      - GitHub automatically secures your site with an SSL certificate, a process that may take up to 24 hours.

### f) Update URL in _config.yml to Custom Subdomain
   - Open your Jekyll project in your Cloud9.
   - Open the `_config.yml` file in the root directory of your Jekyll project.
   - Find the `url` field in the _config.yml file. It might look something like this:
     ```yaml
url: "https://USERNAME.github.io"
     ```
     {: .nolineno }
   - Update the url field to use your custom subdomain. Replace `https://USERNAME.github.io` with `https://docs.example.com` 
     ```yaml
url: "https://docs.example.com"
     ```
     {: .nolineno }
   - Save the changes to the _config.yml file.
   
   > By updating the urL field in your _config.yml file to `https://docs.example.com`, you ensure that all internal links, metadata, and references within your Jekyll site point to the correct custom subdomain. This step is crucial for maintaining consistency and accuracy across your site, especially when using a custom domain. 
   {: .prompt-tip }

   - After making this change, push the updated `_config.yml` file to your GitHub repository.

Your GitHub Pages site will be accessible via your custom domain `docs.example.com`, leveraging GitHub's secure and reliable hosting.

## Video Tutorial
{% include embed/youtube.html id='7cLkDE8_tCI' %}