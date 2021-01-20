import time

def info(msg):
	print(time.ctime(), "info", msg)

def error(msg):
	print(time.ctime(), "error", msg)

def warn(msg):
	print(time.ctime(), "warn", msg)

def debug(msg):
	print(time.ctime(), "debug", msg)

