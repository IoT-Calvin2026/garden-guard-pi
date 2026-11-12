from datetime import datetime
from time import sleep
from picamzero import Camera

DELAY_SECONDS = 5  # Time between photos
TOTAL_PHOTOS = 1  # Use a while True loop for infinite
SAVE_DIRECTORY = "/home/pi/images"

cam = Camera()

print(f"Starting automated capture. Waiting {DELAY_SECONDS} seconds between shots...")

try:
    for i in range(1, TOTAL_PHOTOS + 1):
        # Generate a unique timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{SAVE_DIRECTORY}/photo_{timestamp}.jpg"

        print(f"[{i}/{TOTAL_PHOTOS}] Taking photo in...")

        for countdown in range(DELAY_SECONDS, 0, -1):
            print(f"  {countdown}...")
            sleep(1)

        cam.capture_image(filename)
        print(f"  Saved: {filename}")

    print("\nCapture sequence complete!")

except KeyboardInterrupt:
    print("\nCapture sequence stopped by user.")
