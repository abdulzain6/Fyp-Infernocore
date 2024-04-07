import serial
import glob
import time

def find_serial_devices():
    # This will include devices like /dev/ttyUSB* and /dev/ttyACM*
    return glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')

def is_gps_device(device, baud_rate=9600):
    try:
        with serial.Serial(device, baud_rate, timeout=1) as ser:
            time.sleep(2)  # Wait for data to become available
            data = ser.read(2000)  # Read a chunk of data
            if b'$GPGGA' in data:
                return True
    except serial.SerialException:
        pass
    return False

def read_gps_data(device, baud_rate=9600):
    try:
        with serial.Serial(device, baud_rate, timeout=1) as ser:
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line.startswith('$GPGGA'):
                    print(line)  # Here you'd parse the NMEA sentence for detailed GPS data
                time.sleep(0.1)
    except serial.SerialException as e:
        print(f"Error reading from {device}: {e}")

def main():
    devices = find_serial_devices()
    for device in devices:
        if is_gps_device(device):
            print(f"GPS device found: {device}")
            read_gps_data(device)
            break
    else:
        print("No GPS device found.")

if __name__ == "__main__":
    main()
