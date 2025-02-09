import { ActuatorType } from "@/data-access/enums";
import { Field } from "./field.interface";
import { Zone } from "./zone.interface";

export interface Actuator {
  id: number;
  type: ActuatorType;
  min: number;
  max: number;
  sendTopic: string;
  zoneId: Zone["id"];
  fieldId: Field["id"];
  activationTopic: string;
  deactivationTopic: string;

  destroy(): void;
}
