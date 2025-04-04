"""
The SVR2 (System V Release 2) Unix Implementation with Multilevel Feedback Queue (MLFQ) scheduler
 considering dependencies between tasks.
The tasks will now only execute if their dependencies are satisfied,
meaning all the tasks they depend on must complete before they can run.

- Each task can define a list of dependencies (dependencies),
which are other tasks that must complete before it can run.
The can_run function checks if all dependencies for a task are satisfied
before allowing it to execute.

- A completed_tasks set keeps track of all tasks that have finished execution.
Tasks are only considered ready to run if all their dependencies are in
the completed_tasks set.

- Tasks are evaluated for dependencies before execution.
- If a tasks dependencies are not met, it is re-added to its current queue,
ensuring it remains in contention for future execution.
The scheduler skips the task and moves on to the next one.

- Aging is applied as before, ensuring that tasks stuck waiting
(even due to unmet dependencies) can gain priority over time.
"""
import heapq

from svr2_mlfq import TaskSrv2, aging
from tasks import create_priority_queues


def can_run(task, completed_tasks):
    """
    Determines if a task can be executed based on its dependencies.

    A task is allowed to run if all the tasks it depends on have been completed.

    Parameters:
        task (TaskSrv2): The task to be checked.
        completed_tasks (set): A set containing the names of completed tasks.

    Returns:
        bool: True if all dependencies of the task are met, False otherwise.
    """

    # Check if all dependencies of the task are satisfied
    return all(dep in completed_tasks for dep in task.dependencies)


def svr2_mlfq_with_dependencies(queues, queue_quanta, task_quantum, aging_threshold, aging_increment):
    """
    Simulates the SVR2 (System V Release 2) Unix scheduling algorithm,
    with the addition of task dependencies.

    This implementation simulates a Multilevel Feedback Queue (MLFQ) scheduling algorithm.
    In an MLFQ, tasks can move between multiple levels of queues based on their behavior,
    such as time spent in a queue or whether they complete their burst time allocation.

    The can_run function checks if all dependencies for a task are satisfied
    before allowing it to execute.

    - A completed_tasks set keeps track of all tasks that have finished execution.
    Tasks are only considered ready to run if all their dependencies are in
    the completed_tasks set.

    - Tasks are evaluated for dependencies before execution.
    - If a tasks dependencies are not met, it is re-added to its current queue,
    ensuring it remains in contention for future execution.
    The scheduler skips the task and moves on to the next one.

    - Aging is applied as before, ensuring that tasks stuck waiting
    (even due to unmet dependencies) can gain priority over time.

    Parameters:
        queues (list): A list of queues, where each queue is a priority queue
            (implemented as a list) of tasks.
        queue_quanta (list): A list of quantum times for each queue.
        task_quantum (int): The maximum time allocated to any task in a single turn.
        aging_threshold (int): The number of cycles after which priority is incremented.
        aging_increment (int): The amount by which priority increases due to aging.
    """
    completed_tasks = set()  # Keep track of completed tasks

    print("Execution Order:")
    queue_count = len(queues)
    current_queue = queue_count - 1  # Start with the last queue (more priority)

    while any(queues):  # Continue until all queues are empty
        if queues[current_queue]:
            remaining_time = queue_quanta[current_queue]  # Quantum for the current queue

            task_to_reinsert = []  # Placeholder for processed tasks to be reinserted
            while remaining_time > 0 and queues[current_queue]:
                task = heapq.heappop(queues[current_queue])

                if can_run(task, completed_tasks):  # Check if the task's dependencies are met
                    execution_time = min(task.burst_time, task_quantum, remaining_time)
                    print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units")
                    task.burst_time -= execution_time
                    remaining_time -= execution_time

                    if task.burst_time > 0:
                        if current_queue - 1 >= 0:  # Demote to the next lower-priority queue
                            heapq.heappush(queues[current_queue - 1], task)
                        else:
                            # If it's the lowest-priority queue, keep it there
                            task_to_reinsert.append(task)
                    else:
                        task.completed = True
                        completed_tasks.add(task.name)
                        print(f"Task {task.name} has completed")
                else:
                    print(f"Task {task.name} (Queue {current_queue}) cannot run due to unmet dependencies")
                    task_to_reinsert.append(task)  # Re-add the task for future evaluation

        if len(task_to_reinsert) > 0:
            for task in task_to_reinsert:
                heapq.heappush(queues[current_queue], task)

        # Move to the next queue
        current_queue = (current_queue - 1)
        if current_queue < 0:
            current_queue = queue_count - 1
        # print(f"Switching to Queue {current_queue - 1}")

        # Apply aging after each round
        aging(queues, aging_threshold, aging_increment)


if __name__ == "__main__":
    """
    Example usage of the MLFQ scheduler with dependencies.
    """

    # Define tasks with dependencies
    tasks = [
        TaskSrv2("Task1", priority=2, burst_time=10),
        TaskSrv2("Task2", priority=8, burst_time=15, dependencies=["Task1"]),
        TaskSrv2("Task3", priority=4, burst_time=5, dependencies=["Task1"]),
        TaskSrv2("Task4", priority=6, burst_time=20, dependencies=["Task2", "Task3"]),
        TaskSrv2("Task5", priority=5, burst_time=8)
    ]

    # Define priority ranges for queues (e.g., Queue 0 for priorities 1-3, Queue 1 for 4-6, etc.)
    priority_ranges = [(1, 3), (4, 6), (7, 10)]

    # Create queues
    queues = create_priority_queues(tasks, priority_ranges)

    # Define queue quanta
    queue_quanta = [6, 8, 10]  # Queue 0 has the shortest quantum, Queue 2 has the longest quantum
    task_quantum = 4           # Maximum time allocated to any task in a single turn

    # Aging parameters
    aging_threshold = 5        # Number of cycles after which priority is incremented
    aging_increment = 1        # Amount by which priority increases due to aging

    svr2_mlfq_with_dependencies(queues, queue_quanta, task_quantum, aging_threshold, aging_increment)
