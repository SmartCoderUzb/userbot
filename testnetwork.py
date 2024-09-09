import socket

try:
    socket.create_connection(("www.google.com", 80))
    print("Internet connection is available.")
except OSError:
    print("No internet connection.")
