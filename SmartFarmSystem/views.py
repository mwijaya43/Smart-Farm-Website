from django.shortcuts import render
from datetime import datetime
from .models import SmartPlantingActuator,SmartPlantingSensor,EcosystemActuator,EcosystemSensor,FarmManagementActuator,FarmManagementSensor,SmartPlantingActSens,EcosystemActSens,FarmManagementActSens
from joblib import dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from joblib import load
from django.db.models import F  # Import F to use database expressions
import paho.mqtt.client as mqtt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize


#function for getting data
def get_ecosystemsensor():
    sensor1 = "Sensor Suhu"
    sensor2 = "Sensor Kelembapan"
    sensor3 = "Sensor Intensitas Cahaya"
    
    # Retrieve the last 500 entries for each sensor
    sensor_data1 = EcosystemSensor.objects.filter(name=sensor1).order_by('-id')[:500].values_list('value', flat=True)
    sensor_data2 = EcosystemSensor.objects.filter(name=sensor2).order_by('-id')[:500].values_list('value', flat=True)
    sensor_data3 = EcosystemSensor.objects.filter(name=sensor3).order_by('-id')[:500].values_list('value', flat=True)
    
    # Convert QuerySets to lists and then to floats
    sensor_data1_float = [float(value) for value in sensor_data1]
    sensor_data2_float = [float(value) for value in sensor_data2]
    sensor_data3_float = [float(value) for value in sensor_data3]
    
    # Combine all sensor data into a single list
    combined_sensor_data = [sensor_data1_float, sensor_data2_float, sensor_data3_float]
    
    return combined_sensor_data

def get_smartplantingsensor():
    sensor1 = "Sensor Water Level"
    sensor2 = "Sensor Nutrisi"
    sensor3 = "Sensor pH"
    
    # Retrieve the last 500 entries for each sensor
    sensor_data1 = SmartPlantingSensor.objects.filter(name=sensor1).order_by('-id')[:500].values_list('value', flat=True)
    sensor_data2 = SmartPlantingSensor.objects.filter(name=sensor2).order_by('-id')[:500].values_list('value', flat=True)
    sensor_data3 = SmartPlantingSensor.objects.filter(name=sensor3).order_by('-id')[:500].values_list('value', flat=True)
    
    # Convert QuerySets to lists and then to floats
    sensor_data1_float = [float(value) for value in sensor_data1]
    sensor_data2_float = [float(value) for value in sensor_data2]
    sensor_data3_float = [float(value) for value in sensor_data3]
    
    # Combine all sensor data into a single list
    combined_sensor_data = [sensor_data1_float, sensor_data2_float, sensor_data3_float]
    
    return combined_sensor_data


def get_farmmanagementsensor():
    sensor1 = "Sensor Ultrasonic"
    sensor2 = "Sensor Kamera"
    sensor3 = "Sensor LIDAR"
    
    # Retrieve the last 500 entries for each sensor
    sensor_data1 = FarmManagementSensor.objects.filter(name=sensor1).order_by('-id')[:500].values_list('value', flat=True)
    sensor_data2 = FarmManagementSensor.objects.filter(name=sensor2).order_by('-id')[:500].values_list('value', flat=True)
    sensor_data3 = FarmManagementSensor.objects.filter(name=sensor3).order_by('-id')[:500].values_list('value', flat=True)
    
    # Convert QuerySets to lists and then to floats
    sensor_data1_float = [float(value) for value in sensor_data1]
    sensor_data2_float = [float(value) for value in sensor_data2]
    sensor_data3_float = [float(value) for value in sensor_data3]
    
    # Combine all sensor data into a single list
    combined_sensor_data = [sensor_data1_float, sensor_data2_float, sensor_data3_float]
    
    return combined_sensor_data


def get_actuator(actuator_name):
    # Retrieve the last 500 entries for the specified actuator
    if actuator_name == "Kipas & Ventilasi" or actuator_name == "Water Mist Sprinkler" or actuator_name == "Lampu UV":
        actuator_data = EcosystemActuator.objects.filter(name=actuator_name).order_by('-id')[:500].values_list('value', flat=True)
        return list(actuator_data)
    elif actuator_name == "Pompa Air" or actuator_name == "Dispenser Nutrisi" or actuator_name == "Dispenser pH":
        actuator_data = SmartPlantingActuator.objects.filter(name=actuator_name).order_by('-id')[:500].values_list('value', flat=True)
        return list(actuator_data)
    if actuator_name == "LED RGB" or actuator_name == "LCD" or actuator_name == "Alarm":
        actuator_data = FarmManagementActuator.objects.filter(name=actuator_name).order_by('-id')[:500].values_list('value', flat=True)
        return list(actuator_data)

