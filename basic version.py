# basic version

import serial
import csv
import sys
from datetime import datetime

# Open the serial port (check which COM with device manager)
ser = serial.Serial('COM7', 115200)

# Wait for user input to start
input("Press Enter to start reading data...")

# Open the CSV file for writing
with open('hexdata.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write a header row
    csvwriter.writerow(['Timestamp', 'Hexadecimal String', 
                        'Sample 1 (Hex)', 'Sample 2 (Hex)', 'Sample 3 (Hex)', 'Sample 4 (Hex)', 'Sample 5 (Hex)',
                        'Sample 1 (Dec)', 'Sample 2 (Dec)', 'Sample 3 (Dec)', 'Sample 4 (Dec)', 'Sample 5 (Dec)', 
                        'Sample 1 (mV)', 'Sample 2 (mV)', 'Sample 3 (mV)', 'Sample 4 (mV)', 'Sample 5 (mV)'])
    
    try:
        print("Reading data... Press Ctrl+C to stop.")
        
        # Continuously read from the serial port
        while True:
            # Read incoming data (44 characters total in string, 22 pairs of 2 characters = 22 bytes)
            incoming_data = ser.read(22)
            
            # Convert to hexadecimal string (I think it already is?)
            hex_string = incoming_data.hex()
            
            # Check if the string starts with '7e'
            if hex_string.startswith('7e'):
                
# Get current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] # Take away 3 decimal places for miliseconds
                
                # Extract sample bytes (samples start after 11 bytes, which is 22 characters)
                # it's set to 5 samples per API/in each hex string
                sample_start_index = 11 * 2
                sample_bytes_hex = [
                    hex_string[sample_start_index:sample_start_index+4],
                    hex_string[sample_start_index+4:sample_start_index+8],
                    hex_string[sample_start_index+8:sample_start_index+12],
                    hex_string[sample_start_index+12:sample_start_index+16],
                    hex_string[sample_start_index+16:sample_start_index+20]
                ]
                
                # Convert the hexadecimal sample values to decimal numbers
                sample_bytes_dec = [int(sample, 16) for sample in sample_bytes_hex]
                
                # Convert the decimal sample values to milivolts
               # My voltage goes from 0 to 3925mV, the number coming in represents that as a number between 0 and 1023 (1023 steps). 3925 / 1023 = 3.22mV per step
                mv_conversion_factor = 3.22
                sample_bytes_mv = [round(sample_dec * mv_conversion_factor, 2) for sample_dec in sample_bytes_dec]
                
                
                # Prepare row with timestamp, hex string, and all sample values grouped by type
                row = [timestamp, hex_string]
                row.extend(sample_bytes_hex)
                row.extend(sample_bytes_dec)
                row.extend(sample_bytes_mv)
                
                # Write the row to the CSV file
                csvwriter.writerow(row)
                csvfile.flush()  # Ensure data is written to the file immediately
                
                # Optional print sample data to the console
                # print(f"Timestamp: {timestamp}, Received data: {hex_string}, Samples (Hex): {sample_bytes_hex}, Samples (Dec): {sample_bytes_dec}, Samples (mV): {sample_bytes_mv}")
    
    except KeyboardInterrupt:
        print("\nData reading stopped by user.")
    
    finally:
        # Close the serial port
        ser.close()
        print("Serial port closed.")
