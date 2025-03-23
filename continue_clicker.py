import pyautogui
import time
import sys
from PIL import ImageGrab
import pytesseract
from datetime import datetime, timedelta

# Fail-safe: Moving mouse to corner will stop the program
pyautogui.FAILSAFE = True

# Settings
TIMEOUT_MINUTES = 30
TIMEOUT_SECONDS = TIMEOUT_MINUTES * 60
POST_CLICK_WAIT_SECONDS = 60  # Wait 1 minute after clicking before resuming checks

def get_timestamp():
    """Return current timestamp in a readable format."""
    return datetime.now().strftime("%H:%M:%S")

def format_duration(seconds):
    """Format duration in seconds to a readable string."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

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
        print(f"[{get_timestamp()}] Error checking screen: {e}")
        return False

def print_summary(runtime, click_count):
    """Print a summary of the script's activity."""
    print(f"[{get_timestamp()}] Total runtime: {runtime}")
    print(f"[{get_timestamp()}] Total clicks: {click_count}")

def main():
    print("\n=== Cursor Continue Clicker ===")
    print("This script will:")
    print("1. Remember where to click")
    print("2. Watch for the continue prompt")
    print("3. Click when needed")
    print(f"4. Stop after {TIMEOUT_MINUTES} minutes of inactivity")
    print(f"5. Wait {POST_CLICK_WAIT_SECONDS} seconds after each click")
    print("\nTo stop: Press Ctrl+C or move mouse to any corner")
    
    print("\nStep 1: Move your mouse over the 'resume the conversation' text")
    print("Step 2: Press Ctrl+C to capture the position")
    
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        # Get current mouse position
        click_x, click_y = pyautogui.position()
        print(f"\n[{get_timestamp()}] Position captured. Starting auto-clicker...")
        
        try:
            last_clicked = False  # Track if we clicked last time
            dots_count = 0  # Track number of dots printed
            last_activity = datetime.now()  # Track time of last click
            start_time = None  # Track when first click occurs
            click_count = 0  # Track number of clicks
            next_check_time = None  # Track when to resume checking after a click
            
            while True:
                current_time = datetime.now()
                
                # Check for timeout
                if (current_time - last_activity).total_seconds() > TIMEOUT_SECONDS:
                    runtime = format_duration((current_time - start_time).total_seconds()) if start_time else "0s"
                    print(f"\n[{get_timestamp()}] No activity for {TIMEOUT_MINUTES} minutes. Stopping...")
                    print_summary(runtime, click_count)
                    return
                
                # If we're waiting after a click, check if it's time to resume
                if next_check_time and current_time < next_check_time:
                    time.sleep(0.5)
                    continue
                
                # Check if the text is visible right now
                text_visible = check_for_resume_text()
                
                if text_visible and not last_clicked:
                    if dots_count > 0:  # If we printed dots, add a newline
                        print()
                        dots_count = 0
                    print(f"[{get_timestamp()}] Prompt detected - clicking...")
                    
                    # Save current mouse position
                    original_x, original_y = pyautogui.position()
                    
                    # Move to target and click
                    pyautogui.moveTo(click_x, click_y)
                    time.sleep(0.5)  # Give a moment to see where it's going to click
                    pyautogui.click()
                    click_count += 1
                    
                    # Return to original position
                    pyautogui.moveTo(original_x, original_y)
                    
                    # Set up post-click wait period
                    next_check_time = current_time + timedelta(seconds=POST_CLICK_WAIT_SECONDS)
                    print(f"[{get_timestamp()}] Waiting {POST_CLICK_WAIT_SECONDS} seconds before resuming checks...")
                    
                    last_clicked = True
                    last_activity = datetime.now()  # Update last activity time
                    if start_time is None:  # Record first click time
                        start_time = datetime.now()
                    
                elif not text_visible or (text_visible and current_time >= next_check_time):
                    if last_clicked and current_time >= next_check_time:
                        if dots_count > 0:  # If we printed dots, add a newline
                            print()
                            dots_count = 0
                        print(f"[{get_timestamp()}] Resuming prompt detection...")
                        last_clicked = False
                        next_check_time = None
                    elif not last_clicked:
                        print(".", end="", flush=True)  # Show it's still running
                        dots_count += 1
                        if dots_count >= 50:  # Start a new line after 50 dots
                            remaining_minutes = int((TIMEOUT_SECONDS - (current_time - last_activity).total_seconds()) / 60)
                            print(f" [{get_timestamp()}] ({remaining_minutes}m until timeout)")
                            dots_count = 0
                    time.sleep(0.5)
                
        except KeyboardInterrupt:
            runtime = format_duration((datetime.now() - start_time).total_seconds()) if start_time else "0s"
            print(f"\n[{get_timestamp()}] Stopping...")
            print_summary(runtime, click_count)
        
if __name__ == "__main__":
    main() 