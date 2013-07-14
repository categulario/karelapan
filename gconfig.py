import multiprocessing

bind = "192.168.1.72:8000"
workers = multiprocessing.cpu_count() * 2 + 1
