# Task Tracker

*current version 0.0.1*
## Description
A simple task tracker built for the command line.
Built with Python and SQLite3. 

**Note:** Work in progress

It currently uses the system user. The idea is that you can start the program, enter or select a task, and do whatever you are going to do.
No frills to interfere with your workflow.


## Installation
1. Clone the repository
2. Change into TaskTracker directory (or wherever you cloned the repo)
```
cd TaskTracker
```
3. Install dependencies with 
``` 
pip install -r requirements.txt 
```
4. Install the commands (created with the click library)
```
pip install --editable . 
```
Now you can use the `tasks` command to interact with the application.

## Setup
Once installed, the first thing you need to do is create a new database. To do this, run the following command:
```cli
tasks init-db 
```

## Usage

Run the program
```cli
tasks run <username> -p <password>
```