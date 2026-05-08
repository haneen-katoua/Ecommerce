import psutil
import time
import os

def monitor_django_server():
    django_process = None
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'python' in proc.info['name'].lower() and 'manage.py' in str(proc.info['cmdline']):
                django_process = proc
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not django_process:
        print("faild to run python manage.py runserver")
        return

    print(f"{'CPU %':<10} | {'Memory (MB)':<15} | {'Active Threads':<15}")
    print("-" * 50)

    try:
        while django_process.is_running():

            cpu_usage = django_process.cpu_percent(interval=0.5)
            memory_usage = django_process.memory_info().rss / (1024 * 1024)
            threads_count = django_process.num_threads()

            print(f"{cpu_usage:<10} | {memory_usage:<15.2f} | {threads_count:<15}")
            time.sleep(0.5)
    except (psutil.NoSuchProcess, KeyboardInterrupt):
        print("\n out")

if __name__ == "__main__":
    monitor_django_server()