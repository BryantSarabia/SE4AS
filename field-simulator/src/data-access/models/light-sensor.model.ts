import random from "random";
import { MeasurementUnit, SensorType } from "../enums";
import { CreateSensor } from "../interfaces";
import { BaseSensor } from "./base-sensor.model";

export class LightSensor extends BaseSensor<number> {
  constructor(sensor: CreateSensor<number>) {
    const type = SensorType.LIGHT;
    const unit = MeasurementUnit.LIGHT;
    const simulationInterval = 30 * 1000; // 30 seconds
    super({ ...sensor, type, unit, simulationInterval });
  }

  generateValue(): number {
    const probability = 50;
    const randomProbability = random.int(0, 100);
    if (randomProbability > probability) {
      const by = random.int(-10, 10);
      this.value += by;
    }
    return this.value;
  }
}
