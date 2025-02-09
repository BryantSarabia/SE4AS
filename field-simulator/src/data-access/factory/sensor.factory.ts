/* eslint-disable @typescript-eslint/no-explicit-any */
import { SensorType } from "../enums";
import { SensorCreate } from "../interfaces";
import {
  HumiditySensor,
  LightSensor,
  SoilMoistureSensor,
  TemperatureSensor,
} from "../models";

export class SensorFactory {
  static sensors = {
    [SensorType.TEMPERATURE]: TemperatureSensor,
    [SensorType.HUMIDITY]: HumiditySensor,
    [SensorType.LIGHT]: LightSensor,
    [SensorType.SOIL_MOISTURE]: SoilMoistureSensor,
  };

  static create({
    type,
    min,
    max,
    id,
    fieldId,
    zoneId,
    logger,
    value,
    simulationInterval,
  }: SensorCreate<any> & { type: SensorType }) {
    const Sensor = SensorFactory.sensors[type];
    if (!Sensor) {
      throw new Error(`Sensor type ${type} not found`);
    }
    return new Sensor({
      min,
      max,
      id,
      fieldId,
      zoneId,
      logger,
      value,
      simulationInterval,
    });
  }
}
