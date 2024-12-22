export class People {
  id: number;
  name: string;
  birthday: string;
  gender: number;
  favor: number;
  latestEvent: Event[];
  constructor(
    id: number,
    name: string,
    birthday: string,
    gender: number,
    favor: number
  ) {
    this.id = id;
    this.name = name;
    this.birthday = birthday;
    this.gender = gender;
    this.favor = favor;
    this.latestEvent = [];
  }
}

export class Event {
  id: number;
  ownerId: number;
  title: string;
  description: string;
  eventDate: Date;
  constructor(
    id: number,
    ownerId: number,
    title: string,
    description: string,
    eventDate: string
  ) {
    this.id = id;
    this.ownerId = ownerId;
    this.title = title;
    this.description = description;
    this.eventDate = new Date(eventDate); // yyyy-MM-dd
  }
}
