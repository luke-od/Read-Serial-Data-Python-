# Read-Serial-Data-Python-
Read in serail data (from a USB) and print it into the terminal using this Python script

Read it in as Hexidecimal
Converts to the Analog-to-Digital Converter (ADC) value (this is 1023 [2^10] for this 10-Bit example)
Convert converts ADC to Volts (this is a 3.2V example)

You might need to change your ADC conversion factor (1023 for 10-Bit) or the Voltage range value (3.2V)
Output number / 1023 x 3.2V = voltage value from sensor
