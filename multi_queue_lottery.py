"""
    Lottery Scheduling using multiple queues.

    Each queue can represent different priority levels, and tasks are assigned to
    queues based on their priority. Each queue is processed using lottery scheduling,
    and queues are processed in a round-robin manner.

    - Tasks are assigned to multiple queues based on their priority,
    with each queue having its own time quantum (queue_quanta).

    - Task must be ojects of type `TaskLottery`.

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
import random
from collections import deque

from tasks import Task
from tasks import create_queues


class TaskLottery(Task):

    def __init__(self, name, priority, burst_time, tickets, dependencies=None):
        """
        Initialize a TaskLottery object.

        Args:
            name (str): Task name
            priority (int): Task priority
            burst_time (int): Task burst time
            tickets (int): Number of tickets assigned to the task
            dependencies (list or None): List of task names this task depends on
        """
        super().__init__(name, priority, burst_time, dependencies=dependencies)
        self.tickets = tickets  # Number of tickets assigned to the task


def draw_lottery(tasks):
    """
    Select a task randomly based on ticket distribution.

    This function takes a list of tasks, each with an assigned number of tickets,
    and selects one task randomly by drawing a ticket. A winning ticket is drawn
    randomly from a range of 1 to the total number of tickets across all tasks.
    The function iterates through the tasks, accumulating their ticket counts,
    and identifies the task whose ticket range includes the winning ticket number.

    If no tickets are available (i.e., all tasks have 0 tickets), the function
    returns None.

    Parameters:
        tasks (list): A list of TaskL objects participating in the lottery.

    Returns:
        TaskL or None: The task selected by the lottery, or None if there are no tickets.
    """

    total_tickets = sum(task.tickets for task in tasks)
    if total_tickets == 0:
        return None  # No tickets left to draw
    winning_ticket = random.randint(1, total_tickets)
    cumulative_tickets = 0
    for task in tasks:
        cumulative_tickets += task.tickets
        if cumulative_tickets >= winning_ticket:
            return task

def can_run(task, completed_tasks):
    """
    Check if a task is ready to run based on its dependencies and burst time remaining.

    A task is considered ready to run if all its dependencies have completed and it has
    remaining burst time.

    Parameters:
        task (TaskL): The task to check
        completed_tasks (set): A set of task names representing completed tasks

    Returns:
        bool: True if the task is ready to run, False otherwise
    """

    all_ok = all([x in completed_tasks for x in  task.dependencies])
    return all_ok and task.burst_time > 0



def multi_queue_lottery_scheduler_with_dependencies(queues, queue_quanta, task_quantum):
    """
    Multi-queue lottery scheduler considering dependencies between tasks.

    Tasks are assigned to multiple queues based on their priority, with each queue
    having its own time quantum (queue_quanta). Tasks are processed in a round-robin
    manner across queues, and a lottery is drawn for each task in the current queue
    to select the next task to execute. The lottery draw is based on the number of
    tickets assigned to each task. The can_run function checks if a task is ready to
    run based on its dependencies and burst time remaining.

    Parameters:
    - queues (list): A list of lists of TaskL objects, where each sublist represents a queue
    - queue_quanta (list): A list of time quanta for each queue
    - task_quantum (int): Time allocated to each task per turn

    Returns:
        None
    """
    # Map tasks by name for easy lookup and assign them to their respective queues
    task_map = {task.name: task for tasks in queues for task in tasks}
    completed_tasks = set()

    print("Execution Order:")
    queue_count = len(queues)
    current_queue = queue_count - 1  # Start with the last queue (more priority)

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
        # Move to the next queue
        current_queue = (current_queue - 1)
        if current_queue < 0:
            current_queue = queue_count - 1


if __name__ == "__main__":
    #
    # Example
    #
    # Starts with Queue 2 (highest priority),
    # Skips Queue 1, because all tasks have dependencies on Queue 0
    # Runs tasks on Queue 0 (lowest priority)
    # Then moves to Queue 1, after tasks from Queue 0 finish

    # Define tasks with dependencies
    tasks = [
        TaskLottery("Task1", priority=1, burst_time=10, tickets=5),
        TaskLottery("Task2", priority=2, burst_time=15, tickets=10, dependencies=["Task1"]),
        TaskLottery("Task3", priority=3, burst_time=5, tickets=20, dependencies=["Task1"]),
        TaskLottery("Task4", priority=4, burst_time=20, tickets=8, dependencies=["Task2", "Task3"]),
        TaskLottery("Task5", priority=7, burst_time=8, tickets=12)
    ]

    # Define queue quanta
    queue_quanta = [8, 16, 32]  # Different quanta for each queue
    # Maximum time allocated to any task in a single turn. If you want don't task_quantum to be limited, set it to a large number
    # (e.g., 1000). This is useful for tasks that may take a long time to complete.
    task_quantum = 4

    # Define priority ranges for queues (e.g., Queue 0 for priorities 1-3, Queue 1 for 4-6, etc.)
    priority_ranges = [(1, 3), (4, 6), (7, 10)]

    # Create queues
    queues = create_queues(tasks, priority_ranges)

    multi_queue_lottery_scheduler_with_dependencies(queues, queue_quanta, task_quantum)