def train_actuator(data_Sensor, actuator_name):
    # Ensure the data is limited to 500 samples for each sensor
    limited_data_Sensor = [data[-500:] for data in data_Sensor]

    X = np.array(limited_data_Sensor).T  # Transpose the data for proper shape
    actuator_data = get_actuator(actuator_name)[-500:]  # Fetch the last 500 actuator data
    y = np.array(actuator_data)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    predictions = clf.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    # print(f"Accuracy for {actuator_name}: {accuracy}")

    dump(clf, f'model_{actuator_name}.joblib')


# Fungsi untuk memprediksi keluaran aktuator berdasarkan data sensor baru
def predict_actuator_output(sensor1, sensor2, sensor3, actuator_name):
    # Load model yang sesuai
    model = load(f'model_{actuator_name}.joblib')

    # Data sensor baru sebagai input
    new_sensor_data = np.array([sensor1, sensor2, sensor3]).reshape(1, -1)  # Reshape menjadi bentuk yang sesuai dengan model

    # Lakukan prediksi menggunakan model
    prediction = model.predict(new_sensor_data)
    return prediction[0]  # Kembalikan prediksi dari aktuator




broker_address = "127.0.0.1"
port = 1886
topics = ["Sensor_Ultrasonics", "Sensor_Kameras", "Sensor_LIDARs", "Sensor_Water_Levels", "Sensor_Nutrisis", "Sensor_pHs", "Sensor_Suhus", "Sensor_Kelembapans", "Sensor_IntensitasCahayas"]

# Class to represent a sensor
class Sensor:
    def __init__(self, name, value, timestamp):
        self.name = name
        self.value = value
        self.timestamp = timestamp

# Global variable for storing the most recent sensor data
recent_topic_payloads = {topic: Sensor(name="", value=0, timestamp=datetime.now()) for topic in topics}

# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    # print(f"Connected with result code {rc}")
    for topic in topics:
        client.subscribe(topic)

# Callback when a message is received from the server
def on_message(client, userdata, msg):
    global recent_topic_payloads

    payload = msg.payload.decode("utf-8")
    # print(f"Received payload: {payload}")

    try:
        # Update the recent_topic_payloads dictionary
        recent_topic_payloads[msg.topic] =  np.round(float(payload),3)
        # print(f"Payload stored for topic {msg.topic}: {payload}")
    except KeyError as e:
        print(f"KeyError: {e}")

# Set up the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, port, 60)

# Start the client loop in the background
client.loop_start()

