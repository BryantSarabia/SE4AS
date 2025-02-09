import { ActuatorType } from "../enums";
import { ActuatorCreate } from "../interfaces";
import { BaseActuator } from "./base-actuator.model";

export class DripIrrigation extends BaseActuator<number> {
  constructor(actuator: ActuatorCreate<number>) {
    const type = ActuatorType.DRIP_IRRIGATION;
    super({ ...actuator, type });
  }

  setValue(value: number): void {
    this.value = Math.min(Math.max(value, this.min), this.max);
  }
}
