import {
  Actuator,
  FieldCreate,
  Field as FieldInterface,
  Sensor,
} from "../../data-access/interfaces";
import { ActuatorType, SensorType } from "../enums";

export class Field implements FieldInterface {
  id: number;
  name: string;
  soil_moisture: number = 0;
  temperature: number = 0;
  humidity: number = 0;
  light: number = 0;
  sensors: Sensor[] = [];
  actuators: Actuator[] = [];
  zoneId: number;

  constructor({ id, name, zoneId }: FieldCreate) {
    this.id = id;
    this.name = name;
    this.zoneId = zoneId;
  }

  getSensorById(id: number): Sensor | undefined {
    return this.sensors.find((sensor) => sensor.id === id);
  }

  getActuatorById(id: number): Actuator | undefined {
    return this.actuators.find((actuator) => actuator.id === id);
  }

  getSensorsByType(type: SensorType): Sensor[] {
    return this.sensors.filter((sensor) => sensor.type === type);
  }

  getActuatorsByType(type: ActuatorType): Actuator[] {
    return this.actuators.filter((actuator) => actuator.type === type);
  }

  addSensor(sensor: Sensor): void {
    this.sensors = [...this.sensors, sensor];
  }

  addActuator(actuator: Actuator): void {
    this.actuators = [...this.actuators, actuator];
  }

  deleteSensor(id: Sensor["id"]): void {
    const index = this.sensors.findIndex((sensor) => sensor.id === id);
    const sensorToDelete = this.sensors[index];
    sensorToDelete.destroy();
    this.sensors = [
      ...this.sensors.slice(0, index),
      ...this.sensors.slice(index + 1),
    ];
  }

  deleteActuator(id: Actuator["id"]): void {
    const index = this.actuators.findIndex((actuator) => actuator.id === id);
    const actuatorToDelete = this.actuators[index];
    actuatorToDelete.destroy();
    this.actuators = [
      ...this.actuators.slice(0, index),
      ...this.actuators.slice(index + 1),
    ];
  }

  getTemperature(): number {
    const temperatureSensors = this.getSensorsByType(SensorType.TEMPERATURE);
    const totalTemperature = temperatureSensors.reduce(
      (acc, sensor) => acc + (sensor.getValue() as number),
      0
    );
    return totalTemperature / Math.max(1, temperatureSensors.length);
  }

  getHumidity(): number {
    const humiditySensors = this.getSensorsByType(SensorType.HUMIDITY);
    const totalHumidity = humiditySensors.reduce(
      (acc, sensor) => acc + (sensor.getValue() as number),
      0
    );
    return totalHumidity / Math.max(1, humiditySensors.length);
  }

  getLight(): number {
    const lightSensors = this.getSensorsByType(SensorType.LIGHT);
    const totalLight = lightSensors.reduce(
      (acc, sensor) => acc + (sensor.getValue() as number),
      0
    );
    return totalLight / Math.max(1, lightSensors.length);
  }

  getSoilMoisture(): number {
    const soilMoistureSensors = this.getSensorsByType(SensorType.SOIL_MOISTURE);
    const totalSoilMoisture = soilMoistureSensors.reduce(
      (acc, sensor) => acc + (sensor.getValue() as number),
      0
    );
    return totalSoilMoisture / Math.max(1, soilMoistureSensors.length);
  }

  setTemperature(temperature: number): void {
    this.temperature = temperature;
  }

  setHumidity(humidity: number): void {
    this.humidity = humidity;
  }

  setLight(light: number): void {
    this.light = light;
  }

  setSoilMoisture(soilMoisture: number): void {
    this.soil_moisture = soilMoisture;
  }

  destroy(): void {
    this.sensors.forEach((sensor) => sensor.destroy());
    this.actuators.forEach((actuator) => actuator.destroy());
  }
}
