---
title: "AWS Console Demos with Camtasia and After Effects for YouTube"
date: 2025-12-23 18:00:00 +0000
categories: [After Effects, Video Production]
tags: [Camtasia, After Effects, Screen Recording, YouTube, Video Production]
description: "A workflow for recording AWS Console demos and exporting 4K video for YouTube. Covers display settings, Camtasia configuration, After Effects composition, and Media Encoder export settings."
image:
  path: /assets/img/headers/awsconsole.webp
  lqip: data:image/webp;base64,UklGRmoAAABXRUJQVlA4IF4AAACQAwCdASoUAAsAPzmGulQvKSWjMAgB4CcJZgCdAB5pdswaGsAAAP6vjUaN0i/Pg3Ony42DQTbz01kQ412qdos7+cdtuzQLhn5izoZWLrtOOiACL6tbozWUE8LnMhAA
---

## Overview

This post documents a practical workflow for recording AWS Console screen captures and exporting them as high-quality 4K video for YouTube. The workflow uses Camtasia for capture, After Effects for compositing, and Adobe Media Encoder for final export. The goal is sharp, readable UI text, both at full screen and when footage is scaled inside device frame mockups.

### Problem

Recording AWS Console walkthroughs at 1920×1080 generally looked fine during capture, especially when uploaded directly to YouTube. The limitations only became obvious once I started importing recordings into After Effects and scaling them for device frame mockups.

### Solution

After testing several resolutions on my 5K display, I initially settled on 2560×1440 as a good compromise. Anything higher made the AWS Console feel cramped and forced me to rely too heavily on browser zoom, while 1080p didn't leave enough resolution headroom for compositing.

At 1440p, the UI remains comfortable to work with, the capture retains significantly more detail than 1080p, and scaling to a 4K timeline stays clean and predictable.

Why 2560×1440 works:

- **Higher than 1440p** — UI becomes uncomfortably small during recording, even with browser zoom
- **1080p** — insufficient resolution headroom; text softness becomes obvious when scaling
- **1440p** — nearly 80% more pixels than 1080p, providing enough detail for compositing and a clean 1.5× upscale to 4K

### Pushing Further: 3200×1800

After working with 1440p, I tested whether a higher capture resolution could improve device frame quality. The Apple Studio Display offers 3200×1800 (QHD+) as an intermediate step before jumping to 5K.

| Resolution | Chrome Zoom | AE Full Screen Scale | AE Device Frame Scale |
|------------|-------------|----------------------|----------------------|
| 2560×1440 | 125% | 150% | ~85% |
| 3200×1800 | 175% | 120% | ~70% |

At 3200×1800 with 175% Chrome zoom, the UI remained comfortable and the additional pixels produced noticeably sharper results when scaling down for device frames. The gentler 120% upscale for full-screen shots also meant less reliance on sharpening in post.

I now use 3200×1800 as my default capture resolution.

The next step up on the Studio Display is 5120×2880, but this exceeds the 4K composition size. Recording at 5K would require scaling *down* to fit the timeline, which defeats the purpose of capturing extra pixels for flexibility. After testing various scale percentages in After Effects, 3200×1800 is the practical ceiling for this workflow on the Studio Display.

### Display Resolution Comparison

I have access to both an Apple Studio Display (5K) and a Dell U2723QE (4K). Here are the available resolutions on each:

| Apple Studio Display | Dell U2723QE |
|---------------------|--------------|
| 5120×2880 | 3840×2160 |
| 3200×1800 | 3360×1890 |
| 2880×1620 | 3200×1800 |
| 2560×1440 (Default) | 3008×1692 |
| 2048×1152 | 2560×1440 |
| 1920×1080 | 2304×1296 |
| 1600×900 | 2048×1152 |
| 1440×810 | 1920×1080 (Default) |
| 1280×720 | |

The Dell offers 3360×1890 and native 3840×2160, which could theoretically provide even more headroom. However, these require 185-200% browser zoom, making the console cramped during recording. The marginal quality gains are unlikely to be worth the discomfort.

### Why 4K Export?

The recording resolution and export resolution are intentionally different.

**1440p (2560×1440)** or **QHD+ (3200×1800)** is the capture resolution. Both keep the AWS Console UI readable during recording. **4K (3840×2160)** is the export resolution. The footage scales up to fill the 4K frame—150% for 1440p, 120% for 3200×1800.

