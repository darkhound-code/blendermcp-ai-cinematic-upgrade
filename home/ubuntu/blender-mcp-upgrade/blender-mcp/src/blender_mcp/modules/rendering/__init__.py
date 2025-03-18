"""
BlenderMCP Ultimate Cinematic Upgrade - Rendering Module
This module handles rendering engine selection, optimization, and post-processing effects.
"""

import bpy
import os
import json
import math
import random
from mathutils import Vector, Euler, Quaternion
from pathlib import Path

class RenderEngineManager:
    """
    Handles render engine selection and optimization.
    """
    
    def __init__(self):
        # Render engine presets with different quality settings
        self.render_presets = {
            "preview": {
                "engine": "BLENDER_EEVEE",
                "samples": 16,
                "use_denoising": True,
                "use_ambient_occlusion": True,
                "use_bloom": True,
                "use_motion_blur": False,
                "use_volumetrics": True,
                "use_screen_space_reflections": False,
                "shadow_cube_size": "512",
                "shadow_cascade_size": "512"
            },
            "medium": {
                "engine": "BLENDER_EEVEE",
                "samples": 64,
                "use_denoising": True,
                "use_ambient_occlusion": True,
                "use_bloom": True,
                "use_motion_blur": True,
                "use_volumetrics": True,
                "use_screen_space_reflections": True,
                "shadow_cube_size": "1024",
                "shadow_cascade_size": "1024"
            },
            "high": {
                "engine": "CYCLES",
                "samples": 128,
                "use_denoising": True,
                "use_adaptive_sampling": True,
                "use_caustics": False,
                "use_motion_blur": True,
                "light_bounces": 4,
                "transparent_max_bounces": 8,
                "use_gpu": True
            },
            "ultra": {
                "engine": "CYCLES",
                "samples": 512,
                "use_denoising": True,
                "use_adaptive_sampling": True,
                "use_caustics": True,
                "use_motion_blur": True,
                "light_bounces": 8,
                "transparent_max_bounces": 16,
                "use_gpu": True
            }
        }
    
    def set_render_engine(self, engine_type="CYCLES"):
        """
        Set the render engine.
        
        Args:
            engine_type (str): Render engine type (CYCLES, BLENDER_EEVEE)
            
        Returns:
            dict: Result information
        """
        try:
            # Set the render engine
            bpy.context.scene.render.engine = engine_type
            
            return {
                "status": "success",
                "engine": engine_type
            }
        
        except Exception as e:
            print(f"Error setting render engine: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to set render engine: {str(e)}"
            }
    
    def apply_render_preset(self, preset="medium"):
        """
        Apply a render preset.
        
        Args:
            preset (str): Render preset to use
            
        Returns:
            dict: Result information
        """
        try:
            # Get the preset settings
            preset_settings = self.render_presets.get(preset, self.render_presets["medium"])
            
            # Set the render engine
            bpy.context.scene.render.engine = preset_settings["engine"]
            
            # Apply the preset settings
            if preset_settings["engine"] == "CYCLES":
                # Cycles settings
                bpy.context.scene.cycles.samples = preset_settings["samples"]
                bpy.context.scene.cycles.use_denoising = preset_settings["use_denoising"]
                bpy.context.scene.cycles.use_adaptive_sampling = preset_settings["use_adaptive_sampling"]
                bpy.context.scene.cycles.caustics_reflective = preset_settings["use_caustics"]
                bpy.context.scene.cycles.caustics_refractive = preset_settings["use_caustics"]
                bpy.context.scene.render.use_motion_blur = preset_settings["use_motion_blur"]
                bpy.context.scene.cycles.max_bounces = preset_settings["light_bounces"]
                bpy.context.scene.cycles.transparent_max_bounces = preset_settings["transparent_max_bounces"]
                
                # Set GPU acceleration if available
                if preset_settings["use_gpu"]:
                    bpy.context.scene.cycles.device = 'GPU'
                    
                    # Enable all available GPUs
                    if hasattr(bpy.context.preferences.addons["cycles"], "preferences"):
                        cycles_prefs = bpy.context.preferences.addons["cycles"].preferences
                        cycles_prefs.compute_device_type = 'CUDA'  # or 'OPTIX' or 'HIP' depending on hardware
                        
                        for device in cycles_prefs.devices:
                            device.use = True
            
            elif preset_settings["engine"] == "BLENDER_EEVEE":
                # Eevee settings
                bpy.context.scene.eevee.taa_render_samples = preset_settings["samples"]
                bpy.context.scene.eevee.use_gtao = preset_settings["use_ambient_occlusion"]
                bpy.context.scene.eevee.use_bloom = preset_settings["use_bloom"]
                bpy.context.scene.render.use_motion_blur = preset_settings["use_motion_blur"]
                bpy.context.scene.eevee.use_volumetric_shadows = preset_settings["use_volumetrics"]
                bpy.context.scene.eevee.use_ssr = preset_settings["use_screen_space_reflections"]
                bpy.context.scene.eevee.shadow_cube_size = preset_settings["shadow_cube_size"]
                bpy.context.scene.eevee.shadow_cascade_size = preset_settings["shadow_cascade_size"]
            
            return {
                "status": "success",
                "preset": preset,
                "engine": preset_settings["engine"]
            }
        
        except Exception as e:
            print(f"Error applying render preset: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to apply render preset: {str(e)}"
            }
    
    def optimize_render_settings(self, target_quality="medium", target_time=None):
        """
        Optimize render settings based on target quality or render time.
        
        Args:
            target_quality (str): Target quality level
            target_time (float): Target render time in seconds per frame
            
        Returns:
            dict: Result information
        """
        try:
            # Start with a preset based on target quality
            self.apply_render_preset(target_quality)
            
            # If target time is specified, adjust settings to meet the target time
            if target_time is not None:
                # Estimate current render time (this would require a more sophisticated algorithm in a real implementation)
                estimated_time = self._estimate_render_time()
                
                # Adjust settings to meet target time
                if estimated_time > target_time:
                    # Reduce quality to meet target time
                    self._reduce_quality_for_target_time(target_time)
                elif estimated_time < target_time * 0.8:
                    # Increase quality if we have headroom
                    self._increase_quality_for_target_time(target_time)
            
            # Get the current render settings
            current_settings = self._get_current_render_settings()
            
            return {
                "status": "success",
                "target_quality": target_quality,
                "target_time": target_time,
                "current_settings": current_settings
            }
        
        except Exception as e:
            print(f"Error optimizing render settings: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to optimize render settings: {str(e)}"
            }
    
    def _estimate_render_time(self):
        """
        Estimate render time for current settings.
        
        Returns:
            float: Estimated render time in seconds per frame
        """
        # In a real implementation, this would use a more sophisticated algorithm
        # For now, we'll use a simple heuristic based on render settings
        
        if bpy.context.scene.render.engine == "CYCLES":
            samples = bpy.context.scene.cycles.samples
            bounces = bpy.context.scene.cycles.max_bounces
            
            # Simple heuristic: time is proportional to samples and bounces
            estimated_time = samples * (bounces + 1) * 0.01
            
            # Adjust for GPU acceleration
            if bpy.context.scene.cycles.device == 'GPU':
                estimated_time *= 0.3
        
        else:  # BLENDER_EEVEE
            samples = bpy.context.scene.eevee.taa_render_samples
            
            # Simple heuristic: time is proportional to samples
            estimated_time = samples * 0.05
        
        return estimated_time
    
    def _reduce_quality_for_target_time(self, target_time):
        """
        Reduce quality to meet target render time.
        
        Args:
            target_time (float): Target render time in seconds per frame
        """
        # In a real implementation, this would use a more sophisticated algorithm
        # For now, we'll use a simple approach
        
        if bpy.context.scene.render.engine == "CYCLES":
            # Reduce samples until we meet the target time
            while self._estimate_render_time() > target_time and bpy.context.scene.cycles.samples > 16:
                bpy.context.scene.cycles.samples = max(16, int(bpy.context.scene.cycles.samples * 0.8))
            
            # If still not meeting target, reduce bounces
            while self._estimate_render_time() > target_time and bpy.context.scene.cycles.max_bounces > 2:
                bpy.context.scene.cycles.max_bounces -= 1
            
            # If still not meeting target, switch to Eevee
            if self._estimate_render_time() > target_time:
                self.apply_render_preset("medium")
        
        else:  # BLENDER_EEVEE
            # Reduce samples until we meet the target time
            while self._estimate_render_time() > target_time and bpy.context.scene.eevee.taa_render_samples > 8:
                bpy.context.scene.eevee.taa_render_samples = max(8, int(bpy.context.scene.eevee.taa_render_samples * 0.8))
            
            # Disable features to improve performance
            if self._estimate_render_time() > target_time:
                bpy.context.scene.eevee.use_ssr = False
            
            if self._estimate_render_time() > target_time:
                bpy.context.scene.eevee.use_volumetric_shadows = False
            
            if self._estimate_render_time() > target_time:
                bpy.context.scene.render.use_motion_blur = False
    
    def _increase_quality_for_target_time(self, target_time):
        """
        Increase quality to use available render time.
        
        Args:
            target_time (float): Target render time in seconds per frame
        """
        # In a real implementation, this would use a more sophisticated algorithm
        # For now, we'll use a simple approach
        
        if bpy.context.scene.render.engine == "BLENDER_EEVEE":
            # If we have significant headroom, switch to Cycles
            if self._estimate_render_time() < target_time * 0.3:
                self.apply_render_preset("high")
                
                # Adjust samples to meet target time
                while self._estimate_render_time() < target_time * 0.8:
                    bpy.context.scene.cycles.samples = min(1024, int(bpy.context.scene.cycles.samples * 1.2))
            
            else:
                # Increase Eevee samples
                while self._estimate_render_time() < target_time * 0.8:
                    bpy.context.scene.eevee.taa_render_samples = min(64, int(bpy.context.scene.eevee.taa_render_samples * 1.2))
                
                # Enable features for better quality
                if self._estimate_render_time() < target_time * 0.8:
                    bpy.context.scene.eevee.use_ssr = True
                
                if self._estimate_render_time() < target_time * 0.8:
                    bpy.context.scene.eevee.use_volumetric_shadows = True
                
                if self._estimate_render_time() < target_time * 0.8:
                    bpy.context.scene.render.use_motion_blur = True
        
        else:  # CYCLES
            # Increase samples
            while self._estimate_render_time() < target_time * 0.8:
                bpy.context.scene.cycles.samples = min(1024, int(bpy.context.scene.cycles.samples * 1.2))
            
            # Increase bounces for better quality
            if self._estimate_render_time() < target_time * 0.8 and bpy.context.scene.cycles.max_bounces < 8:
                bpy.context.scene.cycles.max_bounces += 1
    
    def _get_current_render_settings(self):
        """
        Get the current render settings.
        
        Returns:
            dict: Current render settings
        """
        settings = {
            "engine": bpy.context.scene.render.engine
        }
        
        if settings["engine"] == "CYCLES":
            settings.update({
                "samples": bpy.context.scene.cycles.samples,
                "use_denoising": bpy.context.scene.cycles.use_denoising,
                "use_adaptive_sampling": bpy.context.scene.cycles.use_adaptive_sampling,
                "use_caustics": bpy.context.scene.cycles.caustics_reflective,
                "use_motion_blur": bpy.context.scene.render.use_motion_blur,
                "light_bounces": bpy.context.scene.cycles.max_bounces,
                "transparent_max_bounces": bpy.context.scene.cycles.transparent_max_bounces,
                "device": bpy.context.scene.cycles.device
            })
        
        elif settings["engine"] == "BLENDER_EEVEE":
            settings.update({
                "samples": bpy.context.scene.eevee.taa_render_samples,
                "use_ambient_occlusion": bpy.context.scene.eevee.use_gtao,
                "use_bloom": bpy.context.scene.eevee.use_bloom,
                "use_motion_blur": bpy.context.scene.render.use_motion_blur,
                "use_volumetrics": bpy.context.scene.eevee.use_volumetric_shadows,
                "use_screen_space_reflections": bpy.context.scene.eevee.use_ssr,
                "shadow_cube_size": bpy.context.scene.eevee.shadow_cube_size,
                "shadow_cascade_size": bpy.context.scene.eevee.shadow_cascade_size
            })
        
        return settings
    
    def set_output_settings(self, resolution_x=1920, resolution_y=1080, resolution_percentage=100, file_format="PNG", output_path="//render/"):
        """
        Set output settings for rendering.
        
        Args:
            resolution_x (int): X resolution
            resolution_y (int): Y resolution
            resolution_percentage (int): Resolution percentage
            file_format (str): Output file format
            output_path (str): Output path
            
        Returns:
            dict: Result information
        """
        try:
            # Set resolution
            bpy.context.scene.render.resolution_x = resolution_x
            bpy.context.scene.render.resolution_y = resolution_y
            bpy.context.scene.render.resolution_percentage = resolution_percentage
            
            # Set output format
            bpy.context.scene.render.image_settings.file_format = file_format
            
<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>