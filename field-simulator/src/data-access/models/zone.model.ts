import { Field, Zone as ZoneInterface } from "@/data-access/interfaces";

export class Zone implements ZoneInterface {
  id: number;
  name: string;
  fields: Field[] = [];

  constructor({ id, name }: ZoneInterface) {
    this.id = id;
    this.name = name;
  }

  getFields(): Field[] {
    return this.fields;
  }

  addField(field: Field): void {
    this.fields = [...this.fields, field];
  }
  removeField(id: Field["id"]): void {
    const index = this.fields.findIndex((field) => field.id === id);
    if (index === -1) {
      return;
    }
    const fieldToRemove = this.fields[index];
    fieldToRemove.destroy();
    this.fields = [
      ...this.fields.slice(0, index),
      ...this.fields.slice(index + 1),
    ];
  }
  getFieldById(id: Field["id"]): Field | undefined {
    return this.fields.find((field) => field.id === id);
  }
}
