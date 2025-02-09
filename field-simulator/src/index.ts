import { DATA } from "./data-access/constants";
import { ActuatorFactory, SensorFactory } from "./data-access/factory";
import { Field, Logger, Zone } from "./data-access/models";

let id = 0;
export const createId = () => id++;
const logger = new Logger();

function initApp() {
  for (const zone of DATA) {
    const zoneObj = new Zone({
      ...zone,
      id: createId(),
    });
    for (const field of zone.fields) {
      const fieldObj = new Field({
        ...field,
        id: createId(),
        zoneId: zoneObj.id,
      });
      for (const sensor of field.sensors) {
        const sensorObj = SensorFactory.create({
          ...sensor,
          id: createId(),
          fieldId: fieldObj.id,
          zoneId: zoneObj.id,
          logger,
        });
        fieldObj.addSensor(sensorObj);
      }
      for (const actuator of field.actuators) {
        const actuatorObj = ActuatorFactory.create({
          ...actuator,
          id: createId(),
          fieldId: fieldObj.id,
          zoneId: zoneObj.id,
          logger,
        });
        fieldObj.addActuator(actuatorObj);
      }
    }
  }
}

initApp();
