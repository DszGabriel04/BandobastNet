import json
import os
import threading
import time
from django.conf import settings

class JsonUpdater:
    def __init__(self):
        self.lock = threading.Lock()
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self.update_combined_json, daemon=True)

    def start(self):
        if not self.thread.is_alive():  # Ensure the thread is not already running
            self.thread.start()

    def stop(self):
        self._stop_event.set()  # Signal the thread to stop
        self.thread.join()  # Wait for the thread to finish

    def update_combined_json(self):
        while not self._stop_event.is_set():
            with self.lock:  # Ensure thread safety
                # Load the police data and duty data JSON files
                with open('policedata.json', 'r') as f1:
                    file1 = json.load(f1)

                with open('policedutydata.json', 'r') as f2:
                    file2 = json.load(f2)

                # Combine logic
                combined = []
                # Your combining logic...

                combined_file_path = os.path.join(settings.BASE_DIR, 'map', 'static', 'map', 'combinedpoldat.json')

                os.makedirs(os.path.dirname(combined_file_path), exist_ok=True)

                with open(combined_file_path, 'w') as combined_file:
                    json.dump(combined, combined_file, indent=2)

            time.sleep(1)  # Update every second
