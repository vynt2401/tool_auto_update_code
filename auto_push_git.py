import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class GitAutoPusher(FileSystemEventHandler):
    def __init__(self, commit_message="Auto update"):
        self.commit_message = commit_message
        self.ignore_extensions = {'.swp', '.tmp', '.pyc'}  # ignore temp files

    def on_modified(self, event):
        if any(event.src_path.endswith(ext) for ext in self.ignore_extensions):
            return
        print(f"[+] File changed: {event.src_path}")
        self.git_push()

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"[+] File created: {event.src_path}")
        self.git_push()

    def on_deleted(self, event):
        if event.is_directory:
            return
        print(f"[+] File deleted: {event.src_path}")
        self.git_push()

    def git_push(self):
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", self.commit_message], check=True)
            subprocess.run(["git", "push"], check=True)
            print("[✓] Code pushed to GitHub!")
        except subprocess.CalledProcessError as e:
            print(f"[!] Git error: {e}")


def start_watching(path="."):
    event_handler = GitAutoPusher()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    print(f"🚀 Watching for changes in '{path}'... (Press Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("❌ Stopped.")
    observer.join()


if __name__ == "__main__":
    start_watching(".")  # Current folder
