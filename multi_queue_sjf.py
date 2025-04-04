from collections import deque

from tasks import Task
from tasks import create_queues


def multi_queue_sjf_scheduler(queues, queue_quanta, task_quantum):
    """
    Shortest Job First (SJF) Multi-Queue Scheduler.

    Tasks are organized into multiple queues, each with its own time quantum.
    The scheduler processes tasks using the shortest job first policy within each queue.
    Queues are processed in a round-robin manner, starting with the highest-priority queue.
    Within each queue, tasks are sorted by their burst time, with shorter tasks given
    priority. Tasks exceeding their allocated burst time are re-added to their queue,
    ensuring that all tasks eventually complete execution.

    Parameters:
        queues (list): A list of deques, each containing Task objects. Each deque represents a queue.
        queue_quanta (list): A list of time quanta for each queue.
        task_quantum (int): Maximum time allocated to each task per turn.

    Returns:
        None
    """

    print("Execution Order:")
    queue_count = len(queues)
    current_queue = queue_count - 1  # Start with the last queue (more priority)

    while any(queues):  # Continue until all queues are empty
        if queues[current_queue]:
            # Sort the queue by burst time for SJF scheduling (shortest job first)
            # Note: This is a simple implementation. In a real-world scenario, you might want to consider other factors.
            # such as task priority or arrival time.
            # This implementation assumes that the queues are already sorted by priority.
            queues[current_queue] = deque(sorted(queues[current_queue], key=lambda t: t.burst_time, reverse=False))

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
    # Example
    tasks = [
        Task("Task1", priority=2, burst_time=10),
        Task("Task2", priority=5, burst_time=15),
        Task("Task3", priority=8, burst_time=7),
        Task("Task4", priority=4, burst_time=12),
        Task("Task5", priority=6, burst_time=6)
    ]

    # Define priority ranges for queues (e.g., Queue 0 for priorities 1-3, Queue 1 for 4-6, etc.)
    priority_ranges = [(1, 3), (4, 6), (7, 10)]

    # Create queues
    queues = create_queues(tasks, priority_ranges)

    # **Important**: It can simulate SJF, if you configure the `task_quantum` and `queue_quanta` values larger enough such as every task can be executed without preempting.
    # Define quantum times for each queue
    queue_quanta = [6, 8, 10]  # Different time quanta for each queue

    # Maximum time allocated to any task in a single turn. If you want don't task_quantum to be limited, set it to a large number
    # (e.g., 1000). This is useful for tasks that may take a long time to complete.
    task_quantum = 4

    multi_queue_sjf_scheduler(queues, queue_quanta, task_quantum)
