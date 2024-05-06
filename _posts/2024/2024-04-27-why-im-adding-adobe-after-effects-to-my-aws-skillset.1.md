---
title: "Why I'm Adding Adobe After Effects to My AWS Skillset"
date: 2024-04-11 08:00:00 - 0500
categories: [Adobe Creative Cloud, After Effects]
tags: [adobe, after effects, animation, creative cloud, illustrator, premiere pro]
image:
  path: /assets/img/headers/aftereffects.webp
  lqip: data:image/webp;base64 iVBORw0KGgoAAAANSUhEUgAAAAoAAAAFBAMAAACOSmBbAAAAHlBMVEUAAFsAAFoBAVsICGEGBl8BAVwvMIwtLooAAVoKCmODQ3rkAAAAIElEQVQIHWNgYBBgAAImkwAgyZjeACRZLRWAJIMgAwMAHP0B7kNteIIAAAAASUVORK5CYII=
---

I’ve always been intrigued by the creative side of technology, particularly the animation capabilities of `Adobe After Effects`, a digital visual effects and motion graphics application widely used in the post-production process of film making, video games, and television production. 

Despite my interest, there wasn't a compelling reason to learn it until I began working with AWS. My experience in cloud computing grew as I built solutions and shared them on my YouTube channel, [Hands On with Digital Den](https://www.youtube.com/channel/UCHoxUz0IfdhOieSXox_mwSw){:target="_blank"}. 

Recently, I was faced with the choice of either pursuing another AWS certification or diversifying my skills with Adobe After Effects, I opted for the latter. This decision is driven by a desire to develop a unique skill set that combines creative tools with cloud computing functionalities.

>
With Adobe After Effects, I am planning to create custom motion graphics and visual effects to enhance the educational experience. My goal is to add a layer of clarity and engagement that surpasses traditional screen recording methods.
{: .prompt-info }

## TechSmith Camtasia
Camtasia has been my go-to tool for creating video demos. It allows me to record my screen, edit the footage, and add basic transitions and effects. The software's ability to handle multiple audio and video tracks simultaneously makes it perfect for layering tutorial elements effectively. 

Here's a screenshot from a recent lesson I put together for Cloud Academy, captured during the editing process in Camtasia.

![Camtasia](/assets/img/posts/camtasia.webp)
_Create Web Applications Using Amplify_

Despite its strengths, I've found that Camtasia has limitations, particularly when it comes to creating more dynamic and engaging animations.

## Cloud Academy
My passion for creating content eventually led me to a job at Cloud Academy, a company that specializes in cloud technology training.

At Cloud Academy lessons and courses created by content creators like me are transformed into animated explainer videos by a team of motion designers, graphic designers, and previs artists:


{% include embed/youtube.html id='eOd5w78HB6k' %}

The high-quality animations at Cloud Academy motivated me to start learning Adobe After Effects to add similar animations to my videos. While my primary focus remains on producing high-quality AWS content, I aim to integrate animation clips throughout my hands-on demos to clarify complex cloud concept.

