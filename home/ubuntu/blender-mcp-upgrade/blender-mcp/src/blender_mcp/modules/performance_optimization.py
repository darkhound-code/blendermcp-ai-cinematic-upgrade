"""
BlenderMCP Ultimate Cinematic Upgrade - Performance Optimization Module
This module handles performance optimization and testing for all features.
"""

import bpy
import gc
import time
import psutil
import platform
import sys
from typing import Dict, List, Optional, Callable, Any, Union

class PerformanceOptimizer:
    """
    Handles performance optimization for BlenderMCP operations.
    """
    
    def __init__(self):
        self.performance_metrics = {}
        self.optimization_settings = {
            "memory_limit": 8 * 1024 * 1024 * 1024,  # 8 GB default memory limit
            "viewport_quality": "medium",
            "background_processes": True,
            "use_gpu": True,
            "subdivision_limit": 2,
            "texture_size_limit": 2048,
            "particle_limit": 100000,
            "physics_quality": "medium"
        }
    
    def measure_performance(self, operation_name: str, callback: Callable) -> Dict:
        """
        Measure the performance of an operation.
        
        Args:
            operation_name: Name of the operation to measure
            callback: Function to execute and measure
            
        Returns:
            Dict with performance metrics
        """
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        # Get initial time
        start_time = time.time()
        
        # Execute the callback
        try:
            result = callback()
            success = True
        except Exception as e:
            result = str(e)
            success = False
        
        # Get final time
        end_time = time.time()
        
        # Get final memory usage
        final_memory = process.memory_info().rss
        
        # Calculate metrics
        execution_time = end_time - start_time
        memory_usage = final_memory - initial_memory
        
        # Store metrics
        metrics = {
            "operation_name": operation_name,
            "execution_time": execution_time,
            "memory_usage": memory_usage,
            "success": success,
            "timestamp": time.time()
        }
        
        self.performance_metrics[operation_name] = metrics
        
        return {
            "metrics": metrics,
            "result": result
        }
    
    def optimize_memory_usage(self) -> Dict:
        """
        Optimize memory usage in Blender.
        
        Returns:
            Dict with optimization results
        """
        initial_memory = psutil.Process().memory_info().rss
        
        # Force garbage collection
        gc.collect()
        
        # Purge Blender data
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        
        # Clear undo history
        bpy.context.preferences.edit.undo_steps = 1
        bpy.ops.ed.undo_push()
        bpy.context.preferences.edit.undo_steps = 32  # Reset to default
        
        # Remove unused datablocks
        for datablock in [bpy.data.meshes, bpy.data.materials, bpy.data.textures, 
                         bpy.data.images, bpy.data.actions, bpy.data.armatures]:
            for item in datablock:
                if item.users == 0:
                    datablock.remove(item)
        
        final_memory = psutil.Process().memory_info().rss
        memory_saved = initial_memory - final_memory
        
        return {
            "initial_memory": initial_memory,
            "final_memory": final_memory,
            "memory_saved": memory_saved,
            "success": memory_saved > 0
        }
    
    def optimize_viewport_performance(self, quality: str = "medium") -> Dict:
        """
        Optimize viewport performance.
        
        Args:
            quality: Viewport quality level (low, medium, high)
            
        Returns:
            Dict with optimization results
        """
        # Store original settings
        original_settings = {
            "show_only_render": bpy.context.space_data.show_only_render if hasattr(bpy.context, "space_data") else False,
            "show_textured_solid": bpy.context.space_data.show_textured_solid if hasattr(bpy.context, "space_data") else False,
            "show_overlays": bpy.context.space_data.overlay.show_overlays if hasattr(bpy.context, "space_data") and hasattr(bpy.context.space_data, "overlay") else True,
            "subdivision_levels": {}
        }
        
        # Apply settings based on quality
        if quality == "low":
            # Set viewport to solid mode
            if hasattr(bpy.context, "space_data"):
                bpy.context.space_data.shading.type = 'SOLID'
                bpy.context.space_data.show_only_render = False
                bpy.context.space_data.show_textured_solid = False
                if hasattr(bpy.context.space_data, "overlay"):
                    bpy.context.space_data.overlay.show_overlays = False
            
            # Reduce subdivision levels
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    for modifier in obj.modifiers:
                        if modifier.type == 'SUBSURF':
                            original_settings["subdivision_levels"][obj.name] = modifier.levels
                            modifier.levels = 0
        
        elif quality == "medium":
            # Set viewport to solid mode with textures
            if hasattr(bpy.context, "space_data"):
                bpy.context.space_data.shading.type = 'SOLID'
                bpy.context.space_data.show_only_render = False
                bpy.context.space_data.show_textured_solid = True
                if hasattr(bpy.context.space_data, "overlay"):
                    bpy.context.space_data.overlay.show_overlays = True
            
            # Reduce subdivision levels
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    for modifier in obj.modifiers:
                        if modifier.type == 'SUBSURF':
                            original_settings["subdivision_levels"][obj.name] = modifier.levels
                            modifier.levels = min(modifier.levels, 1)
        
        elif quality == "high":
            # Set viewport to material preview
            if hasattr(bpy.context, "space_data"):
                bpy.context.space_data.shading.type = 'MATERIAL'
                bpy.context.space_data.show_only_render = False
                bpy.context.space_data.show_textured_solid = True
                if hasattr(bpy.context.space_data, "overlay"):
                    bpy.context.space_data.overlay.show_overlays = True
            
            # Keep subdivision levels as is
        
        # Update the optimization settings
        self.optimization_settings["viewport_quality"] = quality
        
        return {
            "quality": quality,
            "original_settings": original_settings,
            "success": True
        }
    
    def optimize_render_settings(self, target_quality: str = "medium") -> Dict:
        """
        Optimize render settings for better performance.
        
        Args:
            target_quality: Target quality level (preview, medium, high, ultra)
            
        Returns:
            Dict with optimization results
        """
        # Store original settings
        original_settings = {
            "engine": bpy.context.scene.render.engine,
            "samples": bpy.context.scene.cycles.samples if bpy.context.scene.render.engine == 'CYCLES' else bpy.context.scene.eevee.taa_render_samples,
            "use_denoising": bpy.context.scene.cycles.use_denoising if bpy.context.scene.render.engine == 'CYCLES' else False,
            "use_adaptive_sampling": bpy.context.scene.cycles.use_adaptive_sampling if bpy.context.scene.render.engine == 'CYCLES' else False,
            "light_bounces": bpy.context.scene.cycles.max_bounces if bpy.context.scene.render.engine == 'CYCLES' else 0
        }
        
        # Apply settings based on quality
        if target_quality == "preview":
            # Use Eevee for preview quality
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            bpy.context.scene.eevee.taa_render_samples = 16
            bpy.context.scene.eevee.use_gtao = True
            bpy.context.scene.eevee.use_bloom = True
            bpy.context.scene.render.use_motion_blur = False
            bpy.context.scene.eevee.use_volumetric_shadows = True
            bpy.context.scene.eevee.use_ssr = False
            bpy.context.scene.eevee.shadow_cube_size = '512'
            bpy.context.scene.eevee.shadow_cascade_size = '512'
        
        elif target_quality == "medium":
            # Use Eevee for medium quality
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            bpy.context.scene.eevee.taa_render_samples = 64
            bpy.context.scene.eevee.use_gtao = True
            bpy.context.scene.eevee.use_bloom = True
            bpy.context.scene.render.use_motion_blur = True
            bpy.context.scene.eevee.use_volumetric_shadows = True
            bpy.context.scene.eevee.use_ssr = True
            bpy.context.scene.eevee.shadow_cube_size = '1024'
            bpy.context.scene.eevee.shadow_cascade_size = '1024'
        
        elif target_quality == "high":
            # Use Cycles for high quality
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.samples = 128
            bpy.context.scene.cycles.use_denoising = True
            bpy.context.scene.cycles.use_adaptive_sampling = True
            bpy.context.scene.cycles.caustics_reflective = False
            bpy.context.scene.cycles.caustics_refractive = False
            bpy.context.scene.render.use_motion_blur = True
            bpy.context.scene.cycles.max_bounces = 4
            bpy.context.scene.cycles.transparent_max_bounces = 8
            
            # Use GPU if available
            if self.optimization_settings["use_gpu"]:
                bpy.context.scene.cycles.device = 'GPU'
                
                # Enable all available GPUs
                if hasattr(bpy.context.preferences.addons["cycles"], "preferences"):
                    cycles_prefs = bpy.context.preferences.addons["cycles"].preferences
                    cycles_prefs.compute_device_type = 'CUDA'  # or 'OPTIX' or 'HIP' depending on hardware
                    
                    for device in cycles_prefs.devices:
                        device.use = True
        
        elif target_quality == "ultra":
            # Use Cycles for ultra quality
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.samples = 512
            bpy.context.scene.cycles.use_denoising = True
            bpy.context.scene.cycles.use_adaptive_sampling = True
            bpy.context.scene.cycles.caustics_reflective = True
            bpy.context.scene.cycles.caustics_refractive = True
            bpy.context.scene.render.use_motion_blur = True
            bpy.context.scene.cycles.max_bounces = 8
            bpy.context.scene.cycles.transparent_max_bounces = 16
            
            # Use GPU if available
            if self.optimization_settings["use_gpu"]:
                bpy.context.scene.cycles.device = 'GPU'
                
                # Enable all available GPUs
                if hasattr(bpy.context.preferences.addons["cycles"], "preferences"):
                    cycles_prefs = bpy.context.preferences.addons["cycles"].preferences
                    cycles_prefs.compute_device_type = 'CUDA'  # or 'OPTIX' or 'HIP' depending on hardware
                    
                    for device in cycles_prefs.devices:
                        device.use = True
        
        return {
            "target_quality": target_quality,
            "original_settings": original_settings,
            "success": True
        }
    
    def optimize_physics_simulation(self, quality: str = "medium") -> Dict:
        """
        Optimize physics simulation settings.
        
        Args:
            quality: Physics quality level (low, medium, high)
            
        Returns:
            Dict with optimization results
        """
        # Store original settings
        original_settings = {
            "substeps": bpy.context.scene.rigidbody_world.substeps if hasattr(bpy.context.scene, "rigidbody_world") else 10,
            "solver_iterations": bpy.context.scene.rigidbody_world.solver_iterations if hasattr(bpy.context.scene, "rigidbody_world") else 10,
            "point_cache_frame_step": bpy.context.scene.rigidbody_world.point_cache.frame_step if hasattr(bpy.context.scene, "rigidbody_world") and hasattr(bpy.context.scene.rigidbody_world, "point_cache") else 1
        }
        
        # Apply settings based on quality
        if hasattr(bpy.context.scene, "rigidbody_world"):
            if quality == "low":
                bpy.context.scene.rigidbody_world.substeps = 5
                bpy.context.scene.rigidbody_world.solver_iterations = 5
                if hasattr(bpy.context.scene.rigidbody_world, "point_cache"):
                    bpy.context.scene.rigidbody_world.point_cache.frame_step = 2
            
            elif quality == "medium":
                bpy.context.scene.rigidbody_world.substeps = 10
                bpy.context.scene.rigidbody_world.solver_iterations = 10
                if hasattr(bpy.context.scene.rigidbody_world, "point_cache"):
                    bpy.context.scene.rigidbody_world.point_cache.frame_step = 1
            
            elif quality == "high":
                bpy.context.scene.rigidbody_world.substeps = 20
                bpy.context.scene.rigidbody_world.solver_iterations = 20
                if hasattr(bpy.context.scene.rigidbody_world, "point_cache"):
                    bpy.context.scene.rigidbody_world.point_cache.frame_step = 1
        
        # Update the optimization settings
        self.optimization_settings["physics_quality"] = quality
        
        return {
            "quality": quality,
            "original_settings": original_settings,
            "success": hasattr(bpy.context.scene, "rigidbody_world")
        }
    
    def get_system_info(self) -> Dict:
        """
        Get system information for performance analysis.
        
        Returns:
            Dict with system information
        """
        system_info = {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "blender_version": bpy.app.version_string,
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "gpu_info": self._get_gpu_info()
        }
        
        return system_info
    
    def _get_gpu_info(self) -> List[Dict]:
        """
        Get GPU information.
        
        Returns:
            List of dicts with GPU information
        """
        gpu_info = []
        
        # Try to get GPU info from Cycles preferences
        if hasattr(bpy.context.preferences.addons, "cycles") and "cycles" in bpy.context.preferences.addons:
            cycles_prefs = bpy.context.preferences.addons["cycles"].preferences
            if hasattr(cycles_prefs, "devices"):
                for device in cycles_prefs.devices:
                    gpu_info.append({
                        "name": device.name,
                        "type": device.type,
                        "use": device.use
                    })
        
        return gpu_info
    
    def analyze_performance_metrics(self) -> Dict:
        """
        Analyze collected performance metrics.
        
        Returns:
            Dict with performance analysis
        """
  <response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>