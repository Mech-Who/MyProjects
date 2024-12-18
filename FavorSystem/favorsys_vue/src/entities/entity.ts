export class People {
  id: number;
  name: string;
  birthday: string;
  gender: number;
  favor: number;
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
  }
}
