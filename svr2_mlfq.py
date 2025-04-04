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
import heapq

from tasks import Task
from tasks import create_priority_queues


class TaskSrv2(Task):

    def __lt__(self, other):
        """
        Compare two tasks based on their priority and burst time.

        If the priorities do not match, the task with the higher priority comes first.
        If the priorities match, the task with the shorter remaining burst time comes first.

        Parameters:
            other: Another TaskSrv2 instance

        Returns:
            True if this task should come before the other task
        """

        # Higher priority tasks will come first, and if priorities match, sort by burst time
        return self.priority > other.priority if self.priority != other.priority else self.burst_time < other.burst_time


def aging(queues, aging_threshold, aging_increment):
    """
    Increment the waiting time of each task in the queues, and increase its priority
    by aging_increment if the waiting time exceeds aging_threshold.

    Parameters:
        queues: The queues containing the tasks to age
        aging_threshold: The waiting time threshold for aging
        aging_increment: The priority increment for aging tasks
    """
    for queue in queues:
        for task in queue:
            task.waiting_time += 1  # Increment waiting time for each task
            if task.waiting_time >= aging_threshold:
                task.priority += aging_increment  # Increase priority
                task.waiting_time = 0  # Reset waiting time


def svr2_multilevel_feedback_queue(queues, queue_quanta, task_quantum, aging_threshold, aging_increment):
    """
    Simulates the SVR2 (System V Release 2) Unix scheduling algorithm,
    which uses a Multilevel Feedback Queue (MLFQ) and incorporates aging.

    The algorithm iterates through the queues, starting with the highest-priority queue.
    For each queue, it executes as many tasks as possible within the allocated time quantum.
    If a task is not completed within the allocated time, it is moved to a lower-priority queue.
    The algorithm continues until all queues are empty.

    Parameters:
        queues (list of lists): A list of queues, where each queue is a list of Task objects.
        queue_quanta (list of int): A list of time quanta for each queue.
        task_quantum (int): A maximum time allocated to any task in a single turn.
        aging_threshold (int): The number of cycles after which priority is incremented.
        aging_increment (int): The amount by which priority increases due to aging.
    """
    print("Execution Order:")
    queue_count = len(queues)
    current_queue = queue_count - 1  # Start with the last queue (more priority)

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
                    if current_queue - 1 >= 0:
                        # Demote to the next lower-priority queue
                        heapq.heappush(queues[current_queue - 1], task)

                    else:
                        # If it's the lowest-priority queue, keep it there
                        heapq.heappush(queues[current_queue], task)

        # Move to the next queue
        current_queue = (current_queue - 1)
        if current_queue < 0:
            current_queue = queue_count - 1

        # Apply aging after each round
        aging(queues, aging_threshold, aging_increment)

if __name__ == "__main__":

    # Example
    tasks = [
        TaskSrv2("Task1", priority=2, burst_time=10),
        TaskSrv2("Task2", priority=8, burst_time=20),
        TaskSrv2("Task3", priority=4, burst_time=5),
        TaskSrv2("Task4", priority=6, burst_time=15),
        TaskSrv2("Task5", priority=5, burst_time=8)
    ]

    # Define priority ranges for queues (e.g., Queue 0 for priorities 1-3, Queue 1 for 4-6, etc.)
    priority_ranges = [(1, 3), (4, 6), (7, 10)]

    # Create queues
    queues = create_priority_queues(tasks, priority_ranges)

    # Define queue quanta (different time quanta for each queue)
    queue_quanta = [6, 8, 10]  # Queue 0 has the shortest quantum, Queue 2 has the longest quantum
    task_quantum = 4           # Maximum time allocated to any task in a single turn

    # Aging parameters
    aging_threshold = 5        # Number of cycles after which priority is incremented
    aging_increment = 1        # Amount by which priority increases due to aging

    svr2_multilevel_feedback_queue(queues, queue_quanta, task_quantum, aging_threshold, aging_increment)
