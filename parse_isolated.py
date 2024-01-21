# Isolated parsing

import re
# My
#  SG_ (\w+) : (\d+)\|(\d+)\@(\d)([+-])
# (\([\d\.]+\)) 
# \[([\d\.,]+)\|([\d\.,]+)\]

# SG_ (\w+) : (\d+)\|(\d+)@([-\d\.]+)([+\-]) (\([\d\.,]+\)) \[([\d\.,]+)\|([\d\.,]+)\]

# My winner
#   SG_ (\w+) : (\d+)\|(\d+)@([-\d\.]+)([+\-]) \(([0-9.]+)\,([0-9.]+)\) \[([\d\.,]+)\|([\d\.,]+)\] \"(.*?)\" \s*(\w+)

# Chatgpt winnner (doesnt work)
# (\d+)\|(\d+)@([-\d\.]+)([+\-]) \(([\d.]+),([\d.]+)\) \[([\d.,]+)\|([\d.,]+)\] "(.*?)"\s*(.*?)$

def extract_messages_and_signals(file_content):
    messages = {}
    current_message = None

    lines = file_content.split('\n')
    for line in lines:
        if line.startswith("BO_"):
            # Extract message information
            pattern = r'BO_ (\d+) (\w+): (\d+) (\w+)'
            match = re.match(pattern, line)
            if match:
                message_id, message_name, message_length, message_sender = match.groups()
                current_message = {
                    "id": int(message_id),
                    "name": message_name,
                    "length": int(message_length),
                    "sender": message_sender,
                    "signals": []
                }
                messages[message_name] = current_message

        elif line.startswith(" SG_ "):
            # Extract signal information
            pattern = r' SG_ (\w+) : (\d+)\|(\d+)@([-\d\.]+)([+\-]) \(([0-9.]+)\,([0-9.]+)\) \[([\d\.,]+)\|([\d\.,]+)\] \"(.*?)\" \s*(\w+)'
            match = re.match(pattern, line)
            if match and current_message:
                signal_name, start_bit, signal_length, byte_order, signed, scale, offset, min, max, unit, receiver = match.groups()
                signal = {
                    "name": signal_name,
                    "start_bit": int(start_bit),
                    "length": int(signal_length),
                    "byte_order": int(byte_order), # 0 = little endian, 1 = big endian
                    "signed": signed,
                    "scale": float(scale),
                    "offset": float(offset),
                    "min": float(min),
                    "max": float(max),
                    "unit": unit,
                    "receiver": receiver
                }
                current_message["signals"].append(signal)

    return messages

# Read the content of the provided file
file_path = "volvo_v40_2017_pt.dbc"
with open(file_path, 'r') as file:
    file_content = file.read()

# Extract and print messages and signals
messages = extract_messages_and_signals(file_content)
for message_name, message in messages.items():
    print(f"Message: {message_name}")
    print(f"ID: {message['id']}, Length: {message['length']}, Sender: {message['sender']}")
    print("Signals:")
    for signal in message['signals']:
        print(f"  - {signal['name']}")
    print("\n")

print("Debug")