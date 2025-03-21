import sqlite3
import os
from backend.classes.Sample import Sample
from backend.classes.Report import Report
from backend.classes.Person import Person
from backend.classes.Address import Address
from backend.classes.Company import Company
from backend.classes.exceptions import CNPJAlreadyExistsError
from backend.classes.utils import *
from backend.classes.Property import Property


class Database:
    def __init__(self) -> None:
        base_dir: str = os.path.dirname(os.path.abspath(__file__))
        db_path: str = os.path.join(base_dir, 'soil_analysis.db')
        self.__con: sqlite3.Connection = sqlite3.connect(db_path)
        self.__con.row_factory = sqlite3.Row
        self.__cur: sqlite3.Cursor = self.__con.cursor()
        self.__cur.execute("""PRAGMA foreign_keys = ON;""")
        self.__con.commit()
        self.create_database()

    def create_database(self) -> None:
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS requester(
        requester_id integer primary key, phone_number varchar(15), email varchar(255), fk_address_id integer,
        FOREIGN KEY(fk_address_id) REFERENCES address(address_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS country(
        country_id integer primary key, country_name varchar(255) UNIQUE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS state(
                state_id integer primary key, state_name varchar(255), fk_country_id integer,
                UNIQUE(state_name, fk_country_id),
                 FOREIGN KEY(fk_country_id) REFERENCES country(country_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS city(
                city_id integer primary key, city_name varchar(255), fk_state_id integer,
                UNIQUE(city_name, fk_state_id),
                FOREIGN KEY(fk_state_id) REFERENCES state(state_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS street(
                street_id integer primary key, street_name varchar(255), fk_city_id integer,
                UNIQUE(street_name, fk_city_id),
                FOREIGN KEY(fk_city_id) REFERENCES city(city_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS address(
        cep varchar(10), address_id integer primary key, fk_country_id integer, fk_state_id integer, fk_city_id integer,
        fk_street_id integer, address_number varchar(10),
        FOREIGN KEY(fk_country_id) REFERENCES country(country_id) ON DELETE CASCADE,
        FOREIGN KEY(fk_state_id) REFERENCES state(state_id) ON DELETE CASCADE,
        FOREIGN KEY(fk_city_id) REFERENCES city(city_id) ON DELETE CASCADE,
        FOREIGN KEY(fk_street_id) REFERENCES street(street_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS person(
        id INTEGER PRIMARY KEY,
        name varchar(255), birth_date varchar(20), cpf varchar(15) UNIQUE, email VARCHAR(255),
        phone_number VARCHAR(15), fk_requester_id integer,
        FOREIGN KEY(fk_requester_id) REFERENCES requester(requester_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS company(
        id INTEGER PRIMARY KEY,
        company_name varchar(255), cnpj varchar(20) UNIQUE, fk_requester_id integer,
        FOREIGN KEY(fk_requester_id) REFERENCES requester(requester_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS property(
        id INTEGER PRIMARY KEY, property_name varchar(255), location varchar(255), registration_number integer, fk_city_id integer, fk_requester_id integer,
        FOREIGN KEY (fk_city_id) REFERENCES city(city_id) ON DELETE CASCADE,
        FOREIGN KEY (fk_requester_id) REFERENCES requester(requester_id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS sample(
        id INTEGER PRIMARY KEY, description varchar(255), sample_number integer, collection_date varchar(20), total_area float,
        latitude float, smp float, longitude float, depth float, phosphorus float, potassium float, organic_matter float, ph float,
         aluminum float, h_al float, calcium float, magnesium float, copper float, iron float, manganese float, 
         zinc float, base_sum float, clay float, silte float, classification string, sand float, ctc float, v_percent float, aluminum_saturation float,
        effective_ctc float, used_config, fk_property_id, FOREIGN KEY (fk_property_id) REFERENCES property(id) ON DELETE CASCADE)""")
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS report(id INTEGER PRIMARY KEY, file_location varchar(255), agreement varchar(255), fk_sample_id integer,
        FOREIGN KEY (fk_sample_id) REFERENCES sample(id) ON DELETE CASCADE)""")
        self.__con.commit()

    def insert_person(self, person: Person, address: Address) -> None:
        address_id: int = self.insert_address(address)
        requester_id: int = self.insert_requester(person, address_id)
        person_dict: dict[str, Any] = to_dict(person)
        person_dict['requester_id'] = requester_id
        try:
            self.__cur.execute("""INSERT INTO person(name, birth_date, cpf, fk_requester_id)
            VALUES(:name, :birth_date, :cpf, :requester_id)""", person_dict)
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed: person.cpf' in str(e):
                raise CPFAlreadyExistsError(person_dict['cpf'])
        self.__con.commit()

    def edit_person(self, person: Person, address: Address, id: int, requester_id: int) -> None:
        person_dict: dict[str, Any] = to_dict(person)
        person_dict['id'] = id
        self.edit_address(address, id, person)
        self.edit_requester(person, requester_id)
        self.__cur.execute("""
            UPDATE person
            SET name = :name, birth_date = :birth_date, cpf = :cpf, email = :email, phone_number = :phone_number
            WHERE id = :id
        """, person_dict)
        self.__con.commit()

    def edit_property(self, property: Property, property_id: int) -> None:
        property_dict: dict[str, Any] = to_dict(property)
        property_dict['id'] = property_id
        property_dict['city_id'] = self.insert_city(property.get_location())
        self.__cur.execute("""
            UPDATE property
            SET property_name = :name, location = :location, registration_number = :registration_number, fk_city_id = :city_id
            WHERE id = :id
        """, property_dict)
        self.__con.commit()

    def edit_sample(self, sample: Sample, sample_id: int) -> None:
        sample_dict: dict[str, Any] = to_dict(sample)
        sample_dict['id'] = sample_id
        self.__cur.execute("""
            UPDATE sample
            SET description = :description, collection_date = :collection_date, 
                total_area = :total_area, latitude = :latitude, longitude = :longitude, depth = :depth,
                phosphorus = :phosphorus, potassium = :potassium, organic_matter = :organic_matter, ph = :ph,
                aluminum = :aluminum, h_al = :h_al, calcium = :calcium, magnesium = :magnesium, copper = :copper,
                iron = :iron, manganese = :manganese, zinc = :zinc, base_sum = :base_sum, ctc = :ctc, v_percent = :v_percent,
                aluminum_saturation = :aluminum_saturation, effective_ctc = :effective_ctc, used_config = :used_config, smp = :smp, silte = :silte,
                 sand = :sand, clay =:clay, classification = :classification
            WHERE id = :id
        """, sample_dict)
        self.__con.commit()

    def edit_company(self, company: Company, address: Address, id: int, requester_id: int) -> None:
        company_dict: dict[str, Any] = to_dict(company)
        company_dict['id'] = id
        self.edit_address(address, id, company)
        self.edit_requester(company, requester_id)
        self.__cur.execute("""
            UPDATE company
            SET company_name = :company_name, cnpj = :cnpj 
            WHERE id = :id
        """, company_dict)
        self.__con.commit()

    def delete_person(self, id: int) -> None:
        person_records: list[sqlite3.Row] = self.get_persons(id=id)
        if not person_records:
            raise ValueError("Solicitante não encontrado.")

        person_dict: sqlite3.Row = person_records[0]

        self.__cur.execute("""DELETE FROM person WHERE id = :id""", {'id': id})
        self.__cur.execute("""DELETE FROM requester WHERE requester_id = :requester_id""",
                           {'requester_id': person_dict['requester_id']})
        self.__cur.execute("""DELETE FROM address WHERE address_id = :address_id""",
                           {'address_id': person_dict['address_id']})
        self.__con.commit()

    def delete_company(self, id: int) -> None:
        company_dict: sqlite3.Row = self.get_companies(id=id)[0]
        self.__cur.execute("""DELETE from address 
        WHERE address_id = :address_id """, {'address_id': company_dict['address_id']})
        self.__con.commit()

    def delete_property(self, id: int) -> None:
        self.__cur.execute("""DELETE from property 
        WHERE id = :id """, {'id': id})
        self.__con.commit()

    def delete_sample(self, id: int) -> None:
        self.__cur.execute("""DELETE from sample
        WHERE id = :id """, {'id': id})
        self.__con.commit()

    def edit_address(self, address: Address, id: int, requester_type: Person | Company) -> None:
        requester: sqlite3.Row = self.get_persons(id=id)[0] if isinstance(requester_type, Person) else \
        self.get_companies(id=id)[0]
        address_dict: dict[str, str] = to_dict(address)
        is_equal: bool = True
        for key in address_dict.keys():
            if address_dict[key] != requester[key]:
                is_equal = False
        if is_equal is True:
            return
        new_address_id: int = self.insert_address(address)
        self.__cur.execute("UPDATE requester "
                           "SET fk_address_id = :new_address_id "
                           "WHERE requester_id = :requester_id",
                           {"new_address_id": new_address_id, "requester_id": requester["requester_id"]})
        self.__cur.execute("DELETE from address "
                           "WHERE address_id = :id", {"id": requester["address_id"]})
        self.__con.commit()

    def insert_company(self, company: Company, address: Address) -> None:
        address_id: int = self.insert_address(address)
        requester_id: int = self.insert_requester(company, address_id)
        company_dict: dict[str, Any] = to_dict(company)
        company_dict['requester_id'] = requester_id
        try:
            self.__cur.execute("""INSERT INTO company(company_name, cnpj, fk_requester_id)
            VALUES(:company_name, :cnpj, :requester_id)""", company_dict)
        except sqlite3.IntegrityError as e:
            print(str(e))
            if 'UNIQUE constraint failed: company.cnpj' in str(e):
                raise CNPJAlreadyExistsError(company_dict['cnpj'])
        self.__con.commit()

    def insert_requester(self, requester: Person | Company, address_id: int) -> int:
        requester_dict: dict[str, Any] = to_dict(requester)
        requester_dict['address_id'] = address_id
        self.__cur.execute("""INSERT INTO requester(phone_number, email, fk_address_id)
        VALUES(:phone_number, :email, :address_id)""", requester_dict)
        self.__con.commit()
        return self.__cur.lastrowid

    def edit_requester(self,  requester: Person | Company, requester_id: int):
        self.__cur.execute("""
            UPDATE requester
            SET phone_number = :phone_number, email = :email 
            WHERE requester_id = :id
        """, {'id': requester_id, 'email': requester.get_email(), 'phone_number': requester.get_phone_number()})
        self.__con.commit()

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

    def insert_city(self, location: dict[str, str]) -> int:
        try:
            self.__cur.execute("""
                INSERT OR IGNORE INTO country (country_name)
                VALUES (:country)
            """, location)
            self.__cur.execute("""
                INSERT OR IGNORE INTO state (state_name, fk_country_id)
                VALUES (:state, (SELECT country_id FROM country WHERE country_name = :country))
            """, location)
            self.__cur.execute("""
                INSERT OR IGNORE INTO city (city_name, fk_state_id)
                VALUES (:city, (SELECT state_id FROM state WHERE state_name = :state AND fk_country_id = (SELECT country_id FROM country WHERE country_name = :country)))
            """, location)
            self.__cur.execute("""
                SELECT city_id FROM city
                WHERE city_name = :city AND fk_state_id = (SELECT state_id FROM state WHERE state_name = :state AND fk_country_id = (SELECT country_id FROM country WHERE country_name = :country))
            """, location)
            city_id = self.__cur.fetchone()['city_id']
            self.__con.commit()
            return city_id

        except Exception as e:
            self.__con.rollback()
            raise e

    def insert_property(self, property: Property, requester_id: int) -> None:
        property_dict: dict[str, Any] = to_dict(property)
        city_id: int = self.insert_city(property.get_location())
        property_dict['city_id'] = city_id
        property_dict['location'] = property.get_location()['location']
        property_dict['requester_id'] = requester_id
        self.__cur.execute("""
        INSERT INTO property(property_name, location, registration_number, fk_city_id, fk_requester_id) 
        VALUES(:name, :location, :registration_number, :city_id, :requester_id)""", property_dict)
        self.__con.commit()

    def insert_sample(self, sample: Sample, property_id: int, sample_number: int) -> None:
        sample_dict: dict[str, Any] = to_dict(sample)
        
        sample_dict['property_id'] = property_id
        sample_dict['sample_number'] = sample_number

        self.__cur.execute("""
        INSERT INTO sample(
            description, sample_number, collection_date, total_area, latitude, longitude, 
            depth, phosphorus, potassium, organic_matter, ph, aluminum, h_al, calcium, magnesium, 
            copper, iron, manganese, zinc, base_sum, ctc, v_percent, aluminum_saturation,
            effective_ctc, fk_property_id, smp, silte, sand, clay, classification, used_config
        ) 
        VALUES(
            :description, :sample_number, :collection_date, :total_area, :latitude, :longitude, 
            :depth, :phosphorus, :potassium, :organic_matter, :ph, :aluminum, :h_al, :calcium, 
            :magnesium, :copper, :iron, :manganese, :zinc, :base_sum, :ctc, :v_percent, 
            :aluminum_saturation, :effective_ctc, :property_id, :smp, :silte, :sand, :clay, :classification, :used_config
        )
        """, sample_dict)
        
        self.__con.commit()

    def insert_report(self, report: Report, sample_id: int) -> None:
        report_dict: dict[str, Any] = to_dict(report)
        report_dict['sample_id'] = sample_id
        self.__cur.execute("""INSERT INTO report(file_location, agreement, fk_sample_id) 
        VALUES(:file_location, :agreement, :sample_id)""", report_dict)
        self.__con.commit()

    def get_next_report_id(self) -> int:
        self.__cur.execute("""SELECT id from report""")
        list_of_report_ids: list[sqlite3.Row] = self.__cur.fetchall()
        return len(list_of_report_ids) + 1

    def get_countries(self) -> list[str]:
        self.__cur.execute("""SELECT country_name, country_id from country""")
        return [row['country_name'] for row in self.__cur.fetchall()]

    def get_states(self, country: str) -> list[str]:
        self.__cur.execute("""
                    SELECT s.state_name
                    FROM state s
                    INNER JOIN country c ON s.fk_country_id = c.country_id
                    WHERE c.country_name = ?
                        """, (country,))
        return [row['state_name'] for row in self.__cur.fetchall()]

    def get_cities(self, state: str) -> list[str]:
        self.__cur.execute("""
                    SELECT c.city_name
                    FROM city c
                    INNER JOIN state s ON s.state_id = c.fk_state_id
                    WHERE s.state_name = ?
                        """, (state,))
        return [row['city_name'] for row in self.__cur.fetchall()]

    def get_streets(self, city: str) -> list[str]:
        self.__cur.execute("""
                    SELECT street_name
                    FROM street
                    INNER JOIN city c ON c.city_id = street.fk_city_id
                    WHERE c.city_name = ?
                        """, (city,))
        return [row['street_name'] for row in self.__cur.fetchall()]

    def insert_address_components(self, table: str, row_name: str,
                                  previous_attribute: str, previous_attribute_id: int) -> int:
        self.__cur.execute(f"""SELECT {table}_id FROM {table}
        WHERE lower({table}_name) = lower(?)""", (row_name,))
        matches: list[sqlite3.Row] = self.__cur.fetchall()
        if not matches:
            if previous_attribute == '':
                self.__cur.execute(f"""INSERT INTO {table}({table}_name)
                VALUES(?)""", (row_name,))
                return self.__cur.lastrowid
            self.__cur.execute(f"""INSERT INTO {table}({table}_name, fk_{previous_attribute}_id)
            VALUES(?, ?)""", (row_name, previous_attribute_id))
            return self.__cur.lastrowid
        self.__con.commit()
        return matches[0][f'{table}_id']

    def close_connection(self):
        self.__cur.close()
        self.__con.close()

    def get_persons(self, **kwargs) -> list[sqlite3.Row]:
        query: str = """SELECT
            p.id AS id, 
            p.name,
            p.birth_date,
            p.cpf,
            r.requester_id,
            r.phone_number,
            r.email,
            a.cep,
            a.address_number,
            a.address_id,
            s.street_name as street,
            c.city_name as city,
            st.state_name as state,
            co.country_name as country
            FROM 
            person p
            INNER JOIN 
            requester r ON p.fk_requester_id = r.requester_id
            INNER JOIN 
            address a ON r.fk_address_id = a.address_id
            INNER JOIN 
            street s ON a.fk_street_id = s.street_id
            INNER JOIN 
            city c ON a.fk_city_id = c.city_id
            INNER JOIN 
            state st ON a.fk_state_id = st.state_id
            INNER JOIN 
            country co ON a.fk_country_id = co.country_id
            """
        id: int = kwargs.get("id")
        cpf: str = kwargs.get("cpf")
        name: str = kwargs.get("name")
        params: dict[str, Any] = {}
        if id:
            query += " WHERE id = :id"
            params = {"id": id}
        elif cpf:
            query += " WHERE cpf LIKE :cpf"
            params = {"cpf": f"{cpf}%"}
        elif name:
            query += " WHERE name LIKE :name"
            params = {"name": f"%{name}%"}
        self.__cur.execute(query + " ORDER BY name", params)
        return self.__cur.fetchall()

    def get_companies(self, **kwargs) -> list[sqlite3.Row]:
        query: str = """SELECT 
            cn.id AS id,
            cn.company_name,
            cn.cnpj,
            r.requester_id,
            r.phone_number,
            r.email,
            a.cep,
            a.address_number,
            a.address_id,
            s.street_name as street,
            c.city_name as city,
            st.state_name as state,
            co.country_name as country
            FROM 
            company cn
            INNER JOIN 
            requester r ON cn.fk_requester_id = r.requester_id
            INNER JOIN 
            address a ON r.fk_address_id = a.address_id
            INNER JOIN 
            street s ON a.fk_street_id = s.street_id
            INNER JOIN 
            city c ON a.fk_city_id = c.city_id
            INNER JOIN 
            state st ON a.fk_state_id = st.state_id
            INNER JOIN 
            country co ON a.fk_country_id = co.country_id"""
        id: int = kwargs.get("id")
        cnpj: str = kwargs.get("cnpj")
        company_name: str = kwargs.get("company_name")
        params: dict[str, Any] = {}
        if id:
            query += " WHERE id = :id"
            params = {"id": id}
        elif cnpj:
            query += " WHERE cnpj LIKE :cnpj"
            params = {"cnpj": f"{cnpj}%"}
        elif company_name:
            query += " WHERE company_name LIKE :company_name"
            params = {"company_name": f"%{company_name}%"}
        self.__cur.execute(query + " ORDER BY company_name", params)
        return self.__cur.fetchall()

    def get_requesters(self, **kwargs) -> list[sqlite3.Row] | None:
        requester_id: int = kwargs.get('requester_id')
        params: dict = {}

        query: str = """
        SELECT
            r.requester_id,
            r.phone_number,
            r.email,
            p.name AS name,
            p.id AS id,
            p.cpf AS document_number,
            'person' AS requester_type 
        FROM 
            requester r
        INNER JOIN 
            person p ON r.requester_id = p.fk_requester_id
        """
        if requester_id:
            query += " WHERE r.requester_id = :requester_id"
            params['requester_id'] = requester_id

        query += """
        UNION 
        SELECT 
            r.requester_id,
            r.phone_number,
            r.email,
            c.company_name AS name,
            c.id AS id,
            c.cnpj AS document_number,
            'company' AS requester_type
        FROM 
            requester r
        INNER JOIN 
            company c ON r.requester_id = c.fk_requester_id
        """
        if requester_id:
            query += " WHERE r.requester_id = :requester_id"

        self.__cur.execute(query, params)
        return self.__cur.fetchall()

    def get_properties(self, **kwargs) -> list[sqlite3.Row]:
        query: str = """SELECT
            property.id as id,
            property.property_name as name,
            property.location,
            property.registration_number,
            city.city_name as city,
            state.state_name as state,
            country.country_name as country 
        FROM
            property
        JOIN
            requester ON property.fk_requester_id = requester.requester_id
        JOIN
            city ON property.fk_city_id = city.city_id
        JOIN
            state ON city.fk_state_id = state.state_id
        JOIN
            country ON state.fk_country_id = country.country_id
        """
        requester_id = kwargs.get('requester_id')
        property_id = kwargs.get('id')

        if requester_id:
            query += "WHERE property.fk_requester_id = :requester_id"
            params = {"requester_id": requester_id}
        elif property_id:
            query += "WHERE property.id = :property_id"
            params = {"property_id": property_id}
        else:
            params = {}

        self.__cur.execute(query, params)
        return self.__cur.fetchall()

    def get_samples(self, **kwargs) -> list[sqlite3.Row]:
        query = """SELECT
            * from sample  
        """
        property_id = kwargs.get('property_id')
        sample_id = kwargs.get('sample_id')
        id_list = kwargs.get('id_list')
        if sample_id:
            query += "WHERE id = :sample_id"
            params = {"sample_id": sample_id}
        elif property_id:
            query += "WHERE fk_property_id = :property_id"
            params = {"property_id": property_id}
        elif id_list:
            query += " WHERE id = :sample_id_0"
            params = {"sample_id_0": id_list[0]}
            for i in range(1, len(id_list)):
                query += f" OR id = :sample_id_{i}"
                params[f"sample_id_{i}"] = id_list[i]
        else:
            params = {}
        self.__cur.execute(query, params)
        return self.__cur.fetchall()

    def get_sample_info(self, sample_id: int):
        self.__cur.execute("""SELECT
            COALESCE(person.name, company.company_name) AS requester_name,
            COALESCE(person.cpf, company.cnpj) AS document_number,
            CASE 
            WHEN person.cpf IS NOT NULL THEN 'cpf' 
            WHEN company.cnpj IS NOT NULL THEN 'cnpj' 
            ELSE NULL 
            END AS document_type,
            CONCAT(street.street_name, ', ', address.address_number, ', ', city.city_name, ', ', state.state_name, ', ', country.country_name) AS address,
            property.property_name, 
            city.city_name as city, 
            state.state_name as state, 
            sample.description AS sample_description,
            sample.sample_number,
            sample.collection_date,
            sample.depth,
            sample.total_area, 
            property.registration_number
            FROM
                sample
            JOIN property ON sample.fk_property_id = property.id
            JOIN requester ON property.fk_requester_id = requester.requester_id
            LEFT JOIN person ON person.fk_requester_id = requester.requester_id
            LEFT JOIN company ON company.fk_requester_id = requester.requester_id
            JOIN address ON requester.fk_address_id = address.address_id
            JOIN street ON address.fk_street_id = street.street_id
            JOIN city ON address.fk_city_id = city.city_id
            JOIN state ON address.fk_state_id = state.state_id
            JOIN country ON address.fk_country_id = country.country_id
            WHERE sample.id = ?;
        """, (sample_id,))
        return self.__cur.fetchone()
    
    def get_report_info(self) -> list[sqlite3.Row]:
        self.__cur.execute("""SELECT 
                report.id AS id, 
                COALESCE(person.name, company.company_name) AS requester_name,
                sample.collection_date AS date,
                property.property_name AS property 
                FROM  
                report 
                JOIN sample ON report.fk_sample_id = sample.id 
                JOIN property ON sample.fk_property_id = property.id 
                JOIN requester ON property.fk_requester_id = requester.requester_id 
                LEFT JOIN person ON requester.requester_id = person.fk_requester_id 
                LEFT JOIN company ON requester.requester_id = company.fk_requester_id;""")
        return self.__cur.fetchall()
