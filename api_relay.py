import requests
from pymodbus.client import ModbusTcpClient
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError
import time, hashlib

def fetch_data(url):
    response = requests.get(url, timeout=3)  # Set a short timeout for real-time
    response.raise_for_status()
    data = response.json()['advice']
    data.pop("id", None)
    data.pop("updated_at", None)
    return data

def write_to_plc(client, address_map, data):
    status = {}
    for key, address in address_map.items():
        value = bool(data[key])
        client.write_register(address, value)
        status[address] = value
    return status

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
    date_today = time.strftime("%Y-%m-%d")
    hashToday = hashlib.md5(date_today.encode()).hexdigest()
    payload = {f"{hashToday}": data}
    response = requests.post(url, json=payload, timeout=3)  # Set a short timeout for real-time
    response.raise_for_status()
    return response.status_code, payload

def main():
    api_url = 'https://inamas.id/dev/faperta/?actuator'
    post_url = 'https://inamas.id/dev/faperta/?sensor'

    write_addresses = {
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
        'wl_low': 12,
        'wl_mid': 13,
        'wl_hig': 14
    }

    PLC_IP = '192.168.0.2'
    PLC_PORT = 502

    client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
    client.connect()

    try:
        while True:
            try:
                # Fetch and write data to PLC
                data = fetch_data(api_url)
                write_data = write_to_plc(client, write_addresses, data)

                # Read data from PLC
                read_data = read_from_plc(client, read_addresses)

                # Send POST request with read data
                status_code, response_text = send_post(post_url, read_data)

                print(f"API Write: {write_data}")
                print(f"POST status: {status_code}, response: {response_text}\n")

            except (Timeout, ConnectionError, HTTPError) as e:
                print(f"Network-related error occurred: {e}")
                continue  # Skip this iteration and retry immediately

            except RequestException as e:
                print(f"Request failed: {e}")
                continue  # Skip this iteration and retry immediately

            except Exception as e:
                print(f"Unexpected error occurred: {e}")
                continue  # Skip this iteration and retry immediately

    except KeyboardInterrupt:
        print("Stopping the script.")

    finally:
        client.close()

if __name__ == "__main__":
    main()
