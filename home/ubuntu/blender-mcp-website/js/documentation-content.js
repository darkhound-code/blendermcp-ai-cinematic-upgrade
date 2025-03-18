// Documentation Content Structure
const documentationContent = {
  title: "BlenderMCP Ultimate Documentation",
  description: "Comprehensive documentation for the BlenderMCP Ultimate Cinematic Upgrade.",
  sections: [
    {
      id: "getting-started",
      title: "Getting Started",
      subsections: [
        {
          id: "installation",
          title: "Installation",
          content: `
# Installation Guide

Installing BlenderMCP Ultimate is a straightforward process. Follow these steps to get started:

## System Requirements

Before installing, make sure your system meets the following requirements:

- **Blender:** 2.83 or newer
- **Operating System:** Windows 10/11, macOS 10.15+, Linux
- **RAM:** 8GB minimum, 16GB recommended
- **GPU:** NVIDIA GTX 1060 / AMD RX 580 or better
- **Storage:** 500MB for addon, additional space for assets
- **Internet Connection:** Required for asset downloading

## Installation Steps

1. **Download the Addon**
   - Download the latest version of BlenderMCP Ultimate from the [download page](/download.html)
   - Save the ZIP file to a location you can easily access

2. **Open Blender Preferences**
   - Launch Blender
   - Go to Edit > Preferences > Add-ons

3. **Install the Addon**
   - Click "Install..."
   - Navigate to the downloaded ZIP file and select it
   - Click "Install Add-on"

4. **Enable the Addon**
   - Find "AI: BlenderMCP Ultimate" in the addon list
   - Check the box next to it to enable the addon
   - The addon is now installed and ready to use

5. **Verify Installation**
   - The BlenderMCP Ultimate panel should now be available in the sidebar
   - Press N to open the sidebar if it's not already visible
   - Look for the "BlenderMCP Ultimate" tab

## Troubleshooting

If you encounter any issues during installation:

- Make sure you're using a compatible version of Blender
- Check that the ZIP file was downloaded completely
- Try restarting Blender after installation
- Verify that you have administrator privileges on your system

For more detailed troubleshooting, see the [Troubleshooting Guide](#troubleshooting).
          `
        },
        {
          id: "quick-start",
          title: "Quick Start Guide",
          content: `
# Quick Start Guide

This guide will help you get up and running with BlenderMCP Ultimate quickly. We'll create a simple cinematic sequence to demonstrate the basic workflow.

## Setting Up Your First Project

1. **Create a New Blender File**
   - Open Blender and create a new file
   - Save the file to your desired location

2. **Open the BlenderMCP Ultimate Panel**
   - Press N to open the sidebar
   - Click on the "BlenderMCP Ultimate" tab

3. **Connect to Claude**
   - Enter your API key in the settings panel
   - Click "Connect" to establish a connection
   - You should see a "Connected" status message

## Creating Your First Cinematic Sequence

Let's create a simple scene with a character walking through a forest environment.

1. **Set Up the Environment**
   - In the BlenderMCP Ultimate panel, go to "Scene Setup"
   - Type: "Create a forest environment with morning sunlight filtering through trees"
   - Click "Generate Environment"
   - Wait for the environment to be created (progress will be shown in the tracking panel)

2. **Add a Character**
   - Go to the "Character" tab
   - Type: "Add a male explorer character with hiking gear"
   - Click "Import Character"
   - The character will be imported and automatically rigged

3. **Create an Animation**
   - Go to the "Animation" tab
   - With the character selected, type: "Make the character walk along a path through the forest, looking around curiously"
   - Click "Generate Animation"
   - The AI will create keyframes for the walking animation

4. **Add Camera Work**
   - Go to the "Camera" tab
   - Type: "Create a tracking shot that follows the character from behind, then circles around to reveal their face"
   - Click "Generate Camera"
   - A camera with the specified movement will be created

5. **Render the Sequence**
   - Go to the "Rendering" tab
   - Choose your preferred quality settings
   - Click "Render Sequence"
   - The sequence will be rendered with all the specified elements

## Next Steps

Congratulations! You've created your first cinematic sequence with BlenderMCP Ultimate. To learn more about the advanced features, check out the following sections:

- [Scene Setup & Asset Importing](#scene-setup)
- [Character Animation & Motion Control](#animation)
- [Physics & VFX Integration](#physics-vfx)
- [Rendering & Post-Processing](#rendering)

For more detailed tutorials, visit our [Tutorials page](/tutorials.html).
          `
        },
        {
          id: "ui-overview",
          title: "UI Overview",
          content: `
# UI Overview

BlenderMCP Ultimate integrates seamlessly into Blender's interface, providing powerful AI-driven tools while maintaining a familiar workflow. This guide will help you understand the different components of the BlenderMCP Ultimate interface.

## Main Panel

The main BlenderMCP Ultimate panel is located in the sidebar (N panel) of Blender. It contains the following tabs:

### Home Tab

The Home tab provides quick access to common functions and displays your connection status.

- **Connection Status**: Shows whether you're connected to Claude
- **Quick Actions**: Buttons for common tasks
- **Recent Projects**: List of recently opened projects
- **Help & Resources**: Links to documentation and tutorials

### Scene Setup Tab

This tab contains tools for creating and managing environments and assets.

- **Environment Generation**: Create complete environments from text descriptions
- **Asset Import**: Import characters and objects from various sources
- **HDRI Lighting**: Set up lighting using HDRI maps
- **Scene Composition**: Arrange objects in cinematically pleasing ways

### Animation Tab

The Animation tab provides tools for character rigging and animation.

- **Auto-Rigging**: Automatically rig characters using Rigify
- **Animation Generation**: Create animations from text descriptions
- **Motion Library**: Access pre-made animations
- **Animation Editing**: Tools for refining and combining animations

### Physics & VFX Tab

This tab contains tools for adding realistic physics and visual effects.

- **Cloth Simulation**: Set up and control cloth physics
- **Destruction**: Create realistic destruction effects
- **Particle Effects**: Add smoke, fire, and other particle-based effects
- **Weather**: Add rain, snow, and other weather effects

### Camera Tab

The Camera tab provides tools for creating cinematic camera work.

- **Camera Generation**: Create camera setups from text descriptions
- **Shot Types**: Quick access to common shot types (close-up, medium, wide, etc.)
- **Camera Movement**: Tools for creating smooth camera movements
- **Multi-Camera Setup**: Create and manage multiple camera angles

### Rendering Tab

This tab contains tools for rendering and post-processing.

- **Render Settings**: Optimize render settings for quality and speed
- **Post-Processing**: Add color grading and other effects
- **Output Options**: Configure output formats and locations
- **Batch Rendering**: Set up and manage batch renders

### Progress Tracking Panel

The Progress Tracking panel shows the status of all AI operations.

- **Current Operations**: List of currently running operations
- **Progress Bars**: Visual indication of operation progress
- **Time Estimates**: Estimated time remaining for each operation
- **Log Viewer**: Detailed log of all operations

## Context Menus

BlenderMCP Ultimate also adds context menu items throughout Blender for quick access to relevant functions.

- **Object Context Menu**: Right-click on objects for BlenderMCP Ultimate options
- **Timeline Context Menu**: Right-click in the timeline for animation options
- **3D View Context Menu**: Right-click in empty space for scene setup options

## Keyboard Shortcuts

BlenderMCP Ultimate adds several keyboard shortcuts for common operations:

- **Alt+C**: Open the BlenderMCP Ultimate command input
- **Alt+G**: Generate environment from selected text
- **Alt+A**: Generate animation from selected text
- **Alt+R**: Optimize render settings
- **Alt+P**: Toggle Progress Tracking panel

These shortcuts can be customized in the Preferences panel.
          `
        }
      ]
    },
    {
      id: "scene-setup",
      title: "Scene Setup & Asset Importing",
      subsections: [
        {
          id: "environment-generation",
          title: "Environment Generation",
          content: `
# Environment Generation

BlenderMCP Ultimate's environment generation system allows you to create complete, realistic environments from simple text descriptions. This guide explains how to use this powerful feature effectively.

## Basic Environment Generation

To generate a basic environment:

1. Go to the Scene Setup tab in the BlenderMCP Ultimate panel
2. Enter a description of the environment you want to create in the text field
3. Click "Generate Environment"

For example, you might enter:
- "A misty forest at dawn with a small clearing"
- "A futuristic city skyline at night with neon lights"
- "A desert landscape with rock formations and a small oasis"

The AI will analyze your description and create a complete environment including terrain, vegetation, lighting, and atmospheric effects.

## Advanced Environment Parameters

For more control over the generated environment, you can use the advanced parameters:

### Style and Mood

- **Style**: Choose from realistic, stylized, cartoon, fantasy, sci-fi, etc.
- **Mood**: Set the emotional tone (peaceful, tense, mysterious, etc.)
- **Time of Day**: Specify when the scene takes place (dawn, noon, dusk, night)
- **Weather**: Set weather conditions (clear, cloudy, rainy, snowy, etc.)

### Terrain Settings

- **Terrain Type**: Specify the main terrain type (mountains, plains, hills, etc.)
- **Scale**: Set the scale of the terrain features
- **Detail Level**: Control the amount of detail in the terrain
- **Erosion**: Adjust the level of erosion simulation

### Vegetation and Objects

- **Vegetation Density**: Control how much vegetation appears
- **Vegetation Types**: Specify the types of plants and trees
- **Object Placement**: Control the placement of additional objects
- **Population**: Add characters or creatures to the environment

## Environment Templates

BlenderMCP Ultimate includes several environment templates for common scenarios:

- **Natural Landscapes**: Forests, mountains, deserts, beaches, etc.
- **Urban Environments**: Cities, towns, streets, interiors, etc.
- **Fantasy Settings**: Magical forests, castles, alien worlds, etc.
- **Sci-Fi Settings**: Space stations, futuristic cities, alien planets, etc.

To use a template:
1. Select a template from the dropdown menu
2. Customize the parameters as needed
3. Click "Generate Environment"

## Editing Generated Environments

After generating an environment, you can still edit it using standard Blender tools or BlenderMCP Ultimate's refinement options:

- **Refine Region**: Select a region of the environment to regenerate with new parameters
- **Add Elements**: Add specific elements to the existing environment
- **Adjust Lighting**: Fine-tune the lighting setup
- **Modify Terrain**: Sculpt or adjust the terrain

## Performance Considerations

Environment generation can be resource-intensive. Consider these tips for better performance:

- Start with a lower detail level and increase as needed
- Generate environments in stages (terrain first, then vegetation, etc.)
- Use region refinement for detailed areas instead of regenerating the entire environment
- Save your file before generating complex environments

## Examples

Here are some example prompts and the environments they might generate:

- **"A tropical beach at sunset with palm trees and gentle waves"**
  - Creates a beach scene with golden lighting, palm trees, and animated water
  
- **"A cyberpunk alleyway with rain puddles reflecting neon signs"**
  - Generates an urban alley with buildings, neon lights, and reflective puddles
  
- **"A medieval village surrounded by autumn forest with a castle on a hill"**
  - Creates a village with houses, paths, autumn trees, and a castle landmark
          `
        },
        {
          id: "asset-importing",
          title: "Asset Importing",
          content: `
# Asset Importing

BlenderMCP Ultimate provides seamless integration with various asset libraries and marketplaces, allowing you to import characters, objects, and materials directly into your Blender projects.

## Supported Asset Sources

BlenderMCP Ultimate can import assets from the following sources:

### Character Sources
- **Mixamo**: Human characters with animations
- **Ready Player Me**: Customizable avatars
- **Character Creator**: Realistic human characters

### 3D Model Sources
- **Sketchfab**: Diverse collection of 3D models
- **TurboSquid**: Professional 3D assets
- **CGTrader**: Marketplace for 3D models

### Material and Texture Sources
- **Quixel Megascans**: High-quality scanned materials
- **Poliigon**: Materials and textures
- **Texture Haven**: Free PBR materials

## Importing Characters

To import a character:

1. Go to the Scene Setup tab in the BlenderMCP Ultimate panel
2. Select the "Character Import" section
3. Choose a character source (e.g., Mixamo)
4. Enter a description of the character you want
5. Click "Import Character"

For example, you might enter:
- "A male soldier in combat gear"
- "A female business professional in formal attire"
- "A stylized fantasy elf with armor"

The AI will search for the most appropriate character and import it into your scene, automatically setting up materials and, in many cases, rigging.

## Importing Objects and Props

To import objects and props:

1. Go to the Scene Setup tab
2. Select the "Object Import" section
3. Choose an object source (e.g., Sketchfab)
4. Enter a description of the object you want
5. Click "Import Object"

For example:
- "A vintage wooden desk with drawers"
- "A sci-fi laser gun with glowing elements"
- "A medieval stone castle tower"

## Importing Materials

To import materials:

1. Go to the Scene Setup tab
2. Select the "Material Import" section
3. Choose a material source (e.g., Quixel Megascans)
4. Enter a description of the material you want
5. Click "Import Material"

For example:
- "Weathered rusty metal"
- "Polished marble with veins"
- "Mossy forest ground"

## Asset Management

BlenderMCP Ultimate includes an asset management system to help you organize imported assets:

- **Asset Browser**: Browse and search all imported assets
- **Categories**: Automatically categorizes assets by type
- **Tags**: Add custom tags to assets for easier searching
- **Favorites**: Mark assets as favorites for quick access

## Working with Imported Assets

After importing assets, you can:

- **Modify Materials**: Adjust material properties
- **Resize and Position**: Scale and position assets in your scene
- **Add Physics**: Apply physics properties to objects
- **Combine Assets**: Create complex objects by combining multiple assets

## Customization Options

When importing assets, you can customize various aspects:

- **Scale**: Set the scale of imported assets
- **Level of Detail**: Choose between different detail levels
- **Material Quality**: Select material resolution
- **Variants**: Some assets offer variant options (e.g., different colors)

## Troubleshooting

If you encounter issues with asset importing:

- **Connection Issues**: Ensure you have an active internet connection
- **API Limits**: Some sources have daily or monthly usage limits
- **Compatibility**: Some assets may require specific Blender versions
- **Size Limitations**: Very large assets may take longer to import

For more detailed troubleshooting, see the [Troubleshooting Guide](#troubleshooting).
          `
        },
        {
          id: "<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>