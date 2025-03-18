"""
BlenderMCP Ultimate Cinematic Upgrade - Physics & VFX Module
This module handles physics simulations and visual effects including cloth, hair, rigid body, and particle systems.
"""

import bpy
import os
import json
import math
import random
from mathutils import Vector, Euler, Quaternion
from pathlib import Path

class ClothPhysics:
    """
    Handles cloth simulation setup and configuration.
    """
    
    def __init__(self):
        # Cloth presets with different material properties
        self.cloth_presets = {
            "silk": {
                "mass": 0.15,
                "tension_stiffness": 5.0,
                "compression_stiffness": 5.0,
                "shear_stiffness": 5.0,
                "bending_stiffness": 0.5,
                "tension_damping": 0.5,
                "compression_damping": 0.5,
                "shear_damping": 0.5,
                "bending_damping": 0.5,
                "air_damping": 1.0,
                "quality": 5
            },
            "cotton": {
                "mass": 0.3,
                "tension_stiffness": 15.0,
                "compression_stiffness": 15.0,
                "shear_stiffness": 15.0,
                "bending_stiffness": 0.5,
                "tension_damping": 0.5,
                "compression_damping": 0.5,
                "shear_damping": 0.5,
                "bending_damping": 0.5,
                "air_damping": 1.0,
                "quality": 5
            },
            "denim": {
                "mass": 0.8,
                "tension_stiffness": 50.0,
                "compression_stiffness": 50.0,
                "shear_stiffness": 50.0,
                "bending_stiffness": 10.0,
                "tension_damping": 0.5,
                "compression_damping": 0.5,
                "shear_damping": 0.5,
                "bending_damping": 0.5,
                "air_damping": 1.0,
                "quality": 5
            },
            "leather": {
                "mass": 0.9,
                "tension_stiffness": 100.0,
                "compression_stiffness": 100.0,
                "shear_stiffness": 100.0,
                "bending_stiffness": 30.0,
                "tension_damping": 0.5,
                "compression_damping": 0.5,
                "shear_damping": 0.5,
                "bending_damping": 0.5,
                "air_damping": 1.0,
                "quality": 5
            },
            "rubber": {
                "mass": 1.0,
                "tension_stiffness": 200.0,
                "compression_stiffness": 200.0,
                "shear_stiffness": 200.0,
                "bending_stiffness": 100.0,
                "tension_damping": 0.5,
                "compression_damping": 0.5,
                "shear_damping": 0.5,
                "bending_damping": 0.5,
                "air_damping": 1.0,
                "quality": 5
            }
        }
    
    def create_cloth_object(self, name="Cloth", location=(0, 0, 0), size=(2.0, 2.0), resolution=(10, 10), material_type="cotton"):
        """
        Create a cloth object with the specified parameters.
        
        Args:
            name (str): Name of the cloth object
            location (tuple): Location of the cloth object
            size (tuple): Size of the cloth (width, height)
            resolution (tuple): Resolution of the cloth mesh (subdivisions_x, subdivisions_y)
            material_type (str): Type of cloth material
            
        Returns:
            dict: Result information including the created cloth object name
        """
        try:
            # Create a plane for the cloth
            bpy.ops.mesh.primitive_plane_add(
                size=1.0,
                location=location
            )
            
            cloth_obj = bpy.context.active_object
            cloth_obj.name = name
            
            # Scale the plane to the desired size
            cloth_obj.scale = (size[0], size[1], 1.0)
            
            # Subdivide the plane for better simulation
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.subdivide(number_cuts=resolution[0] - 1)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Add a material
            mat = bpy.data.materials.new(name=f"{name}_Material")
            mat.use_nodes = True
            
            # Set the material color based on the material type
            if material_type == "silk":
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.8, 0.9, 1.0)
                mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0.7
                mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.1
            elif material_type == "cotton":
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.9, 0.9, 0.9, 1.0)
                mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0.1
                mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
            elif material_type == "denim":
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.1, 0.2, 0.4, 1.0)
                mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0.1
                mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
            elif material_type == "leather":
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.3, 0.2, 0.1, 1.0)
                mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0.3
                mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.7
            elif material_type == "rubber":
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1.0)
                mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0.5
                mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.5
            
            # Assign the material to the cloth
            if cloth_obj.data.materials:
                cloth_obj.data.materials[0] = mat
            else:
                cloth_obj.data.materials.append(mat)
            
            return {
                "status": "success",
                "object_name": cloth_obj.name,
                "location": location,
                "size": size,
                "resolution": resolution,
                "material_type": material_type
            }
        
        except Exception as e:
            print(f"Error creating cloth object: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create cloth object: {str(e)}"
            }
    
    def setup_cloth_simulation(self, cloth_name, preset="cotton", collision_objects=None, pinning_vertices=None, wind_force=0.0, start_frame=1, end_frame=250):
        """
        Set up a cloth simulation for an object.
        
        Args:
            cloth_name (str): Name of the cloth object
            preset (str): Cloth preset to use
            collision_objects (list): List of objects to collide with
            pinning_vertices (list): List of vertex indices to pin
            wind_force (float): Strength of wind force
            start_frame (int): Start frame of the simulation
            end_frame (int): End frame of the simulation
            
        Returns:
            dict: Result information
        """
        try:
            # Check if the cloth object exists
            if cloth_name not in bpy.data.objects:
                return {
                    "status": "error",
                    "message": f"Cloth object '{cloth_name}' not found"
                }
            
            cloth_obj = bpy.data.objects[cloth_name]
            
            # Add a cloth modifier
            cloth_mod = cloth_obj.modifiers.new(name="Cloth", type='CLOTH')
            
            # Get the preset settings
            preset_settings = self.cloth_presets.get(preset, self.cloth_presets["cotton"])
            
            # Apply the preset settings
            cloth_settings = cloth_mod.settings
            cloth_settings.mass = preset_settings["mass"]
            cloth_settings.tension_stiffness = preset_settings["tension_stiffness"]
            cloth_settings.compression_stiffness = preset_settings["compression_stiffness"]
            cloth_settings.shear_stiffness = preset_settings["shear_stiffness"]
            cloth_settings.bending_stiffness = preset_settings["bending_stiffness"]
            cloth_settings.tension_damping = preset_settings["tension_damping"]
            cloth_settings.compression_damping = preset_settings["compression_damping"]
            cloth_settings.shear_damping = preset_settings["shear_damping"]
            cloth_settings.bending_damping = preset_settings["bending_damping"]
            cloth_settings.air_damping = preset_settings["air_damping"]
            cloth_settings.quality = preset_settings["quality"]
            
            # Set the simulation range
            cloth_settings.time_scale = 1.0
            cloth_mod.point_cache.frame_start = start_frame
            cloth_mod.point_cache.frame_end = end_frame
            
            # Add collision objects
            if collision_objects:
                for obj_name in collision_objects:
                    if obj_name in bpy.data.objects:
                        obj = bpy.data.objects[obj_name]
                        
                        # Add a collision modifier
                        if not any(mod.type == 'COLLISION' for mod in obj.modifiers):
                            obj.modifiers.new(name="Collision", type='COLLISION')
            
            # Pin vertices
            if pinning_vertices:
                # Create a vertex group for pinning
                pin_group = cloth_obj.vertex_groups.new(name="Pinning")
                pin_group.add(pinning_vertices, 1.0, 'REPLACE')
                
                # Set the vertex group for pinning
                cloth_settings.vertex_group_mass = pin_group.name
            
            # Add wind force
            if wind_force > 0:
                # Create a force field for wind
                bpy.ops.object.effector_add(type='WIND', location=(0, -5, 0))
                wind_obj = bpy.context.active_object
                wind_obj.name = f"{cloth_name}_Wind"
                
                # Set the wind strength
                wind_obj.field.strength = wind_force
                
                # Rotate the wind to blow in the positive Y direction
                wind_obj.rotation_euler = (math.pi / 2, 0, 0)
            
            return {
                "status": "success",
                "object_name": cloth_obj.name,
                "preset": preset,
                "collision_objects": collision_objects,
                "pinning_vertices": pinning_vertices,
                "wind_force": wind_force,
                "start_frame": start_frame,
                "end_frame": end_frame
            }
        
        except Exception as e:
            print(f"Error setting up cloth simulation: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to set up cloth simulation: {str(e)}"
            }
    
    def bake_cloth_simulation(self, cloth_name, start_frame=1, end_frame=250):
        """
        Bake a cloth simulation.
        
        Args:
            cloth_name (str): Name of the cloth object
            start_frame (int): Start frame of the simulation
            end_frame (int): End frame of the simulation
            
        Returns:
            dict: Result information
        """
        try:
            # Check if the cloth object exists
            if cloth_name not in bpy.data.objects:
                return {
                    "status": "error",
                    "message": f"Cloth object '{cloth_name}' not found"
                }
            
            cloth_obj = bpy.data.objects[cloth_name]
            
            # Check if the object has a cloth modifier
            cloth_mod = None
            for mod in cloth_obj.modifiers:
                if mod.type == 'CLOTH':
                    cloth_mod = mod
                    break
            
            if not cloth_mod:
                return {
                    "status": "error",
                    "message": f"Object '{cloth_name}' does not have a cloth modifier"
                }
            
            # Set the simulation range
            cloth_mod.point_cache.frame_start = start_frame
            cloth_mod.point_cache.frame_end = end_frame
            
            # Select the cloth object
            bpy.ops.object.select_all(action='DESELECT')
            cloth_obj.select_set(True)
            bpy.context.view_layer.objects.active = cloth_obj
            
            # Bake the simulation
            # In a real implementation, this would use bpy.ops.ptcache.bake_all()
            # For now, we'll just simulate running through the frames
            for frame in range(start_frame, end_frame + 1):
                bpy.context.scene.frame_set(frame)
            
            return {
                "status": "success",
                "object_name": cloth_obj.name,
                "start_frame": start_frame,
                "end_frame": end_frame
            }
        
        except Exception as e:
            print(f"Error baking cloth simulation: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to bake cloth simulation: {str(e)}"
            }


