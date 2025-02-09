import { Field } from "./field.interface";

export interface Zone {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  fields: Field[];

  getFields(): Field[];
  addField(field: Field): void;
  removeField(id: Field["id"]): void;
  getFieldById(id: Field["id"]): Field | undefined;
}

export type ZoneCreate = Pick<Zone, "id" | "name" | "latitude" | "longitude">;
