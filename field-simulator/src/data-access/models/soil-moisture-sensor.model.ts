import random from "random";
import { MeasurementUnit, SensorType } from "../enums";
import { SensorCreate } from "../interfaces";
import { BaseSensor } from "./base-sensor.model";

export class SoilMoistureSensor extends BaseSensor<number> {
  constructor(sensor: SensorCreate<number>) {
    const type = SensorType.soil_moisture_threshold;
    const unit = MeasurementUnit.soil_moisture_threshold;
    super({ ...sensor, type, unit });
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
