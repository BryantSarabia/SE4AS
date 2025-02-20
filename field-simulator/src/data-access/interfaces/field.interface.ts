import { ActuatorType, SensorType } from "../enums";
import { Actuator } from "./actuator.interface";
import { Sensor } from "./sensor.interface";
import { Zone } from "./zone.interface";

export interface Field {
  id: number;
  name: string;
  soil_moisture_threshold: number;
  temperature: number;
  humidity: number;
  light: number;
  sensors: Sensor[];
  actuators: Actuator[];
  zoneId: Zone["id"];

  getSensorById(id: number): Sensor | undefined;
  getActuatorById(id: number): Actuator | undefined;
  getSensorsByType(type: SensorType): Sensor[];
  getActuatorsByType(type: ActuatorType): Actuator[];
  addSensor(sensor: Sensor): void;
  addActuator(actuator: Actuator): void;
  deleteSensor(id: Sensor["id"]): void;
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

export type FieldCreate = Pick<Field, "id" | "name" | "zoneId">;
