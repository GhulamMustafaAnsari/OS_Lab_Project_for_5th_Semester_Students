"""
Visualization utilities for CPU scheduling simulation
"""

from typing import List, Tuple, Dict
from process import Process


def print_gantt_chart(gantt_chart: List[Tuple[int, int, str]], algorithm_name: str = ""):
    """
    Print a visual Gantt chart for process scheduling
    
    Args:
        gantt_chart: List of tuples (start_time, end_time, process_id)
        algorithm_name: Name of the scheduling algorithm
    """
    if not gantt_chart:
        return
    
    print(f"\n{'='*70}")
    if algorithm_name:
        print(f"Gantt Chart - {algorithm_name}")
    else:
        print("Gantt Chart")
    print(f"{'='*70}\n")
    
    # Print process names
    print("|", end="")
    for start, end, proc in gantt_chart:
        duration = end - start
        spacing = max(1, duration * 2 - len(proc))
        print(f" {proc}{' ' * spacing}|", end="")
    print()
    
    # Print timeline
    print(f"{gantt_chart[0][0]}", end="")
    for start, end, proc in gantt_chart:
        duration = end - start
        spacing = max(0, duration * 2 - len(str(end)) + len(proc))
        print(f"{' ' * spacing}{end}", end="")
    print("\n")


def print_process_table(processes: List[Process]):
    """
    Print a formatted table of process information
    
    Args:
        processes: List of Process objects
    """
    print(f"{'='*90}")
    print(f"{'Process Details':^90}")
    print(f"{'='*90}")
    print(f"{'PID':<6} {'Arrival':<10} {'Burst':<10} {'Priority':<10} {'Completion':<12} "
          f"{'TAT':<8} {'WT':<8} {'RT':<8}")
    print(f"{'-'*90}")
    
    for process in processes:
        print(f"{process.pid:<6} {process.arrival_time:<10} {process.burst_time:<10} "
              f"{process.priority:<10} {process.completion_time:<12} "
              f"{process.turnaround_time:<8} {process.waiting_time:<8} {process.response_time:<8}")
    
    print(f"{'='*90}\n")


def print_statistics(stats: List[dict], metrics: dict, algorithm_name: str = ""):
    """
    Print detailed statistics for scheduled processes
    
    Args:
        stats: List of process statistics dictionaries
        metrics: Average metrics dictionary
        algorithm_name: Name of the scheduling algorithm
    """
    print(f"{'='*90}")
    if algorithm_name:
        print(f"Statistics - {algorithm_name}")
    else:
        print("Statistics")
    print(f"{'='*90}\n")
    
    # Print individual process statistics
    print(f"{'PID':<6} {'Arrival':<10} {'Burst':<10} {'Priority':<10} {'Completion':<12} "
          f"{'TAT':<8} {'WT':<8} {'RT':<8}")
    print(f"{'-'*90}")
    
    for stat in stats:
        print(f"{stat['pid']:<6} {stat['arrival_time']:<10} {stat['burst_time']:<10} "
              f"{stat['priority']:<10} {stat['completion_time']:<12} "
              f"{stat['turnaround_time']:<8} {stat['waiting_time']:<8} {stat['response_time']:<8}")
    
    print(f"{'-'*90}")
    
    # Print average metrics
    print(f"\n{'Average Metrics':^90}")
    print(f"{'-'*90}")
    print(f"Average Turnaround Time: {metrics['avg_turnaround_time']}")
    print(f"Average Waiting Time:    {metrics['avg_waiting_time']}")
    print(f"Average Response Time:   {metrics['avg_response_time']}")
    print(f"Total Processes:         {metrics['total_processes']}")
    print(f"{'='*90}\n")


def compare_algorithms(results: Dict[str, Tuple[List[dict], dict]]):
    """
    Compare results from different scheduling algorithms
    
    Args:
        results: Dictionary mapping algorithm name to (stats, metrics) tuple
    """
    print(f"\n{'='*90}")
    print(f"{'Algorithm Comparison':^90}")
    print(f"{'='*90}\n")
    
    print(f"{'Algorithm':<25} {'Avg TAT':<15} {'Avg WT':<15} {'Avg RT':<15}")
    print(f"{'-'*90}")
    
    for algo_name, (stats, metrics) in results.items():
        print(f"{algo_name:<25} {metrics['avg_turnaround_time']:<15} "
              f"{metrics['avg_waiting_time']:<15} {metrics['avg_response_time']:<15}")
    
    print(f"{'='*90}\n")
    
    # Find best algorithm for each metric
    best_tat = min(results.items(), key=lambda x: x[1][1]['avg_turnaround_time'])
    best_wt = min(results.items(), key=lambda x: x[1][1]['avg_waiting_time'])
    best_rt = min(results.items(), key=lambda x: x[1][1]['avg_response_time'])
    
    print("Best Algorithms:")
    print(f"  Lowest Avg Turnaround Time: {best_tat[0]} ({best_tat[1][1]['avg_turnaround_time']})")
    print(f"  Lowest Avg Waiting Time:    {best_wt[0]} ({best_wt[1][1]['avg_waiting_time']})")
    print(f"  Lowest Avg Response Time:   {best_rt[0]} ({best_rt[1][1]['avg_response_time']})")
    print(f"{'='*90}\n")


def print_header(title: str):
    """Print a formatted header"""
    print(f"\n{'='*90}")
    print(f"{title:^90}")
    print(f"{'='*90}\n")


def print_section_separator():
    """Print a section separator"""
    print(f"\n{'-'*90}\n")
