# Temporal Demos Python
Various demos demonstrating the features of Temporal in Python


## Prerequisites

To run the demos in this repo, the follow prerequisites are required:

- Python >= 3.8
- [Local Temporal server running](https://docs.temporal.io/application-development/foundations#run-a-development-cluster)

## Virtual Environment Setup
Before attempting to execute any of the code in this repository, it is necessary
to setup a virtual environment and install all necessary packages.


With this repository cloned, create a virtual environment at the root directory
named `venv`:

```bash
python3 -m venv venv
```

Next, activate your virtual environment:

```bash
source venv/bin/activate
```

Finally, install the necessary libraries to run the demos:

```bash
pip install -r requirements.txt
```