import heapq

from tasks import Task
from tasks import create_priority_queues
from utils import can_run



"""
a heapq priority queue is used to manage tasks based on their priority.
The priority queue ensures that tasks with higher priority are processed first, if the dependencies are met.
After executing a task for the time quantum, if the task isn't finished,
it is reinserted into the priority queue for further processing
"""
def priority_based(queues, queue_quanta, task_quantum, reinsert=True):
    completed_tasks = set()  # Keep track of completed tasks
    print("Execution Order {}:".format("with task reinsertion" if reinsert else "without task reinsertion"))

    queue_count = len(queues)
    current_queue = queue_count - 1  # Start with the last queue (more priority)

    while any(queues):  # Continue until all queues are empty
        if queues[current_queue]:
            remaining_time = queue_quanta[current_queue]  # Quantum for the current queue

            task_to_reinsert = []
            while remaining_time > 0 and queues[current_queue]:
                task = heapq.heappop(queues[current_queue])

                if can_run(task, completed_tasks):  # Check if the task's dependencies are met
                    execution_time = min(task.burst_time, task_quantum, remaining_time)
                    print(f"Task {task.name} (Queue {current_queue}) executed for {execution_time} units")
                    task.burst_time -= execution_time
                    remaining_time -= execution_time

                    if task.burst_time > 0:
                        if reinsert:
                            heapq.heappush(queues[current_queue], task)
                        else:
                            task_to_reinsert.append(task)
                    else:
                        task.completed = True
                        completed_tasks.add(task.name)
                        print(f"Task {task.name} completed")
                else:
                    print(f"Task {task.name} (Queue {current_queue}) cannot run due to unmet dependencies")
                    # In this case, the only option is to re-add the task for future evaluation
                    # that way, given opportunity to the dependencies to complete
                    task_to_reinsert.append(task)

        if len(task_to_reinsert) > 0:
            for task in task_to_reinsert:
                heapq.heappush(queues[current_queue], task)

        # Move to the next queue
        current_queue = (current_queue - 1)
        if current_queue < 0:
            current_queue = queue_count - 1


def test(queues, queue_quanta, task_quantum, reinsert):
    # Execute the tasks
    priority_based(queues, queue_quanta, task_quantum, reinsert)


if __name__ == "__main__":
    import sys
    from copy import deepcopy

    # Example
    tasks = [
        Task("Task1", priority=2, burst_time=10),
        Task("Task2", priority=8, burst_time=15, dependencies=["Task1"]),
        Task("Task3", priority=4, burst_time=5, dependencies=["Task1"]),
        Task("Task4", priority=6, burst_time=20, dependencies=["Task2", "Task3"]),
        Task("Task5", priority=5, burst_time=8)
    ]

    queues = create_priority_queues(tasks, None)
    queue_quanta = [sys.maxsize]  # There is only one queue. Since this is maxed out, only `task_quantum` is considered

    # --------------------------------------------------------------------------------
    #
    # **Note**: must use `deepcopy` to avoid modifying the original queues
    #
    # --------------------------------------------------------------------------------
    # Test with reinsertion
    test(deepcopy(queues), queue_quanta, task_quantum=4, reinsert=True)
    print('\n\n')

    # Test without reinsertion
    test(deepcopy(queues), queue_quanta, task_quantum=4, reinsert=False)
    print('\n\n')

    # Test without reinsertion and with max quantum
    # In this case, the order of execution is strictly based on the priority of the tasks
    test(deepcopy(queues), queue_quanta, task_quantum=sys.maxsize, reinsert=False)
