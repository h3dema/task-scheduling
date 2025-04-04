"""
    Priority Queue for shortest remaining time (STR) Scheduling

    This scheduler implements a multi-queue scheduling algorithm where tasks are divided into separate priority queues
    based on their remaining burst time.
    Each queue is assigned a quantum time, and tasks are executed in a round-robin fashion across the queues.
    Each queue is implemented as a priority queue using Python's heapq.
    The tasks are sorted into queues based on their priority ranges, which are defined as tuples of (min_priority, max_priority).
    The scheduler uses a multi-queue approach to manage tasks with different priorities.
    Each queue operates as an independent priority queue, and tasks are dynamically re-added as they are processed.
    Tasks are stored and retrieved based on their remaining burst time, ensuring that the task with the STR is executed first.

    The scheduler processes queues cyclically, allocating each queue its respective quantum (queue_quanta).
    This implementation ensures that tasks with shorter remaining times are always prioritized within their respective queue while balancing fairness across queues. Let me know if you'd like additional modifications!

    The `__lt__` method in the TaskSTR class ensures that tasks are automatically prioritized by remaining burst time.
"""
import heapq

from tasks import create_priority_queues
from tasks import Task


class TaskSTR(Task):

    def __lt__(self, other):
        """
        Compare two tasks based on their remaining burst time.

        Parameters:
            other (TaskSTR): Another TaskSTR instance

        Returns:
            True if this task has shorter remaining burst time than the other task
        """
        # Task with shorter remaining burst time will have higher priority in the priority queue
        return self.burst_time < other.burst_time


def multi_queue_str_priority_scheduler(queues, queue_quanta, task_quantum):
    """
    Priority Queue Scheduler for Shortest Remaining Time (STR) with Multiple Queues.

    This function implements a multi-queue scheduling algorithm where tasks are divided into
    separate priority queues based on their remaining burst time. Each queue has a specific
    quantum time, and tasks are executed in a round-robin fashion across the queues.

    Tasks are stored in priority queues with the shortest remaining time prioritized.
    During each cycle, the scheduler selects the task with the shortest remaining time
    from the current queue, executes it for the lesser of task's burst time, task quantum,
    or remaining queue quantum, and then re-inserts the task if it hasn't completed.

    Parameters:
        queues (list): A list of priority queues (heaps), each containing TaskSTR objects.
                       Each priority queue represents a different priority range.
        queue_quanta (list): A list of time quanta for each queue.
        task_quantum (int): Maximum time allocated to each task per turn.

    Returns:
        None
    """

    print("Execution Order:")
    queue_count = len(queues)
    current_queue = queue_count - 1  # Start with the last queue (more priority)

    while any(queues):  # Continue until all priority queues are empty
        if queues[current_queue]:
            remaining_time = queue_quanta[current_queue]  # Quantum for the current queue

            # ---------------------------------------------------------------------------------------
            # **NOTE**:
            #
            # this implementation runs the same task consecutively if it has smaller burst time,
            # when its quantum finishes, the task remains with the smallest burst time
            # in the queue and will be executed again in the next cycle.
            # This can lead to starvation for tasks with larger burst times.
            # ---------------------------------------------------------------------------------------
            while remaining_time > 0 and queues[current_queue]:
                task = heapq.heappop(queues[current_queue])  # Get the task with the shortest remaining time

                execution_time = min(task.burst_time, task_quantum, remaining_time)
                print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units")
                task.burst_time -= execution_time
                remaining_time -= execution_time

                if task.burst_time > 0:
                    heapq.heappush(queues[current_queue], task)  # Reinsert task into the priority queue if not completed
        # Move to the next queue
        current_queue = (current_queue - 1)
        if current_queue < 0:
            current_queue = queue_count - 1


if __name__ == "__main__":
    #
    # Example
    #

    # Define tasks
    # TODO: with dependencies?
    tasks = [
        TaskSTR("Task1", priority=2, burst_time=10),
        TaskSTR("Task2", priority=5, burst_time=15),
        TaskSTR("Task3", priority=8, burst_time=7),
        TaskSTR("Task4", priority=4, burst_time=12),
        TaskSTR("Task5", priority=6, burst_time=6)
    ]

    # Define priority ranges for queues (e.g., Queue 0 for priorities 1-3, Queue 1 for 4-6, etc.)
    priority_ranges = [(1, 3), (4, 6), (7, 10)]

    # Create priority queues
    queues = create_priority_queues(tasks, priority_ranges)

    # Define quantum times for each queue
    queue_quanta = [6, 8, 10]  # Different time quanta for each queue
    # Time allocated to each task per turn
    # TODO: maybe different for each queue?
    task_quantum = 4

    multi_queue_str_priority_scheduler(queues, queue_quanta, task_quantum)
