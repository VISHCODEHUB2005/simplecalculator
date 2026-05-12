# Advanced Calculator

## Overview

This is an advanced command-line calculator built in Python. It supports multiple calculation modes, input validation, history tracking, variable storage, expression evaluation, and batch processing.

## Features

- **Sequential Mode**: Chain operations step by step using the current result.
- **Expression Mode**: Evaluate mathematical expressions such as `10 + 5 * 2`.
- **Batch Mode**: Enter multiple expressions and evaluate them all at once.
- **Memory Mode**: Assign and use variables like `X = 10 + 5`, then reuse `X` later.
- **History**: Save every calculation in a session and display the history.
- **Settings**: Control decimal precision for display.
- **Error handling**: Handles invalid input, division by zero, invalid expressions, and invalid variable names.

## Setup

1. Install Python 3.10 or later.
2. Open a terminal.
3. Navigate to the project folder:

```bash
cd "c:\Users\viswa\OneDrive\Desktop\Scratch\Phase_01"
```

## Run the Calculator

Run the calculator script with Python:

```bash
python Calculator.py
```

## Usage

### Main Menu

When the program starts, choose one of the following modes:

1. **Sequential Mode** - perform calculations one step at a time.
2. **Expression Mode** - evaluate a complete arithmetic expression.
3. **Batch Mode** - evaluate multiple expressions in one session.
4. **Memory Mode** - assign variables and reuse them.
5. **View History** - review past calculations.
6. **Settings** - change decimal precision.
0. **Exit** - close the program.

### Examples

#### Sequential Mode

- Enter the first number.
- Choose an operation.
- Enter the next number.
- Continue chaining or exit.

#### Expression Mode

- Enter a complete expression such as `12 + 5 * 3`.
- Supported operators: `+`, `-`, `*`, `/`.

#### Batch Mode

- Enter expressions one by one.
- Type `DONE` when finished.
- The program evaluates each expression and shows results.

#### Memory Mode

- Assign variables using syntax like `X = 10 + 5`.
- View stored variables with `SHOW`.
- Delete a variable with `DELETE X`.
- Clear all stored variables with `CLEAR`.
- Exit memory mode with `EXIT`.

## Notes

- The calculator uses `float` values, so decimal calculations are supported.
- Use the Settings menu to adjust result precision from `1` to `10` decimal places.

## License

This project is for learning and demonstration purposes.
