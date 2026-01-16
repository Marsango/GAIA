CREATE TABLE requester(
        requester_id integer primary key, phone_number varchar(15), email varchar(255), fk_address_id integer,
        FOREIGN KEY(fk_address_id) REFERENCES address(address_id) ON DELETE CASCADE);
CREATE TABLE country(
        country_id integer primary key, country_name varchar(255) UNIQUE);
CREATE TABLE state(
                state_id integer primary key, state_name varchar(255), fk_country_id integer,
                UNIQUE(state_name, fk_country_id),
                 FOREIGN KEY(fk_country_id) REFERENCES country(country_id) ON DELETE CASCADE);
CREATE TABLE city(
                city_id integer primary key, city_name varchar(255), fk_state_id integer,
                UNIQUE(city_name, fk_state_id),
                FOREIGN KEY(fk_state_id) REFERENCES state(state_id) ON DELETE CASCADE);
CREATE TABLE street(
                street_id integer primary key, street_name varchar(255), fk_city_id integer,
                UNIQUE(street_name, fk_city_id),
                FOREIGN KEY(fk_city_id) REFERENCES city(city_id) ON DELETE CASCADE);
CREATE TABLE address(
        cep varchar(10), address_id integer primary key, fk_country_id integer, fk_state_id integer, fk_city_id integer,
        fk_street_id integer, address_number varchar(10),
        FOREIGN KEY(fk_country_id) REFERENCES country(country_id) ON DELETE CASCADE,
        FOREIGN KEY(fk_state_id) REFERENCES state(state_id) ON DELETE CASCADE,
        FOREIGN KEY(fk_city_id) REFERENCES city(city_id) ON DELETE CASCADE,
        FOREIGN KEY(fk_street_id) REFERENCES street(street_id) ON DELETE CASCADE);
CREATE TABLE person(
        id INTEGER PRIMARY KEY,
        name varchar(255), birth_date varchar(20), cpf varchar(15) UNIQUE, email VARCHAR(255),
        phone_number VARCHAR(15), fk_requester_id integer,
        FOREIGN KEY(fk_requester_id) REFERENCES requester(requester_id) ON DELETE CASCADE);
CREATE TABLE company(
        id INTEGER PRIMARY KEY,
        company_name varchar(255), cnpj varchar(20) UNIQUE, fk_requester_id integer,
        FOREIGN KEY(fk_requester_id) REFERENCES requester(requester_id) ON DELETE CASCADE);
CREATE TABLE property(
        id INTEGER PRIMARY KEY, property_name varchar(255), location varchar(255), registration_number integer, fk_city_id integer, fk_requester_id integer,
        FOREIGN KEY (fk_city_id) REFERENCES city(city_id) ON DELETE CASCADE,
        FOREIGN KEY (fk_requester_id) REFERENCES requester(requester_id) ON DELETE CASCADE);
CREATE TABLE sample(
        id INTEGER PRIMARY KEY, description varchar(255), sample_number integer, collection_date varchar(20), total_area float,
        latitude float, smp float, longitude float, depth float, phosphorus float, potassium float, organic_matter float, ph float,
         aluminum float, h_al float, calcium float, magnesium float, copper float, iron float, manganese float, 
         zinc float, base_sum float, clay float, silte float, classification string, sand float, ctc float, v_percent float, aluminum_saturation float,
        effective_ctc float, used_config, fk_property_id, FOREIGN KEY (fk_property_id) REFERENCES property(id) ON DELETE CASCADE);
CREATE TABLE report(id INTEGER PRIMARY KEY, file_location varchar(255), agreement varchar(255), fk_sample_id integer,
        FOREIGN KEY (fk_sample_id) REFERENCES sample(id) ON DELETE CASCADE);
