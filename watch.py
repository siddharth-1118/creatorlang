#!/usr/bin/env python3
"""CreatorLang Auto-Reload Watcher - Automatically recompile on file changes"""

import sys
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CreateFileHandler(FileSystemEventHandler):
    def __init__(self, file_to_watch):
        self.file_to_watch = os.path.abspath(file_to_watch)
        self.last_modified = 0
        
    def on_modified(self, event):
        if event.src_path == self.file_to_watch:
            # Debounce - only recompile if 0.5 seconds have passed
            current_time = time.time()
            if current_time - self.last_modified > 0.5:
                self.last_modified = current_time
                print(f"\n🔄 Detected change in {os.path.basename(self.file_to_watch)}")
                self.compile_file()
    
    def compile_file(self):
        try:
            print(f"⚙️  Compiling...")
            result = subprocess.run(
                ['python', 'compiler.py', self.file_to_watch],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(result.stdout)
                print("✅ Ready! Edit the file again to see changes.")
            else:
                print(f"❌ Compilation error:\n{result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python watch.py <file.create>")
        print("Example: python watch.py examples/doraemon_simple.create")
        sys.exit(1)
    
    file_to_watch = sys.argv[1]
    
    if not os.path.exists(file_to_watch):
        print(f"❌ Error: File '{file_to_watch}' not found")
        sys.exit(1)
    
    # Initial compilation
    print(f"👀 Watching {file_to_watch} for changes...")
    print(f"💡 Tip: Keep output/doraemon_frame.png open to see live updates!\n")
    
    handler = CreateFileHandler(file_to_watch)
    handler.compile_file()  # Compile once at start
    
    # Watch for file changes
    observer = Observer()
    watch_dir = os.path.dirname(os.path.abspath(file_to_watch)) or '.'
    observer.schedule(handler, watch_dir, recursive=False)
    observer.start()
    
    try:
        print("\n⏸️  Press Ctrl+C to stop watching...\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 Stopped watching. Goodbye!")
    
    observer.join()

if __name__ == "__main__":
    main()
