import requests
import datetime


# Previous CO2 readings (example values in ppm)
previous_co2_values = [440, 450, 460, 470, 480]
normal_threshold_margin = 0.10  # 10% margin

# NGSI-LD entity and endpoint

co2_entity = "urn:ngsi-ld:AirQualitySensor:Sen5X_SCD41:002"
url_co2 = f"http://172.16.101.172:1026/ngsi-ld/v1/entities/{co2_entity}"

headers = {
    "Accept": "application/ld+json",
    "fiware-service": "openiot",
    "fiware-servicepath": "/"
}

# Send GET request to fetch current CO2 value
response = requests.get(url_co2, headers=headers)

if response.status_code == 200:
    data = response.json()

    # Extract the current CO2 value
    co2_value = data.get("SCD41_CO2_value", {}).get("value")
    if co2_value is not None:
        print(f"Current CO2 Value: {co2_value} ppm")

        # Calculate average of previous values
        average_co2 = sum(previous_co2_values) / len(previous_co2_values)
        threshold = average_co2 * (1 + normal_threshold_margin)

        # Compare current CO2 with threshold
        is_co2_normal = co2_value <= threshold

        print(f"Average CO2: {average_co2:.2f} ppm")
        print(f"Threshold (+10%): {threshold:.2f} ppm")
        print(f"Is CO2 normal? {is_co2_normal}")
        print(datetime.datetime.now())

    else:
        print("'SCD41_CO2_value' attribute not found in response.")
else:
    print(f"Error {response.status_code}: {response.text}")
