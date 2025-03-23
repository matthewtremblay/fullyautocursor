# Cursor Continue Clicker

A utility that automatically clicks the "resume the conversation" text in Cursor when it appears after reaching the tool call limit. The script will:
1. Remember where to click based on your mouse position
2. Watch for the "resume the conversation" text
3. Click the saved position when the text appears
4. Stop clicking once the text disappears
5. Resume clicking when the text reappears

## Setup Instructions

1. Make sure you have Python 3.7+ installed on your system

2. Clone or download this repository to your local machine

3. Open a terminal and navigate to the project directory

4. Create a virtual environment:
```bash
python3 -m venv venv
```

5. Activate the virtual environment:
   - On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   - On Windows:
   ```bash
   .\venv\Scripts\activate
   ```

6. Install the required dependencies:
```bash
pip install pyautogui opencv-python numpy pillow pytesseract
```

7. Install Tesseract OCR:
   - On macOS:
   ```bash
   brew install tesseract
   ```
   - On Windows:
     - Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
   - On Linux:
   ```bash
   sudo apt-get install tesseract-ocr
   ```

## Running the App

1. With the virtual environment activated, run:
```bash
python continue_clicker.py
```

2. When the script starts:
   - Move your mouse cursor over the "resume the conversation" text
   - Press Ctrl+C in the terminal to capture that position
   - The script will start monitoring for the text

3. The script will:
   - Show dots (.) while waiting for the text to appear
   - Click automatically when the text appears
   - Stop clicking once the text disappears
   - Resume clicking if the text reappears

## Stopping the App

You can stop the app in two ways:
1. Press Ctrl+C in the terminal
2. Move your mouse cursor to any corner of the screen (failsafe)

## How It Works

- The script uses OCR (Optical Character Recognition) to detect when the "resume the conversation" text appears
- When detected, it clicks at the previously saved coordinates
- It takes a fresh screenshot before each click attempt to ensure the text is still there
- The script includes a failsafe: moving your mouse to any corner of the screen will stop it immediately

## Troubleshooting

If you encounter any issues:
1. Make sure you're running the script from within the virtual environment (you should see `(venv)` at the start of your terminal prompt)
2. Ensure all dependencies are installed correctly, including Tesseract OCR
3. If the script isn't detecting the text:
   - Make sure your screen resolution and text are clear
   - Try moving your mouse cursor to a different part of the "resume the conversation" text when capturing the click position 