import pyautogui
import time
import sys
from PIL import ImageGrab
import pytesseract

# Fail-safe: Moving mouse to corner will stop the program
pyautogui.FAILSAFE = True

def check_for_resume_text():
    """Check if 'resume the conversation' text is visible on screen."""
    try:
        # Take a fresh screenshot each time
        screenshot = ImageGrab.grab()
        
        # Convert to text
        text = pytesseract.image_to_string(screenshot).lower()
        
        # Check if our target text is in there
        return 'resume the conversation' in text or 'resume conversation' in text
        
    except Exception as e:
        print(f"Error checking screen: {e}")
        return False

def main():
    print("\n=== Cursor Continue Clicker ===")
    print("This script will:")
    print("1. Remember where to click")
    print("2. Watch for the continue prompt")
    print("3. Click when needed")
    print("\nTo stop: Press Ctrl+C or move mouse to any corner")
    
    print("\nStep 1: Move your mouse over the 'resume the conversation' text")
    print("Step 2: Press Ctrl+C to capture the position")
    
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        # Get current mouse position
        click_x, click_y = pyautogui.position()
        print(f"\nPosition captured. Starting auto-clicker...")
        
        try:
            last_clicked = False  # Track if we clicked last time
            while True:
                # Check if the text is visible right now
                text_visible = check_for_resume_text()
                
                if text_visible and not last_clicked:
                    print("\nPrompt detected - clicking...")
                    pyautogui.moveTo(click_x, click_y)
                    time.sleep(0.5)  # Give a moment to see where it's going to click
                    pyautogui.click()
                    last_clicked = True
                    time.sleep(2)  # Wait a bit before checking again
                elif not text_visible:
                    if last_clicked:
                        print("\nPrompt handled - waiting for next one...")
                        last_clicked = False
                    else:
                        print(".", end="", flush=True)  # Show it's still running
                    time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\nStopping...")
        
if __name__ == "__main__":
    main() 