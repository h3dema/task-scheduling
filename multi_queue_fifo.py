"""
    First-Come, First-Served (FCFS) Multi-Queue Scheduler

    This scheduler implements a multi-queue scheduling algorithm where tasks are divided
    into separate FIFO queues based on their priority. Each queue has its own time quantum.
    Queues are processed cyclically (round-robin). Each queue receives queue_quantum time.
    Tasks are divided into separate FIFO queues based on non-overlapping priority ranges
    (priority_ranges). Remaining tasks are re-added to the end of their respective queues.
"""

from tasks import Task
from tasks import create_queues


def multi_queue_scheduler(queues, queue_quanta, task_quantum):
    """
    First-Come, First-Served (FCFS) multi-queue scheduler.

    Tasks are divided into separate FIFO queues based on their priority. Each queue has its own time quantum.
    Queues are processed cyclically (round-robin). Each queue receives queue_quantum time.
    Tasks are divided into separate FIFO queues based on non-overlapping priority ranges (priority_ranges).
    Remaining tasks are re-added to the end of their respective queues.

    Parameters:
        queues (list): A list of lists of Task objects, where each sublist represents a queue
        queue_quanta (list): A list of time quanta for each queue
        task_quantum (int): Time allocated to each task per turn

    Returns:
        None
    """
    print("Execution Order:")
    queue_count = len(queues)
    current_queue = queue_count - 1  # Start with the last queue (more priority)

    while any(queues):  # Continue until all queues are empty
        if queues[current_queue]:
            remaining_time = queue_quanta[current_queue]  # Quantum for the current queue
            while remaining_time > 0 and queues[current_queue]:
                task = queues[current_queue].popleft()

                if task.burst_time > task_quantum:
                    execution_time = min(task_quantum, remaining_time)
                    print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units")
                    task.burst_time -= execution_time
                    remaining_time -= execution_time
                    if task.burst_time > 0:
                        queues[current_queue].append(task)
                else:
                    execution_time = min(task.burst_time, remaining_time)
                    print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units and completed")
                    remaining_time -= execution_time
        # Move to the next queue
        current_queue = (current_queue - 1)
        if current_queue < 0:
            current_queue = queue_count - 1


if __name__ == "__main__":
    #
    # Example
    #


    # Define tasks with dependencies
    # Notice that Task2 is put at the of the list below, so it will be executed last because Task4 and Task5 comes first.
    # TODO: maybe implement dependencies?
    tasks = [
        Task("Task1", priority=2, burst_time=10),
        Task("Task3", priority=8, burst_time=7),
        Task("Task4", priority=4, burst_time=12),
        Task("Task5", priority=6, burst_time=6),
        Task("Task2", priority=5, burst_time=15),
    ]

    # Define priority ranges for queues (e.g., Queue 0 for priorities 1-3, Queue 1 for 4-6, etc.)
    priority_ranges = [(1, 3), (4, 6), (7, 10)]

    # Create queues
    queues = create_queues(tasks, priority_ranges)

    # Define quantum times
    queue_quanta = [6, 8, 10]  # Different time quanta for each queue
    # Time allocated to each task per turn
    # TODO: maybe different for each queue?
    task_quantum = 4

    multi_queue_scheduler(queues, queue_quanta, task_quantum)
