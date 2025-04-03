import heapq

from tasks import Task


class TaskSrv2(Task):
 
    def __lt__(self, other):
        # Higher priority tasks will come first, and if priorities match, sort by burst time
        return self.priority > other.priority if self.priority != other.priority else self.burst_time < other.burst_time

def aging(queues, aging_threshold, aging_increment):
    for queue in queues:
        for task in queue:
            task.waiting_time += 1  # Increment waiting time for each task
            if task.waiting_time >= aging_threshold:
                task.priority += aging_increment  # Increase priority
                task.waiting_time = 0  # Reset waiting time

"""
The SVR2 (System V Release 2) Unix Implementation of the 
Multilevel Feedback Queue is known for incorporating the 
idea of aging and dynamically adjusting task priority to avoid starvation.

- Tasks accumulate a "waiting time" when they remain in a queue without being executed.
If a task's waiting time exceeds a threshold (aging_threshold), 
its priority is increased (aging_increment), ensuring older tasks eventually move up 
in priority and avoid starvation.

- Tasks start in the highest-priority queue and move to lower-priority queues 
if they are not completed within their allocated time.

- The priority of tasks is adjusted dynamically based on their waiting time, 
allowing long-waiting tasks to break through the queue hierarchy.
"""
def svr2_multilevel_feedback_queue(tasks, queue_quanta, task_quantum, aging_threshold, aging_increment):
    # Create priority queues for multilevel feedback queues
    queues = [[] for _ in range(len(queue_quanta))]
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

                execution_time = min(task.burst_time, task_quantum, remaining_time)
                print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units")
                task.burst_time -= execution_time
                remaining_time -= execution_time

                # If the task is not completed, demote or keep it in the current queue
                if task.burst_time > 0:
                    if current_queue + 1 < len(queues):  # Demote to the next lower-priority queue
                        heapq.heappush(queues[current_queue + 1], task)
                    else:  # If it's the lowest-priority queue, keep it there
                        heapq.heappush(queues[current_queue], task)
        current_queue = (current_queue + 1) % queue_count  # Move to the next queue

        # Apply aging after each round
        aging(queues, aging_threshold, aging_increment)

# Example
tasks = [
    TaskSrv2("Task1", priority=1, burst_time=10),
    TaskSrv2("Task2", priority=2, burst_time=20),
    TaskSrv2("Task3", priority=3, burst_time=5),
    TaskSrv2("Task4", priority=1, burst_time=15),
    TaskSrv2("Task5", priority=2, burst_time=8)
]

# Define queue quanta (different time quanta for each queue)
queue_quanta = [8, 16, 32]  # Queue 0 has the shortest quantum, Queue 2 has the longest quantum
task_quantum = 4           # Maximum time allocated to any task in a single turn

# Aging parameters
aging_threshold = 5        # Number of cycles after which priority is incremented
aging_increment = 1        # Amount by which priority increases due to aging

svr2_multilevel_feedback_queue(tasks, queue_quanta, task_quantum, aging_threshold, aging_increment)
