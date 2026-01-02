#!/usr/bin/env python3
"""
OS Lab Project: Multi-Threaded Process Management & CPU Scheduling Simulator
Main simulator that demonstrates various CPU scheduling algorithms and multi-threading concepts
"""

import sys
from typing import List
from process import Process
from scheduler import (FCFSScheduler, SJFScheduler, SRTFScheduler, 
                       RoundRobinScheduler, PriorityScheduler)
from visualization import (print_gantt_chart, print_statistics, 
                           compare_algorithms, print_header, print_section_separator)
from multithreading import MultiThreadedSimulator, SynchronizationDemo, demonstrate_deadlock_prevention


def create_sample_processes() -> List[Process]:
    """Create a sample set of processes for demonstration"""
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5, priority=2),
        Process(pid=2, arrival_time=1, burst_time=3, priority=1),
        Process(pid=3, arrival_time=2, burst_time=8, priority=3),
        Process(pid=4, arrival_time=3, burst_time=6, priority=2),
        Process(pid=5, arrival_time=4, burst_time=4, priority=1),
    ]
    return processes


def create_custom_processes() -> List[Process]:
    """Allow user to create custom processes"""
    processes = []
    print("\nEnter process details (or press Enter to finish):")
    
    pid = 1
    while True:
        try:
            print(f"\nProcess {pid}:")
            arrival_input = input(f"  Arrival Time (or press Enter to finish): ").strip()
            
            if not arrival_input:
                break
            
            arrival_time = int(arrival_input)
            burst_time = int(input(f"  Burst Time: "))
            priority = int(input(f"  Priority (lower = higher priority): "))
            
            processes.append(Process(pid, arrival_time, burst_time, priority))
            pid += 1
            
        except ValueError:
            print("Invalid input. Please enter integers only.")
        except KeyboardInterrupt:
            print("\n\nInput cancelled.")
            break
    
    return processes


def run_scheduling_algorithms(processes: List[Process]):
    """Run all CPU scheduling algorithms and display results"""
    if not processes:
        print("No processes to schedule!")
        return
    
    print_header("CPU SCHEDULING ALGORITHMS SIMULATION")
    
    # Store results for comparison
    results = {}
    
    # 1. FCFS Scheduling
    print_header("1. First Come First Serve (FCFS)")
    fcfs = FCFSScheduler(processes)
    stats, metrics, gantt = fcfs.schedule()
    print_gantt_chart(gantt, "FCFS")
    print_statistics(stats, metrics, "FCFS")
    results["FCFS"] = (stats, metrics)
    
    # 2. SJF Scheduling
    print_header("2. Shortest Job First (SJF)")
    sjf = SJFScheduler(processes)
    stats, metrics, gantt = sjf.schedule()
    print_gantt_chart(gantt, "SJF")
    print_statistics(stats, metrics, "SJF")
    results["SJF"] = (stats, metrics)
    
    # 3. SRTF Scheduling
    print_header("3. Shortest Remaining Time First (SRTF)")
    srtf = SRTFScheduler(processes)
    stats, metrics, gantt = srtf.schedule()
    print_gantt_chart(gantt, "SRTF")
    print_statistics(stats, metrics, "SRTF")
    results["SRTF"] = (stats, metrics)
    
    # 4. Round Robin Scheduling
    print_header("4. Round Robin (Time Quantum = 2)")
    rr = RoundRobinScheduler(processes, time_quantum=2)
    stats, metrics, gantt = rr.schedule()
    print_gantt_chart(gantt, "Round Robin (Q=2)")
    print_statistics(stats, metrics, "Round Robin (Q=2)")
    results["Round Robin (Q=2)"] = (stats, metrics)
    
    # 5. Priority Scheduling
    print_header("5. Priority Scheduling (Non-Preemptive)")
    priority = PriorityScheduler(processes)
    stats, metrics, gantt = priority.schedule()
    print_gantt_chart(gantt, "Priority Scheduling")
    print_statistics(stats, metrics, "Priority Scheduling")
    results["Priority Scheduling"] = (stats, metrics)
    
    # Compare all algorithms
    compare_algorithms(results)


def run_multithreading_demo(processes: List[Process]):
    """Run multi-threading demonstration"""
    print_header("MULTI-THREADED PROCESS SIMULATION")
    
    simulator = MultiThreadedSimulator(processes, max_concurrent=3)
    execution_log, shared_data = simulator.simulate()
    
    print("\nExecution Summary:")
    print(f"  Total processes: {len(processes)}")
    print(f"  Completed processes: {len(shared_data['completed'])}")
    print(f"  Process IDs completed: {sorted(shared_data['completed'])}")


def run_synchronization_demo():
    """Run process synchronization demonstration"""
    demo = SynchronizationDemo()
    demo.demonstrate_synchronization()
    demonstrate_deadlock_prevention()


def display_menu():
    """Display the main menu"""
    print("\n" + "="*90)
    print(" "*20 + "OS LAB PROJECT - CPU SCHEDULING SIMULATOR")
    print("="*90)
    print("\n1. Run All CPU Scheduling Algorithms (with sample data)")
    print("2. Run All CPU Scheduling Algorithms (with custom data)")
    print("3. Run Multi-Threaded Process Simulation")
    print("4. Run Process Synchronization Demonstration")
    print("5. Run Complete Demo (All Features)")
    print("6. Exit")
    print("\n" + "="*90)


def main():
    """Main program entry point"""
    print_header("Multi-Threaded Process Management & CPU Scheduling Simulator")
    print("OS Lab Project for 5th Semester Students\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        # Run complete demo automatically
        processes = create_sample_processes()
        run_scheduling_algorithms(processes)
        run_multithreading_demo(processes)
        run_synchronization_demo()
        return
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                processes = create_sample_processes()
                print("\nUsing sample processes:")
                for p in processes:
                    print(f"  {p}")
                run_scheduling_algorithms(processes)
                
            elif choice == '2':
                processes = create_custom_processes()
                if processes:
                    run_scheduling_algorithms(processes)
                else:
                    print("\nNo processes entered. Returning to menu.")
                
            elif choice == '3':
                processes = create_sample_processes()
                print("\nUsing sample processes:")
                for p in processes:
                    print(f"  {p}")
                run_multithreading_demo(processes)
                
            elif choice == '4':
                run_synchronization_demo()
                
            elif choice == '5':
                print("\n" + "="*90)
                print("Running Complete Demonstration...")
                print("="*90)
                processes = create_sample_processes()
                print("\nUsing sample processes:")
                for p in processes:
                    print(f"  {p}")
                
                run_scheduling_algorithms(processes)
                run_multithreading_demo(processes)
                run_synchronization_demo()
                
                print_header("DEMONSTRATION COMPLETE")
                print("All features have been demonstrated successfully!")
                
            elif choice == '6':
                print("\n" + "="*90)
                print("Thank you for using the CPU Scheduling Simulator!")
                print("="*90 + "\n")
                break
                
            else:
                print("\nInvalid choice. Please enter a number between 1 and 6.")
            
            # Wait for user before showing menu again
            if choice in ['1', '2', '3', '4', '5']:
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n" + "="*90)
            print("Program interrupted. Exiting...")
            print("="*90 + "\n")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
