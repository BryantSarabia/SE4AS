import { BROKER_URL } from "@/config/config";
import { MqttClient } from "mqtt/*";
import { createMqttClient } from "../clients";
import { MeasurementUnit, SensorType } from "../enums";
import { CreateSensor, OnMqttMessage, Sensor } from "../interfaces";
import { Logger } from "./logger.model";

export abstract class BaseSensor<T> implements Sensor<T> {
  id: number;
  type: SensorType;
  value: T;
  min: number;
  max: number;
  unit: MeasurementUnit;
  zoneId: number;
  fieldId: number;
  topic: string;
  activationTopic: string;
  deactivationTopic: string;
  publishTopic: string;
  simulationInterval: number;
  mqttClient!: MqttClient;
  intervalId: NodeJS.Timeout | null = null;
  logger: Logger;

  constructor({
    id,
    type,
    value,
    min,
    max,
    unit,
    zoneId,
    fieldId,
    simulationInterval,
    logger,
  }: CreateSensor<T>) {
    this.id = id;
    this.type = type;
    this.value = value;
    this.min = min;
    this.max = max;
    this.unit = unit;
    this.zoneId = zoneId;
    this.fieldId = fieldId;
    this.simulationInterval = simulationInterval;
    this.logger = logger;
    this.topic = `zone/${zoneId}/field/${fieldId}/sensor/${id}/${type}`;
    this.publishTopic = this.topic;
    this.activationTopic = `${this.topic}/activate`;
    this.deactivationTopic = `${this.topic}/deactivate`;
    this.connectToMqtt();
  }

  abstract generateValue(): T;

  initialize(): void {
    this.mqttClient.subscribe(this.deactivationTopic);
    this.mqttClient.on("message", this.deactivate.bind(this));
    this.mqttClient.publish(this.activationTopic, "");
    this.simulate();
  }

  connectToMqtt(): void {
    try {
      this.mqttClient = createMqttClient({ brokerUrl: BROKER_URL });
    } catch (error) {
      this.logger.error(`Error connecting to MQTT broker: ${error}`);
    }
  }

  simulate(): void {
    this.intervalId = setInterval(() => {
      this.updateValue(this.generateValue());
      this.send();
    }, this.simulationInterval);
  }

  updateValue(value: T): void {
    this.value = value;
  }

  send(): void {
    try {
      const value = this.getValue();
      const data = JSON.stringify({ value });
      this.logger.info(
        `Sensor ${this.id} with type ${this.type} sending value: ${value}`,
      );
      this.mqttClient.publish(this.publishTopic, data); // zone/:zoneId/field/:fieldId/sensor/:sensorId/:sensorType
    } catch (error) {
      this.logger.error(
        `Error sending data from sensor ${this.id} with type ${this.type}: ${error}`,
      );
    }
  }

  activate(): void {
    this.mqttClient.publish(this.activationTopic, "");
  }

  deactivate(): OnMqttMessage {
    return (topic) => {
      if (!topic || !(topic === this.deactivationTopic)) return;
      this.destroy();
    };
  }

  destroy(): void {
    if (this.intervalId) clearInterval(this.intervalId);
    this.mqttClient.unsubscribe(this.deactivationTopic);
    this.mqttClient.end();
  }

  getData(): Pick<Sensor<T>, "id" | "value" | "unit" | "zoneId" | "fieldId"> {
    const { id, value, unit, zoneId, fieldId } = this;
    return { id, value, unit, zoneId, fieldId };
  }

  getValue(): T {
    return this.value;
  }
}
