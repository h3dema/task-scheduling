import heapq

from svr2. import TaskSrv2, aging


def can_run(task, completed_tasks):
    # Check if all dependencies of the task are satisfied
    return all(dep in completed_tasks for dep in task.dependencies)


"""
the Multilevel Feedback Queue (MLFQ) scheduler considering dependencies between tasks.
The tasks will now only execute if their dependencies are satisfied, 
meaning all the tasks they depend on must complete before they can run.
"""
def svr2_mlfq_with_dependencies(tasks, queue_quanta, task_quantum, aging_threshold, aging_increment):
    # Create multilevel priority queues
    queues = [[] for _ in range(len(queue_quanta))]
    task_map = {task.name: task for task in tasks}  # Map task names to task objects
    completed_tasks = set()  # Keep track of completed tasks

    for task in tasks:
        heapq.heappush(queues[0], task)  # Initially, all tasks start in the highest-priority queue

    print("Execution Order:")
    queue_count = len(queues)
    current_queue = 0

    while any(queues):  # Continue until all queues are empty
        if queues[current_queue]:
            remaining_time = queue_quanta[current_queue]  # Quantum for the current queue

            while remaining_time > 0 and queues[current_queue]:
                task = heapq.heappop(queues[current_queue])

                if can_run(task, completed_tasks):  # Check if the task's dependencies are met
                    execution_time = min(task.burst_time, task_quantum, remaining_time)
                    print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units")
                    task.burst_time -= execution_time
                    remaining_time -= execution_time

                    if task.burst_time > 0:
                        if current_queue + 1 < len(queues):  # Demote to the next lower-priority queue
                            heapq.heappush(queues[current_queue + 1], task)
                        else:  # If it's the lowest-priority queue, keep it there
                            heapq.heappush(queues[current_queue], task)
                    else:
                        task.completed = True
                        completed_tasks.add(task.name)
                        print(f"Task {task.name} has completed")
                else:
                    print(f"Task {task.name} (Queue {current_queue}) cannot run due to unmet dependencies")
                    heapq.heappush(queues[current_queue], task)  # Re-add the task for future evaluation
                    break  # Exit the loop to give other queues a chance
        current_queue = (current_queue + 1) % queue_count  # Move to the next queue

        # Apply aging after each round
        aging(queues, aging_threshold, aging_increment)

# Example
tasks = [
    Task("Task1", priority=1, burst_time=10),
    Task("Task2", priority=2, burst_time=15, dependencies=["Task1"]),
    Task("Task3", priority=3, burst_time=5, dependencies=["Task1"]),
    Task("Task4", priority=1, burst_time=20, dependencies=["Task2", "Task3"]),
    Task("Task5", priority=2, burst_time=8)
]

# Define queue quanta
queue_quanta = [8, 16, 32]  # Queue 0 has the shortest quantum, Queue 2 has the longest quantum
task_quantum = 4           # Maximum time allocated to any task in a single turn

# Aging parameters
aging_threshold = 5        # Number of cycles after which priority is incremented
aging_increment = 1        # Amount by which priority increases due to aging

svr2_mlfq_with_dependencies(tasks, queue_quanta, task_quantum, aging_threshold, aging_increment)
