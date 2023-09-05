import socket

def get_device_name(ip_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except (socket.gaierror, socket.herror, socket.error):
        return "Unknown"

