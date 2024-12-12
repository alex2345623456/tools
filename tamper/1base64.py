import base64
import argparse

def base64_encode(payload):
    """Encode the payload with Base64."""
    return base64.b64encode(payload.encode()).decode()

def char_encode(payload):
    """Encode each character in the payload as '\\xHH'."""
    return ''.join(f'\\x{ord(c):02x}' for c in payload)

def append_null_byte(payload):
    """Append a null byte to the payload."""
    return payload + '\x00'

def tamper_payload(payload):
    """Apply tamper techniques: base64encode -> charencode -> appendnullbyte."""
    encoded_payload = base64_encode(payload)
    char_encoded_payload = char_encode(encoded_payload)
    tampered_payload = append_null_byte(char_encoded_payload)
    return tampered_payload

def process_payload_file(input_file, output_file):
    """Read payloads from a file, tamper them, and save to a new file."""
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            tampered = tamper_payload(line.strip())
            outfile.write(tampered + '\n')
            print(f"Original: {line.strip()}\nTampered: {tampered}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Payload Tamper Script")
    parser.add_argument('-l', '--list', required=True, help="Input file containing payloads")
    parser.add_argument('-o', '--output', required=True, help="Output file for tampered payloads")

    args = parser.parse_args()

    process_payload_file(args.list, args.output)
