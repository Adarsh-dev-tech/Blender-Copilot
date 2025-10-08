import bpy
import time
import unittest
import psutil
import os
from typing import Dict, List, Tuple


class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmark tests for three-point lighting operator"""
    
    def setUp(self):
        """Set up test environment"""
        # Clear scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Reset to default state
        bpy.context.view_layer.update()
        
        # Track initial memory
        self.process = psutil.Process(os.getpid())
        self.initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Clear orphaned data
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    
    def create_test_object(self, complexity: str = 'simple') -> bpy.types.Object:
        """
        Create test objects of varying complexity.
        
        Args:
            complexity: 'simple', 'medium', 'complex', or 'extreme'
            
        Returns:
            Created test object
        """
        if complexity == 'simple':
            # Simple cube
            bpy.ops.mesh.primitive_cube_add()
            obj = bpy.context.active_object
            
        elif complexity == 'medium':
            # Subdivided monkey (medium complexity)
            bpy.ops.mesh.primitive_monkey_add()
            obj = bpy.context.active_object
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.subdivide(number_cuts=2)
            bpy.ops.object.mode_set(mode='OBJECT')
            
        elif complexity == 'complex':
            # Highly subdivided sphere
            bpy.ops.mesh.primitive_uv_sphere_add()
            obj = bpy.context.active_object
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.subdivide(number_cuts=4)
            bpy.ops.object.mode_set(mode='OBJECT')
            
        elif complexity == 'extreme':
            # Very high poly object
            bpy.ops.mesh.primitive_uv_sphere_add()
            obj = bpy.context.active_object
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.subdivide(number_cuts=6)
            bpy.ops.object.mode_set(mode='OBJECT')
        
        return obj
    
    def measure_execution_time(self, complexity: str, iterations: int = 3) -> Dict[str, float]:
        """
        Measure execution time for lighting creation.
        
        Args:
            complexity: Object complexity level
            iterations: Number of test iterations
            
        Returns:
            Dict with timing statistics
        """
        times = []
        
        for i in range(iterations):
            # Create fresh test object
            obj = self.create_test_object(complexity)
            obj_name = obj.name
            
            # Measure execution time
            start_time = time.time()
            result = bpy.ops.copilot.create_three_point_lighting()
            end_time = time.time()
            
            execution_time = end_time - start_time
            times.append(execution_time)
            
            # Verify operation succeeded
            self.assertIn(result, [{'FINISHED'}], 
                         f"Operation failed for {complexity} object")
            
            # Clean up for next iteration
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete(use_global=False)
        
        return {
            'min': min(times),
            'max': max(times),
            'avg': sum(times) / len(times),
            'times': times
        }
    
    def test_simple_object_performance(self):
        """Test performance with simple objects"""
        stats = self.measure_execution_time('simple')
        
        # Simple objects should execute very quickly
        self.assertLess(stats['max'], 0.5, 
                       f"Simple object execution too slow: {stats['max']:.3f}s")
        self.assertLess(stats['avg'], 0.3,
                       f"Simple object average too slow: {stats['avg']:.3f}s")
        
        print(f"Simple object performance: {stats}")
    
    def test_medium_object_performance(self):
        """Test performance with medium complexity objects"""
        stats = self.measure_execution_time('medium')
        
        # Medium objects should still be under 1 second
        self.assertLess(stats['max'], 1.0,
                       f"Medium object execution too slow: {stats['max']:.3f}s")
        self.assertLess(stats['avg'], 0.7,
                       f"Medium object average too slow: {stats['avg']:.3f}s")
        
        print(f"Medium object performance: {stats}")
    
    def test_complex_object_performance(self):
        """Test performance with complex objects"""
        stats = self.measure_execution_time('complex')
        
        # Complex objects should meet 1-second requirement
        self.assertLess(stats['max'], 1.0,
                       f"Complex object execution too slow: {stats['max']:.3f}s")
        
        print(f"Complex object performance: {stats}")
    
    def test_extreme_object_performance(self):
        """Test performance with very high-poly objects"""
        stats = self.measure_execution_time('extreme', iterations=1)
        
        # Even extreme objects should complete in reasonable time
        self.assertLess(stats['max'], 2.0,
                       f"Extreme object execution too slow: {stats['max']:.3f}s")
        
        print(f"Extreme object performance: {stats}")
        
        # Warn if approaching limits
        if stats['max'] > 1.5:
            print(f"WARNING: Extreme object near performance limit")
    
    def test_memory_usage(self):
        """Test memory usage during operations"""
        initial_memory = self.initial_memory
        
        # Create multiple lighting rigs
        memory_samples = []
        
        for i in range(5):
            obj = self.create_test_object('medium')
            
            # Measure memory before operation
            memory_before = self.process.memory_info().rss / 1024 / 1024
            
            # Execute operation
            bpy.ops.copilot.create_three_point_lighting()
            
            # Measure memory after operation
            memory_after = self.process.memory_info().rss / 1024 / 1024
            memory_delta = memory_after - memory_before
            
            memory_samples.append({
                'before': memory_before,
                'after': memory_after,
                'delta': memory_delta
            })
            
            # Don't clean up - test memory accumulation
        
        # Check memory usage
        total_memory_increase = memory_samples[-1]['after'] - initial_memory
        avg_per_operation = sum(s['delta'] for s in memory_samples) / len(memory_samples)
        
        print(f"Memory usage - Initial: {initial_memory:.1f}MB, "
              f"Final: {memory_samples[-1]['after']:.1f}MB, "
              f"Increase: {total_memory_increase:.1f}MB")
        print(f"Average per operation: {avg_per_operation:.1f}MB")
        
        # Memory usage should be reasonable
        self.assertLess(total_memory_increase, 100,
                       f"Excessive memory usage: {total_memory_increase:.1f}MB")
        self.assertLess(avg_per_operation, 20,
                       f"Excessive per-operation memory: {avg_per_operation:.1f}MB")
    
    def test_ui_responsiveness(self):
        """Test UI responsiveness during operation"""
        # This test is more qualitative - ensure operations don't block UI
        
        obj = self.create_test_object('complex')
        
        start_time = time.time()
        result = bpy.ops.copilot.create_three_point_lighting()
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Operation should complete quickly enough to not freeze UI
        self.assertLess(execution_time, 1.0,
                       "Operation may cause UI freeze")
        
        # In a real UI test, would check for UI updates during operation
        print(f"UI responsiveness test: {execution_time:.3f}s")
    
    def test_batch_operations(self):
        """Test performance with multiple consecutive operations"""
        times = []
        
        # Create multiple objects and lighting rigs in sequence
        for i in range(10):
            obj = self.create_test_object('simple')
            
            start_time = time.time()
            result = bpy.ops.copilot.create_three_point_lighting()
            end_time = time.time()
            
            times.append(end_time - start_time)
            
            # Verify success
            self.assertIn(result, [{'FINISHED'}])
        
        # Check for performance degradation over time
        first_half_avg = sum(times[:5]) / 5
        second_half_avg = sum(times[5:]) / 5
        
        performance_ratio = second_half_avg / first_half_avg
        
        print(f"Batch performance - First half: {first_half_avg:.3f}s, "
              f"Second half: {second_half_avg:.3f}s, "
              f"Ratio: {performance_ratio:.2f}")
        
        # Performance should not degrade significantly
        self.assertLess(performance_ratio, 1.5,
                       "Significant performance degradation in batch operations")
    
    def test_scale_variations(self):
        """Test performance with objects of different scales"""
        scales = [0.1, 1.0, 10.0, 100.0]
        scale_times = {}
        
        for scale in scales:
            obj = self.create_test_object('medium')
            obj.scale = (scale, scale, scale)
            bpy.context.view_layer.update()
            
            start_time = time.time()
            result = bpy.ops.copilot.create_three_point_lighting()
            end_time = time.time()
            
            scale_times[scale] = end_time - start_time
            
            # Clean up
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete(use_global=False)
        
        print(f"Scale performance: {scale_times}")
        
        # All scales should perform reasonably
        for scale, time_taken in scale_times.items():
            self.assertLess(time_taken, 1.0,
                           f"Scale {scale} too slow: {time_taken:.3f}s")
    
    def run_full_benchmark_suite(self):
        """Run complete performance benchmark suite"""
        print("\n" + "="*50)
        print("BLENDER COPILOT PERFORMANCE BENCHMARK")
        print("="*50)
        
        benchmark_results = {}
        
        test_methods = [
            ('Simple Objects', self.test_simple_object_performance),
            ('Medium Objects', self.test_medium_object_performance),
            ('Complex Objects', self.test_complex_object_performance),
            ('Memory Usage', self.test_memory_usage),
            ('UI Responsiveness', self.test_ui_responsiveness),
            ('Batch Operations', self.test_batch_operations),
            ('Scale Variations', self.test_scale_variations)
        ]
        
        for name, method in test_methods:
            print(f"\nRunning {name} test...")
            try:
                start = time.time()
                method()
                duration = time.time() - start
                benchmark_results[name] = {'status': 'PASS', 'duration': duration}
                print(f"✓ {name}: PASSED ({duration:.2f}s)")
            except AssertionError as e:
                benchmark_results[name] = {'status': 'FAIL', 'error': str(e)}
                print(f"✗ {name}: FAILED - {e}")
            except Exception as e:
                benchmark_results[name] = {'status': 'ERROR', 'error': str(e)}
                print(f"⚠ {name}: ERROR - {e}")
        
        # Summary
        print("\n" + "="*50)
        print("BENCHMARK SUMMARY")
        print("="*50)
        
        passed = sum(1 for r in benchmark_results.values() if r['status'] == 'PASS')
        total = len(benchmark_results)
        
        print(f"Tests passed: {passed}/{total}")
        
        if passed == total:
            print("🎉 ALL BENCHMARKS PASSED")
        else:
            print("⚠️  SOME BENCHMARKS FAILED")
        
        return benchmark_results


if __name__ == "__main__":
    # Run individual tests
    unittest.main()
    
    # Or run full benchmark suite
    # suite = TestPerformanceBenchmarks()
    # suite.run_full_benchmark_suite()