def SmartFarmSystemLoop(request):
    ultrasonic = recent_topic_payloads["Sensor_Ultrasonics"]
    kamera = recent_topic_payloads["Sensor_Kameras"]
    lidar = recent_topic_payloads["Sensor_LIDARs"]
    waterlevel = recent_topic_payloads["Sensor_Water_Levels"]
    nutrisi = recent_topic_payloads["Sensor_Nutrisis"]
    ph = recent_topic_payloads["Sensor_pHs"]
    suhu = recent_topic_payloads["Sensor_Suhus"]
    kelembapan = recent_topic_payloads["Sensor_Kelembapans"]
    cahaya = recent_topic_payloads["Sensor_IntensitasCahayas"]
    # Train dan Db
    data_EcosystemSensor = get_ecosystemsensor()  
    train_actuator(data_EcosystemSensor, 'Kipas & Ventilasi')
    train_actuator(data_EcosystemSensor, 'Water Mist Sprinkler')
    train_actuator(data_EcosystemSensor, 'Lampu UV')

    data_SmartPlantingSensor = get_smartplantingsensor() 
    train_actuator(data_SmartPlantingSensor, 'Pompa Air')
    train_actuator(data_SmartPlantingSensor, 'Dispenser Nutrisi')
    train_actuator(data_SmartPlantingSensor, 'Dispenser pH')

    data_FarmManagementSensor = get_farmmanagementsensor() 
    train_actuator(data_FarmManagementSensor, 'LED RGB')
    train_actuator(data_FarmManagementSensor, 'Alarm')


    def pompa_air(waterlevel, nutrisi, ph, actuator_name):
        output_actuator = predict_actuator_output(waterlevel, nutrisi, ph, actuator_name)
        return str(output_actuator)
        
    def dispenser_nutrisi(waterlevel, nutrisi, ph, actuator_name):
        output_actuator = predict_actuator_output(waterlevel, nutrisi, ph, actuator_name)
        return str(output_actuator)

    def dispenser_ph(waterlevel, nutrisi, ph, actuator_name):
        output_actuator = predict_actuator_output(waterlevel, nutrisi, ph, actuator_name)
        return str(output_actuator)
    
    def kipas_ventilasi(suhu, kelembapan, cahaya, actuator_name):
        output_actuator = predict_actuator_output(suhu, kelembapan, cahaya, actuator_name)
        return str(output_actuator)

    def water_mist(suhu, kelembapan, cahaya, actuator_name):
        output_actuator = predict_actuator_output(suhu, kelembapan, cahaya, actuator_name)
        return str(output_actuator)
    
    def lampu_uv(suhu, kelembapan, cahaya, actuator_name):
        output_actuator = predict_actuator_output(suhu, kelembapan, cahaya, actuator_name)
        return str(output_actuator)
        
    def led_rgb(ultrasonic, kamera, lidar, actuator_name):
        output_actuator = predict_actuator_output(ultrasonic, kamera, lidar, actuator_name)
        return str(output_actuator)
    
    def alarm(ultrasonic, kamera, lidar, actuator_name):
        output_actuator = predict_actuator_output(ultrasonic, kamera, lidar, actuator_name)
        return str(output_actuator)
        
    def lcd(ultrasonic, kamera, lidar, status_led_rgb, status_alarm):
        # print(f'Alarm Condition: {status_alarm}, Led Condition: {status_led_rgb}')
        return f'Alarm Condition: {status_alarm}, Led Condition: {status_led_rgb}'
    
    # def pompa_air(waterlevel, nutrisi, ph, name):
    #     if waterlevel <= 50 and nutrisi < 100 and (ph > 5 and ph < 7):
    #         return "On"
    #     elif waterlevel > 80 and nutrisi < 80:
    #         return "On"  
    #     elif nutrisi < 80:
    #         return "Off" 
    #     else: 
    #         return "Off"
        
    # def dispenser_nutrisi(waterlevel, nutrisi, ph, name):
    #     if nutrisi < 90 and waterlevel < 90 and (ph > 5 and ph < 7):
    #         return "On"
    #     elif nutrisi < 90 and (ph < 5.5 or ph > 7 ):
    #         return "Off"
    #     else: 
    #         return "On"

    # def dispenser_ph(waterlevel, nutrisi, ph, name):
    #     if (ph > 5.5 and ph < 7) and waterlevel > 50 and nutrisi < 60:
    #         return "Off"
    #     else: 
    #         return "On"
        
    # def kipas_ventilasi(suhu, kelembapan, cahaya, name):
    #     if (suhu > 27 and suhu <=30) and kelembapan >= 60 and cahaya > 6000:
    #         return "1"      
    #     if (suhu > 30 and suhu <=35) and kelembapan >= 40 and cahaya > 5000:
    #         return "2"
    #     if (suhu > 35 and suhu <= 40) and kelembapan >= 20 and cahaya > 4000:
    #         return "3"
    #     else: 
    #         return "0"

    # def water_mist(suhu, kelembapan, cahaya, name):
    #     if (suhu > 31 and kelembapan < 60) and cahaya > 5000:
    #         return "On" 
    #     elif kelembapan > 80:
    #         return "Off"
    #     elif suhu > 36:
    #         return "On"
    #     return "Off"
    
    # def lampu_uv(suhu, kelembapan, cahaya, name):
    #     if cahaya >= 7000 and suhu > 30 and kelembapan > 50 :
    #         return "Off"
    #     else:
    #         return "On"
        
    # def led_rgb(ultrasonic, kamera, lidar, name):
    #     if ultrasonic > 50 and kamera == 1 and lidar < 10:
    #         return "Red"
    #     elif ultrasonic < 40:
    #         return "Yellow"
    #     else:
    #         return "Green"
    
    # def alarm(ultrasonic, kamera, lidar, name):
    #     if ultrasonic > 50 and kamera == 1 and lidar < 10:
    #         return "On"
    #     else:
    #         return "Off"
        
    # def lcd(ultrasonic, kamera, lidar, name, name2):
    #     return f'Alarm Condition: {alarm(ultrasonic,kamera,lidar, name)}, Led Condition: {led_rgb(ultrasonic,kamera,lidar, name)}'

    
    
    status_pompa_air = pompa_air(waterlevel, nutrisi, ph, "Pompa Air")
    status_dispenser_nutrisi = dispenser_nutrisi(waterlevel, nutrisi, ph, "Dispenser Nutrisi")
    status_dispenser_ph = dispenser_ph(waterlevel, nutrisi, ph, "Dispenser pH")
    status_kipas_vent = kipas_ventilasi(suhu, kelembapan, cahaya, "Kipas & Ventilasi")
    status_water_mist = water_mist(suhu, kelembapan, cahaya, "Water Mist Sprinkler")
    status_lampu_uv = lampu_uv(suhu, kelembapan, cahaya, "Lampu UV")
    status_led_rgb = led_rgb(ultrasonic, kamera, lidar, "LED RGB")
    status_alarm = alarm(ultrasonic, kamera, lidar, "Alarm")
    lcd_monitor = lcd(ultrasonic, kamera, lidar, status_led_rgb, status_alarm)

    # Create SensorData instances and save them to the database
    SmartPlantingSensor.objects.create(name='Sensor Water Level', value=waterlevel)
    SmartPlantingSensor.objects.create(name='Sensor Nutrisi', value=nutrisi)
    SmartPlantingSensor.objects.create(name='Sensor pH', value=ph)

    SmartPlantingActuator.objects.create(name='Pompa Air', value=status_pompa_air)
    SmartPlantingActuator.objects.create(name='Dispenser Nutrisi', value=status_dispenser_nutrisi)
    SmartPlantingActuator.objects.create(name='Dispenser pH', value=status_dispenser_ph)

    EcosystemSensor.objects.create(name='Sensor Suhu', value=suhu)
    EcosystemSensor.objects.create(name='Sensor Kelembapan', value=kelembapan)
    EcosystemSensor.objects.create(name='Sensor Intensitas Cahaya', value=cahaya)

    EcosystemActuator.objects.create(name='Kipas & Ventilasi', value=status_kipas_vent)
    EcosystemActuator.objects.create(name='Water Mist Sprinkler', value=status_water_mist)
    EcosystemActuator.objects.create(name='Lampu UV', value=status_lampu_uv)

    FarmManagementSensor.objects.create(name='Sensor Ultrasonic', value=ultrasonic)
    FarmManagementSensor.objects.create(name='Sensor Kamera', value=kamera)
    FarmManagementSensor.objects.create(name='Sensor LIDAR', value=lidar)

    FarmManagementActuator.objects.create(name='LED RGB', value=status_led_rgb)
    FarmManagementActuator.objects.create(name='LCD', value=lcd_monitor)
    FarmManagementActuator.objects.create(name='Alarm', value=status_alarm)

    EcosystemActSens.objects.create(suhuvalue=suhu, kelembapanvalue=kelembapan, intensitascahayavalue=cahaya, kipasvalue=status_kipas_vent, watersprinklervalue=status_water_mist, lampuUVvalue=status_lampu_uv)
    SmartPlantingActSens.objects.create(waterlevelvalue=waterlevel, nutrisiTDSvalue=nutrisi, pHvalue=ph, pompaairvalue=status_pompa_air, nutrisivalue=status_dispenser_nutrisi, dispenservalue=status_dispenser_ph)
    FarmManagementActSens.objects.create(ultrasonicvalue=ultrasonic, kameravalue=kamera, LIDARvalue=lidar, LEDRGBvalue=status_led_rgb, LCDvalue=lcd_monitor, alarmvalue=status_alarm)

    sensor_data_ecosystem = EcosystemSensor.objects.all()
    sensor_data_smart_planting = SmartPlantingSensor.objects.all()
    sensor_data_farm_management = FarmManagementSensor.objects.all()

    actuator_data_ecosystem = EcosystemActuator.objects.all()
    actuator_data_smart_planting = SmartPlantingActuator.objects.all()
    actuator_data_farm_management = FarmManagementActuator.objects.all()


    # tsensor_data_ecosystem = sensor_data_ecosystem.order_by('-id')[:3]
    # tactuator_data_ecosystem = actuator_data_ecosystem.order_by('-id')[:3]
    # tsensor_data_smart_planting = sensor_data_smart_planting.order_by('-id')[:3]
    # tactuator_data_smart_planting = actuator_data_smart_planting.order_by('-id')[:3]
    # tsensor_data_farm_management = sensor_data_farm_management.order_by('-id')[:3]
    # tactuator_data_farm_management = actuator_data_farm_management.order_by('-id')[:3]
    

    return render(
        request, 
        'SmartFarmSystem/base.html', 
        {
            'sensor_data_ecosystem': sensor_data_ecosystem,
            'sensor_data_smart_planting': sensor_data_smart_planting,
            'sensor_data_farm_management': sensor_data_farm_management,
            'actuator_data_ecosystem': actuator_data_ecosystem,
            'actuator_data_smart_planting': actuator_data_smart_planting,
            'actuator_data_farm_management': actuator_data_farm_management,
            # 'tsensor_data_ecosystem': tsensor_data_ecosystem,
            # 'tsensor_data_smart_planting': tsensor_data_smart_planting,
            # 'tsensor_data_farm_management': tsensor_data_farm_management,
            # 'tactuator_data_ecosystem': tactuator_data_ecosystem,
            # 'tactuator_data_smart_planting': tactuator_data_smart_planting,
            # 'tactuator_data_farm_management': tactuator_data_farm_management,
        }
    )

