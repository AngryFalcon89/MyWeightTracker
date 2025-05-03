# MyWeightTracker

A comprehensive weight tracking application built with Python and Tkinter. This application helps users track their weight measurements, particularly focusing on pre and post-gym weights, along with additional metrics like meal information and workout conditions.

## Features

- Track pre and post-gym weights
- Record workout conditions (Normal, Fast, Hydrated, etc.)
- Log calorie intake
- Add notes and meal information
- View historical data in a table format
- Visualize weight trends through graphs
- Export data functionality
- User-friendly GUI interface

## Prerequisites

Before running MyWeightTracker, ensure you have the following installed on your macOS:

1. Python 3.13 or later
2. Homebrew (macOS package manager)
3. Tkinter support for Python

## Installation Guide

### 1. Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python with Tkinter Support
```bash
brew install python-tk@3.13
```

### 3. Clone the Repository
```bash
git clone <repository-url>
cd MyWeightTracker
```

### 4. Set Up Virtual Environment and Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

## Running the Application

1. Ensure you're in the project directory and your virtual environment is activated:
```bash
cd MyWeightTracker
source venv/bin/activate
```

2. Run the application:
```bash
python app.py
```

## Usage Guide

### Main Interface
- The application opens to a main window with several panels:
  - Input Panel: For entering new weight measurements
  - Statistics Panel: Shows trends and analytics
  - History Table: Displays all recorded entries

### Adding a New Entry
1. Select the date using the calendar widget
2. Enter pre-gym weight
3. Enter post-gym weight
4. Select workout condition from dropdown
5. Enter calories (optional)
6. Add any notes or meal information
7. Click "Add Entry" to save

### Viewing Statistics
- The statistics panel shows:
  - Average weight changes
  - Trends over time
  - Progress charts

### Data Management
- Your data is stored locally in a CSV file
- Regular backups are recommended
- Data can be exported for external analysis

## Troubleshooting

### Common Issues and Solutions

1. **Tkinter Not Found Error**
   ```
   ModuleNotFoundError: No module named '_tkinter'
   ```
   Solution: Reinstall Python with Tkinter support:
   ```bash
   brew uninstall python@3.13
   brew install python-tk@3.13
   ```

2. **Dependencies Installation Issues**
   If you encounter any issues with installing dependencies, try:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Application Not Starting**
   - Ensure your virtual environment is activated
   - Verify all dependencies are installed correctly
   - Check if the data file exists and has proper permissions

## Data Privacy

- All data is stored locally on your machine
- No data is sent to external servers
- Regular backups are recommended to prevent data loss

## Support

If you encounter any issues or need assistance:
1. Check the troubleshooting section above
2. Verify your Python and dependency versions
3. Ensure your system meets all prerequisites

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

## Building for Distribution

To build a standalone application for distribution, you can use the `py2app` tool.

1. Ensure you have `py2app` installed:
```bash
pip install py2app
```

2. Run the build script:
```bash
python setup.py py2app
```

This will create a standalone application that you can distribute to other users. 