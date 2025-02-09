import random from "random";
import { MeasurementUnit, SensorType } from "../enums";
import { SensorCreate } from "../interfaces";
import { BaseSensor } from "./base-sensor.model";

export class TemperatureSensor extends BaseSensor<number> {
  constructor(sensor: SensorCreate<number>) {
    const type = SensorType.TEMPERATURE;
    const unit = MeasurementUnit.TEMPERATURE;
    super({ ...sensor, type, unit });
  }

  generateValue(): number {
    const probability = 50;
    const randomProbability = random.int(0, 100);
    if (randomProbability > probability) {
      const by = random.float(-1, 1);
      this.value += by;
    }
    return this.value;
  }
}
