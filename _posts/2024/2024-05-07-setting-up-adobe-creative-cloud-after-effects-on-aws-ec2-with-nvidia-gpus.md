---
title: "Setting Up Adobe Creative Cloud and After Effects on AWS EC2 with NVIDIA GPUs"
date: 2024-05-03 08:00:00 - 0500
categories: [AWS, Adobe Creative Cloud]
tags: [adobe, after effects, aws, ec2, nvidia, gpu]
image:
  path: /assets/img/headers/adobe-aws-nvida-gpu.webp
  lqip: data:image/webp;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAFCAMAAABLuo1aAAAAUVBMVEUBAQAAAAABAAAAAAEYDQAWHyUAAgYGBQMEBAUTIAANFwBDKx48YlgACxBDQD8+Pj8LDAtVcSU4ShcSFBciICEJCAcKCgoLCwsKCgsjIScZGBzwCGTZAAAANUlEQVQIHWNgYGRkYmRkZGZmYGBkYWVj52Dk5GJkYOTm4eXjFxAUAjKFRUTFxCUkpYBMOAAAIrUBeMU/YbsAAAAASUVORK5CYII=
---

Learn how to set up an optimized environment for `Adobe Creative Cloud` and After Effects on an `AWS EC2` Instance equipped with powerful `NVIDIA GPUs.` Explore two different methods:

1. **Manual Setup**: Launch a standard Windows Server instance and manually install NVIDIA GRID drivers. This approach gives you full control over the configuration, allowing you to customize the installation according to your requirements.

2. **Pre-configured AMI**: For a quicker and simpler setup, utilize the pre-configured NVIDIA RTX Virtual Workstation AMI, which comes with the necessary drivers pre-installed, eliminating the need for manual installations.

These methods are designed to address the needs of users who require advanced graphics processing capabilities without the investment in high-end local hardware. Whether you're a freelancer, part of a small studio, or simply looking to efficiently scale your creative projects, this post will provide you with a cloud-based solution tailored to your Adobe Creative Cloud workflows.

> Before we start, ensure you check and increase your AWS service quotas for GPU instances if needed.
{: .prompt-tip }

Here's an overview of the steps we'll cover:

- Launch a `g4dn.2xlarge` EC2 instance equipped with an NVIDIA GPU and set up an additional EBS GP3 volume for After Effects caching.
- Establish a Microsoft Remote Desktop connection from your MacBook to the instance.
- For the manual setup, use PowerShell to download and install the necessary NVIDIA GRID drivers to fully leverage the GPU's capabilities.
- For the pre-configured AMI method, you'll skip the manual driver installation step.
- Download and install Adobe Creative Cloud, tackling potential JavaScript-related issues that may arise during the installation.
- Ensure that the attached EBS volume is properly activated and configured within the instance.
- Prepare the EBS volume for use with Adobe After Effects by creating specific folders for caching, which will help speed up rendering and previewing by offloading intensive data processing to a separate drive.
- Enable audio playback on the Windows EC2 instance, which is typically disabled by default in server editions of Windows.

By the end of this post, you'll have a powerful, GPU-accelerated AWS environment optimized for Adobe Creative Cloud workflows, tailored to your preferred setup method. A complementary video tutorial is also provided for a more comprehensive learning experience.

## Checking and Increasing AWS Service Quotas
We're selecting the [g4dn.2xlarge](https://aws.amazon.com/ec2/instance-types/g4/){:target="_blank"} instance for our AWS EC2 setup.

| Instance Size                | GPU      | vCPU    | RAM    | On-Demand Price/hr* |
| :--------------------------- | :------- | :------ | :----- | :------------------ |
| g4dn.2xlarge                 | 1        | 8       | 16GB   | $0.752              |


The g4dn.2xlarge has a good balance of graphics performance and cost-efficiency. The included NVIDIA GPU is efficient for After Effects, enabling robust rendering capabilities. With sufficient compute and memory resources, it can handle complex tasks and large projects effectively.

