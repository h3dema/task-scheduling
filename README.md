# Scheduling algorithms

There are a number of popular process scheduling algorithms teams use to optimize task processes:

- [First Come First Served](#first-come-first-served) (FCFS)
- Shortest Job First (SJF) and [Shortest Time Remaining](#shortest-job-first-and-shortest-time-remaining)
- [Round Robin Scheduling](#round-robin)
- [Priority scheduling](#priority-queue)
- [Priority Scheduling with STR](#priority-queue-for-shortest-remaining-time-str-scheduling)
- [Lottery Scheduling](#lottery-scheduling-using-multiple-queues)
- [Multilevel Feedback Queue (MLFQ)](#multilevel-feedback-queue-mlfq)
- [SVR2 (System V Release 2) Unix scheduling](#svr2-system-v-release-2-unix-scheduling) algorithm

This repository demonstrates the implementation of these scheduling algorithms in Python.


## First Come First Served

First-Served (FCFS) scheduling is a simple algorithm where tasks are processed in the order they arrive, without prioritization.
Our implementation has multiple queue. Queues with higher numbers are executed first, providing a simple prioritization mechanism.
Inside the queue, the tasks are executed in FCFS manner.


```bash
python multi_queue_fifo.py
```

The [code](multi_queue_fifo.py) simulates multiples queues.
Each queue has a maximum quantum of time to run per round (see `queue_quanta`).
System starts with Queue 2 (maximum priority) and runs the tasks.
Notice that since queue_quanta[2] is large enough, Task 3 runs twice.
Then the code goes to Queue 1, runs its tasks until queue_quanta[1] is reached.
It runs Task4 and Task5 before Task2 because Task2 is added last to Queue 1 (see list `tasks` in [multi_queue_fifo.py](multi_queue_fifo.py)).
Task4 and Task5 use all queue_quanta[1] so Task2 is postponed to run after one round of Queue 0.
When it is time to run Queue 1 again, Task2 runs and then Task4, because Task4 was reinserted at the end of Queue 1 when it ran last time.

<pre style="background-color:rgb(255, 247, 130)">
Execution Order:
Task Task3 (Queue 2) executed for 4 units
Task Task3 (Queue 2) executed for 3 units and completed
Task Task4 (Queue 1) executed for 4 units
Task Task5 (Queue 1) executed for 4 units
Task Task1 (Queue 0) executed for 4 units
Task Task1 (Queue 0) executed for 2 units
Task Task2 (Queue 1) executed for 4 units
Task Task4 (Queue 1) executed for 4 units
Task Task1 (Queue 0) executed for 4 units and completed
Task Task5 (Queue 1) executed for 2 units and completed
Task Task2 (Queue 1) executed for 4 units
Task Task4 (Queue 1) executed for 2 units and completed
Task Task2 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 3 units and completed
</pre>

## Shortest Job First and Shortest Time Remaining


Shortest job next (SJN), also known as shortest job first (SJF) or shortest process next (SPN), is a scheduling policy that selects for execution the waiting process with the smallest execution time. SJN is a non-preemptive algorithm.
Our implementation is actually of Shortest time remaining (STR), which is a preemptive variant of SJN.
It can simulate SJF, if you configure the `task_quantum` and `queue_quanta` values larger enough such as every task can be executed without preempting.

To run the simulation, use the following command:

```bash
python multi_queue_sjf.py
```

The [code](multi_queue_sjf.py) simulates multiples queues.
Each queue has a maximum quantum of time to run per round (see `queue_quanta`).
System starts with Queue 2 (maximum priority) and runs the tasks.
Notice that since queue_quanta[2] is large enough, Task 3 runs twice.
Task5 is the first to run from Queue 1, because it has the shortest burst time, and then Task4 (second shortest burst time).
The quantum of Queue 1 is reached, then Queue 0 is executed.
And so on...


<pre style="background-color:rgb(255, 247, 130)">
Execution Order:
Task Task3 (Queue 2) executed for 4 units
Task Task3 (Queue 2) executed for 3 units and completed
Task Task5 (Queue 1) executed for 4 units
Task Task4 (Queue 1) executed for 4 units
Task Task1 (Queue 0) executed for 4 units
Task Task1 (Queue 0) executed for 2 units
Task Task5 (Queue 1) executed for 2 units and completed
Task Task4 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 2 units
Task Task1 (Queue 0) executed for 4 units and completed
Task Task4 (Queue 1) executed for 4 units and completed
Task Task2 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 1 units and completed
</pre>


## Round Robin

[Code](multi_queue_fifo.py) simulates multiples queues.
Each queue has a maximum quantum of time to run per round (see `queue_quanta`).
System starts with Queue 2 (maximum priority) and runs the tasks.
Notice that since queue_quanta[2] is large enough, Task 3 runs twice.
Then the code goes to Queue 1, runs its tasks until queue_quanta[1] is reached.
Then it performs tasks from Queue 0.
The system continues until the end.

```bash
python multi_queue_round_robin.py
```

<pre style="background-color:rgb(255, 247, 130)">
Execution Order:
Task Task3 (Queue 2) executed for 4 units
Task Task3 (Queue 2) executed for 3 units
Task Task2 (Queue 1) executed for 4 units
Task Task4 (Queue 1) executed for 4 units
Task Task1 (Queue 0) executed for 4 units
Task Task1 (Queue 0) executed for 2 units
Task Task5 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 4 units
Task Task1 (Queue 0) executed for 4 units
Task Task4 (Queue 1) executed for 4 units
Task Task5 (Queue 1) executed for 2 units
Task Task2 (Queue 1) executed for 2 units
Task Task4 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 1 units
</pre>


## Priority Queue

This implementation uses a priority queue to manage tasks based on their priority.
The priority queue ensures that tasks with higher priority are processed first.
Our [implementation](priority_based.py) has two behaviors:
(1) after running the taks for the time quantum, if the task isn't finished, it is reinserted into the priority queue for further processing in the same queue quantum. This allows the task to be executed multiple times in the same queue quantum (see below)'
(2) the task is scheduled to be executed in the next queue quantum.

```bash
python priority_based.py
```

There is only one queue in the example below.
In the left column, the code reinserts the task into the queue after executing it, which allows the task to be executed immediately.
In the right column, the code only reinserts the task after all the tasks are executed.
Notice that for that to happen, we need to set queue_quanta[0] to a large number, such as `sys.maxsize`.
`task_quantum` is set to 4, which is the maximum time quantum each task can run, thus, this is why we see the same task running multiple times. If you set `task_quantum` to `sys.maxsize`, the task will be executed only once.


<div style="display: flex; gap: 2rem; padding: 2rem; border: 0px solid #333; border-radius: 10px; background-color: #f0f0f0;">
<div style="display: flex; flex-direction: column;">
<pre style="background-color:rgb(255, 247, 130)">
Execution Order with task reinsertion
Task Task2 (Queue 0) executed for 4 units
Task Task2 (Queue 0) executed for 2 units
Task Task2 (Queue 0) executed for 4 units
Task Task2 (Queue 0) executed for 2 units
Task Task2 (Queue 0) executed for 4 units
Task Task2 (Queue 0) executed for 2 units
Task Task2 (Queue 0) executed for 2 units
Task Task2 completed
Task Task4 (Queue 0) executed for 4 units
Task Task4 (Queue 0) executed for 4 units
Task Task4 (Queue 0) executed for 2 units
Task Task4 (Queue 0) executed for 4 units
Task Task4 (Queue 0) executed for 1 units
Task Task4 completed
Task Task5 (Queue 0) executed for 1 units
Task Task5 (Queue 0) executed for 4 units
Task Task5 (Queue 0) executed for 2 units
Task Task5 (Queue 0) executed for 1 units
Task Task5 completed
Task Task3 (Queue 0) executed for 4 units
Task Task3 (Queue 0) executed for 1 units
Task Task3 completed
Task Task1 (Queue 0) executed for 4 units
Task Task1 (Queue 0) executed for 2 units
Task Task1 (Queue 0) executed for 4 units
Task Task1 completed
</pre>
    </div>
    <div style="display: flex; flex-direction: column;">
<pre style="background-color:rgb(255, 247, 130)">
Execution Order without task reinsertion:
Task Task2 (Queue 0) executed for 4 units
Task Task4 (Queue 0) executed for 4 units
Task Task5 (Queue 0) executed for 4 units
Task Task3 (Queue 0) executed for 4 units
Task Task1 (Queue 0) executed for 4 units
Task Task2 (Queue 0) executed for 4 units
Task Task4 (Queue 0) executed for 4 units
Task Task5 (Queue 0) executed for 4 units
Task Task5 completed
Task Task3 (Queue 0) executed for 1 units
Task Task3 completed
Task Task1 (Queue 0) executed for 4 units
Task Task2 (Queue 0) executed for 4 units
Task Task4 (Queue 0) executed for 4 units
Task Task1 (Queue 0) executed for 2 units
Task Task1 completed
Task Task2 (Queue 0) executed for 4 units
Task Task4 (Queue 0) executed for 3 units
Task Task4 completed
Task Task2 (Queue 0) executed for 4 units
Task Task2 completed
</pre>
</div>
</div>




## Priority Queue for shortest remaining time (STR) Scheduling

In Shortest Remaining Time (SRT) scheduling, a priority queue is used to efficiently manage processes based on their remaining execution time, ensuring the process with the shortest remaining time is always selected for execution, making it a preemptive scheduling algorithm.


```bash
python multi_queue_str_priority.py
```

Our [implementation ](multi_queue_str_priority.py) is a multi-queue implementation.
Tasks are assigned to queues based on their `priority` parameter. Queues with higher number have higher priority.
Inside each queue, the tasks are prioritized using the remaining burst time (smaller has more priority).
The output below shows how the code behaves.
The code starts with Queue 2 (maximum priority) and runs the tasks in it.
It only has Task 3, which runs for 2 quantum, because the total quanta of Queue 2 is large enough.
Then the code goes to Queue 1, runs Task5 that has smaller burst time, moving to


<pre style="background-color:rgb(255, 247, 130)">
Execution Order:
Task Task3 (Queue 2) executed for 4 units
Task Task3 (Queue 2) executed for 3 units
Task Task5 (Queue 1) executed for 4 units
Task Task5 (Queue 1) executed for 2 units
Task Task4 (Queue 1) executed for 2 units
Task Task1 (Queue 0) executed for 4 units
Task Task1 (Queue 0) executed for 2 units
Task Task4 (Queue 1) executed for 4 units
Task Task4 (Queue 1) executed for 4 units
Task Task1 (Queue 0) executed for 4 units
Task Task4 (Queue 1) executed for 2 units
Task Task2 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 2 units
Task Task2 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 1 units
</pre>

## Lottery Scheduling using multiple queues.


```bash
python multi_queue_lottery.py
```

The [code](multi_queue_lottery.py) starts with Queue 2 (highest priority).
After that, it skips Queue 1, because all tasks have dependencies on Queue 0.
It runs tasks on Queue 0 (lowest priority).
When finished, it then moves to Queue 1.
The output is as follows:

<pre style="background-color:rgb(255, 247, 130)">
Execution Order:
Task Task5 (Queue 2) executed for 4 units
Task Task5 (Queue 2) executed for 4 units
Task Task5 has completed
Task Task1 (Queue 0) executed for 4 units
Task Task1 (Queue 0) executed for 4 units
Task Task1 (Queue 0) executed for 2 units
Task Task1 has completed
Task Task3 (Queue 0) executed for 4 units
Task Task3 (Queue 0) executed for 1 units
Task Task3 has completed
Task Task2 (Queue 0) executed for 1 units
Task Task2 (Queue 0) executed for 4 units
Task Task2 (Queue 0) executed for 4 units
Task Task2 (Queue 0) executed for 4 units
Task Task2 (Queue 0) executed for 2 units
Task Task2 has completed
Task Task4 (Queue 1) executed for 4 units
Task Task4 (Queue 1) executed for 4 units
Task Task4 (Queue 1) executed for 4 units
Task Task4 (Queue 1) executed for 4 units
Task Task4 (Queue 1) executed for 4 units
Task Task4 has completed
</pre>

## Multilevel Feedback Queue (MLFQ)

Our [implementation](multilevel_feedback_queue.py) has multiple queues.
The algorithm iterates through the queues, starting with the highest-priority queue.
For each queue, it executes as many tasks as possible within the allocated time quantum.
If a task is not completed within the allocated time, it is moved to a lower-priority queue.
The algorithm continues until all queues are empty.

```bash
python multilevel_feedback_queue.py
```

**Problem**: if the tasks need long enough time, they can end up all in the lowest priority queue.

<pre  style="background-color:rgb(255, 247, 130)">
Execution Order:
Task Task2 (Queue 2) executed for 4 units
Task Task3 (Queue 1) executed for 4 units
Task Task5 (Queue 1) executed for 4 units
Task Task1 (Queue 0) executed for 4 units
Task Task4 (Queue 0) executed for 2 units
Task Task2 (Queue 1) executed for 4 units
Task Task3 (Queue 1) executed for 1 units
Task Task5 (Queue 1) executed for 3 units
Task Task1 (Queue 0) executed for 4 units
Task Task4 (Queue 0) executed for 2 units
Task Task2 (Queue 1) executed for 4 units
Task Task5 (Queue 1) executed for 1 units
Task Task2 (Queue 1) executed for 3 units
Task Task1 (Queue 0) executed for 2 units
Task Task4 (Queue 0) executed for 4 units
Task Task2 (Queue 1) executed for 4 units
Task Task2 (Queue 1) executed for 1 units
Task Task4 (Queue 0) executed for 4 units
Task Task4 (Queue 0) executed for 2 units
Task Task4 (Queue 0) executed for 1 units
</pre>

## SVR2 (System V Release 2) Unix scheduling

Our implementation simulates the SVR2 (System V Release 2) Unix scheduling algorithm, with the addition of task dependencies.

```bash
python svr2_mlfq_with_dependencies.py
```

The code starts with the highest priority queue.
However Task2 has dependencies on Task1 and Task3.
Since the task is not ready to run, it is moved to the next queue.
Only Task5 can run because it has no dependencies. This task is moved to a lower priority queue, i.e., Queue 0.
When the code moves to Queue 0, Task5 runs again and completes.
Also Task1 can run because it has no dependencies and there is enough quantum left to run it but not to complete the task.
The code moves to the next queue, i.e., Queue 2 because it was in the lowest priority queue.
The loop goes on, and the same logic applies.

The output is as follows:

<pre  style="background-color:rgb(255, 247, 130)">
Execution Order:
Task Task2 (Queue 2) cannot run due to unmet dependencies
Task Task4 (Queue 1) cannot run due to unmet dependencies
Task Task5 (Queue 1) executed for 4 units
Task Task3 (Queue 1) cannot run due to unmet dependencies
Task Task5 (Queue 0) executed for 4 units
Task Task5 has completed
Task Task1 (Queue 0) executed for 2 units
Task Task2 (Queue 2) cannot run due to unmet dependencies
Task Task4 (Queue 1) cannot run due to unmet dependencies
Task Task3 (Queue 1) cannot run due to unmet dependencies
Task Task1 (Queue 0) executed for 4 units
Task Task2 (Queue 2) cannot run due to unmet dependencies
Task Task4 (Queue 1) cannot run due to unmet dependencies
Task Task3 (Queue 1) cannot run due to unmet dependencies
Task Task1 (Queue 0) executed for 4 units
Task Task1 has completed
Task Task2 (Queue 2) executed for 4 units
Task Task2 (Queue 1) executed for 4 units
Task Task4 (Queue 1) cannot run due to unmet dependencies
Task Task3 (Queue 1) executed for 4 units
Task Task2 (Queue 0) executed for 4 units
Task Task3 (Queue 0) executed for 1 units
Task Task3 has completed
Task Task4 (Queue 1) cannot run due to unmet dependencies
Task Task2 (Queue 0) executed for 3 units
Task Task2 has completed
Task Task2 (Queue 2) executed for 0 units
Task Task2 has completed
Task Task4 (Queue 1) executed for 4 units
Task Task4 (Queue 0) executed for 4 units
Task Task4 (Queue 0) executed for 4 units
Task Task4 (Queue 2) executed for 4 units
Task Task4 (Queue 1) executed for 4 units
Task Task4 has completed
Task Task4 (Queue 1) executed for 0 units
Task Task4 has completed
Task Task4 (Queue 0) executed for 0 units
Task Task4 has completed
</pre>

> There is another (and simpler) implementation of the SVR2 scheduling algorithm in [svr2_mlfq.py](svr2_mlfq.py).