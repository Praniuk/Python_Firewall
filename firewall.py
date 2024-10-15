import pydivert
import time
import logging
import socket

# Get the device's local IP address so it doesnt block it's own background packets
local_ip = socket.gethostbyname(socket.gethostname())

# Configure the rate limiting parameters, 
PACKET_LIMIT_PER_SECOND = 40  
BLOCK_DURATION = 60                  # In seconds
blacklisted_ips = []
whitelisted_ips = [local_ip]         # Best to add your router's local adress here after your device's IP, so it doesn't constantly trigger DDos blocks
temp_blocked_ips = {}                # Dictionary to store temporary blocked IPs and the time they were blocked
packet_counts = {}                   # Dictionary to store packet counts for each IP
last_checked_time = time.time()

# Configure the logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename='firewall_logs.log', encoding='utf-8', level=logging.DEBUG)

# Function to clean up blocked IPs after block duration
def cleanup_blocked_ips():
    current_time = time.time()

    for ip in list(temp_blocked_ips):
        if current_time - temp_blocked_ips[ip] > BLOCK_DURATION:
            print(f"Unblocking IP: {ip}")
            del temp_blocked_ips[ip]  

# Function to check and block IPs that exceed the packet rate limit
def check_ddos_protection(ip):
    current_time = time.time()
    global last_checked_time
    
    # Reset packet counts every second
    if current_time - last_checked_time >= 1:
        packet_counts.clear()
        last_checked_time = current_time

    # Increment packet count for the IP
    if ip in packet_counts:
        packet_counts[ip] += 1
    else:
        packet_counts[ip] = 1

    # If the IP exceeds the packet limit, block it
    if packet_counts[ip] > PACKET_LIMIT_PER_SECOND:
        temp_blocked_ips[ip] = current_time
        logger.warning(f"Blocking IP due to DDoS: {ip}")   # Log the blocking of an IP
        print(f"Blocking IP due to DDoS: {ip}")

# Main loop that captures all packets and decides what to do with them
with pydivert.WinDivert("true") as w:  # Capture all traffic coming to the socket
    print("Firewall up, monitoring...")

    # Check every captured packet
    for packet in w:
        src_ip = packet.src_addr  # Get the packet's source IP

        cleanup_blocked_ips()     # Clean up blocked IPs that are expired

        # Check if the IP exceeds the DDoS protection limit, omit packets with no payload
        if packet.payload is not None and len(packet.payload) > 0 and src_ip not in whitelisted_ips:
            check_ddos_protection(src_ip)
            
        # Check if the IP is currently blocked
        if src_ip in temp_blocked_ips or src_ip in blacklisted_ips:
            logger.info(f"Blocked packet from {src_ip}")
            print(f"Blocked packet from {src_ip}")
            continue              # If the IP is blocked, drop the packet

        
        w.send(packet)            # If not blocked, forward the packet