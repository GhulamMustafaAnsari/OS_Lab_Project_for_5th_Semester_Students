#!/usr/bin/env python3
"""
Test suite for CPU scheduling algorithms
"""

from process import Process, ProcessState
from scheduler import FCFSScheduler, SJFScheduler, RoundRobinScheduler, PriorityScheduler, SRTFScheduler


def test_process_creation():
    """Test process creation and initialization"""
    print("Testing process creation...")
    p = Process(1, 0, 5, 2)
    
    assert p.pid == 1
    assert p.arrival_time == 0
    assert p.burst_time == 5
    assert p.priority == 2
    assert p.state == ProcessState.NEW
    assert p.remaining_time == 5
    print("✓ Process creation test passed")


def test_fcfs():
    """Test FCFS scheduling algorithm"""
    print("\nTesting FCFS scheduling...")
    processes = [
        Process(1, 0, 4, 0),
        Process(2, 1, 3, 0),
        Process(3, 2, 2, 0),
    ]
    
    scheduler = FCFSScheduler(processes)
    stats, metrics, gantt = scheduler.schedule()
    
    # Verify completion times
    assert stats[0]['completion_time'] == 4  # P1: 0-4
    assert stats[1]['completion_time'] == 7  # P2: 4-7
    assert stats[2]['completion_time'] == 9  # P3: 7-9
    
    # Verify turnaround times
    assert stats[0]['turnaround_time'] == 4  # 4 - 0
    assert stats[1]['turnaround_time'] == 6  # 7 - 1
    assert stats[2]['turnaround_time'] == 7  # 9 - 2
    
    print("✓ FCFS test passed")


def test_sjf():
    """Test SJF scheduling algorithm"""
    print("\nTesting SJF scheduling...")
    processes = [
        Process(1, 0, 7, 0),
        Process(2, 2, 4, 0),
        Process(3, 4, 1, 0),
        Process(4, 5, 4, 0),
    ]
    
    scheduler = SJFScheduler(processes)
    stats, metrics, gantt = scheduler.schedule()
    
    # Verify that shortest jobs are executed first (when available)
    # P1 arrives at 0 and must execute first: 0-7
    # P3 has burst 1 (shortest): 7-8
    # P2 and P4 both have burst 4, P2 arrived first: 8-12
    # P4: 12-16
    
    assert stats[0]['pid'] == 1
    assert stats[0]['completion_time'] == 7
    
    print("✓ SJF test passed")


def test_round_robin():
    """Test Round Robin scheduling algorithm"""
    print("\nTesting Round Robin scheduling...")
    processes = [
        Process(1, 0, 5, 0),
        Process(2, 1, 3, 0),
        Process(3, 2, 1, 0),
    ]
    
    scheduler = RoundRobinScheduler(processes, time_quantum=2)
    stats, metrics, gantt = scheduler.schedule()
    
    # All processes should complete
    assert len(stats) == 3
    assert all(s['pid'] in [1, 2, 3] for s in stats)
    
    print("✓ Round Robin test passed")


def test_priority():
    """Test Priority scheduling algorithm"""
    print("\nTesting Priority scheduling...")
    processes = [
        Process(1, 0, 4, priority=2),
        Process(2, 1, 3, priority=1),
        Process(3, 2, 2, priority=3),
    ]
    
    scheduler = PriorityScheduler(processes)
    stats, metrics, gantt = scheduler.schedule()
    
    # P1 starts at 0 (only process available): 0-4
    # P2 has priority 1 (highest): 4-7
    # P3 has priority 3 (lowest): 7-9
    
    assert stats[0]['pid'] == 1
    assert stats[1]['pid'] == 2
    assert stats[2]['pid'] == 3
    
    print("✓ Priority scheduling test passed")


def test_srtf():
    """Test SRTF scheduling algorithm"""
    print("\nTesting SRTF scheduling...")
    processes = [
        Process(1, 0, 8, 0),
        Process(2, 1, 4, 0),
        Process(3, 2, 2, 0),
        Process(4, 3, 1, 0),
    ]
    
    scheduler = SRTFScheduler(processes)
    stats, metrics, gantt = scheduler.schedule()
    
    # All processes should complete
    assert len(stats) == 4
    
    print("✓ SRTF test passed")


def test_metrics_calculation():
    """Test that metrics are calculated correctly"""
    print("\nTesting metrics calculation...")
    processes = [
        Process(1, 0, 3, 0),
        Process(2, 2, 2, 0),
    ]
    
    scheduler = FCFSScheduler(processes)
    stats, metrics, gantt = scheduler.schedule()
    
    # Verify metrics exist
    assert 'avg_turnaround_time' in metrics
    assert 'avg_waiting_time' in metrics
    assert 'avg_response_time' in metrics
    assert 'total_processes' in metrics
    
    assert metrics['total_processes'] == 2
    
    print("✓ Metrics calculation test passed")


def run_all_tests():
    """Run all test cases"""
    print("="*70)
    print(" "*20 + "RUNNING TEST SUITE")
    print("="*70)
    
    try:
        test_process_creation()
        test_fcfs()
        test_sjf()
        test_round_robin()
        test_priority()
        test_srtf()
        test_metrics_calculation()
        
        print("\n" + "="*70)
        print(" "*20 + "ALL TESTS PASSED ✓")
        print("="*70 + "\n")
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        print("="*70 + "\n")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        print("="*70 + "\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
