import requests
from pymodbus.client.sync import ModbusTcpClient
import time

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def write_to_plc(client, address_map, data):
    for key, address in address_map.items():
        value = bool(data[key])
        client.write_coil(address, value)

def read_from_plc(client, addresses):
    results = {}
    for key, address in addresses.items():
        result = client.read_coils(address, 1)
        if result.isError():
            print(f"Error reading {key} at address {address}")
            results[key] = None
        else:
            results[key] = result.bits[0]
    return results

def send_post(url, data):
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.status_code, response.text

def main():
    api_url = 'http://inamas.id/dev/faperta/dummy-api.php'
    post_url = 'http://inamas.id/dev/faperta/dummy-api.php?waterlevel'  # Replace with your POST API endpoint

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
    PLC_PORT = 502

    client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
    client.connect()

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
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
