## Approximation of the solutions of ordinary differential equations of order 1


## Project 
This Python project leverages Tkinter to develop a graphical user interface (GUI) designed for solving first-order linear differential equations. The application allows users to
:-Input differential equations and initial conditions.
-Choose from various numerical methods to approximate solutions.
-Visualize the approximate solutions and compare them with exact solutions computed using SciPy's odeint function.
-Assess the accuracy of numerical methods by visualizing both absolute and relative errors.

## Features
### Data Input:
- **Manual Input**:
  - Enter the function f(dy/dt) in the format a*t+b or a*t, where a and b are constants.
  - Enter the initial value y0.
  - Enter the time interval in the format t_end,nr_steps.
  - Click "Save Data" button.
- **File Input**:
  - Click "Read Function from File" button.
  - Select a .txt file containing data in the correct format:
    ```
    f: a*t+b
    y0: value
    t: t_end,nr_steps
    ```
- **Random Data Generation**:
  - Click "Generate Random Function" button.

### Numerical Methods Selection:
- **Explicit Euler Method**
- **Implicit Euler Method**
- **Second Order Runge-Kutta Method**
- **Fourth Order Runge-Kutta Method**

### Visualization of Solutions:
- View approximate solutions on a graph using Matplotlib.
- Animation of the solution as it evolves over time.
- Comparison of numerical solution with exact solution.
- Display of absolute and relative errors for each time step.

### Data Management:
- Reset data and graph.
- Save animation as .gif file.

### Table Generation:
- Generate a table containing calculated numerical data for each time step.
- Display the table in a new window.

## Requirements
- Python 3.x
- Required Libraries:
  - tkinter
  - numpy
  - matplotlib
  - scipy
  - pandas
  - sympy
  - random
  - re
  - csv
## Installation of Required Libraries
To install all required libraries, run the following command:

```bash
pip install numpy matplotlib scipy pandas sympy
```

## How to Use the Application

### Data Input
#### Manual Input:
- Enter the function f(dy/dt) in the specified format.
- Enter y0 and the time interval.
- Click "Save Data".

#### File Input:
- Click "Read Function from File".
- Select the .txt file with the required format.

#### Random Data:
- Click "Generate Random Function".

### Numerical Method Selection
Select one of the available numerical methods from the "Choose Method" section.

### Viewing the Solution
- Click "Start Animation" to begin the animation.
- Click "Stop Animation" to pause the animation.
- Click "Resume Animation" to continue the animation.
- Click "Show Table" to generate and display the numerical data table.
- Click "Save Animation" to save the animation as a .gif file.

### Resetting Data
- Click "Reset" to clear all data and the graph.

## Code Structure

### Calculation Methods
- `euler_explicit(f, y0, t)`
- `euler_implicit(f, y0, t)`
- `runge_kutta_2(f, y0, t)`
- `runge_kutta_4(f, y0, t)`

### Data Handling Functions
- `read_file()`
- `input_random_data()`
- `save_data()`
- `reset_data()`
- `calculate_absolute_error(y1, y2)`
- `calculate_relative_error(y1, y2)`
- `process_t(t, nr_steps)`
- `create_function(f_str)`
- `generate_table()`

### Animation Functions
- `start_animation()`
- `stop_animation()`
- `resume_animation()`
- `save_animation()`

### GUI Components
- Tkinter elements for data input and manipulation.
- Matplotlib elements for graph visualization and animation.
- Tkinter elements for displaying the numerical data table.

## Description 
The approximation of first-order ordinary differential solutions using Euler's explicit Implicit Runge Kutta2 and Runge Kutta4 methods is crucial in various scientific and engineering fields. Numerical methods, such as explicit Euler, implicit Euler, Runge-Kutta of order 2 and Runge-Kutta of order 4, are used to obtain approximate solutions to such equations.
