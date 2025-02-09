import { MqttClient } from "mqtt/*";
import { ActuatorType } from "../../data-access/enums";
import { Field } from "./field.interface";
import { Logger } from "./logger.interface";
import { Zone } from "./zone.interface";

export interface Actuator<T = unknown> {
  id: number;
  type: ActuatorType;
  min: number;
  max: number;
  value: T;
  zoneId: Zone["id"];
  fieldId: Field["id"];
  activationTopic: string;
  deactivationTopic: string;
  mqttClient: MqttClient;
  logger: Logger;

  initialize(): void;
  getValue(): T;
  setValue(value: T): void;
  activate(): void;
  deactivate(): void;
  destroy(): void;
}

export type ActuatorCreate<T> = Pick<
  Actuator<T>,
  "id" | "min" | "max" | "zoneId" | "fieldId" | "value" | "logger"
>;
