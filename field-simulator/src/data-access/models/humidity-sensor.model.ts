import random from "random";
import { MeasurementUnit, SensorType } from "../enums";
import { SensorCreate } from "../interfaces";
import { BaseSensor } from "./base-sensor.model";

export class HumiditySensor extends BaseSensor<number> {
  constructor(sensor: SensorCreate<number>) {
    const type = SensorType.LIGHT;
    const unit = MeasurementUnit.LIGHT;
    super({ ...sensor, type, unit });
  }

  generateValue(): number {
    const probability = 50;
    const randomProbability = random.int(0, 100);
    if (randomProbability > probability) {
      const by = random.int(-5, 5);
      this.value += by;
    }
    return this.value;
  }
}
