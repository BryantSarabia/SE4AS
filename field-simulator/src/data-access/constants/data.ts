import { ActuatorType, SensorType } from "../enums";
import { ActuatorCreate, SensorCreate } from "../interfaces";

const SOIL_MOISTURE_SAMPLING_INTERVAL = 5 * 60 * 1000; // 5 minutes
const LIGHT_SAMPLING_INTERVAL = 60 * 1000; // 1 minute
const HUMIDITY_SAMPLING_INTERVAL = 5 * 60 * 1000; // 5 minutes
const TEMPERATURE_SAMPLING_INTERVAL = 5 * 60 * 1000; // 5 minutes

type Sensor = Pick<
  SensorCreate<unknown>,
  "value" | "min" | "max" | "simulationInterval"
> & { type: SensorType };

const SENSORS: Sensor[] = [
  {
    type: SensorType.SOIL_MOISTURE,
    value: 0,
    min: 0,
    max: 100,
    simulationInterval: SOIL_MOISTURE_SAMPLING_INTERVAL,
  },
  {
    type: SensorType.SOIL_MOISTURE,
    value: 0,
    min: 0,
    max: 100,
    simulationInterval: SOIL_MOISTURE_SAMPLING_INTERVAL,
  },
  {
    type: SensorType.SOIL_MOISTURE,
    value: 0,
    min: 0,
    max: 100,
    simulationInterval: SOIL_MOISTURE_SAMPLING_INTERVAL,
  },
  {
    type: SensorType.SOIL_MOISTURE,
    value: 0,
    min: 0,
    max: 100,
    simulationInterval: SOIL_MOISTURE_SAMPLING_INTERVAL,
  },
  {
    type: SensorType.SOIL_MOISTURE,
    value: 0,
    min: 0,
    max: 100,
    simulationInterval: SOIL_MOISTURE_SAMPLING_INTERVAL,
  },
  {
    type: SensorType.LIGHT,
    simulationInterval: LIGHT_SAMPLING_INTERVAL,
    value: 0,
    min: 0,
    max: 3000,
  },
  {
    type: SensorType.LIGHT,
    simulationInterval: LIGHT_SAMPLING_INTERVAL,
    value: 0,
    min: 0,
    max: 3000,
  },
  {
    type: SensorType.LIGHT,
    simulationInterval: LIGHT_SAMPLING_INTERVAL,
    value: 0,
    min: 0,
    max: 3000,
  },
  {
    type: SensorType.LIGHT,
    simulationInterval: LIGHT_SAMPLING_INTERVAL,
    value: 0,
    min: 0,
    max: 3000,
  },
  {
    type: SensorType.LIGHT,
    simulationInterval: LIGHT_SAMPLING_INTERVAL,
    value: 0,
    min: 0,
    max: 3000,
  },
  {
    type: SensorType.HUMIDITY,
    simulationInterval: HUMIDITY_SAMPLING_INTERVAL,
    value: 0,
    min: 0,
    max: 100,
  },
  {
    type: SensorType.HUMIDITY,
    simulationInterval: HUMIDITY_SAMPLING_INTERVAL,
    value: 0,
    min: 0,
    max: 100,
  },
  {
    type: SensorType.HUMIDITY,
    simulationInterval: HUMIDITY_SAMPLING_INTERVAL,
    value: 0,
    min: 0,
    max: 100,
  },
  {
    type: SensorType.HUMIDITY,
    simulationInterval: HUMIDITY_SAMPLING_INTERVAL,
    value: 0,
    min: 0,
    max: 100,
  },
  {
    type: SensorType.HUMIDITY,
    simulationInterval: HUMIDITY_SAMPLING_INTERVAL,
    value: 0,
    min: 0,
    max: 100,
  },
  {
    type: SensorType.TEMPERATURE,
    simulationInterval: TEMPERATURE_SAMPLING_INTERVAL,
    value: 0,
    min: -20,
    max: 80,
  },
  {
    type: SensorType.TEMPERATURE,
    simulationInterval: TEMPERATURE_SAMPLING_INTERVAL,
    value: 0,
    min: -20,
    max: 80,
  },
  {
    type: SensorType.TEMPERATURE,
    simulationInterval: TEMPERATURE_SAMPLING_INTERVAL,
    value: 0,
    min: -20,
    max: 80,
  },
  {
    type: SensorType.TEMPERATURE,
    simulationInterval: TEMPERATURE_SAMPLING_INTERVAL,
    value: 0,
    min: -20,
    max: 80,
  },
  {
    type: SensorType.TEMPERATURE,
    simulationInterval: TEMPERATURE_SAMPLING_INTERVAL,
    value: 0,
    min: -20,
    max: 80,
  },
];

type Actuator = Pick<ActuatorCreate<unknown>, "min" | "max" | "value"> & {
  type: ActuatorType;
};

const ACTUATORS: Actuator[] = [
  {
    type: ActuatorType.DRIP_IRRIGATION,
    min: 0,
    max: 100,
    value: 0,
  },
  {
    type: ActuatorType.DRIP_IRRIGATION,
    min: 0,
    max: 100,
    value: 0,
  },
  {
    type: ActuatorType.DRIP_IRRIGATION,
    min: 0,
    max: 100,
    value: 0,
  },
  {
    type: ActuatorType.SPRINKLER,
    min: 0,
    max: 100,
    value: 0,
  },
  {
    type: ActuatorType.SPRINKLER,
    min: 0,
    max: 100,
    value: 0,
  },
  {
    type: ActuatorType.SPRINKLER,
    min: 0,
    max: 100,
    value: 0,
  },
];

export const DATA = [
  {
    name: "Coppito",
    latitude: 42.3702262,
    longitude: 13.3267021,
    fields: [
      {
        name: "Pomodori",
        sensors: SENSORS,
        actuators: ACTUATORS,
      },
      {
        name: "Zucchine",
        sensors: SENSORS,
        actuators: ACTUATORS,
      },
      {
        name: "Peperoni",
        sensors: SENSORS,
        actuators: ACTUATORS,
      },
    ],
  },
  {
    name: "Collebrincioni",
    latitude: 42.4037844,
    longitude: 13.4275238,
    fields: [
      {
        name: "Pomodori",
        sensors: SENSORS,
        actuators: ACTUATORS,
      },
      {
        name: "Zucchine",
        sensors: SENSORS,
        actuators: ACTUATORS,
      },
      {
        name: "Peperoni",
        sensors: SENSORS,
        actuators: ACTUATORS,
      },
    ],
  },
];
