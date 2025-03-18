"""
BlenderMCP Ultimate Cinematic Upgrade - Integration Module
This module integrates all the enhanced functionality modules with the existing BlenderMCP addon.
"""

import bpy
import os
import json
import importlib
from typing import Dict, List, Optional, Any, Union

# Import BlenderMCP modules
from blender_mcp.modules.asset_management import (
    mixamo_integration,
    sketchfab_integration,
    turbosquid_integration,
    quixel_integration
)
from blender_mcp.modules.scene_setup import (
    hdri_lighting,
    procedural_environment,
    scene_composition
)
from blender_mcp.modules.character_animation import (
    rigify_auto_rigging,
    animation_retargeting,
    ikfk_switching,
    keyframe_generation,
    cinematic_camera
)
from blender_mcp.modules.physics_vfx import (
    cloth_physics,
    hair_physics,
    rigid_body_physics,
    particle_effects
)
from blender_mcp.modules.rendering import (
    render_engine_manager,
    post_processing,
    multi_camera_manager
)
from blender_mcp.modules.progress_tracking import (
    progress_tracker,
    progress_wrapper,
    progress_ui,
    ProgressStatus
)
from blender_mcp.modules.performance_optimization import (
    performance_optimizer,
    error_handler,
    compatibility_tester
)

