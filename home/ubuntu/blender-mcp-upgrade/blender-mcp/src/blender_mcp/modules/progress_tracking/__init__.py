"""
BlenderMCP Ultimate Cinematic Upgrade - Progress Tracking Module
This module provides real-time feedback on AI operations and task progress.
"""

import bpy
import time
import threading
import datetime
import json
from enum import Enum
from typing import Dict, List, Optional, Callable, Any, Union

class ProgressStatus(Enum):
    """Status values for progress tracking"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class ProgressTracker:
    """
    Main class for tracking progress of operations in BlenderMCP.
    Provides real-time feedback on AI operations.
    """
    
    def __init__(self):
        self.operations = {}
        self.active_operation_id = None
        self.listeners = []
        self.log_entries = []
        self.max_log_entries = 1000
        
        # Create a property group for Blender UI
        if not hasattr(bpy.types, "BlenderMCPProgressProperties"):
            class BlenderMCPProgressProperties(bpy.types.PropertyGroup):
                active_operation: bpy.props.StringProperty(
                    name="Active Operation",
                    description="Currently active operation",
                    default=""
                )
                progress: bpy.props.FloatProperty(
                    name="Progress",
                    description="Progress of the current operation",
                    default=0.0,
                    min=0.0,
                    max=1.0,
                    subtype='PERCENTAGE'
                )
                status: bpy.props.StringProperty(
                    name="Status",
                    description="Status of the current operation",
                    default="Not started"
                )
                message: bpy.props.StringProperty(
                    name="Message",
                    description="Current progress message",
                    default=""
                )
                
            bpy.utils.register_class(BlenderMCPProgressProperties)
            bpy.types.Scene.blender_mcp_progress = bpy.props.PointerProperty(type=BlenderMCPProgressProperties)
    
    def start_operation(self, operation_id: str, operation_name: str, total_steps: int = 100, parent_id: Optional[str] = None) -> Dict:
        """
        Start tracking a new operation.
        
        Args:
            operation_id: Unique identifier for the operation
            operation_name: Human-readable name of the operation
            total_steps: Total number of steps in the operation
            parent_id: ID of parent operation if this is a sub-operation
            
        Returns:
            Dict with operation information
        """
        timestamp = datetime.datetime.now().isoformat()
        
        operation = {
            "id": operation_id,
            "name": operation_name,
            "status": ProgressStatus.IN_PROGRESS.value,
            "progress": 0.0,
            "current_step": 0,
            "total_steps": total_steps,
            "start_time": timestamp,
            "end_time": None,
            "elapsed_time": 0,
            "estimated_time_remaining": None,
            "message": f"Starting {operation_name}...",
            "parent_id": parent_id,
            "sub_operations": [],
            "logs": []
        }
        
        self.operations[operation_id] = operation
        
        # If this is a sub-operation, add it to the parent
        if parent_id and parent_id in self.operations:
            self.operations[parent_id]["sub_operations"].append(operation_id)
        
        # Set as active operation if no other operation is active
        if self.active_operation_id is None:
            self.active_operation_id = operation_id
            
            # Update Blender UI properties
            if hasattr(bpy.context.scene, "blender_mcp_progress"):
                bpy.context.scene.blender_mcp_progress.active_operation = operation_name
                bpy.context.scene.blender_mcp_progress.progress = 0.0
                bpy.context.scene.blender_mcp_progress.status = "In progress"
                bpy.context.scene.blender_mcp_progress.message = f"Starting {operation_name}..."
        
        # Log the operation start
        self._log(operation_id, f"Started operation: {operation_name}")
        
        # Notify listeners
        self._notify_listeners("operation_started", operation)
        
        return operation
    
    def update_progress(self, operation_id: str, step: int = None, progress: float = None, message: Optional[str] = None) -> Dict:
        """
        Update the progress of an operation.
        
        Args:
            operation_id: ID of the operation to update
            step: Current step number (if using step-based progress)
            progress: Direct progress value between 0 and 1 (if not using steps)
            message: Optional message describing the current progress state
            
        Returns:
            Dict with updated operation information
        """
        if operation_id not in self.operations:
            return {"error": f"Operation {operation_id} not found"}
        
        operation = self.operations[operation_id]
        
        # Update step if provided
        if step is not None:
            operation["current_step"] = min(step, operation["total_steps"])
            operation["progress"] = operation["current_step"] / operation["total_steps"]
        
        # Or update progress directly if provided
        elif progress is not None:
            operation["progress"] = max(0.0, min(1.0, progress))
            operation["current_step"] = int(operation["progress"] * operation["total_steps"])
        
        # Update message if provided
        if message:
            operation["message"] = message
        
        # Calculate elapsed time
        start_time = datetime.datetime.fromisoformat(operation["start_time"])
        now = datetime.datetime.now()
        elapsed_seconds = (now - start_time).total_seconds()
        operation["elapsed_time"] = elapsed_seconds
        
        # Estimate remaining time
        if operation["progress"] > 0:
            estimated_total_time = elapsed_seconds / operation["progress"]
            estimated_remaining = estimated_total_time - elapsed_seconds
            operation["estimated_time_remaining"] = estimated_remaining
        
        # Update Blender UI properties if this is the active operation
        if operation_id == self.active_operation_id and hasattr(bpy.context.scene, "blender_mcp_progress"):
            bpy.context.scene.blender_mcp_progress.progress = operation["progress"]
            if message:
                bpy.context.scene.blender_mcp_progress.message = message
        
        # Log the progress update
        if message:
            self._log(operation_id, message)
        
        # Notify listeners
        self._notify_listeners("progress_updated", operation)
        
        return operation
    
    def complete_operation(self, operation_id: str, message: Optional[str] = None) -> Dict:
        """
        Mark an operation as completed.
        
        Args:
            operation_id: ID of the operation to complete
            message: Optional completion message
            
        Returns:
            Dict with completed operation information
        """
        if operation_id not in self.operations:
            return {"error": f"Operation {operation_id} not found"}
        
        operation = self.operations[operation_id]
        
        # Update operation status
        operation["status"] = ProgressStatus.COMPLETED.value
        operation["progress"] = 1.0
        operation["current_step"] = operation["total_steps"]
        operation["end_time"] = datetime.datetime.now().isoformat()
        
        if message:
            operation["message"] = message
        else:
            operation["message"] = f"Completed: {operation['name']}"
        
        # Calculate final elapsed time
        start_time = datetime.datetime.fromisoformat(operation["start_time"])
        end_time = datetime.datetime.fromisoformat(operation["end_time"])
        operation["elapsed_time"] = (end_time - start_time).total_seconds()
        operation["estimated_time_remaining"] = 0
        
        # Update Blender UI properties if this is the active operation
        if operation_id == self.active_operation_id and hasattr(bpy.context.scene, "blender_mcp_progress"):
            bpy.context.scene.blender_mcp_progress.progress = 1.0
            bpy.context.scene.blender_mcp_progress.status = "Completed"
            if message:
                bpy.context.scene.blender_mcp_progress.message = message
            else:
                bpy.context.scene.blender_mcp_progress.message = f"Completed: {operation['name']}"
        
        # Clear active operation if this was it
        if operation_id == self.active_operation_id:
            self.active_operation_id = None
            
            # Find a parent operation that's still in progress
            if operation["parent_id"] and operation["parent_id"] in self.operations:
                parent = self.operations[operation["parent_id"]]
                if parent["status"] == ProgressStatus.IN_PROGRESS.value:
                    self.active_operation_id = operation["parent_id"]
        
        # Log the operation completion
        self._log(operation_id, f"Completed operation: {operation['name']}")
        
        # Notify listeners
        self._notify_listeners("operation_completed", operation)
        
        return operation
    
    def fail_operation(self, operation_id: str, error_message: str) -> Dict:
        """
        Mark an operation as failed.
        
        Args:
            operation_id: ID of the operation that failed
            error_message: Error message describing the failure
            
        Returns:
            Dict with failed operation information
        """
        if operation_id not in self.operations:
            return {"error": f"Operation {operation_id} not found"}
        
        operation = self.operations[operation_id]
        
        # Update operation status
        operation["status"] = ProgressStatus.FAILED.value
        operation["end_time"] = datetime.datetime.now().isoformat()
        operation["message"] = f"Failed: {error_message}"
        
        # Calculate final elapsed time
        start_time = datetime.datetime.fromisoformat(operation["start_time"])
        end_time = datetime.datetime.fromisoformat(operation["end_time"])
        operation["elapsed_time"] = (end_time - start_time).total_seconds()
        
        # Update Blender UI properties if this is the active operation
        if operation_id == self.active_operation_id and hasattr(bpy.context.scene, "blender_mcp_progress"):
            bpy.context.scene.blender_mcp_progress.status = "Failed"
            bpy.context.scene.blender_mcp_progress.message = f"Failed: {error_message}"
        
        # Clear active operation if this was it
        if operation_id == self.active_operation_id:
            self.active_operation_id = None
        
        # Log the operation failure
        self._log(operation_id, f"Failed operation: {operation['name']} - {error_message}")
        
        # Notify listeners
        self._notify_listeners("operation_failed", operation)
        
        return operation
    
    def cancel_operation(self, operation_id: str) -> Dict:
        """
        Cancel an in-progress operation.
        
        Args:
            operation_id: ID of the operation to cancel
            
        Returns:
            Dict with cancelled operation information
        """
        if operation_id not in self.operations:
            return {"error": f"Operation {operation_id} not found"}
        
        operation = self.operations[operation_id]
        
        # Can only cancel operations that are in progress
        if operation["status"] != ProgressStatus.IN_PROGRESS.value:
            return {"error": f"Operation {operation_id} is not in progress"}
        
        # Update operation status
        operation["status"] = ProgressStatus.CANCELLED.value
        operation["end_time"] = datetime.datetime.now().isoformat()
        operation["message"] = "Cancelled"
        
        # Calculate final elapsed time
        start_time = datetime.datetime.fromisoformat(operation["start_time"])
        end_time = datetime.datetime.fromisoformat(operation["end_time"])
        operation["elapsed_time"] = (end_time - start_time).total_seconds()
        
        # Update Blender UI properties if this is the active operation
        if operation_id == self.active_operation_id and hasattr(bpy.context.scene, "blender_mcp_progress"):
            bpy.context.scene.blender_mcp_progress.status = "Cancelled"
            bpy.context.scene.blender_mcp_progress.message = "Operation cancelled"
        
        # Clear active operation if this was it
        if operation_id == self.active_operation_id:
            self.active_operation_id = None
        
        # Cancel all sub-operations
        for sub_op_id in operation["sub_operations"]:
            if sub_op_id in self.operations and self.operations[sub_op_id]["status"] == ProgressStatus.IN_PROGRESS.value:
                self.cancel_operation(sub_op_id)
        
        # Log the operation cancellation
        self._log(operation_id, f"Cancelled operation: {operation['name']}")
        
        # Notify listeners
        self._notify_listeners("operation_cancelled", operation)
        
        return operation
    
    def get_operation(self, operation_id: str) -> Dict:
        """
        Get information about an operation.
        
        Args:
            operation_id: ID of the operation to retrieve
            
        Returns:
            Dict with operation information
        """
        if operation_id not in self.operations:
            return {"error": f"Operation {operation_id} not found"}
        
        return self.operations[operation_id]
    
    def get_active_operation(self) -> Optional[Dict]:
        """
        Get the currently active operation.
        
        Returns:
            Dict with active operation information or None if no active operation
        """
        if self.active_operation_id and self.active_operation_id in self.operations:
            return self.operations[self.active_operation_id]
        
        return None
    
    def get_all_operations(self) -> Dict[str, Dict]:
        """
        Get all operations.
        
        Returns:
            Dict mapping operation IDs to operation information
        """
        return self.operations
    
    def add_listener(self, listener: Callable[[str, Dict], None]) -> None:
        """
        Add a listener for progress events.
        
        Args:
            listener: Callback function that takes event_type and operation_data
        """
        if listener not in self.listeners:
            self.listeners.append(listener)
    
    def remove_listener(self, listener: Callable[[str, Dict], None]) -> None:
        """
        Remove a progress event listener.
        
        Args:
            listener: Listener to remove
        """
        if listener in self.listeners:
            self.listeners.remove(listener)
    
    def _notify_listeners(self, event_type: str, operation_data: Dict) -> None:
        """
        Notify all listeners of a progress event.
        
        Args:
            event_type: Type of event (operation_started, progress_updated, etc.)
            operation_data: Data about the operation
        """
        for listener in self.listeners:
            try:
                listener(event_type, operation_data)
            except Exception as e:
                print(f"Error in progress listener: {str(e)}")
    
    def _log(self, opera<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>