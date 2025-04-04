"""
Multilevel Feedback Queue (MLFQ) scheduler.

This implementation simulates a Multilevel Feedback Queue (MLFQ) scheduling algorithm.
In an MLFQ, tasks can move between multiple levels of queues based on their behavior,
such as time spent in a queue or whether they complete their burst time allocation.

Tasks are organized into multiple levels of queues. High-priority tasks start
in the highest-priority queue (Queue 0) and are demoted to lower-priority queues
if they are not completed within the allocated time quantum.

Each queue has a unique time quantum (queue_quanta), which determines the
total amount of time the scheduler allocates to tasks in that queue during one pass.

Tasks are initially placed in the highest-priority queue.
If a task isn't completed within its allocated time, it is moved to a lower-priority queue.
Tasks in lower-priority queues receive larger time quanta, reflecting their reduced priority.
"""
from collections import deque

from tasks import Task
from tasks import create_queues


def multilevel_feedback_queue(queues, queue_quanta, task_quantum):
    """
    Simulates a Multilevel Feedback Queue (MLFQ) scheduling algorithm.

    The algorithm iterates through the queues, starting with the highest-priority queue.
    For each queue, it executes as many tasks as possible within the allocated time quantum.
    If a task is not completed within the allocated time, it is moved to a lower-priority queue.
    The algorithm continues until all queues are empty.

    Parameters:
        queues (list of deques): A list of queues, where each queue is a deque of Task objects.
        queue_quanta (list of int): A list of time quanta for each queue.
        task_quantum (int): A maximum time allocated to any task in a single turn.

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

                execution_time = min(task.burst_time, task_quantum, remaining_time)
                print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units")
                task.burst_time -= execution_time
                remaining_time -= execution_time

                # If the task is not completed, demote it to the next queue
                if task.burst_time > 0:
                    if current_queue - 1 >= 0:
                        # Demote to the next lower-priority queue
                        queues[current_queue - 1].append(task)
                    else:
                        # If it's the lowest-priority queue, put it back in the same queue
                        queues[current_queue].append(task)

        # Move to the next queue
        current_queue = (current_queue - 1)
        if current_queue < 0:
            current_queue = queue_count - 1


if __name__ == "__main__":
    # Example
    tasks = [
        Task("Task1", priority=2, burst_time=10),
        Task("Task2", priority=8, burst_time=20),
        Task("Task3", priority=4, burst_time=5),
        Task("Task4", priority=1, burst_time=15),
        Task("Task5", priority=5, burst_time=8)
    ]

    # Define priority ranges for queues (e.g., Queue 0 for priorities 1-3, Queue 1 for 4-6, etc.)
    priority_ranges = [(1, 3), (4, 6), (7, 10)]

    # Create queues
    queues = create_queues(tasks, priority_ranges)

    # Define queue quanta
    queue_quanta = [6, 8, 10]  # Different time quanta for each queue
    task_quantum = 4           # Maximum time allocated to any task in a single turn

    multilevel_feedback_queue(queues, queue_quanta, task_quantum)