class BlenderMCPUltimate:
    """
    Main integration class for BlenderMCP Ultimate Cinematic Upgrade.
    Provides a unified interface for all enhanced functionality.
    """
    
    def __init__(self):
        self.modules = {
            "asset_management": {
                "mixamo": mixamo_integration,
                "sketchfab": sketchfab_integration,
                "turbosquid": turbosquid_integration,
                "quixel": quixel_integration
            },
            "scene_setup": {
                "hdri_lighting": hdri_lighting,
                "procedural_environment": procedural_environment,
                "scene_composition": scene_composition
            },
            "character_animation": {
                "rigify_auto_rigging": rigify_auto_rigging,
                "animation_retargeting": animation_retargeting,
                "ikfk_switching": ikfk_switching,
                "keyframe_generation": keyframe_generation,
                "cinematic_camera": cinematic_camera
            },
            "physics_vfx": {
                "cloth_physics": cloth_physics,
                "hair_physics": hair_physics,
                "rigid_body_physics": rigid_body_physics,
                "particle_effects": particle_effects
            },
            "rendering": {
                "render_engine_manager": render_engine_manager,
                "post_processing": post_processing,
                "multi_camera_manager": multi_camera_manager
            },
            "progress_tracking": {
                "progress_tracker": progress_tracker,
                "progress_wrapper": progress_wrapper,
                "progress_ui": progress_ui
            },
            "performance_optimization": {
                "performance_optimizer": performance_optimizer,
                "error_handler": error_handler,
                "compatibility_tester": compatibility_tester
            }
        }
        
        # Initialize progress tracking UI
        progress_ui.start_updates()
        
        # Run compatibility checks
        self.compatibility_results = compatibility_tester.run_all_checks()
        
        # Register error handlers
        self._register_error_handlers()
    
    def _register_error_handlers(self):
        """Register error handlers for common error types."""
        
        # Handler for memory errors
        def handle_memory_error(error_info):
            # Try to optimize memory usage
            optimization_result = performance_optimizer.optimize_memory_usage()
            return {
                "action": "memory_optimization",
                "result": optimization_result
            }
        
        error_handler.register_error_handler("MemoryError", handle_memory_error)
        
        # Handler for render errors
        def handle_render_error(error_info):
            # Try to optimize render settings
            optimization_result = performance_optimizer.optimize_render_settings("medium")
            return {
                "action": "render_optimization",
                "result": optimization_result
            }
        
        error_handler.register_error_handler("RenderError", handle_render_error)
    
    def execute_command(self, command: str, params: Dict = None) -> Dict:
        """
        Execute a command with the specified parameters.
        
        Args:
            command: Command to execute
            params: Parameters for the command
            
        Returns:
            Dict with command result
        """
        if params is None:
            params = {}
        
        # Generate a unique operation ID for progress tracking
        operation_id = f"cmd_{command}_{id(params)}"
        
        # Start tracking the operation
        progress_tracker.start_operation(
            operation_id=operation_id,
            operation_name=f"Executing command: {command}",
            total_steps=100
        )
        
        try:
            # Update progress
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=10,
                message=f"Parsing command: {command}"
            )
            
            # Parse the command to determine which module and function to call
            command_parts = command.split('.')
            
            if len(command_parts) < 2:
                return {
                    "status": "error",
                    "message": f"Invalid command format: {command}"
                }
            
            # Extract module and function names
            module_name = command_parts[0]
            function_name = command_parts[-1]
            submodule_path = command_parts[1:-1] if len(command_parts) > 2 else []
            
            # Update progress
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=20,
                message=f"Locating module: {module_name}"
            )
            
            # Check if the module exists
            if module_name not in self.modules:
                progress_tracker.fail_operation(
                    operation_id=operation_id,
                    error_message=f"Module not found: {module_name}"
                )
                return {
                    "status": "error",
                    "message": f"Module not found: {module_name}"
                }
            
            # Navigate to the submodule if specified
            module = self.modules[module_name]
            for submodule in submodule_path:
                if submodule not in module:
                    progress_tracker.fail_operation(
                        operation_id=operation_id,
                        error_message=f"Submodule not found: {submodule}"
                    )
                    return {
                        "status": "error",
                        "message": f"Submodule not found: {submodule}"
                    }
                module = module[submodule]
            
            # Update progress
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=30,
                message=f"Locating function: {function_name}"
            )
            
            # Check if the function exists
            if not hasattr(module, function_name):
                progress_tracker.fail_operation(
                    operation_id=operation_id,
                    error_message=f"Function not found: {function_name}"
                )
                return {
                    "status": "error",
                    "message": f"Function not found: {function_name}"
                }
            
            # Get the function
            func = getattr(module, function_name)
            
            # Update progress
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=50,
                message=f"Executing function: {function_name}"
            )
            
            # Measure performance
            performance_result = performance_optimizer.measure_performance(
                operation_name=command,
                callback=lambda: func(**params)
            )
            
            # Get the result
            result = performance_result["result"]
            
            # Update progress
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=90,
                message=f"Processing result"
            )
            
            # Add performance metrics to the result
            if isinstance(result, dict):
                result["performance_metrics"] = performance_result["metrics"]
            
            # Complete the operation
            progress_tracker.complete_operation(
                operation_id=operation_id,
                message=f"Command executed successfully: {command}"
            )
            
            return result
        
        except Exception as e:
            # Log the error
            error_info = error_handler.log_error(
                error_type=type(e).__name__,
                error_message=str(e),
                operation_name=command,
                context=params
            )
            
            # Fail the operation
            progress_tracker.fail_operation(
                operation_id=operation_id,
                error_message=str(e)
            )
            
            return {
                "status": "error",
                "message": str(e),
                "error_info": error_info
            }
    
    def get_available_commands(self) -> Dict:
        """
        Get a list of all available commands.
        
        Returns:
            Dict with available commands
        """
        commands = {}
        
        for module_name, module in self.modules.items():
            commands[module_name] = self._get_module_commands(module, module_name)
        
        return commands
    
    def _get_module_commands(self, module, prefix):
        """
        Recursively get commands from a module.
        
        Args:
            module: Module to get commands from
            prefix: Command prefix
            
        Returns:
            Dict with module commands
        """
        commands = {}
        
        if isinstance(module, dict):
            # This is a module dictionary
            for submodule_name, submodule in module.items():
                subcommands = self._get_module_commands(submodule, f"{prefix}.{submodule_name}")
                commands.update(subcommands)
        else:
            # This is an actual module
            for attr_name in dir(module):
                # Skip private attributes
                if attr_name.startswith('_'):
                    continue
                
                attr = getattr(module, attr_name)
                
                # Only include functions and methods
                if callable(attr):
                    command = f"{prefix}.{attr_name}"
                    commands[command] = {
                        "name": command,
                        "doc": attr.__doc__ or "No documentation available"
                    }
        
        return commands
    
    def create_cinematic_sequence(self, prompt: str, duration: int = 250, quality: str = "medium") -> Dict:
        """
        Create a complete cinematic sequence from a text prompt.
        
        Args:
            prompt: Text prompt describing the desired sequence
            duration: Duration of the sequence in frames
            quality: Quality level (preview, medium, high, ultra)
            
        Returns:
            Dict with sequence creation result
        """
        # Generate a unique operation ID for progress tracking
        operation_id = f"cinematic_sequence_{id(prompt)}"
        
        # Start tracking the operation
        progress_tracker.start_operation(
            operation_id=operation_id,
            operation_name="Creating cinematic sequence",
            total_steps=100
        )
        
        try:
            # Step 1: Parse the prompt to extract key elements
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=5,
                message="Analyzing prompt"
            )
            
            # In a real implementation, this would use AI to parse the prompt
            # For now, we'll just use some simple parsing
            
            # Step 2: Set up the scene
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=10,
                message="Setting up scene"
            )
            
            # Clear the existing scene
            bpy.ops.wm.read_factory_settings(use_empty=True)
            
            # Step 3: Create environment
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=20,
                message="Creating environment"
            )
            
            # Create a simple environment based on the prompt
            environment_result = self.execute_command(
                "scene_setup.procedural_environment.create_environment",
                {
                    "environment_type": "generic",
                    "prompt": prompt
                }
            )
            
            # Step 4: Import characters
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=30,
                message="Importing characters"
            )
            
            # Import a character
            character_result = self.execute_command(
                "asset_management.mixamo.import_character",
                {
                    "character_type": "generic"
                }
            )
            
            # Step 5: Set up animation
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=40,
                message="Setting up animation"
            )
            
            # Create a simple animation based on the prompt
            animation_result = self.execute_command(
                "character_animation.keyframe_generation.generate_animation",
                {
                    "character_name": character_result.get("character_name", "Character"),
                    "animation_type": "generic",
                    "prompt": prompt,
                    "duration": duration
                }
            )
            
            # Step 6: Set up camera
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=50,
                message="Setting up camera"
            )
            
            # Create a cinematic camera
            camera_result = self.execute_command(
                "character_animation.cinematic_camera.create_cinematic_camera",
                {
                    "camera_type": "tracking",
                    "target_name": character_result.get("character_name", "Character"),
                    "duration": duration
                }
            )
            
            # Step 7: Add physics and effects
            progress_tracker.update_progress(
                operation_id=operation_id,
                step=60,
                message="Adding physics and effects"
            )
            
            # Add some physics effects based on the prompt
            physics_result = self.execute_command(
                "physics_vfx.particle_effects.create_fog",
                {
                    "name": "At<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>