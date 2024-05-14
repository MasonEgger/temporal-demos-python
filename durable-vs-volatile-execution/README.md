# Durable vs Volatile Execution

Temporal is a Durable Execution system. Durable Execution is a relatively new
term to developers, so we need to introduce it to him.

Volatile Execution is also a new phrase (I think), but we're using it as a contrast
to Durable Execution. In this instance, Volatile Execution refers to any code
that is not running in a Durable Execution System. Volatile Execution can approach
Durable Execution, but this requires a _lot_ of error handling code and persistence,
which is the entire benefit of Temporal.

## Overview
H
This demo's is based on a presentation that Tom Wheeler 