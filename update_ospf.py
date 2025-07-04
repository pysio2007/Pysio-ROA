import json
import time
import sys

# Usage: python update_ospf.py <input_json> <output_json> <asn> <trust_anchor>

def main():
    if len(sys.argv) != 5:
        print("Usage: python update_ospf.py <input_json> <output_json> <asn> <trust_anchor>")
        sys.exit(1)

    input_json = sys.argv[1]
    output_json = sys.argv[2]
    asn = sys.argv[3]
    trust_anchor = sys.argv[4]

    with open(input_json, 'r') as f:
        data = json.load(f)

    roas = []
    for entry in data.get('NN', []):
        prefix = entry['prefix']
        maxlen = int(prefix.split('/')[1])
        roas.append({
            'asn': f'AS{asn}',
            'prefix': prefix,
            'maxLength': maxlen,
            'ta': trust_anchor
        })

    output = {
        'metadata': {
            'counts': len(roas),
            'generated': int(time.time()),
            'valid': int(time.time())
        },
        'roas': roas
    }

    with open(output_json, 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