The reason for exporting at 4K comes down to how YouTube processes uploads. YouTube applies better compression codecs (VP9 or AV1) to 4K uploads, so a 4K upload looks sharper at 1080p playback than a native 1080p upload. This workflow takes advantage of that encoding pipeline.

Both source resolutions provide flexibility for device frame compositions. When scaling footage down to fit inside a laptop or monitor mockup, starting with more pixels produces a cleaner result. The 3200×1800 source has a clear advantage here, offering more pixels to discard when scaling down.

## Display Configuration

Open **System Settings → Displays** and set the resolution.

For the baseline workflow, use **2560 × 1440**. For improved device frame quality, use **3200 × 1800**.

| Resolution | Name | Best For |
|------------|------|----------|
| 2560×1440 | QHD | Balanced workflow, comfortable UI |
| 3200×1800 | QHD+ | Sharper device frames, still workable UI |

### Browser Zoom

Chrome zoom compensates for the higher resolution by scaling web content to a comfortable size. The zoom setting affects only the browser and does not reduce recording quality.

Open Chrome and navigate to **Settings → Appearance → Page zoom**.

| Display Resolution | Chrome Zoom |
|-------------------|-------------|
| 2560×1440 | 125% |
| 3200×1800 | 175% |

At these zoom levels, the AWS Console appears similar to how it would look at 1080p, but the recording captures more pixel data for scaling operations in After Effects.

> Chrome zoom only affects browser content. It does not reduce recording quality or change the capture resolution.
{: .prompt-info }

## Camtasia Configuration

Camtasia handles screen recording only. All compositing and effects happen in After Effects.

### Project Settings

Open **Camtasia → Settings → Project** and set **Canvas Dimensions** to match your display resolution.

| Display Resolution | Camtasia Canvas |
|-------------------|-----------------|
| 2560×1440 | QHD (2560x1440) |
| 3200×1800 | Custom: 3200x1800 |

For 3200×1800, Camtasia doesn't have a preset. Select **Custom** and enter the dimensions manually.

The default "Maximum 1080p HD" would downsample the recording before export, discarding pixel data useful for After Effects.

### Recording Settings

Open **Camtasia → Settings → Recording** and verify the following:

| Setting | Value |
|---------|-------|
| Target Capture Frame Rate | Full-motion (30 fps) |
| Camera Encoding | h264 |

### Export Settings

Select **File → Export** and open **Advanced Export Options**.

| Setting | Value |
|---------|-------|
| Dimensions | Current (match your recording resolution) |
| Data Rate | Custom: 20,000 kbits/sec |
| Compression Type | H.264 |
| Keyframe Rate | 30 frames |
| Profile | High |
| Entropy | CABAC |

> The default Camtasia bitrate is often too low for screen recordings with text. Compression artifacts around text edges become more visible after scaling and re-encoding. A higher bitrate here prevents quality loss downstream.
{: .prompt-tip }

Audio settings are not relevant for this workflow because I record audio separately and add it in After Effects.

## After Effects Composition

After Effects handles compositing, including scaling footage for full-screen shots or positioning it within device frame mockups.

### Composition Setup

Create a new composition:

| Setting | Value |
|---------|-------|
| Width | 3840 px |
| Height | 2160 px |
| Pixel Aspect Ratio | Square Pixels |
| Frame Rate | 30 fps |
| Resolution | Full |

### Importing Footage

Import the Camtasia export and drag it into the composition.

The footage appears at 100% scale within the 3840×2160 composition, with black bars visible around it. After Effects scale percentages are relative to the source footage dimensions, not the composition size.

> When you import footage into a larger composition, After Effects does not automatically scale it to fit. This is different from how some other editing applications handle imported media.
{: .prompt-info }

### Scaling

For full-screen shots, scale the footage to fill the 4K frame:

| Source Resolution | Full Screen Scale |
|-------------------|-------------------|
| 2560×1440 | 150% |
| 3200×1800 | 120% |

For device frame mockups, use clean percentages where possible:

| Scale | Use Case |
|-------|----------|
| 100% | Original size, black bars visible |
| 85% | Large device frame (1440p source) |
| 80% | Medium device frame |
| 70% | Large device frame (3200×1800 source) |
| 50% | Half size |

### Quality Settings

Select the footage layer and set the quality to **Best**.

