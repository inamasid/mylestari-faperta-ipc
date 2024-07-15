import requests
import snap7
import time

def fetch_data(url):
    response = requests.get(url)
    return response.json()

def write_to_plc(client, address_map, data):
    for key, address in address_map.items():
        value = data[key]
        # Convert boolean value to bytearray
        byte_value = bytearray([1 if value else 0])
        client.write_area(snap7.types.Areas.PA, 0, address, byte_value)

def read_from_plc(client, addresses):
    results = {}
    for key, address in addresses.items():
        result = client.read_area(snap7.types.Areas.PA, 0, address, 1)
        if not result:
            print(f"Error reading {key} at address {address}")
            results[key] = None
        else:
            results[key] = bool(result[0])
    return results

def send_post(url, data):
    response = requests.post(url, json=data)
    return response.status_code, response.text

def main():
    api_url = 'http://localhost/api.php'
    post_url = 'http://localhost/post_api.php'  # Replace with your POST API endpoint

    address_map = {
        'dAB': 0,
        'dPhUp': 1,
        'dPhDown': 2,
        'co2': 3,
        'plantPump': 4,
        'sensorPump': 5,
        'grow1': 6,
        'grow2': 7,
        'grow3': 8,
        'grow4': 9,
        'grow5': 10,
        'grow6': 11
    }

    read_addresses = {
        'WLLo': 20,
        'WLMed': 21,
        'WLHi': 22
    }

    PLC_IP = '192.168.1.10'  # Replace with your PLC IP address

    client = snap7.client.Client()
    client.connect(PLC_IP, 0, 1)

    try:
        while True:
            # Fetch and write data to PLC
            data = fetch_data(api_url)
            write_to_plc(client, address_map, data)
            
            # Read data from PLC
            read_data = read_from_plc(client, read_addresses)
            
            # Send POST request with read data
            status_code, response_text = send_post(post_url, read_data)
            print(f"POST status: {status_code}, response: {response_text}")
            
            time.sleep(1)  # Delay between each iteration (1 second)
    except KeyboardInterrupt:
        print("Stopping the script.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