Before we launch the g4dn.2xlarge instance for the Adobe Creative Cloud suite, ensure that your AWS account service quotas support your needs. AWS imposes default service quotas to manage resource allocation. If you haven't used GPU instances before, you may need to request an increase for specific quotas for GPU instance instances.

- In the [Service Quotas Console](https://us-east-1.console.aws.amazon.com/servicequotas/home){:target="_blank"} use the search function to find quotas associated with EC2 services. Ensure you're in the region where you want to deploy the GPU instances.
- Search for and select the quota **"Running On-Demand G and VT instances".**

If you see that your quota is 8 or higher, you're ready to proceed with the instance launch. If your quota is anything less, you'll need to request an increase. 
- Click on **"Request increase at the account level"** and specify an increase from 0 to at least 8 vCPUs. This adjustment is required to meet the minimum vCPU requirement for launching g4dn.2xlarge instances. 

> When you submit your quota increase request, AWS will review it, which typically takes a few days. AWS will then inform you via email once your quota increase request has been processed.
{: .prompt-tip }

## Launching and Configuring the EC2 Instance

1. Navigate to the AWS EC2 Management Console and click on **"Launch Instance."**
2. Name your instance **"AdobeCC-AE-Instance".**
3. Select the right AMI for your setup:
   - Filter the list of AMIs by Windows and search for the **"Microsoft Windows Server 2022 Base."**
   - This AMI features a full graphical user interface, making it ideal for managing Adobe Creative Cloud applications directly and handling tasks visually.
   - While there is also a **"Microsoft Windows Server 2022 Core Base"** version optimized for command-line use, it has a lighter system footprint and enhanced security but is less suited for our needs which require a graphical interface.
4. Select the **"Windows Server 2022 Base AMI"** and choose the **"g4dn.2xlarge"** instance type.
5. Create a key pair for secure operations:
   - Click on **"Create Key Pair."**
   - Name it **"AdobeCloudKey."**
   - Select **"RSA"** as the key type, and **"pem"** as the file format.
   - Download and save the key pair; this file is essential for decrypting the Windows administrator password after the instance launches.
6. For network settings, use the default VPC and subnets to keep the setup straightforward.
7. Enhance security by creating a dedicated security group:
   - Under network settings, click **"Edit."**
   - For the security group name, enter **"AdobeCC-SG"** with a brief description such as **"Security settings for Adobe Creative Cloud applications."**
   - You'll initially see a default rule that allows inbound RDP traffic on port 3389 from anywhere. This is too broad.
   - Modify this setting by selecting **"My IP"** under the source to restrict RDP access to your current IP address only. This change ensures that only your device can establish a secure remote desktop connection to the instance.
8. Configure storage volumes:
   - The default configuration includes a 30 GB gp2 volume. While generally sufficient for the operating system, the demands of Adobe After Effects require more space.
   - Expand this default gp2 volume to ensure there's enough room for application installations without compromising system performance. Increase the size of the gp2 volume to **50GB.**
   - To further optimize performance, add a separate EBS volume dedicated specifically to After Effects for caching purposes. This separation allows isolating heavy read-write operations from the OS drive, enhancing system responsiveness and application efficiency.
   - Configure a new gp3 volume, known for its cost-effectiveness and higher performance metrics like provisioned IOPS and throughput.
   - Click **"Add New Volume,"** choose **gp3** as the volume type, and set the size to **100GB.**
9. Before finalizing the instance setup, click on **"Advanced Details,"** and enable **"Termination Protection."** This feature prevents the instance from being accidentally terminated, safeguarding your environment against potential disruptions.
10. Once all settings are configured, click **"Launch Instance"** to start your new, optimized Adobe Creative Cloud environment.

## Establishing a Remote Desktop Connection

Once the instance is up and running, establish a remote desktop connection from your MacBook. Use the `Microsoft Remote Desktop` client for this purpose.

1. Download and install the Microsoft Remote Desktop client on your MacBook. If you don't have it already, you can get it from the Mac App Store.
2. Open the Microsoft Remote Desktop application; you're now ready to connect to your EC2 instance.
3. Go back to the EC2 Management Console, and retrieve your Instance's Public DNS:
   - In the instances section, select the instance you've just launched.
   - Locate the **"Public IPv4 IP"** DNS field.
   - Copy this DNS address to your clipboard. This is the address you'll use to connect to your instance.
4. Get the Windows Administrator Password:
   - Still in the Instances section, with your instance selected, click on the **"Actions"** button.
   - From the drop-down menu, choose **"Security"** and select **"Get Windows Password."**
   - You'll be prompted to upload the key pair file you downloaded earlier.
   - Once uploaded, AWS will decrypt the password for you.
   - Copy this password; you'll need it to log in.
5. Set up the connection in Microsoft Remote Desktop:
   - In the Microsoft Remote Desktop client, click **"Add PC."**
   - In the **"PC Name"** field, enter the IPv4 Public IP or Public DNS of your instance.
   - Under **"User Account,"** click **"Add User Account."**
   - Enter **"Administrator"** as the user name and paste the decrypted Windows password you obtained from the AWS console.
   - If you're using a Mac with a Retina display, select the **"Display"** tab and check the **"Optimize for Retina displays"** option. This ensures a sharp, high-resolution interface matching your Mac's display capabilities.
   - Leave the other settings at their defaults.
   - After setting up the connection, click **"Add".**
6. Double-click on the newly created connection to initiate the session.
   - You may receive a warning that the certificate could not be verified; this is expected.
   - Click **"Continue"** to proceed.

You should now be connected to your EC2 instance and see the Windows desktop environment.

## Setting up the AWS CLI and Configuring Credentials

Once connected to the Windows desktop environment you may notice that GPU metrics are not visible in the Task Manager's Performance tab. To utilize the GPU, set up the AWS CLI for essential AWS interactions, including fetching the latest NVIDIA drivers to configure the GPU for use.

1. In the search box next to the **"Start"** menu, type **"PowerShell"** and right-click on **"Windows PowerShell".**
2. Select **"Run as administrator"** to open PowerShell with administrative privileges.
3. To download and install the AWS CLI, execute the following command in PowerShell:

   ```powershell
   Invoke-WebRequest -Uri "https://awscli.amazonaws.com/AWSCLIV2.msi" -OutFile "AWSCLIV2.msi"
   Start-Process msiexec.exe -Wait -ArgumentList "/i AWSCLIV2.msi"
   aws --version
   ```

4. If you encounter any problems with downloading or installing the AWS CLI using PowerShell, or if you prefer a manual approach, you can download directly from the [AWS](https://aws.amazon.com/cli/){:target="_blank"}.
5. After installation, restart PowerShell.
6. Run `aws --version` to confirm the successful installation of AWS CLI.
7. Configure the AWS CLI with your AWS credentials. You can do this by running `aws configure`.
8. You will be prompted to enter your AWS Access Key ID and Secret Access Key, which you can get from your IAM user details in the AWS Management Console.
9. For the default region name, enter the region code where your EC2 instance is located, such as **"us-east-1"**

## Installing NVIDIA GRID Drivers on Your Windows Instance

The next step is to install NVIDIA GRID drivers. These drivers are critical as they enable GPU virtualization. This feature is essential for efficiently leveraging the EC2 instance's NVIDIA GPU for graphics-intensive applications like Adobe After Effects, ensuring smooth operation and optimal performance. By installing these drivers, you can take full advantage of the accelerated graphics capabilities necessary for complex rendering tasks and enhanced video editing workflows.

1. To begin the installation, download the drivers from Amazon S3 to your desktop. Use the following PowerShell commands:

   ```powershell
   $Bucket = "ec2-windows-nvidia-drivers"
   $KeyPrefix = "latest"
   $LocalPath = "$home\Desktop\NVIDIA"
   $Objects = Get-S3Object -BucketName $Bucket -KeyPrefix $KeyPrefix -Region us-east-1
   foreach ($Object in $Objects) {
       $LocalFileName = $Object.Key
       if ($LocalFileName -ne '' -and $Object.Size -ne 0) {
           $LocalFilePath = Join-Path $LocalPath $LocalFileName
           Copy-S3Object -BucketName $Bucket -Key $Object.Key -LocalFile $LocalFilePath -Region us-east-1
       }
   }
   ```

3. After downloading, open the installation file on your desktop to begin the setup.
4. Follow the on-screen instructions to complete the installation.
5. To verify that the GPU is functioning properly and is fully integrated with your system, check the Device Manager. This step confirms the successful installation of the NVIDIA GRID drivers.

## Quick Start with NVIDIA RTX Virtual Workstation AMI

Let's explore a simpler method by launching the `NVIDIA RTX Virtual Workstation AMI` eliminating the need for manual driver installations.

1. Navigate to the AWS EC2 Management Console and click on **"Launch Instance."**
2. Name your instance **"AdobeCC-AE-Instance".**
3. Instead of selecting the Windows Server AMI, use the search bar to find the **"NVIDIA RTX Virtual Workstation AMI"** with the AMI ID: **ami-0a12c6decb9fdb363**. This pre-configured AMI comes with NVIDIA drivers pre-installed, streamlining the setup process significantly.
4. Choose the appropriate instance type for your needs, such as the **"g4dn.2xlarge"** instance type. This instance type offers a good balance of performance and cost-efficiency for Adobe Creative Cloud applications.
5. Create a key pair for secure operations:
   - Click on **"Create Key Pair."**
   - Name it **"AdobeCloudKey."**
   - Select **"RSA"** as the key type, and **"pem"** as the file format.
   - Download and save the key pair; this file is essential for decrypting the Windows administrator password after the instance launches.
6. For network settings, use the default VPC and subnets to keep the setup straightforward.
7. Enhance security by creating a dedicated security group:
   - Under network settings, click **"Edit."**
   - For the security group name, enter **"AdobeCC-SG"** with a brief description such as **"Security settings for Adobe Creative Cloud applications."**
   - You'll initially see a default rule that allows inbound RDP traffic on port 3389 from anywhere. This is too broad.
   - Modify this setting by selecting **"My IP"** under the source to restrict RDP access to your current IP address only. This change ensures that only your device can establish a secure remote desktop connection to the instance.
8. Configure storage volumes:
   - The default configuration includes a 30 GB gp2 volume. While generally sufficient for the operating system, the demands of Adobe After Effects require more space.
   - Expand this default gp2 volume to ensure there's enough room for application installations without compromising system performance. Increase the size of the gp2 volume to **50GB.**
   - To further optimize performance, add a separate EBS volume dedicated specifically to After Effects for caching purposes. This separation allows isolating heavy read-write operations from the OS drive, enhancing system responsiveness and application efficiency.
   - Configure a new gp3 volume, known for its cost-effectiveness and higher performance metrics like provisioned IOPS and throughput.
   - Click **"Add New Volume,"** choose **gp3** as the volume type, and set the size to **100GB.**
9. Before finalizing the instance setup, click on **"Advanced Details,"** and enable **"Termination Protection".** This feature prevents the instance from being accidentally terminated, safeguarding your environment against potential disruptions.
10. Once all settings are configured, click **"Launch Instance"** to start your new, optimized Adobe Creative Cloud environment.

With the NVIDIA RTX Virtual Workstation AMI, you'll have a GPU-accelerated environment ready to run Adobe After Effects and other Creative Cloud applications without the hassle of manual driver installations.

## Setting Up Adobe Creative Cloud
Next, download and install Adobe Creative Cloud.

1. Open Microsoft Edge, and go to the **Adobe Creative Cloud website.**
2. Sign in to your Adobe account with your credentials.
3. Once logged in, you will see an option to download the Creative Cloud desktop app.
4. While downloading, you may encounter a security warning from Windows preventing the installer from running immediately:
   - If a security prompt appears when you try to open the downloaded file, right-click on the file in the download bar and select **"Keep"**.
   - Then click **"Show more"** and then choose **"Keep anyway"**. This action confirms that you trust the download and wish to proceed.
5. Now that the file is unblocked, you can open the installer.
6. If you see a JavaScript warning during Adobe After Effects installation through the Creative Cloud desktop app, it usually means your OS settings need tweaking. Adobe apps often need JavaScript enabled for proper function, especially during setup.
7. On Windows, Adobe products may rely on Internet Explorer settings, so ensure JavaScript is enabled there, even if you don't use it as your main browser:
   - Open Internet Explorer.
   - Click on the gear icon and click on **"Internet Options"**.
   - Go to the **"Security"** tab.
   - Click on the **"Internet"** icon, then click the **"Custom level"** button.
   - Scroll down to the **"Scripting"** section.
   - Under **"Active Scripting"**, select **"Enable"**.
   - Click **"OK"** to close the Security Settings window, then **"OK"** again to close Internet Options.
8. After making these changes, install Adobe After Effects again.

## Configuring the EBS Volume for Adobe After Effects
Ensure that the EBS volume you previously attached is recognized and properly activated within your EC2 instance.

1. To make your EBS volume visible and usable in your EC2 Windows instance, right-click on the **"Start"** menu and select **"Disk Management"**. This utility will show you all the disks attached to your instance.
2. Right-click on the unallocated space of your newly initialized disk. Select **"New Simple Volume"**. This will launch the New Simple Volume Wizard.
3. Follow the wizard to specify the volume size, assign a drive letter, format the volume with a file system (typically NTFS for Windows), and set the Volume Label (e.g., **"After Effects Cache"**). Click **"Finish"** to complete the setup.
4. After setting up and formatting the new EBS volume in your EC2 instance, prepare it for use with Adobe After Effects by creating specific folders for caching. Since After Effects cannot select an empty drive directly for cache purposes, create at least one folder on the new drive:
   - Open **"This PC"** and navigate to the new drive, labeled **"After Effects Cache"**.
   - Right-click in the drive window, select **"New"**, then **"Folder"**, and create two folders: one named **"Disk Cache"** and another named **"Conformed Media Cache"**.
5. Next, configure Adobe After Effects to use this drive:
   - Open Adobe After Effects.
   - Go to **"Edit"** > **"Preferences"** > **"Media & Disk Cache"**.
   - For the Disk Cache, click **"Choose Folder"** and navigate to the **"Disk Cache"** folder you just created on the new drive. Select this folder to store the intermediate renders.
   - For the Conformed Media Cache, navigate to the same preferences panel and under **"Conformed Media Cache"**, click **"Choose Folder"** and select the **"Conformed Media Cache"** folder you created. This folder will store processed media files necessary for quick access during project editing.
   - Set the minimum disk size cache to **50GB** to allow room for growth in After Effects projects.

> Using a separate drive for caching improves After Effects by speeding up rendering and previewing. It prevents the main system drive from becoming overloaded, which helps maintain the overall responsiveness and stability of your system. Managing and scaling storage becomes more straightforward, allowing you to adjust resources based on project requirements without major system reconfigurations.
{: .prompt-tip }

## Enabling Audio Playback on Windows EC2 Instances

To enable audio playback on your Windows EC2 instance, which is typically disabled by default in server editions of Windows, start the Windows Audio service and set it to automatically launch at each reboot.

1. Open the Run dialog by typing **"run"** into the Windows search box and entering **"services.msc"**. This action will open the Services management console.
2. Scroll through the list until you find the **"Windows Audio"** service.
3. Right-click on **"Windows Audio"** and choose **"Properties"**.
4. In the Properties window, set the **"Startup type"** to **"Automatic"**. This ensures that the audio service will start automatically every time the system boots up.
5. Click **"Start"** to initiate the service immediately.
6. Click **"Apply"** and then **"OK"** to save your changes.
7. With these settings, your instance will be configured to play audio using its on-board capabilities.

By following the steps outlined in this post, you now have a powerful, GPU-accelerated AWS environment tailored for Adobe Creative Cloud and After Effects workflows. Whether you chose the manual setup path or leveraged the pre-configured NVIDIA RTX Virtual Workstation AMI, you've successfully deployed a cloud-based solution that utilizes the capabilities of NVIDIA GPUs without the need for expensive local hardware investments.

## Video Tutorial
{% include embed/youtube.html id='bXe3fCoys5M' %}