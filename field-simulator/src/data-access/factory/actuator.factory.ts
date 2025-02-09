/* eslint-disable @typescript-eslint/no-explicit-any */
import { ActuatorType } from "../enums";
import { ActuatorCreate } from "../interfaces";
import { DripIrrigation, Sprinkler } from "../models";

export class ActuatorFactory {
  static actuators = {
    [ActuatorType.DRIP_IRRIGATION]: DripIrrigation,
    [ActuatorType.SPRINKLER]: Sprinkler,
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
  }: ActuatorCreate<any> & { type: ActuatorType }) {
    const Actuator = ActuatorFactory.actuators[type];
    if (!Actuator) {
      throw new Error(`Actuator type ${type} not found`);
    }
    return new Actuator({
      min,
      max,
      id,
      fieldId,
      zoneId,
      logger,
      value,
    });
  }
}