Enable **Bicubic Sampling** by clicking the layer switch in the timeline panel (the icon resembles a curved line). Bicubic sampling produces smoother results than the default bilinear sampling when scaling.

### Sharpening

Scaling footage up introduces slight softness. A subtle sharpening effect compensates for this and helps text survive YouTube compression.

Apply **Effect → Blur & Sharpen → Unsharp Mask**:

| Source Resolution | Amount | Radius | Threshold |
|-------------------|--------|--------|-----------|
| 2560×1440 | 50 | 1.0 | 0 |
| 3200×1800 | 25-30 | 1.0 | 0 |

The 150% upscale from 1440p benefits more from sharpening than the gentler 120% upscale from 3200×1800. Preview at 100% zoom before committing. If the footage looks sharp without the effect, skip it. Over-sharpening is worse than slight softness.

> To preview at 100% zoom, select **View → Resolution → Full** and use the scroll wheel to view at actual pixel size.
{: .prompt-tip }

## Export Configuration

Select **File → Export → Add to Adobe Media Encoder Queue**.

### Media Encoder Settings

| Setting | Value |
|---------|-------|
| Format | H.264 |
| Preset | Match Source - High Bitrate |

The "Match Source - High Bitrate" preset inherits the composition resolution and frame rate while allowing manual bitrate configuration.

### Video Settings

Under the **Video** tab:

| Setting | Value |
|---------|-------|
| Width | 3840 |
| Height | 2160 |
| Frame Rate | 30 |
| Field Order | Progressive |
| Profile | High |

Under **Encoding Settings**:

| Setting | Value |
|---------|-------|
| Bitrate Encoding | VBR, 2 pass |
| Target Bitrate | 40 Mbps |
| Maximum Bitrate | 60 Mbps |

> Selecting VBR 2-pass automatically switches Performance from Hardware Encoding to Software Encoding. This is expected behaviour—2-pass encoding requires software processing.
{: .prompt-info }

VBR 2-pass encoding analyses the video twice to allocate bitrate more efficiently, producing better quality than single-pass at the cost of longer render times.

### Render Quality

At the bottom of the export settings panel, enable **Use Maximum Render Quality**.

Leave "Render at Maximum Depth" disabled—it increases render time without visible benefit for screen recordings.

## Summary

### Baseline Workflow (1440p)

| Stage | Setting | Rationale |
|-------|---------|-----------|
| Display | 2560×1440 | Clean scaling to 4K, comfortable UI |
| Browser | 125% zoom | Readable UI without reducing capture quality |
| Camtasia | QHD, 20,000 kbps | Preserves text detail in intermediate file |
| After Effects | 4K composition | YouTube uses better codec for 4K uploads |
| After Effects | 150% scale (full screen) | Fills 4K frame |
| After Effects | Bicubic + Unsharp Mask 50/1/0 | Compensates for upscale softness |
| Media Encoder | VBR 2-pass, 40/60 Mbps | Maximum quality source for YouTube |

### Upgraded Workflow (3200×1800)

| Stage | Setting | Rationale |
|-------|---------|-----------|
| Display | 3200×1800 | More pixels for device frame scaling |
| Browser | 175% zoom | Readable UI at higher resolution |
| Camtasia | Custom 3200×1800, 20,000 kbps | Captures full resolution |
| After Effects | 4K composition | YouTube uses better codec for 4K uploads |
| After Effects | 120% scale (full screen) | Gentler upscale, sharper result |
| After Effects | Bicubic + Unsharp Mask 25-30/1/0 | Light sharpening if needed |
| Media Encoder | VBR 2-pass, 40/60 Mbps | Maximum quality source for YouTube |

### Which to Choose?

The 1440p workflow is simpler and produces good results for most use cases. The 3200×1800 workflow provides noticeably sharper device frame compositions at the cost of a more cramped UI during recording.

For videos that are primarily full-screen console walkthroughs, 1440p is sufficient. For videos that feature device frame mockups prominently, 3200×1800 is worth the tradeoff.

Recording beyond 3200×1800 on the Studio Display means jumping to 5120×2880, which exceeds the 4K composition size and provides no benefit. On a 4K display like the Dell U2723QE, resolutions of 3360×1890 or 3840×2160 are available but require 185-200% browser zoom, making the console increasingly difficult to work with. The marginal quality gains are unlikely to be worth the discomfort during recording.