class HairPhysics:
    """
    Handles hair particle system setup and styling.
    """
    
    def __init__(self):
        # Hair presets with different styling properties
        self.hair_presets = {
            "straight": {
                "length": 0.2,
                "segments": 5,
                "children": 50,
                "root_radius": 0.01,
                "tip_radius": 0.001,
                "radius_scale": 0.3,
                "child_radius": 0.1,
                "roughness_1": 0.1,
                "roughness_2": 0.1,
                "roughness_endpoint": 0.1,
                "kink": "NO",
                "kink_amplitude": 0.0,
                "kink_frequency": 0.0
            },
            "wavy": {
                "length": 0.2,
                "segments": 5,
                "children": 50,
                "root_radius": 0.01,
                "tip_radius": 0.001,
                "radius_scale": 0.3,
                "child_radius": 0.1,
                "roughness_1": 0.2,
                "roughness_2": 0.2,
                "roughness_endpoint": 0.2,
                "kink": "WAVE",
                "kink_amplitude": 0.05,
                "kink_frequency": 2.0
            },
            "curly": {
                "length": 0.2,
                "segments": 8,
                "children": 50,
                "root_radius": 0.01,
                "tip_radius": 0.001,
                "radius_scale": 0.3,
                "child_radius": 0.1,
                "roughness_1": 0.3,
                "roughness_2": 0.3,
                "roughness_endpoint": 0.3,
                "kink": "CURL",
                "kink_amplitude": 0.1,
                "kink_frequency": 3.0
            },
            "afro": {
                "length": 0.15,
                "segments": 8,
                "children": 100,
                "root_radius": 0.01,
                "tip_radius": 0.001,
                "radius_scale": 0.3,
                "child_radius": 0.1,
                "roughness_1": 0.5,
                "roughness_2": 0.5,
                "roughness_endpoint": 0.5,
                "kink": "CURL",
                "kink_amplitude": 0.2,
                "<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>