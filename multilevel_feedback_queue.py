from collections import deque

from tasks import Task


"""
Multilevel Feedback Queue (MLFQ) scheduler.
In an MLFQ, tasks can move between multiple levels of queues based on their behavior, 
such as time spent in a queue or whether they complete their burst time allocation.

- Tasks are organized into multiple levels of queues. High-priority tasks start 
in the highest-priority queue (Queue 0) and are demoted to lower-priority queues 
if they are not completed within the allocated time quantum.

- Each queue has a unique time quantum (queue_quanta), which determines the 
total amount of time the scheduler allocates to tasks in that queue during one pass.

- Tasks are initially placed in the highest-priority queue. If a task isn’t completed within its allocated time, it is moved to a lower-priority queue.
Tasks in lower-priority queues receive larger time quanta, reflecting their reduced priority.
"""
def multilevel_feedback_queue(tasks, queue_quanta, task_quantum):
    # Create multilevel feedback queues
    queues = [deque() for _ in range(len(queue_quanta))]

    # Initially, all tasks are added to the highest-priority queue (Queue 0)
    for task in tasks:
        queues[0].append(task)

    print("Execution Order:")
    while any(queues):  # Continue until all queues are empty
        for i in range(len(queues)):
            queue = queues[i]
            queue_quantum = queue_quanta[i]

            remaining_time = queue_quantum
            while remaining_time > 0 and queue:
                task = queue.popleft()

                execution_time = min(task.burst_time, task_quantum, remaining_time)
                print(f"Task {task.name} (Queue {i}) executed for {execution_time} units")
                task.burst_time -= execution_time
                remaining_time -= execution_time

                # If the task is not completed, demote it to the next queue
                if task.burst_time > 0:
                    if i + 1 < len(queues):  # Demote to the next lower-priority queue
                        queues[i + 1].append(task)
                    else:  # If it's the lowest-priority queue, put it back in the same queue
                        queue.append(task)

# Example
tasks = [
    Task("Task1", priority=1, burst_time=10),
    Task("Task2", priority=2, burst_time=20),
    Task("Task3", priority=3, burst_time=5),
    Task("Task4", priority=1, burst_time=15),
    Task("Task5", priority=2, burst_time=8)
]

# Define queue quanta (different time quanta for each queue)
queue_quanta = [8, 16, 32]  # Queue 0 has the shortest quantum, Queue 2 has the longest quantum
task_quantum = 4           # Maximum time allocated to any task in a single turn

multilevel_feedback_queue(tasks, queue_quanta, task_quantum)
