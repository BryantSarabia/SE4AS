import random from "random";
import { MeasurementUnit, SensorType } from "../enums";
import { CreateSensor } from "../interfaces";
import { BaseSensor } from "./base-sensor.model";

export class SoilMoistureSensor extends BaseSensor<number> {
  constructor(sensor: CreateSensor<number>) {
    const type = SensorType.SOIL_MOISTURE;
    const unit = MeasurementUnit.SOIL_MOISTURE;
    const simulationInterval = 1 * 60 * 1000; // 1 minute
    super({ ...sensor, type, unit, simulationInterval });
  }

  generateValue(): number {
    const probability = 50;
    const randomProbability = random.int(0, 100);
    if (randomProbability > probability) {
      const by = random.int(1, 5);
      const shouldIncrease = random.boolean();
      this.value = shouldIncrease
        ? Math.min(this.value + by, this.max)
        : Math.max(this.value - by, 0);
    }
    return this.value;
  }
}
