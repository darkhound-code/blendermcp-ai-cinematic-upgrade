"""
BlenderMCP Ultimate Cinematic Upgrade - Character Animation Module
This module handles character animation including rigging, animation retargeting, keyframe generation, and camera work.
"""

import bpy
import os
import json
import math
import random
from mathutils import Vector, Euler, Quaternion
from pathlib import Path

class RigifyAutoRigging:
    """
    Handles automatic character rigging using Blender's Rigify system.
    """
    
    def __init__(self):
        # Ensure Rigify is enabled
        if "rigify" not in bpy.context.preferences.addons:
            try:
                bpy.ops.preferences.addon_enable(module="rigify")
                print("Rigify addon enabled")
            except Exception as e:
                print(f"Error enabling Rigify addon: {str(e)}")
    
    def create_metarig(self, target_mesh, position=(0, 0, 0), scale=1.0, rig_type="humanoid"):
        """
        Create a metarig for a character mesh.
        
        Args:
            target_mesh (str): Name of the mesh to rig
            position (tuple): Position for the metarig
            scale (float): Scale factor for the metarig
            rig_type (str): Type of rig to create (humanoid, quadruped, bird, etc.)
            
        Returns:
            dict: Result information including the created metarig name
        """
        try:
            # Check if the target mesh exists
            if target_mesh not in bpy.data.objects:
                return {
                    "status": "error",
                    "message": f"Target mesh '{target_mesh}' not found"
                }
            
            mesh_obj = bpy.data.objects[target_mesh]
            
            # Create a metarig based on the rig type
            if rig_type == "humanoid":
                bpy.ops.object.armature_human_metarig_add()
            elif rig_type == "quadruped":
                bpy.ops.object.armature_basic_human_metarig_add()
                # In a real implementation, we would modify this to be a quadruped
            elif rig_type == "bird":
                bpy.ops.object.armature_basic_human_metarig_add()
                # In a real implementation, we would modify this to be a bird
            else:
                bpy.ops.object.armature_human_metarig_add()
            
            metarig = bpy.context.active_object
            metarig.name = f"{target_mesh}_metarig"
            
            # Position and scale the metarig
            metarig.location = position
            metarig.scale = (scale, scale, scale)
            
            # Adjust the metarig to fit the mesh
            # In a real implementation, this would use more sophisticated bone positioning
            # based on mesh analysis
            
            # For now, we'll just scale the metarig to roughly match the mesh dimensions
            mesh_dimensions = mesh_obj.dimensions
            metarig.scale = (
                scale * mesh_dimensions.x / 2,
                scale * mesh_dimensions.y / 2,
                scale * mesh_dimensions.z / 2
            )
            
            return {
                "status": "success",
                "metarig_name": metarig.name,
                "rig_type": rig_type
            }
        
        except Exception as e:
            print(f"Error creating metarig: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create metarig: {str(e)}"
            }
    
    def generate_rig(self, metarig_name, generate_widgets=True):
        """
        Generate a rig from a metarig.
        
        Args:
            metarig_name (str): Name of the metarig to generate from
            generate_widgets (bool): Whether to generate control widgets
            
        Returns:
            dict: Result information including the generated rig name
        """
        try:
            # Check if the metarig exists
            if metarig_name not in bpy.data.objects:
                return {
                    "status": "error",
                    "message": f"Metarig '{metarig_name}' not found"
                }
            
            metarig = bpy.data.objects[metarig_name]
            
            # Select the metarig
            bpy.ops.object.select_all(action='DESELECT')
            metarig.select_set(True)
            bpy.context.view_layer.objects.active = metarig
            
            # Generate the rig
            bpy.ops.pose.rigify_generate()
            
            # The generated rig will be the active object
            rig = bpy.context.active_object
            rig.name = metarig_name.replace("_metarig", "_rig")
            
            return {
                "status": "success",
                "rig_name": rig.name,
                "metarig_name": metarig_name
            }
        
        except Exception as e:
            print(f"Error generating rig: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to generate rig: {str(e)}"
            }
    
    def auto_weight_paint(self, mesh_name, rig_name):
        """
        Automatically weight paint a mesh to a rig.
        
        Args:
            mesh_name (str): Name of the mesh to weight paint
            rig_name (str): Name of the rig to weight paint to
            
        Returns:
            dict: Result information
        """
        try:
            # Check if the mesh and rig exist
            if mesh_name not in bpy.data.objects:
                return {
                    "status": "error",
                    "message": f"Mesh '{mesh_name}' not found"
                }
            
            if rig_name not in bpy.data.objects:
                return {
                    "status": "error",
                    "message": f"Rig '{rig_name}' not found"
                }
            
            mesh_obj = bpy.data.objects[mesh_name]
            rig_obj = bpy.data.objects[rig_name]
            
            # Select the mesh and the rig
            bpy.ops.object.select_all(action='DESELECT')
            mesh_obj.select_set(True)
            rig_obj.select_set(True)
            bpy.context.view_layer.objects.active = rig_obj
            
            # Parent the mesh to the rig with automatic weights
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')
            
            return {
                "status": "success",
                "mesh_name": mesh_name,
                "rig_name": rig_name
            }
        
        except Exception as e:
            print(f"Error auto weight painting: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to auto weight paint: {str(e)}"
            }
    
    def auto_rig_character(self, mesh_name, position=(0, 0, 0), scale=1.0, rig_type="humanoid"):
        """
        Automatically rig a character mesh with a complete workflow.
        
        Args:
            mesh_name (str): Name of the mesh to rig
            position (tuple): Position for the rig
            scale (float): Scale factor for the rig
            rig_type (str): Type of rig to create
            
        Returns:
            dict: Result information
        """
        try:
            # Create a metarig
            metarig_result = self.create_metarig(
                target_mesh=mesh_name,
                position=position,
                scale=scale,
                rig_type=rig_type
            )
            
            if metarig_result["status"] == "error":
                return metarig_result
            
            # Generate a rig from the metarig
            rig_result = self.generate_rig(
                metarig_name=metarig_result["metarig_name"],
                generate_widgets=True
            )
            
            if rig_result["status"] == "error":
                return rig_result
            
            # Auto weight paint the mesh to the rig
            weight_result = self.auto_weight_paint(
                mesh_name=mesh_name,
                rig_name=rig_result["rig_name"]
            )
            
            if weight_result["status"] == "error":
                return weight_result
            
            return {
                "status": "success",
                "mesh_name": mesh_name,
                "metarig_name": metarig_result["metarig_name"],
                "rig_name": rig_result["rig_name"],
                "rig_type": rig_type
            }
        
        except Exception as e:
            print(f"Error auto rigging character: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to auto rig character: {str(e)}"
            }