def SmartFarmSystemInformation(request):
    return render(
        request, 
        'SmartFarmSystem/info.html', 
    )


def fetch_sensor_data(request):
    ecosystem_sensors = EcosystemSensor.objects.all().values('name', 'value', 'timestamp')
    smart_planting_sensors = SmartPlantingSensor.objects.all().values('name', 'value', 'timestamp')
    farm_management_sensors = FarmManagementSensor.objects.all().values('name', 'value', 'timestamp')
    ecosystem_actuators = EcosystemActuator.objects.all().values('name', 'value', 'timestamp')
    smart_planting_actuators = SmartPlantingActuator.objects.all().values('name', 'value', 'timestamp')
    farm_management_actuators = FarmManagementActuator.objects.all().values('name', 'value', 'timestamp')

    # Filter data based on sensor and actuator names
    sensor_data = {
        'ultrasonic': list(farm_management_sensors.filter(name='Sensor Ultrasonic')),
        'kamera': list(farm_management_sensors.filter(name='Sensor Kamera')),
        'lidar': list(farm_management_sensors.filter(name='Sensor LIDAR')),
        'waterlevel': list(smart_planting_sensors.filter(name='Sensor Water Level')),
        'nutrisi': list(smart_planting_sensors.filter(name='Sensor Nutrisi')),
        'ph': list(smart_planting_sensors.filter(name='Sensor pH')),
        'suhu': list(ecosystem_sensors.filter(name='Sensor Suhu')),
        'kelembapan': list(ecosystem_sensors.filter(name='Sensor Kelembapan')),
        'cahaya': list(ecosystem_sensors.filter(name='Sensor Intensitas Cahaya')),
        'pompa_air': list(smart_planting_actuators.filter(name='Pompa Air')),
        'dispenser_nutrisi': list(smart_planting_actuators.filter(name='Dispenser Nutrisi')),
        'dispenser_ph': list(smart_planting_actuators.filter(name='Dispenser pH')),
        'kipas_vent': list(ecosystem_actuators.filter(name='Kipas & Ventilasi')),
        'water_mist': list(ecosystem_actuators.filter(name='Water Mist Sprinkler')),
        'lampu_uv': list(ecosystem_actuators.filter(name='Lampu UV')),
        'led_rgb': list(farm_management_actuators.filter(name='LED RGB')),
        'alarm': list(farm_management_actuators.filter(name='Alarm')),
        'monitor': list(farm_management_actuators.filter(name='LCD')),
    }
    return JsonResponse(sensor_data, safe=False)


def trigger_smart_farm_loop(request):
    SmartFarmSystemLoop(request)  # Pass a dummy request or modify your view as needed
    return JsonResponse({'status': 'success'})  # Respond with a success status

def ecosystem_log(request):
    ecosystem_logs = EcosystemActSens.objects.all()  # Fetch all ecosystem logs from the database
    return render(request, 'SmartFarmSystem/ecosystemlog.html', {'ecosystem_logs': ecosystem_logs})

def smart_planting_log(request):
    smart_planting_logs = SmartPlantingActSens.objects.all()  # Fetch all smart planting logs from the database
    return render(request, 'SmartFarmSystem/smartplantinglog.html', {'smart_planting_logs': smart_planting_logs})

def farm_management_log(request):
    farm_management_logs = FarmManagementActSens.objects.all()  # Fetch all farm management logs from the database
    return render(request, 'SmartFarmSystem/farmmanagementlog.html', {'farm_management_logs': farm_management_logs})