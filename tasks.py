from collections import deque
import heapq


class Task:
    """ Generic Task class for multi-queue scheduling.
        This class represents a task with a name, priority, burst time, waiting time,
        and dependencies. It also includes a method for comparing tasks based on their priority.
    """

    def __init__(self, name, priority, burst_time, waiting_time=0, dependencies=None):
        """
        Initialize a Task object.

        Args:
            name (str): The name of the task.
            priority (int): The priority of the task.
            burst_time (int): The total time required by the task to complete.
            waiting_time (int, optional): The waiting time of the task. Defaults to 0.
            dependencies (list, optional): A list of task names that this task depends on. Defaults to an empty list.

        Attributes:
            completed (bool): Indicator of whether the task is completed.
        """

        self.name = name
        self.priority = priority
        self.burst_time = burst_time  # Remaining burst time
        self.total_burst_time = burst_time  # Store the original burst time
        self.waiting_time = waiting_time
        self.dependencies = dependencies or []  # List of task names this task depends on
        self.completed = False  # Track if the task is completed

    def __lt__(self, other):
        """
        Compare two tasks based on their priority.

        Parameters:
            other: Another Task instance

        Returns:
            True if this task has higher priority than the other task
        """
        # Higher priority tasks will come first in the priority queue
        return self.priority > other.priority


def create_queues(tasks: list[Task], priority_ranges: list[tuple[int, int]]) -> list[list[Task]]:
    """
    Create a list of queues based on the given tasks and priority ranges.

    tasks: list of Task objects
    priority_ranges: list of tuples of (low, high) priority ranges

    Returns a list of deques (queues) where each queue contains tasks with priorities
    within the corresponding range in priority_ranges. The tasks are added in the order
    they appear in the input list.
    """
    queues = [deque() for _ in range(len(priority_ranges))]
    for task in tasks:
        for i, (low, high) in enumerate(priority_ranges):
            if low <= task.priority <= high:
                queues[i].append(task)
                break
    return queues



def create_priority_queues(tasks: list[Task], priority_ranges: list[tuple[int, int]]) -> list[list[Task]]:
    """
    Create a list of priority queues based on the given tasks and priority ranges.

    tasks: list of Task objects. The Task must implement the __lt__ method for comparison.
    priority_ranges: list of tuples of (low, high) priority ranges

    Returns a list of priority queues where each queue contains tasks with priorities
    within the corresponding range in priority_ranges. The tasks are added in the order
    they appear in the input list.
    """
    if priority_ranges is None:
        priorities = [task.priority for task in tasks]
        # just one queue for all tasks
        priority_ranges = [[min(priorities), max(priorities)]]
    queues = [[] for _ in range(len(priority_ranges))]
    for task in tasks:
        for i, (low, high) in enumerate(priority_ranges):
            if low <= task.priority <= high:
                heapq.heappush(queues[i], task)
                break
    return queues
