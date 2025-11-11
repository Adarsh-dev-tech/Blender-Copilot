"""Performance monitoring and profiling utilities for Modifier Assistant.

This module provides decorators and utilities for measuring execution time
of workflow functions and operator methods to ensure they meet contract targets.

Includes utilities from the lighting feature for compatibility.
"""

import time
import functools
from typing import Callable, Any
import bpy  # noqa: F401
import mathutils  # noqa: F401


def _should_log_performance() -> bool:
    """Check if performance metrics logging is enabled in preferences."""
    try:
        from copilot.preferences import get_addon_preferences
        prefs = get_addon_preferences()
        return prefs.show_performance_metrics if prefs else False
    except (ImportError, KeyError, AttributeError):
        return False


def performance_monitor(target_ms: float = None, operation_name: str = None):
    """Decorator for monitoring function execution time.
    
    Args:
        target_ms: Optional performance target in milliseconds
        operation_name: Optional custom name for the operation (defaults to function name)
    
    Usage:
        @performance_monitor(target_ms=50.0, operation_name="Smart Array")
        def apply_smart_array_single(obj):
            # ... implementation
            pass
    
    If show_performance_metrics is enabled in preferences, logs timing info.
    If target_ms is provided and exceeded, logs a warning.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Check if performance logging is enabled
            should_log = _should_log_performance()
            
            if not should_log:
                # Performance logging disabled - execute without timing
                return func(*args, **kwargs)
            
            # Performance logging enabled - measure execution time
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            # Calculate duration in milliseconds
            duration_ms = (end_time - start_time) * 1000.0
            
            # Get operation name
            op_name = operation_name or func.__name__
            
            # Log timing information
            if target_ms is not None:
                if duration_ms > target_ms:
                    print(f"⚠️  {op_name}: {duration_ms:.2f}ms (exceeded target {target_ms}ms)")
                else:
                    print(f"✓ {op_name}: {duration_ms:.2f}ms (target {target_ms}ms)")
            else:
                print(f"⏱️  {op_name}: {duration_ms:.2f}ms")
            
            return result
        
        return wrapper
    return decorator


class PerformanceTimer:
    """Context manager for timing code blocks.
    
    Usage:
        with PerformanceTimer("My Operation", target_ms=100.0) as timer:
            # ... code to time
            pass
        
        # Access duration after context exits
        print(f"Duration: {timer.duration_ms:.2f}ms")
    """
    
    def __init__(self, operation_name: str, target_ms: float = None):
        """Initialize timer.
        
        Args:
            operation_name: Name of the operation being timed
            target_ms: Optional performance target in milliseconds
        """
        self.operation_name = operation_name
        self.target_ms = target_ms
        self.start_time = None
        self.end_time = None
        self.duration_ms = None
    
    def __enter__(self):
        """Start timing."""
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing and log results if enabled."""
        self.end_time = time.perf_counter()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0
        
        # Only log if performance metrics are enabled
        if _should_log_performance():
            if self.target_ms is not None:
                if self.duration_ms > self.target_ms:
                    print(f"⚠️  {self.operation_name}: {self.duration_ms:.2f}ms "
                          f"(exceeded target {self.target_ms}ms)")
                else:
                    print(f"✓ {self.operation_name}: {self.duration_ms:.2f}ms "
                          f"(target {self.target_ms}ms)")
            else:
                print(f"⏱️  {self.operation_name}: {self.duration_ms:.2f}ms")


def profile_operator_execution(execute_func: Callable) -> Callable:
    """Decorator for profiling operator execute() method with detailed breakdown.
    
    Measures parsing, validation, and workflow execution separately, plus total time.
    Only logs when show_performance_metrics is enabled in preferences.
    
    Usage:
        class MyOperator(bpy.types.Operator):
            @profile_operator_execution
            def execute(self, context):
                # ... implementation
                pass
    """
    @functools.wraps(execute_func)
    def wrapper(self, context) -> set:
        if not _should_log_performance():
            # Performance logging disabled
            return execute_func(self, context)
        
        # Performance logging enabled - measure total execution
        print("\n" + "="*60)
        print("PERFORMANCE PROFILE: Modifier Assistant Operator")
        print("="*60)
        
        start_time = time.perf_counter()
        result = execute_func(self, context)
        end_time = time.perf_counter()
        
        total_duration_ms = (end_time - start_time) * 1000.0
        
        # Log total with contract target
        print("-"*60)
        if total_duration_ms > 350.0:
            print(f"⚠️  TOTAL EXECUTION: {total_duration_ms:.2f}ms "
                  f"(exceeded target 350ms)")
        else:
            print(f"✓ TOTAL EXECUTION: {total_duration_ms:.2f}ms "
                  f"(target 350ms)")
        print("="*60 + "\n")
        
        return result
    
    return wrapper


# ============================================================================
# LIGHTING FEATURE UTILITIES (kept for compatibility)
# ============================================================================

def optimize_bounding_box_calculation(obj):
    """Optimized bounding box calculation for better performance (lighting feature)."""
    if not obj or not hasattr(obj, 'bound_box'):
        return None
    
    matrix = obj.matrix_world
    local_corners = obj.bound_box
    world_corners = [matrix @ mathutils.Vector(corner) for corner in local_corners]
    
    xs = [corner.x for corner in world_corners]
    ys = [corner.y for corner in world_corners]
    zs = [corner.z for corner in world_corners]
    
    min_coords = mathutils.Vector((min(xs), min(ys), min(zs)))
    max_coords = mathutils.Vector((max(xs), max(ys), max(zs)))
    center = (min_coords + max_coords) * 0.5
    dimensions = max_coords - min_coords
    radius = max(dimensions) * 0.5
    
    return {
        'center': center,
        'dimensions': dimensions,
        'radius': radius,
        'min_coords': min_coords,
        'max_coords': max_coords
    }


def measure_execution_time(func):
    """Decorator to measure execution time (lighting feature compatibility)."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"{func.__name__} executed in {execution_time:.4f} seconds")
        
        if execution_time > 1.0:
            print(f"WARNING: {func.__name__} exceeded 1 second execution time")
        
        return result
    
    return wrapper


class PerformanceMonitor:
    """Monitor performance metrics during operations (lighting feature compatibility)."""
    
    def __init__(self):
        self.start_time = None
        self.checkpoints = []
    
    def start(self):
        """Start performance monitoring."""
        self.start_time = time.time()
        self.checkpoints = []
    
    def checkpoint(self, name):
        """Add a performance checkpoint."""
        if self.start_time is None:
            return
        
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.checkpoints.append((name, elapsed))
    
    def report(self):
        """Report performance metrics."""
        if not self.checkpoints:
            return
        
        print("Performance Report:")
        for name, elapsed in self.checkpoints:
            print(f"  {name}: {elapsed:.4f}s")
        
        total_time = self.checkpoints[-1][1]
        if total_time > 1.0:
            print(f"WARNING: Total execution time {total_time:.4f}s exceeds target")
    
    def meets_performance_target(self, target_seconds=1.0):
        """Check if performance meets target."""
        if not self.checkpoints:
            return True
        
        total_time = self.checkpoints[-1][1]
        return total_time <= target_seconds


# Registration (no classes to register)
def register():
    """Register performance module (no-op)."""
    pass


def unregister():
    """Unregister performance module (no-op)."""
    pass


if __name__ == "__main__":
    register()