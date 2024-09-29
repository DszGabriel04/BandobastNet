from django.shortcuts import render
import json
import os
import threading
import time
from django.conf import settings
from django.http import JsonResponse

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

                # Create a mapping from the duty data
                mapping = {item['off_name']: item for item in file2}

                # Combine the two JSON files
                combined = []
                for item in file1:
                    if item['off_name'] in mapping:
                        combined_item = {**item, **mapping[item['off_name']]}
                        combined.append(combined_item)
                    else:
                        combined.append(item)

                for item in file2:
                    if not any(i['off_name'] == item['off_name'] for i in file1):
                        combined.append(item)

                # Define the path to save the combined JSON
                combined_file_path = os.path.join(settings.BASE_DIR, 'map', 'static', 'map', 'combinedpoldat.json')

                # Create the directory if it doesn't exist
                os.makedirs(os.path.dirname(combined_file_path), exist_ok=True)

                # Save the combined data to a JSON file
                with open(combined_file_path, 'w') as combined_file:
                    json.dump(combined, combined_file, indent=2)

            time.sleep(1)  # Update every second


# Global instance of the JsonUpdater
json_updater = JsonUpdater()

def show_map(request):
    """Render the map HTML and start the JSON updater if it's not running."""
    json_updater.start()  # Start the JSON updater thread if it's not already running
    return render(request, 'map/map.html')

def shutdown():
    """Call this function to stop the JSON updater gracefully."""
    json_updater.stop()

from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_finished)
def stop_json_updater(sender, **kwargs):
    """Stop the JSON updater when the request is finished."""
    shutdown()  # Call the shutdown function to stop the JSON updater
