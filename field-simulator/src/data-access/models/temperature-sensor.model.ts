import random from "random";
import { MeasurementUnit, SensorType } from "../enums";
import { CreateSensor } from "../interfaces";
import { BaseSensor } from "./base-sensor.model";

export class TemperatureSensor extends BaseSensor<number> {
  constructor(sensor: CreateSensor<number>) {
    const type = SensorType.TEMPERATURE;
    const unit = MeasurementUnit.TEMPERATURE;
    const simulationInterval = 5 * 60 * 1000; // 5 minutes
    super({ ...sensor, type, unit, simulationInterval });
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
