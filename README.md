# Scheduling algorithms

There are a number of popular process scheduling algorithms teams use to optimize task processes:

- First Come First Served (FCFS)
- Shortest Job First (SJF) and Shortest Time Remaining
- Round Robin Scheduling
- Priority Scheduling
- SVR2 (System V Release 2) Unix scheduling algorithm
- Lottery Scheduling

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


# Priority Queue for shortest remaining time (STR) Scheduling

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
