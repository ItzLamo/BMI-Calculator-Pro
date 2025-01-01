# BMI Calculator Pro

A Python application for calculating and tracking BMI (Body Mass Index) with an intuitive GUI, developed using `tkinter` and `matplotlib`. The app helps users calculate their BMI, view their health category, and provides health recommendations. It also allows users to save BMI records, view history, and analyze trends over time.

## Features

- **BMI Calculation**: Calculate BMI based on weight and height, with support for different units (kg/lbs and cm/inches).
- **Health Categories**: Categorizes BMI results into various categories like Underweight, Normal, Overweight, etc., and provides relevant health recommendations.
- **History Tracking**: Save and view past BMI calculations with details like weight, height, BMI, and category.
- **Statistics & Trends**: Visualize trends and statistics such as average BMI, lowest/highest BMI, and BMI trends over time using graphs.
- **Data Persistence**: History is stored in a JSON file for easy access and review.

## Requirements

- Python 3.x
- `tkinter` (for GUI)
- `matplotlib` (for plotting graphs)

You can install the required Python libraries with:
```
pip install matplotlib
```

## Usage

1. Run the application.
2. Enter your weight and height, select units (kg/lbs, cm/inches), and click "Calculate BMI."
3. The BMI result and health category will be displayed along with relevant health recommendations.
4. View your BMI history and statistics through the "View" menu.

## File Structure

- `main.py`: Main Python file with the BMI calculator logic and GUI.
