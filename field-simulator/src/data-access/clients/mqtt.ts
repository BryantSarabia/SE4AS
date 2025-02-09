import { connect } from "mqtt";

interface MqttOptions {
  brokerUrl: string;
}

export const createMqttClient = ({ brokerUrl }: MqttOptions) => {
  return connect(brokerUrl);
};