class AnimationRetargeting:
    """
    Handles animation retargeting between different rigs.
    """
    
    def __init__(self):
        pass
    
    def create_bone_mapping(self, source_rig, target_rig, mapping_type="auto"):
        """
        Create a bone mapping between two rigs.
        
        Args:
            source_rig (str): Name of the source rig
            target_rig (str): Name of the target rig
            mapping_type (str): Type of mapping to create (auto, mixamo_to_rigify, custom)
            
        Returns:
            dict: Bone mapping dictionary
        """
        # Check if the rigs exist
        if source_rig not in bpy.data.objects:
            return {
                "status": "error",
                "message": f"Source rig '{source_rig}' not found"
            }
        
        if target_rig not in bpy.data.objects:
            return {
                "status": "error",
                "message": f"Target rig '{target_rig}' not found"
            }
        
        source_obj = bpy.data.objects[source_rig]
        target_obj = bpy.data.objects[target_rig]
        
        # Create a bone mapping based on the mapping type
        bone_mapping = {}
        
        if mapping_type == "auto":
            # Automatically map bones with the same name
            source_bones = [bone.name for bone in source_obj.pose.bones]
            target_bones = [bone.name for bone in target_obj.pose.bones]
            
            for bone in source_bones:
                if bone in target_bones:
                    bone_mapping[bone] = bone
        
        elif mapping_type == "mixamo_to_rigify":
            # Predefined mapping from Mixamo to Rigify
            bone_mapping = {
                "mixamorig:Hips": "hips",
                "mixamorig:Spine": "spine",
                "mixamorig:Spine1": "spine.001",
                "mixamorig:Spine2": "spine.002",
                "mixamorig:Neck": "spine.003",
                "mixamorig:Head": "spine.004",
                "mixamorig:LeftShoulder": "shoulder.L",
                "mixamorig:LeftArm": "upper_arm.L",
                "mixamorig:LeftForeArm": "forearm.L",
                "mixamorig:LeftHand": "hand.L",
                "mixamorig:RightShoulder": "shoulder.R",
                "mixamorig:RightArm": "upper_arm.R",
                "mixamorig:RightForeArm": "forearm.R",
                "mixamorig:RightHand": "hand.R",
                "mixamorig:LeftUpLeg": "thigh.L",
                "mixamorig:LeftLeg": "shin.L",
                "mixamorig:LeftFoot": "foot.L",
                "mixamorig:LeftToeBase": "toe.L",
                "mixamorig:RightUpLeg": "thigh.R",
                "mixamorig:RightLeg": "shin.R",
                "mixamorig:RightFoot": "foot.R",
                "mixamorig:RightToeBase": "toe.R"
            }
        
        elif mapping_type == "custom":
            # In a real implementation, this would allow for custom mapping
            # For now, we'll use a simplified mapping
            bone_mapping = {
                "root": "root",
                "pelvis": "hips",
                "spine": "spine",
                "neck": "neck",
                "head": "head",
                "shoulder.l": "shoulder.L",
                "arm.l": "upper_arm.L",
                "forearm.l": "forearm.L",
                "hand.l": "hand.L",
                "shoulder.r": "shoulder.R",
                "arm.r": "upper_arm.R",
                "forearm.r": "forearm.R",
                "hand.r": "hand.R",
                "thigh.l": "thigh.L",
                "calf.l": "shin.L",
                "foot.l": "foot.L",
                "toe.l": "toe.L",
                "thigh.r": "thigh.R",
                "calf.r": "shin.R",
                "foot.r": "foot.R",
                "toe.r": "toe.R"
            }
        
        return {
            "status": "success",
            "bone_mapping": bone_mapping,
            "source_rig": source_rig,
            "target_rig": target_rig,
            "mapping_type": mapping_type
        }
    
    def retarget_animation(self, source_rig, target_rig, bone_mapping=None, mapping_type="auto", start_frame=1, end_frame=250):
        """
        Retarget an animation from one rig to another.
        
        Args:
            source_rig (str): Name of the source rig
            target_rig (str): Name of the target rig
            bone_mapping (dict, optional): Custom bone mapping
            mapping_type (str): Type of mapping to create if bone_mapping is None
            start_frame (int): Start frame of the animation
            end_frame (int): End frame of the animation
            
        Returns:
            dict: Result information
        """
        try:
            # Check if the rigs exist
            if source_rig not in bpy.data.objects:
                return {
                    "status": "error",
                    "message": f"Source rig '{source_rig}' not found"
                }
            
            if target_rig not in bpy.data.objects:
                return {
                    "status": "error",
                    "message": f"Target rig '{target_rig}' not found"
                }
            
            source_obj = bpy.data.objects[source_rig]
            target_obj = bpy.data.objects[target_rig]
            
            # Get or create bone mapping
            if bone_mapping is None:
                mapping_result = self.create_bone_mapping(
                    source_rig=source_rig,
                    target_rig=target_rig,
                    mapping_type=mapping_type
                )
                
                if mapping_result["status"] == "error":
                    return mapping_result
                
                bone_mapping = mapping_result["bone_mapping"]
            
            # Retarget the animation
            for frame in range(start_frame, end_frame + 1):
                bpy.context.scene.frame_set(frame)
                
                for source_bone, target_bone in bone_mapping.items():
                    if source_bone in source_obj.pose.bones and target_bone in target_obj.pose.bones:
                        # Copy location
                        if len(source_obj.pose.bones[source_bone].constraints) == 0:  # Only if no constraints
                            target_obj.pose.bones[target_bone].location = source_obj.pose.bones[source_bone].location.copy()
                        
                        # Copy rotation
                        target_obj.pose.bones[target_bone].rotation_quaternion = source_obj.pose.bones[source_bone].rotation_quaternion.copy()
                        
                        # Insert keyframes
                        target_obj.pose.bones[target_bone].keyframe_insert(data_path="location", frame=frame)
                        target_obj.pose.bones[target_bone].keyframe_insert(data_path="rotation_quaternion", frame=frame)
            
            return {
                "status": "success",
                "source_rig": source_rig,
                "target_rig": target_rig,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "bones_mapped": len(bone_mapping)
            }
  <response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>