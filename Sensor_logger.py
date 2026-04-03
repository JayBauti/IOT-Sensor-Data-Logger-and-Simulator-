import random
from datetime import datetime

class SensorReading:
    def __init__(self, sensor_id, temperature, humidity, timestamp=None):
        self.sensor_id = sensor_id
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return (f"[{self.timestamp}] Sensor {self.sensor_id} | "
                f"Temp: {self.temperature:.1f}°C | Humidity: {self.humidity:.1f}%")

    def __repr__(self):
        return (f"SensorReading(sensor_id={self.sensor_id!r}, "
                f"temperature={self.temperature}, humidity={self.humidity}, "
                f"timestamp={self.timestamp!r})")

    def __eq__(self, other):
        if not isinstance(other, SensorReading):
            return False
        return self.sensor_id == other.sensor_id and self.timestamp == other.timestamp


class SensorLogger:
    # Cold chain thresholds — dairy transport
    TEMP_MIN = 2.0
    TEMP_MAX = 8.0
    HUMIDITY_MIN = 40.0
    HUMIDITY_MAX = 80.0

    def __init__(self, log_file="sensor_log.txt"):
        self.log_file = log_file
        self.readings = []
        self.alerts = []

    def __len__(self):
        return len(self.readings)

    def __iter__(self):
        return iter(self.readings)

    def __str__(self):
        return f"SensorLogger | {len(self)} readings | File: {self.log_file}"

    def __repr__(self):
        return f"SensorLogger(log_file={self.log_file!r}, readings={len(self)})"

    def add_reading(self, reading):
        self.readings.append(reading)
        anomaly = self._check_anomaly(reading)
        if anomaly:
            self.alerts.append((reading, anomaly))
            print(f"  ⚠️  ALERT: {anomaly}")

    def _check_anomaly(self, reading):
        issues = []
        if reading.temperature < self.TEMP_MIN:
            issues.append(f"Temp TOO LOW ({reading.temperature:.1f}°C < {self.TEMP_MIN}°C)")
        elif reading.temperature > self.TEMP_MAX:
            issues.append(f"Temp TOO HIGH ({reading.temperature:.1f}°C > {self.TEMP_MAX}°C)")
        if reading.humidity < self.HUMIDITY_MIN:
            issues.append(f"Humidity TOO LOW ({reading.humidity:.1f}% < {self.HUMIDITY_MIN}%)")
        elif reading.humidity > self.HUMIDITY_MAX:
            issues.append(f"Humidity TOO HIGH ({reading.humidity:.1f}% > {self.HUMIDITY_MAX}%)")
        return " | ".join(issues) if issues else None

    def save_to_file(self):
        with open(self.log_file, "w") as f:
            for reading in self.readings:
                f.write(f"{reading.timestamp},{reading.sensor_id},"
                        f"{reading.temperature:.2f},{reading.humidity:.2f}\n")
        print(f"\n✅ Saved {len(self)} readings to '{self.log_file}'")

    def load_from_file(self):
        self.readings = []
        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    timestamp = parts[0]
                    sensor_id = parts[1]
                    temperature = float(parts[2])
                    humidity = float(parts[3])
                    self.readings.append(
                        SensorReading(sensor_id, temperature, humidity, timestamp)
                    )
            print(f"📂 Loaded {len(self)} readings from '{self.log_file}'")
        except FileNotFoundError:
            print(f"❌ File '{self.log_file}' not found.")

    def above_threshold(self, temp_threshold):
        return [r for r in self.readings if r.temperature > temp_threshold]

    def summary(self):
        if not self.readings:
            print("No readings available.")
            return
        temps = [r.temperature for r in self.readings]
        humidities = [r.humidity for r in self.readings]
        print("\n📊 --- Summary ---")
        print(f"  Total readings : {len(self)}")
        print(f"  Temp  — Min: {min(temps):.1f}°C | Max: {max(temps):.1f}°C | "
              f"Avg: {sum(temps)/len(temps):.1f}°C")
        print(f"  Humid — Min: {min(humidities):.1f}% | Max: {max(humidities):.1f}% | "
              f"Avg: {sum(humidities)/len(humidities):.1f}%")
        print(f"  Alerts generated: {len(self.alerts)}")


def simulate_esp32_data(sensor_id, num_readings=10):
    readings = []
    for _ in range(num_readings):
        if random.random() < 0.15:       # 15% chance of anomaly
            temp = round(random.uniform(0.0, 15.0), 2)
        else:
            temp = round(random.uniform(2.5, 7.5), 2)
        humidity = round(random.uniform(35.0, 85.0), 2)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        readings.append(SensorReading(sensor_id, temp, humidity, timestamp))
    return readings


if __name__ == "__main__":
    print("=== IoT Cold Chain Sensor Logger ===\n")

    logger = SensorLogger(log_file="cold_chain_log.txt")

    sensors = ["ESP32-01", "ESP32-02"]
    for sensor_id in sensors:
        print(f"📡 Simulating {sensor_id}...")
        readings = simulate_esp32_data(sensor_id, num_readings=8)
        for reading in readings:
            print(f"  {reading}")
            logger.add_reading(reading)
        print()

    logger.summary()
    logger.save_to_file()

    print("\n🔄 Loading from file...")
    logger2 = SensorLogger(log_file="cold_chain_log.txt")
    logger2.load_from_file()

    high_temp = logger2.above_threshold(7.0)
    print(f"\n🌡️  Readings above 7.0°C: {len(high_temp)}")
    for r in high_temp:
        print(f"  {r}")

    print(f"\n🔍 Logger repr: {repr(logger)}")
