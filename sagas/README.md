# Sagas

Sagas are a protocol for implementing long-running processes. The Saga protocol
ensures that a process is atomic, that is, a process executes observably
equivalent to completely or not at all.

## Overview

The booking saga workflow is responsible for coordinating the booking of a
conference package, consisting of a car, hotel, and flight reservation. In the
event of a failure at any point during the booking process, the Workflow will
trigger compensating actions to undo any previous bookings.

![](static/booking-saga.png)

## Design

The booking saga is implemented using the Temporal Workflow framework, which
provides a robust and fault-tolerant platform for coordinating distributed transactions.

The saga workflow consists of three activities: `book_car()`, `book_hotel)()`,
and `book_flight)()`, each of which is responsible for making a reservation with
the corresponding service provider. If any of these activities fail, the workflow
will trigger the corresponding compensating action (`undo_book_car()`, `undo_book_hotel()`,
or `undo_book_flight()`) to undo any previous bookings.

The `non_retryable_error_types` parameter is used to specify a list of error types
that should not be retried when a Workflow or Activity fails.

## Running the demo

Running this demo requires having three terminal windows open. I recommend using
a screen software like `tmux` or `screen`.

### Terminal #1

Run the Temporal server:

```bash
temporal server start-dev --ui-port 8080
```

This will start the Temporal Development Server. If you need to demo Temporal's
ability to recover from a server crash, use a database file:

```bash
temporal server start-dev --ui-port 8080 --db-filename $HOME/.cluster-persistence.db
```

### Terminal #2

Run the worker in a separate terminal:

```bash
python3 run_worker.py
```

### Terminal #3

Finally, run the Workflow/web form in another terminal:

```bash
python3 run_workflow.py
```

### Web UI

Have your Web UI open at http://localhost:8080. You will be showing the Event
History of individual Workflow Executions

### Code Editor

Have a code editor open with `run_worker.py`, `run_workflow.py`, `book_workflow`,
and `activities.py` open. Refer to them as necessary.

### Demo: Happy Path

#### Explanation

Explain that the application simulates booking various services (flight, car rental, hotel)
for a trip to the conference you are at (make it relevant). If any of these bookings
were to fail, you'd want to cancel and roll back all bookings (What good is a care
when I don't have a flight?).

Be _sure_ to explain that in the simulation, we've added artificial sleeps to simulate
calling various microservices, and we're simulating a shakey network with a delay
of 3 seconds in between each "service" call.

#### Demo

Enter your booking information in the Flask app <http://127.0.0.1:8000>, then
see the tasks in the Web UI at <http://localhost:8080/>.

Select your running or completed Workflow ID.

Under **WorkflowExecutionCompleted** car, hotel and flight are booked.

Notice each is executed via an activity.

### Demo: Recover Forward (retries)

Modify `Number of Failures Before Success:` to anything greater than 0 in UI,
so that the booking activities attempt a retry `X` times. If you plan on showing
the failure in the UI, give yourself time so 5 is a good number.

Things to possibly show **during** the failure:

- Show the terminal with the Worker code trying multiple times
- Show the error in the UI, that it shows you what's wrong and that it's retrying
  - Maybe talk about Retry Policies if you have enough time
- Show the code. Show that there is _no_ retry logic. There's just errors. All
  Retry logic is handled by Temporal
- If interest, show the Workflow code and how Workflows are invoked

Things to possibly show **after** the failure and the booking has completed:

- In the Web UI, show the successful completed workflow
- In the Web UI, show the completed Workflow \* Under **ActivityTaskStarted**
  you'll see the Attempts (`X`), and the stack trace message letting you know the
  last failed attempt. Select your running or completed Workflow ID.
- In the Web UI, feel free to hop around the event history explaining what happened.
  However, in large crowds you may lose people.

### Demo: Recover Backward (rollback)

Select one of the following failures in the Web UI:

- Car Booking Failure
- Hotel Booking Failure
- Flight Booking Failure

Any of these will fail that specific Activity _at that point_ in the Workflow.
The Workflow executes the Activities in the following order:

1. Book Car
2. Book Hotel
3. Book Flight

So if you choose to fail the Workflow at `Car Booking Failure`, only the Car Activity
will be rolled back, because that's all that was executed.

**For best results, simulate a Flight Booking Failure**

Things to _discuss_ while examining the Workflow Execution History in the UI:

- The Workflow still completed successfully. Everything was rolled back

**Note: The Saga Pattern is not exclusive to Temporal. Don't know how much
value we get out of talking about it, other than showing how easy it is to
implement.**

### Demo: Multi-Failure (Retries and failure)

Combine the above demos. Set the `Number of Failures Before Success:` to 5 and a
**Flight Booking Failure**. Show that the Activities were retried but a failure
still caused a rollback.
