import { MqttClient } from "mqtt/*";
import { MeasurementUnit, SensorType } from "../enums";
import { Logger } from "../models";
import { Field } from "./field.interface";
import { OnMqttMessage } from "./mqtt.interface";
import { Zone } from "./zone.interface";

export interface Sensor<T> {
  id: number;
  type: SensorType;
  value: T;
  min: number;
  max: number;
  unit: MeasurementUnit;

  mqttClient: MqttClient;

  zoneId: Zone["id"];
  fieldId: Field["id"];

  topic: string;
  publishTopic: string;
  activationTopic: string;
  deactivationTopic: string;

  simulationInterval: number;
  intervalId: NodeJS.Timeout | null;
  logger: Logger;

  initialize(): void;
  send(): void;
  activate(): void;
  deactivate(): OnMqttMessage;
  destroy(): void;
  getData(): Pick<
    Sensor<unknown>,
    "id" | "value" | "unit" | "zoneId" | "fieldId"
  >;
  getValue(): T;
  generateValue(): T;
  updateValue(value: T): void;
  simulate(): void;
  connectToMqtt(): void;
}

export type CreateSensor<T> = Omit<
  Sensor<T>,
  "topic" | "publishTopic" | "activationTopic" | "deactivationTopic"
>;
