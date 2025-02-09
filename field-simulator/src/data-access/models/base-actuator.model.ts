import { MqttClient } from "mqtt/*";
import { BROKER_URL } from "../../config";
import { createMqttClient } from "../clients";
import { ActuatorType } from "../enums";
import { Actuator, ActuatorCreate, Logger, OnMqttMessage } from "../interfaces";

export abstract class BaseActuator<T> implements Actuator<T> {
  id: number;
  type: ActuatorType;
  min: number;
  max: number;
  value: T;
  zoneId: number;
  fieldId: number;
  activationTopic: string;
  deactivationTopic: string;
  mqttClient!: MqttClient;
  logger: Logger;

  constructor({
    id,
    type,
    min,
    max,
    value,
    zoneId,
    fieldId,
    logger,
  }: ActuatorCreate<T> & { type: ActuatorType }) {
    this.id = id;
    this.type = type;
    this.min = min;
    this.max = max;
    this.value = value;
    this.zoneId = zoneId;
    this.fieldId = fieldId;
    this.logger = logger;
    const topic = `zone/${zoneId}/field/${fieldId}/actuator/${id}/${type}`;
    this.activationTopic = `${topic}/activate`;
    this.deactivationTopic = `${topic}/deactivate`;
    this.initialize();
  }

  initialize(): void {
    this.connectToMqtt();
    if (this.mqttClient.connected) {
      this.mqttClient.subscribe(this.deactivationTopic);
      this.mqttClient.on("message", this.deactivate.bind(this));
      this.mqttClient.publish(this.activationTopic, "");
    }
  }

  connectToMqtt(): void {
    try {
      this.mqttClient = createMqttClient({ brokerUrl: BROKER_URL });
    } catch (error) {
      this.logger.error(`Error connecting to MQTT broker: ${error}`);
    }
  }

  getValue(): T {
    return this.value;
  }

  abstract setValue(value: T): void;

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
    this.mqttClient.unsubscribe(this.deactivationTopic);
    this.mqttClient.end();
  }
}
