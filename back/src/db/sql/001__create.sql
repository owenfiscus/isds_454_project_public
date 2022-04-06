create database car_data;

\c car_data;

create table manufacturers(
    manufacturer_id integer primary key,
    manufacturer    Varchar(50)
);

create table vehicle_types(
    vehicle_type_id integer primary key,
    vehicle_type    Varchar(50)
);

create table transmissions(
    transmission_id integer primary key,
    transmission_type Varchar(50)
);

create table drivetrains(
    drivetrain_id integer primary key,
    drivetrain_type Varchar(50)
);

create table toyota_pricing(
    car_id              integer primary key,
    manufacturer_id     integer REFERENCES manufacturers(manufacturer_id),
    model               Varchar(100),
    trim_               Varchar(100),
    vehicle_type_id     integer REFERENCES vehicle_types(vehicle_type_id),
    msrp_price          Varchar(100),
    door_number         integer,
    city_mpg            integer,
    highway_mpg         integer,
    horsepower          integer,
    engine              Varchar(225),
    transmission_id     integer REFERENCES transmissions(transmission_id),
    drivetrain_id       integer  REFERENCES drivetrains(drivetrain_id),
    height_in           double precision,
    width_in            double precision,
    length_in           double precision,
    wheelbase           double precision,
    curb_weight         Varchar(200),
    fuel_tank_size      Varchar(200),
    web_link            Varchar(1500)
);

create table ford_pricing(
    car_id               integer primary key,
    manufacturer_id     integer REFERENCES manufacturers(manufacturer_id),
    model               Varchar(100),
    trim_               Varchar(100),
    vehicle_type_id     integer REFERENCES vehicle_types(vehicle_type_id),
    msrp_price          Varchar(100),
    door_number         integer,
    city_mpg            integer,
    highway_mpg         integer,
    horsepower          integer,
    engine              Varchar(225),
    transmission_id     integer REFERENCES transmissions(transmission_id),
    drivetrain_id       integer REFERENCES drivetrains(drivetrain_id),
    height_in           double precision,
    width_in            double precision,
    length_in           double precision,
    wheelbase           double precision,
    curb_weight         Varchar(200),
    fuel_tank_size      Varchar(200),
    web_link            Varchar(1500)
);

create table lamborghini_pricing(
    car_id               integer primary key,
    manufacturer_id     integer REFERENCES manufacturers(manufacturer_id),
    model               Varchar(100),
    trim_               Varchar(100),
    vehicle_type_id     integer REFERENCES vehicle_types(vehicle_type_id),
    msrp_price          Varchar(100),
    door_number         integer,
    city_mpg            integer,
    highway_mpg         integer,
    horsepower          integer,
    engine              Varchar(225),
    transmission_id     integer REFERENCES transmissions(transmission_id),
    drivetrain_id       integer REFERENCES drivetrains(drivetrain_id),
    height_in           double precision,
    width_in            double precision,
    length_in           double precision,
    wheelbase           double precision,
    curb_weight         Varchar(200),
    fuel_tank_size      Varchar(200),
    web_link            Varchar(1500)
);

create table subaru_pricing(
    car_id               integer primary key,
    manufacturer_id     integer REFERENCES manufacturers(manufacturer_id),
    model               Varchar(100),
    trim_               Varchar(100),
    vehicle_type_id     integer REFERENCES vehicle_types(vehicle_type_id),
    msrp_price          Varchar(100),
    door_number         integer,
    city_mpg            integer,
    highway_mpg         integer,
    horsepower          integer,
    engine              Varchar(225),
    transmission_id     integer REFERENCES transmissions(transmission_id),
    drivetrain_id       integer REFERENCES drivetrains(drivetrain_id),
    height_in           double precision,
    width_in            double precision,
    length_in           double precision,
    wheelbase           double precision,
    curb_weight         Varchar(200),
    fuel_tank_size      Varchar(200),
    web_link            Varchar(1500)
);

create table honda_pricing(
    car_id               integer primary key,
    manufacturer_id     integer REFERENCES manufacturers(manufacturer_id),
    model               Varchar(100),
    trim_               Varchar(100),
    vehicle_type_id     integer REFERENCES vehicle_types(vehicle_type_id),
    msrp_price          Varchar(100),
    door_number         integer,
    city_mpg            integer,
    highway_mpg         integer,
    horsepower          integer,
    engine              Varchar(225),
    transmission_id     integer REFERENCES transmissions(transmission_id),
    drivetrain_id       integer REFERENCES drivetrains(drivetrain_id),
    height_in           double precision,
    width_in            double precision,
    length_in           double precision,
    wheelbase           double precision,
    curb_weight         Varchar(200),
    fuel_tank_size      Varchar(200),
    web_link            Varchar(1500)
);

create table bmw_pricing(
    car_id               integer primary key,
    manufacturer_id     integer REFERENCES manufacturers(manufacturer_id),
    model               Varchar(100),
    trim_               Varchar(100),
    vehicle_type_id     integer REFERENCES vehicle_types(vehicle_type_id),
    msrp_price          Varchar(100),
    door_number         integer,
    city_mpg            integer,
    highway_mpg         integer,
    horsepower          integer,
    engine              Varchar(225),
    transmission_id     integer REFERENCES transmissions(transmission_id),
    drivetrain_id       integer REFERENCES drivetrains(drivetrain_id),
    height_in           double precision,
    width_in            double precision,
    length_in           double precision,
    wheelbase           double precision,
    curb_weight         Varchar(200),
    fuel_tank_size      Varchar(200),
    web_link            Varchar(1500)
);

create table ferrari_pricing(
    car_id               integer primary key,
    manufacturer_id     integer REFERENCES manufacturers(manufacturer_id),
    model               Varchar(100),
    trim_               Varchar(100),
    vehicle_type_id     integer REFERENCES vehicle_types(vehicle_type_id),
    msrp_price          Varchar(100),
    door_number         integer,
    city_mpg            integer,
    highway_mpg         integer,
    horsepower          integer,
    engine              Varchar(225),
    transmission_id     integer REFERENCES transmissions(transmission_id),
    drivetrain_id       integer REFERENCES drivetrains(drivetrain_id),
    height_in           double precision,
    width_in            double precision,
    length_in           double precision,
    wheelbase           double precision,
    curb_weight         Varchar(200),
    fuel_tank_size      Varchar(200),
    web_link            Varchar(1500)
);