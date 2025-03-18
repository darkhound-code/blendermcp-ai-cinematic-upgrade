"""
BlenderMCP Ultimate Cinematic Upgrade - Scene Setup Module
This module handles scene setup including HDRI lighting automation and procedural environment generation.
"""

import bpy
import os
import json
import requests
import tempfile
import random
import math
from pathlib import Path
from mathutils import Vector, Euler

class HDRILightingAutomation:
    """
    Handles HDRI lighting automation based on scene descriptions.
    """
    
    def __init__(self):
        self.hdri_base_url = "https://polyhaven.com/a/hdris"
        self.cache_dir = os.path.join(tempfile.gettempdir(), "blendermcp_hdri_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Dictionary mapping descriptions to HDRI names
        self.hdri_mapping = {
            "sunset": ["sunset_in_the_woods", "venice_sunset", "golden_hour"],
            "sunrise": ["morning_sun", "dawn_meadow", "early_morning"],
            "night": ["night_sky", "moonlit_forest", "starry_night"],
            "indoor": ["office_interior", "studio_lighting", "apartment_interior"],
            "studio": ["studio_small", "photo_studio", "neutral_studio"],
            "forest": ["forest_path", "dense_forest", "misty_forest"],
            "beach": ["tropical_beach", "sandy_shore", "ocean_view"],
            "city": ["city_street", "urban_alley", "downtown"],
            "desert": ["desert_dunes", "arid_landscape", "desert_noon"],
            "mountain": ["snowy_peaks", "mountain_vista", "alpine_meadow"],
            "cloudy": ["overcast_sky", "cloudy_day", "stormy_clouds"],
            "clear": ["clear_blue_sky", "sunny_day", "bright_sky"],
            "rainy": ["rainy_day", "after_rain", "wet_street"],
            "snowy": ["snow_field", "winter_scene", "snowy_forest"],
            "foggy": ["foggy_forest", "misty_morning", "fog_covered_hills"],
            "dramatic": ["dramatic_clouds", "epic_sky", "moody_atmosphere"],
            "warm": ["warm_light", "golden_glow", "sunset_warmth"],
            "cool": ["cool_light", "blue_atmosphere", "winter_cool"],
            "neutral": ["neutral_studio", "balanced_light", "even_lighting"]
        }
    
    def search_hdris(self, description="", limit=10):
        """
        Search for HDRIs based on description.
        
        Args:
            description (str): Description of the desired lighting
            limit (int): Maximum number of results to return
            
        Returns:
            list: List of HDRI dictionaries with id, name, thumbnail_url
        """
        # Parse the description to find matching HDRIs
        matching_hdris = []
        
        # Check for direct matches in our mapping
        for key, hdri_list in self.hdri_mapping.items():
            if key in description.lower():
                for hdri in hdri_list:
                    matching_hdris.append({
                        "id": hdri,
                        "name": hdri.replace("_", " ").title(),
                        "thumbnail_url": f"https://polyhaven.com/thumbnails/{hdri}.png"
                    })
        
        # If no direct matches, return some default options
        if not matching_hdris:
            default_hdris = [
                {"id": "neutral_studio", "name": "Neutral Studio", "thumbnail_url": "https://polyhaven.com/thumbnails/neutral_studio.png"},
                {"id": "clear_blue_sky", "name": "Clear Blue Sky", "thumbnail_url": "https://polyhaven.com/thumbnails/clear_blue_sky.png"},
                {"id": "sunset_in_the_woods", "name": "Sunset in the Woods", "thumbnail_url": "https://polyhaven.com/thumbnails/sunset_in_the_woods.png"},
                {"id": "city_street", "name": "City Street", "thumbnail_url": "https://polyhaven.com/thumbnails/city_street.png"},
                {"id": "forest_path", "name": "Forest Path", "thumbnail_url": "https://polyhaven.com/thumbnails/forest_path.png"}
            ]
            matching_hdris = default_hdris
        
        return matching_hdris[:limit]
    
    def apply_hdri_lighting(self, hdri_name=None, description=None, intensity=1.0, rotation=0.0, background_visible=True):
        """
        Apply HDRI lighting to the scene.
        
        Args:
            hdri_name (str, optional): Name of the HDRI to use
            description (str, optional): Description of the desired lighting
            intensity (float): Intensity of the lighting
            rotation (float): Rotation of the HDRI in degrees
            background_visible (bool): Whether to show the HDRI as background
            
        Returns:
            dict: Result information
        """
        try:
            # If no HDRI name is provided but a description is, search for an HDRI
            if not hdri_name and description:
                hdris = self.search_hdris(description)
                if hdris:
                    hdri_name = hdris[0]["id"]
                else:
                    hdri_name = "neutral_studio"  # Default fallback
            
            # If still no HDRI name, use a default
            if not hdri_name:
                hdri_name = "neutral_studio"
            
            # Set up the world for HDRI lighting
            world = bpy.context.scene.world
            if not world:
                world = bpy.data.worlds.new("World")
                bpy.context.scene.world = world
            
            # Enable nodes for the world
            world.use_nodes = True
            nodes = world.node_tree.nodes
            links = world.node_tree.links
            
            # Clear existing nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes for HDRI setup
            node_coord = nodes.new(type='ShaderNodeTexCoord')
            node_mapping = nodes.new(type='ShaderNodeMapping')
            node_env = nodes.new(type='ShaderNodeTexEnvironment')
            node_background = nodes.new(type='ShaderNodeBackground')
            node_output = nodes.new(type='ShaderNodeOutputWorld')
            
            # Position nodes
            node_coord.location = (-800, 0)
            node_mapping.location = (-600, 0)
            node_env.location = (-400, 0)
            node_background.location = (-200, 0)
            node_output.location = (0, 0)
            
            # Connect nodes
            links.new(node_coord.outputs['Generated'], node_mapping.inputs['Vector'])
            links.new(node_mapping.outputs['Vector'], node_env.inputs['Vector'])
            links.new(node_env.outputs['Color'], node_background.inputs['Color'])
            links.new(node_background.inputs['Color'], node_background.inputs['Color'])
            links.new(node_background.outputs['Background'], node_output.inputs['Surface'])
            
            # Set HDRI rotation
            node_mapping.inputs['Rotation'].default_value = (0, 0, math.radians(rotation))
            
            # Set HDRI intensity
            node_background.inputs['Strength'].default_value = intensity
            
            # In a real implementation, this would load the actual HDRI image
            # For now, we'll just set a color based on the HDRI name
            if "sunset" in hdri_name.lower():
                world.node_tree.nodes["Background"].inputs['Color'].default_value = (0.8, 0.4, 0.2, 1.0)
            elif "night" in hdri_name.lower():
                world.node_tree.nodes["Background"].inputs['Color'].default_value = (0.05, 0.05, 0.1, 1.0)
            elif "forest" in hdri_name.lower():
                world.node_tree.nodes["Background"].inputs['Color'].default_value = (0.2, 0.4, 0.2, 1.0)
            elif "beach" in hdri_name.lower():
                world.node_tree.nodes["Background"].inputs['Color'].default_value = (0.8, 0.8, 1.0, 1.0)
            elif "studio" in hdri_name.lower():
                world.node_tree.nodes["Background"].inputs['Color'].default_value = (0.8, 0.8, 0.8, 1.0)
            else:
                world.node_tree.nodes["Background"].inputs['Color'].default_value = (0.5, 0.7, 1.0, 1.0)
            
            # Set up world settings
            bpy.context.scene.render.film_transparent = not background_visible
            
            return {
                "status": "success",
                "hdri_name": hdri_name,
                "intensity": intensity,
                "rotation": rotation,
                "background_visible": background_visible
            }
        
        except Exception as e:
            print(f"Error applying HDRI lighting: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to apply HDRI lighting: {str(e)}"
            }


class ProceduralEnvironmentGeneration:
    """
    Handles procedural generation of environments including terrain, architecture, and complete scenes.
    """
    
    def __init__(self):
        self.cache_dir = os.path.join(tempfile.gettempdir(), "blendermcp_environment_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def generate_terrain(self, terrain_type="hills", size=100.0, resolution=64, height=10.0, seed=0):
        """
        Generate procedural terrain.
        
        Args:
            terrain_type (str): Type of terrain (hills, mountains, plains, desert, etc.)
            size (float): Size of the terrain
            resolution (int): Resolution of the terrain grid
            height (float): Maximum height of the terrain
            seed (int): Random seed for generation
            
        Returns:
            dict: Result information including the generated terrain object name
        """
        try:
            # Set the random seed
            random.seed(seed)
            
            # Create a grid mesh for the terrain
            bpy.ops.mesh.primitive_grid_add(
                x_subdivisions=resolution,
                y_subdivisions=resolution,
                size=size,
                location=(0, 0, 0)
            )
            
            terrain_obj = bpy.context.active_object
            terrain_obj.name = f"Terrain_{terrain_type}"
            
            # Get the mesh data
            mesh = terrain_obj.data
            
            # Modify the vertices to create the terrain
            for vertex in mesh.vertices:
                # Get the vertex position
                x, y, z = vertex.co
                
                # Calculate the height based on the terrain type
                if terrain_type == "hills":
                    # Simple hills using sine waves
                    z = math.sin(x * 0.1) * math.cos(y * 0.1) * height * 0.5
                    z += random.uniform(-0.5, 0.5) * height * 0.2
                elif terrain_type == "mountains":
                    # More dramatic peaks
                    z = math.sin(x * 0.2) * math.cos(y * 0.2) * height
                    z += random.uniform(-1, 1) * height * 0.5
                elif terrain_type == "plains":
                    # Mostly flat with slight variations
                    z = random.uniform(-0.5, 0.5) * height * 0.1
                elif terrain_type == "desert":
                    # Sand dunes
                    z = math.sin(x * 0.05) * math.cos(y * 0.05) * height * 0.3
                    z += random.uniform(-0.2, 0.2) * height * 0.1
                else:
                    # Default random terrain
                    z = random.uniform(-1, 1) * height * 0.5
                
                # Update the vertex position
                vertex.co.z = z
            
            # Update the mesh
            mesh.update()
            
            # Add a material to the terrain
            mat = bpy.data.materials.new(name=f"Terrain_{terrain_type}_Material")
            mat.use_nodes = True
            
            # Set the material color based on the terrain type
            if terrain_type == "hills":
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.2, 0.5, 0.2, 1.0)
            elif terrain_type == "mountains":
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1.0)
            elif terrain_type == "plains":
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.3, 0.6, 0.3, 1.0)
            elif terrain_type == "desert":
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.7, 0.5, 1.0)
            else:
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.4, 0.4, 0.4, 1.0)
            
            # Assign the material to the terrain
            if terrain_obj.data.materials:
                terrain_obj.data.materials[0] = mat
            else:
                terrain_obj.data.materials.append(mat)
            
            return {
                "status": "success",
                "object_name": terrain_obj.name,
                "terrain_type": terrain_type,
                "size": size,
                "height": height
            }
        
        except Exception as e:
            print(f"Error generating terrain: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to generate terrain: {str(e)}"
            }
    
    def generate_architecture(self, architecture_type="building", size=5.0, complexity=0.5, seed=0):
        """
        Generate procedural architecture.
        
        Args:
            architecture_type (str): Type of architecture (building, house, temple, castle, etc.)
            size (float): Size of the architecture
            complexity (float): Complexity of the architecture (0.0 to 1.0)
            seed (int): Random seed for generation
            
        Returns:
            dict: Result information including the generated architecture object name
        """
        try:
            # Set the random seed
            random.seed(seed)
            
            # Create the base object based on the architecture type
            if architecture_type == "building":
                # Create a simple building with multiple floors
                floors = max(1, int(complexity * 5))
                floor_height = size / floors
                
                # Create the base of the building
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    location=(0, 0, size / 2)
                )
                building_obj = bpy.context.active_object
                building_obj.name = f"Building_{architecture_type}"
                building_obj.scale = (size, size, size)
                
                # Add windows
                for floor in range(floors):
                    for side in range(4):
                        # Calculate window position
                        angle = side * math.pi / 2
                        window_x = math.cos(angle) * (size * 0.4)
                        window_y = math.sin(angle) * (size * 0.4)
                        window_z = floor_height * (floor + 0.5)
                        
                        # Create window
                        bpy.ops.mesh.primitive_cube_add(
                            size=0.2 * size,
                            location=(window_x, window_y, window_z)
                        )
                        window_obj = bpy.context.active_object
                        window_obj.name = f"Building_Window_{floor}_{side}"
                        
                        # Create a boolean modifier to cut the window
                        bool_mod = building_obj.modifiers.new(name="Window", type='BOOLEAN')
                        bool_mod.operation = 'DIFFERENCE'
                        bool_mod.object = window_obj
                        
                        # Apply the modifier
                        bpy.context.view_layer.objects.active = building_obj
                        bpy.ops.object.modifier_apply(modifier="Window")
  <response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>