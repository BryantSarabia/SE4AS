import { ActuatorType, SensorType } from "../enums";
import { Actuator } from "./actuator.interface";
import { Sensor } from "./sensor.interface";
import { Zone } from "./zone.interface";

export interface Field {
  id: number;
  name: string;
  soil_moisture: number;
  temperature: number;
  humidity: number;
  light: number;
  sensors: Sensor<unknown>[];
  actuators: Actuator[];
  zoneId: Zone["id"];

  getSensorById(id: number): Sensor<unknown> | undefined;
  getActuatorById(id: number): Actuator | undefined;
  getSensorsByType(type: SensorType): Sensor<unknown>[];
  getActuatorsByType(type: ActuatorType): Actuator[];
  addSensor(sensor: Sensor<unknown>): void;
  addActuator(actuator: Actuator): void;
  deleteSensor(id: Sensor<unknown>["id"]): void;
  deleteActuator(id: Actuator["id"]): void;
  getTemperature(): number;
  getHumidity(): number;
  getLight(): number;
  getSoilMoisture(): number;
  setTemperature(temperature: number): void;
  setHumidity(humidity: number): void;
  setLight(light: number): void;
  setSoilMoisture(soilMoisture: number): void;
  destroy(): void;
}
