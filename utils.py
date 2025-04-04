

def can_run(task, completed_tasks):
    """
    Determines if a task can be executed based on its dependencies.

    A task is allowed to run if all the tasks it depends on have been completed.

    Parameters:
        task (Task): The task to be checked.
        completed_tasks (set): A set containing the names of completed tasks.

    Returns:
        bool: True if all dependencies of the task are met, False otherwise.
    """

    # Check if all dependencies of the task are satisfied
    return all(dep in completed_tasks for dep in task.dependencies)