Fortunately, Cloud Academy provides a free subscription to Skillshare — an online learning community with thousands of classes for creative and curious people, on topics including illustration, design, photography, and video. It was there I found [The Beginner's Guide to Adobe After Effects](https://www.skillshare.com/en/classes/the-beginners-guide-to-adobe-after-effects/1758053045){:target="_blank"} by Jake Bartlett. This class was my starting block for animation.

## Adobe After Effects The Beginners Guide
Jake Bartlett's class, proved to be an invaluable resource. This comprehensive 6-hour class covered a wide range of essential topics, including:

- Resolution & Frame Rate
- Composition Setup & Parenting
- Pre Comps
- Anchor Points
- Animating with KeyFrames & Pre Comps
- Applying Affects
- Animating the Transition
- Camera Movement
- Looping & Exporting Animations

The class provides all necessary artwork, so there's no need to design anything from scratch, instead you can focus on learning to animate using the assets provided for the project.

In the class project, I developed a looping animation designed specifically for Instagram, rendered in sharp 1080 x 1080 resolution as an MP4 file: [Taco Tuesday](https://youtube.com/shorts/3r48vZNItfs){:target="_blank"}


> After finishing the class, I aimed to apply what I had learned by creating my own animation based on the class. Reinforcing my skills through practical application is how I best absorb new information. This project allowed me to practice the techniques discussed in the class and further integrate my understanding of visual effects.
{: .prompt-tip }

## Adobe Illustrator
`Adobe Illustrator` is a vector graphics editing software widely used for creating and manipulating digital artwork. It excels in allowing users to produce designs with precision and scalability, making it ideal for both print and web media. I began a 7-day trial with Adobe Illustrator to learn how to tailor vector graphics for my animation project, `EC2 Road Rash` 

![Artwork](/assets/img/posts/ec2-road-rash.webp){: .shadow }
_Artwork_

Here are the specific changes I made:
- I renamed the arcade game to `EC2 Road Rash` to better align with the AWS theme.
- I designed new artwork, including an animated version of myself with alternating expressions—one with an open mouth and one with a closed mouth—to add a dynamic element.
- I created images of an AWS bus topped with an EC2 instance and a standalone EC2 instance image to integrate AWS concepts into the game.
- To achieve a retro aesthetic, I pixelated the images, giving them an 8-bit look reminiscent of classic video games.

Given that my primary platform for video sharing is YouTube, I adjusted the dimensions of the animation to 1920 x 1080 pixels, which is more suitable for YouTube's format compared to the smaller Instagram size used in the class.

### Animating the Wheels
The AWS bus image that I used in the animation was originally found at the `AWS On Tour: Developer Tooling Edition Event` 

I liked the bus's design and decided to incorporate it into my animation project. However, to add a dynamic element to the animation, I wanted the bus to bounce on its wheels, which required some modifications to the original image. To accomplish this, I first needed to modify the bus image to animate the wheels independently from the bus body. In Adobe Illustrator, I achieved this by:
- Creating a separate layer specifically for the wheels.
- Isolating the wheels and positioning them on the new layer.

After making these adjustments, I saved the updated Illustrator file and imported it into Adobe After Effects as a composition. This process allowed me to access the `truck.ai` file as a composition in After Effects, where I could manipulate both the truck and wheels layers independently.

Within After Effects, isolating the wheels on a separate layer facilitated specific animations for the wheels while keeping the bus body steady:
- **Layer Isolation:** The wheels were placed on their own layer, allowing for targeted animations independent of the bus body.
- **Position Keyframes:** Keyframes were added to the wheel layer to simulate a bouncing effect, providing dynamic movement.
- **Independent Movement:** Layer separation enabled the wheels to move independently, mimicking the bus’s reaction to the road’s surface, which added realism to the animation.

![Artwork](/assets/img/posts/truck.webp){: .shadow }
_AWS Truck_

## Adobe After Effects
Having customized the graphics in Adobe Illustrator, I then moved on to animate these elements in Adobe After Effects to bring the arcade-style game `EC2 Road Rash` to life. This screenshot from Adobe After Effects outlines some aspects of my arcade-style animation project. Below is an explanation of the tools and effects visible in this image, demonstrating specific functionalities:

![Artwork](/assets/img/posts/timeline.webp){: .shadow }
_Timeline_

**Animation Techniques Used:**
1. **Keyframe Animation:**
   - The AWS bus was animated using position keyframes to simulate movement around the screen.
   - EC2 instances were given a combination of position and rotation keyframes to create the effect of being thrown from the bus towards the character.

2. **Character Dynamics:**
   - The main character, designed to eat the incoming EC2 instances, was animated using opacity keyframes within a pre-composition to create an opening and closing mouth effect.

3. **Ease and Timing:**
   - Easy Ease was applied to the keyframes to smooth transitions and enhance the flow of movements, contributing to a more natural arcade game aesthetic.

4. **Visual Effects:**
   - An adjustment layer was added to incorporate several effects: CC Ball Action, Glow, and Gaussian Blur, all contributing to a retro arcade-style visual theme.

5. **Score Display:**
   - A player score display was integrated at the top of the screen, animated with the numbers effect to dynamically reflect the game’s score.

While this description covers the visible elements and effects in this screenshot, it is only a part of the overall project. The full animation includes additional techniques and details not shown here.

## Adobe Premiere Pro
Following the animation process in After Effects, the project was brought into Adobe Premiere Pro for assembly. `Adobe Premiere Pro` is a video editing software designed for editing various types of media and used primarily for post-production work. I began exploring this tool with a 7-day trial, using it to add and synchronize sound effects with animations from After Effects. 

A great feature of Premiere Pro is its ability to import After Effects compositions directly into the timeline, allowing for real-time updates without the need for rendering. This functionality streamlines the process of adjusting audio and visual elements simultaneously. As I continue to develop my skills in video production, I plan to utilize Premiere Pro to expand my capabilities in creating more polished videos.

In the resulting animation, the AWS bus launches EC2 instances, and the player uses a joystick to direct these at my animated character, who 'eats' the instances as they approach.

Here's a look at my first animation created for YouTube:

{% include embed/youtube.html id='axqQS9aCS4o' %}

## Leveraging AWS Computing Power
As my projects in Adobe After Effects grew more complex, incorporating additional effects and techniques, the limitations of my 2017 MacBook Pro with an Intel Core i5 processor and 8GB of RAM became increasingly apparent. With the installation of applications like Illustrator and Premiere Pro, the device frequently ran out of application memory, operated slowly, and took a long time to render animations

![Artwork](/assets/img/posts/application-memory.webp){: .left }
_Adobe After Effects_

### Instance Selection
To address these challenges and accommodate the expanding scope of my work, I explored a solution that leverages AWS cloud computing power. Opting for a `g4dn.2xlarge` EC2 instance, tailored for graphics-intensive applications, proved effective.

| Instance Size                | GPU      | vCPU    | RAM    | On-Demand Price/hr* |
| :--------------------------- | :------- | :------ | :----- | :------------------ |
| g4dn.2xlarge                 | 1        | 8       | 16GB   | $0.752              |


Upon launching the EC2 instance, I connected to it using `Microsoft Remote Desktop` from my MacBook. I installed the necessary `NVIDIA` drivers and `Adobe Creative Cloud` suite, including Adobe After Effects, Illustrator, and Premiere Pro. I then  set up After Effects to optimize the use of the GPU. 

>
By monitoring the Task Manager on the EC2 instance, I could see that the GPU was effectively utilized during the rendering process. This sped up rendering times and ensured that my local machine was free from the heavy lifting, preventing the application memory issues and lag I previously encountered.
{: .prompt-tip }

### Optimizing Storage with EBS Volumes
Despite the powerful EC2 instance, storage became a concern. The default `EBS gp2 30 GiB` volume provided was insufficient for my needs. Adobe After Effects generates and stores a significant amount of cache data during the rendering process, which can quickly fill up available storage space.

Recognizing the importance of sufficient storage for an efficient workflow, I opted for a more high-performance solution — a `io2 100GB` volume. This choice offered higher IOPS (input/output operations per second) and throughput, ensuring smooth operation and minimizing delays in accessing and saving cache files.

While the io2 volume provided excellent performance, I noticed that the EBS volume was costing $8 a day, which wasn't cost-effective, especially considering it was only used for caching purposes. To address this, I replaced the io2 volume with a `100GB gp3` volume. This change didn't compromise performance and was significantly more cost-effective, costing only a fraction of the price.

## Conclusion
In summary, my journey with Adobe After Effects, has been about expanding my skill set to create more engaging content. What began with a focus on After Effects soon extended to include Illustrator and Premiere Pro, allowing me to explore new avenues for creativity and storytelling.

Leveraging AWS cloud computing helped overcome hardware limitations, significantly improving workflow efficiency. By optimizing storage and resource management, I found cost-effective solutions without compromising performance. I hope to continue learning and improving my skills with these tools, integrating dynamic animations into educational content and enhancing the learning experience for audiences interested in cloud technology.

>
The g4dn.2xlarge instance with Windows_Server-2022-English-Full-Base AMI, and 100GB gp3 volume, ran at an approximate cost of just under $2 per hour. This setup serves as a cost-effective solution, especially considering my available AWS credits and my current preference to avoid investing in a new computer.
{: .prompt-info }