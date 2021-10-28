import shutil
import time
from datetime import datetime
from pathlib import Path

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


def get_date_time_stamp():
    today = datetime.now()
    timestamp = str(today.timestamp()).split('.')[0]
    return f'{today:%m_%d_%Y}_{timestamp}'


class FolderHandler(PatternMatchingEventHandler):

    def __init__(self, target_folder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_folder = target_folder

    def on_created(self, event):
        # to prevent PermissionError: [Errno 13] Permission denied:
        time.sleep(1)
        
        shutil.move(event.src_path, self.target_folder) # move source file to target folder


if __name__ == '__main__':
    # source_folder: watching folder, target_folder: move file to folder.
    folders = {
        'foo': {
            'source_folder': './foo',
            'target_folder': './home'
        },
        'bar': {
            'source_folder': './bar',
            'target_folder': './home'
        }
    }

    observer = Observer()

    for _, folder in folders.items():
        # patterns: txt file only
        event_handler = FolderHandler(target_folder=folder['target_folder'], patterns=['*.txt'],  ignore_directories=True, case_sensitive=False)
        observer.schedule(event_handler,  folder['source_folder'],  recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
