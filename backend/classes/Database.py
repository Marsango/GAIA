import sqlite3
import os
from typing import Any
from datetime import datetime
from backend.classes.Person import Person
from backend.classes.Address import Address
from backend.classes.Company import Company
from backend.classes.utils import *


class Database:
    def __init__(self) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'soil_analysis.db')
        self.__con = sqlite3.connect(db_path)
        self.__con.row_factory = sqlite3.Row
        self.__cur = self.__con.cursor()
        self.__cur.execute("""PRAGMA foreign_keys = ON;""")
        self.__con.commit()
        self.create_database()

    def create_database(self):
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS requester(
        requester_id integer primary key, phone_number varchar(15), email varchar(255), fk_address_id integer,
        FOREIGN KEY(fk_address_id) REFERENCES address(address_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS country(
        country_id integer primary key, country_name varchar(255))""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS state(
                state_id integer primary key, state_name varchar(255), fk_country_id integer,
                 FOREIGN KEY(fk_country_id) REFERENCES country(country_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS city(
                city_id integer primary key, city_name varchar(255), fk_state_id integer,
                FOREIGN KEY(fk_state_id) REFERENCES state(state_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS street(
                street_id integer primary key, street_name varchar(255), fk_city_id integer,
                FOREIGN KEY(fk_city_id) REFERENCES city(city_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS address(
        cep varchar(10), address_id integer primary key, fk_country_id integer, fk_state_id integer, fk_city_id integer,
        fk_street_id integer, address_number integer,
        FOREIGN KEY(fk_country_id) REFERENCES country(country_id) ON DELETE CASCADE,
        FOREIGN KEY(fk_state_id) REFERENCES state(state_id) ON DELETE CASCADE,
        FOREIGN KEY(fk_city_id) REFERENCES city(city_id) ON DELETE CASCADE,
        FOREIGN KEY(fk_street_id) REFERENCES street(street_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS person(
        name varchar(255), birth_date date, fk_requester_id integer,
        FOREIGN KEY(fk_requester_id) REFERENCES requester(requester_id) ON DELETE CASCADE)""")
        self.__con.commit()

    def insert_person(self, person: Person, address: Address) -> None:
        address_id = self.insert_address(address)
        requester_id = self.insert_requester(person, address_id)
        person_dict = to_dict(person)
        person_dict['requester_id'] = requester_id
        self.__cur.execute("""INSERT INTO person(name, birth_date, fk_requester_id)
        VALUES(:name, :birth_date, :requester_id)""", person_dict)
        self.__con.commit()

    def insert_requester(self, requester: Person | Company, address_id: int) -> int:
        requester_dict: dict[str, Any] = to_dict(requester)
        requester_dict['address_id'] = address_id
        self.__cur.execute("""INSERT INTO requester(phone_number, email, fk_address_id)
        VALUES(:phone_number, :email, :address_id)""", requester_dict)
        self.__con.commit()
        return self.__cur.lastrowid

    def insert_address(self, address: Address) -> int:
        address: dict = to_dict(address)
        previous_attribute: str = ''
        previous_attribute_id: int = 0
        for attribute in address.keys():
            if attribute == 'cep' or attribute == 'address_number':
                continue
            address[attribute] = self.insert_address_components(attribute, address[attribute],
                                                                  previous_attribute, previous_attribute_id)
            previous_attribute = attribute
            previous_attribute_id: int = address[attribute]
        self.__cur.execute("""INSERT INTO address(cep, address_number, fk_country_id,
         fk_state_id, fk_city_id, fk_street_id)
         VALUES(:cep, :address_number, :country, :state, :city, :street)""", address)
        self.__con.commit()
        return self.__cur.lastrowid


    def insert_address_components(self, table: str, row_name: str,
                                  previous_attribute: str, previous_attribute_id: int) -> int:
        self.__cur.execute(f"""SELECT {table}_id FROM {table}
        WHERE lower({table}_name) = lower(?)""", (row_name, ))
        matches: list[sqlite3.Row] = self.__cur.fetchall()
        if not matches:
            if previous_attribute == '':
                self.__cur.execute(f"""INSERT INTO {table}({table}_name)
                VALUES(?)""", (row_name, ))
                return self.__cur.lastrowid
            self.__cur.execute(f"""INSERT INTO {table}({table}_name, fk_{previous_attribute}_id)
            VALUES(?, ?)""", (row_name, previous_attribute_id))
            return self.__cur.lastrowid
        self.__con.commit()
        return matches[0][f'{table}_id']

    def close_connection(self):
        self.__cur.close()
        self.__con.close()

    def select_person(self):
        self.__cur.execute("""SELECT * FROM person""")
        return self.__cur.fetchall()

if __name__ == '__main__':
    db = Database()
    address = Address('oi', 'oi', 'oi', 'oi', 'oi', 12)
    person = Person('99999999', 'oiiiiiii', 'oiii', datetime(2024, 10,
                                                             12).date(),
                    'oi', address)
    db.insert_person(person, address)
    print(len(db.select_person()))
    db.close_connection()

