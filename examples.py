"""
Example script demonstrating individual scheduling algorithms
"""

from process import Process
from scheduler import FCFSScheduler, SJFScheduler, RoundRobinScheduler, PriorityScheduler, SRTFScheduler
from visualization import print_gantt_chart, print_statistics


def example_fcfs():
    """Example: First Come First Serve"""
    print("\n" + "="*70)
    print("Example: First Come First Serve (FCFS)")
    print("="*70 + "\n")
    
    processes = [
        Process(1, 0, 6, 0),
        Process(2, 2, 4, 0),
        Process(3, 4, 5, 0),
        Process(4, 6, 3, 0),
    ]
    
    scheduler = FCFSScheduler(processes)
    stats, metrics, gantt = scheduler.schedule()
    
    print_gantt_chart(gantt, "FCFS")
    print_statistics(stats, metrics, "FCFS")


def example_sjf():
    """Example: Shortest Job First"""
    print("\n" + "="*70)
    print("Example: Shortest Job First (SJF)")
    print("="*70 + "\n")
    
    processes = [
        Process(1, 0, 7, 0),
        Process(2, 2, 4, 0),
        Process(3, 4, 1, 0),
        Process(4, 5, 4, 0),
    ]
    
    scheduler = SJFScheduler(processes)
    stats, metrics, gantt = scheduler.schedule()
    
    print_gantt_chart(gantt, "SJF")
    print_statistics(stats, metrics, "SJF")


def example_srtf():
    """Example: Shortest Remaining Time First"""
    print("\n" + "="*70)
    print("Example: Shortest Remaining Time First (SRTF)")
    print("="*70 + "\n")
    
    processes = [
        Process(1, 0, 8, 0),
        Process(2, 1, 4, 0),
        Process(3, 2, 2, 0),
        Process(4, 3, 1, 0),
    ]
    
    scheduler = SRTFScheduler(processes)
    stats, metrics, gantt = scheduler.schedule()
    
    print_gantt_chart(gantt, "SRTF")
    print_statistics(stats, metrics, "SRTF")


def example_round_robin():
    """Example: Round Robin with different time quanta"""
    print("\n" + "="*70)
    print("Example: Round Robin Scheduling")
    print("="*70 + "\n")
    
    processes = [
        Process(1, 0, 5, 0),
        Process(2, 1, 3, 0),
        Process(3, 2, 8, 0),
        Process(4, 3, 6, 0),
    ]
    
    for quantum in [2, 3, 4]:
        print(f"\nTime Quantum = {quantum}")
        print("-" * 70)
        scheduler = RoundRobinScheduler(processes, time_quantum=quantum)
        stats, metrics, gantt = scheduler.schedule()
        
        print_gantt_chart(gantt, f"Round Robin (Q={quantum})")
        print_statistics(stats, metrics, f"Round Robin (Q={quantum})")


def example_priority():
    """Example: Priority Scheduling"""
    print("\n" + "="*70)
    print("Example: Priority Scheduling (Lower number = Higher priority)")
    print("="*70 + "\n")
    
    processes = [
        Process(1, 0, 4, priority=2),
        Process(2, 1, 3, priority=1),
        Process(3, 2, 5, priority=3),
        Process(4, 3, 2, priority=1),
    ]
    
    scheduler = PriorityScheduler(processes)
    stats, metrics, gantt = scheduler.schedule()
    
    print_gantt_chart(gantt, "Priority Scheduling")
    print_statistics(stats, metrics, "Priority Scheduling")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print(" "*15 + "SCHEDULING ALGORITHM EXAMPLES")
    print("="*70)
    
    example_fcfs()
    example_sjf()
    example_srtf()
    example_round_robin()
    example_priority()
    
    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
