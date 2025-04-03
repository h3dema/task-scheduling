import random
from collections import deque

from tasks import Task


class TaskL(Task):
    def __init__(self, name, priority, burst_time, tickets, dependencies=None):
        super().__init__(name, priority, burst_time, dependencies=dependencies)
        self.tickets = tickets  # Number of tickets assigned to the task


def draw_lottery(tasks):
    """Select a task randomly based on ticket distribution."""
    total_tickets = sum(task.tickets for task in tasks)
    if total_tickets == 0:
        return None  # No tickets left to draw
    winning_ticket = random.randint(1, total_tickets)
    cumulative_tickets = 0
    for task in tasks:
        cumulative_tickets += task.tickets
        if cumulative_tickets >= winning_ticket:
            return task


"""
Lottery Scheduling using multiple queues. 

Each queue can represent different priority levels, and tasks are assigned to 
queues based on their priority. Each queue is processed using lottery scheduling,
and queues are processed in a round-robin manner.

- Tasks are assigned to multiple queues based on their priority, 
with each queue having its own time quantum (queue_quanta).

- Each task includes a list of dependencies (other task names).
A task can only run if all its dependencies are completed.
The can_run function checks whether a task's dependencies are satisfied 
by comparing them with the completed_tasks set.

- The scheduler maintains a completed_tasks set to track tasks that have finished
execution. Once a task is completed, its name is added to completed_tasks, 
enabling dependent tasks to become runnable.

- Tasks in each queue are processed using lottery scheduling, 
but only tasks with satisfied dependencies are considered for the lottery draw.
"""
def multi_queue_lottery_scheduler_with_dependencies(tasks, queue_quanta, task_quantum):
    # Create multi-level queues (each as a deque)
    queues = [deque() for _ in range(len(queue_quanta))]

    # Map tasks by name for easy lookup and assign them to their respective queues
    task_map = {task.name: task for task in tasks}
    completed_tasks = set()

    for task in tasks:
        # Priority determines the queue index (e.g., priority 1 goes to queue 0)
        queue_index = min(task.priority - 1, len(queues) - 1)  # Map priority to valid queue
        queues[queue_index].append(task)

    print("Execution Order:")
    queue_count = len(queues)
    current_queue = 0

    while any(queues):  # Continue until all queues are empty
        if queues[current_queue]:
            remaining_time = queue_quanta[current_queue]  # Quantum for the current queue

            while remaining_time > 0 and queues[current_queue]:
                # Create a list of runnable tasks from the current queue
                runnable_tasks = [
                    task for task in queues[current_queue]
                    if task.burst_time > 0 and can_run(task, completed_tasks)
                ]

                if not runnable_tasks:
                    break

                # Draw a lottery to select the next task
                selected_task = draw_lottery(runnable_tasks)
                if not selected_task:
                    break

                # Execute the selected task
                execution_time = min(selected_task.burst_time, task_quantum, remaining_time)
                print(f"Task {selected_task.name} (Queue {current_queue}) executed for {execution_time} units")
                selected_task.burst_time -= execution_time
                remaining_time -= execution_time

                if selected_task.burst_time == 0:
                    selected_task.completed = True
                    completed_tasks.add(selected_task.name)
                    print(f"Task {selected_task.name} has completed")
                    queues[current_queue].remove(selected_task)
                else:
                    # Move the task to the back of the queue for fairness
                    queues[current_queue].remove(selected_task)
                    queues[current_queue].append(selected_task)
        current_queue = (current_queue + 1) % queue_count  # Move to the next queue

# Example
tasks = [
    Task("Task1", priority=1, burst_time=10, tickets=5),
    Task("Task2", priority=2, burst_time=15, tickets=10, dependencies=["Task1"]),
    Task("Task3", priority=3, burst_time=5, tickets=20, dependencies=["Task1"]),
    Task("Task4", priority=1, burst_time=20, tickets=8, dependencies=["Task2", "Task3"]),
    Task("Task5", priority=2, burst_time=8, tickets=12)
]

# Define queue quanta
queue_quanta = [8, 16, 32]  # Different quanta for each queue
task_quantum = 4           # Maximum time allocated to any task in a single turn

multi_queue_lottery_scheduler_with_dependencies(tasks, queue_quanta, task_quantum)
