import socket
import csv
import threading
import queue
import time
# -----------------------
# CONFIGURATION
# -----------------------
UDP_IP = "0.0.0.0" # Listen on all available network
interfaces
RIGHT_HAND_PORT = 8888 # UDP port for right-hand glove data
LEFT_HAND_PORT = 8889 # UDP port for left-hand glove data
OUTPUT_FILE = "bsl_gesture_log_with_imu.csv" # CSV file to
store data
# CSV header structure:
# Right hand: 5 flex + 2 touch + 3 accel + 3 gyro
# Left hand: 5 flex + 2 touch + 3 accel + 3 gyro
HEADERS = [
 # Right hand sensors
 'RH_Flex1', 'RH_Flex2', 'RH_Flex3', 'RH_Flex4', 'RH_Flex5',
 'RH_Touch1', 'RH_Touch2',
 'RH_AccelX', 'RH_AccelY', 'RH_AccelZ',
 'RH_GyroX', 'RH_GyroY', 'RH_GyroZ',
 # Left hand sensors
 'LH_Flex1', 'LH_Flex2', 'LH_Flex3', 'LH_Flex4', 'LH_Flex5',
 'LH_Touch1', 'LH_Touch2',
 'LH_AccelX', 'LH_AccelY', 'LH_AccelZ',
 'LH_GyroX', 'LH_GyroY', 'LH_GyroZ',
 # Gesture label
 'Gesture_Label'
]
# Thread-safe queue for gesture labels
gesture_queue = queue.Queue()
# -----------------------
# FUNCTION: Label Input Thread
# -----------------------
def input_thread():
 """
 Continuously waits for user to type a gesture label
 and adds it to the queue.
 """
 while True:
 label = input()
 gesture_queue.put(label.strip())
# -----------------------
# MAIN FUNCTION
# -----------------------
def main():
 # Create UDP sockets
 sock_right = socket.socket(socket.AF_INET,
socket.SOCK_DGRAM)
 sock_left = socket.socket(socket.AF_INET,
socket.SOCK_DGRAM)
 # Bind to ports
 sock_right.bind((UDP_IP, RIGHT_HAND_PORT))
 sock_left.bind((UDP_IP, LEFT_HAND_PORT))
 # Non-blocking mode
 sock_right.setblocking(False)
 sock_left.setblocking(False)
 # Data storage variables
 right_hand_data = None
 left_hand_data = None
 gesture_label = ""
 print(f"Listening on ports {RIGHT_HAND_PORT} (Right) and
{LEFT_HAND_PORT} (Left)...")
 print("Enter gesture labels at any time. Press Ctrl+C to
stop.")
 # Start label input thread
 threading.Thread(target=input_thread, daemon=True).start()
 # Open CSV for writing
 with open(OUTPUT_FILE, mode='w', newline='') as csvfile:
 writer = csv.writer(csvfile)
 writer.writerow(HEADERS) # Write header row
 try:
 while True:
 # -----------------------
 # Check for new gesture label
 # -----------------------
 if not gesture_queue.empty():
 gesture_label = gesture_queue.get()
 print(f"Gesture label set to:
'{gesture_label}' for next row.")
 # -----------------------
 # Receive right hand data
 # -----------------------
 try:
 data_right, _ = sock_right.recvfrom(1024)
right_hand_data = data_right.decode('utf8').strip().split(',')
 if len(right_hand_data) != 13: # Expecting
5 flex + 2 touch + 3 accel + 3 gyro
 print(f"Malformed right hand data:
{right_hand_data}")
 right_hand_data = None
 else:
 print(f"Right Hand: {right_hand_data}")
 except BlockingIOError:
 pass
 # -----------------------
 # Receive left hand data
 # -----------------------
 try:
 data_left, _ = sock_left.recvfrom(1024)
left_hand_data = data_left.decode('utf8').strip().split(',')
 if len(left_hand_data) != 13: # Expecting
5 flex + 2 touch + 3 accel + 3 gyro
 print(f"Malformed left hand data:
{left_hand_data}")
 left_hand_data = None
 else:
 print(f"Left Hand: {left_hand_data}")
 except BlockingIOError:
 pass
 # -----------------------
 # When both hands have data, log them
 # -----------------------
 if right_hand_data and left_hand_data:
 combined_row = right_hand_data +
left_hand_data + [gesture_label]
 writer.writerow(combined_row)
csvfile.flush()
print(f"Logged row with gesture:
'{gesture_label}'")
 # Reset
 right_hand_data = None
left_hand_data = None
gesture_label = ""
 # Small delay to prevent high CPU usage
 time.sleep(0.05)
 except KeyboardInterrupt:
 print("\nLogging stopped by user.")
# -----------------------
# ENTRY POINT
# -----------------------
if __name__ == "__main__":
 main()
