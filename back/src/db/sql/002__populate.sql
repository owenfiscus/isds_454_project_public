\c car_data;

COPY manufacturers         FROM '/data/Manufacturer.csv'       delimiter ',' csv header;
COPY transmissions         FROM '/data/Transmission.csv'       delimiter ',' csv header;
COPY vehicle_types         FROM '/data/Vehicle_Type.csv'       delimiter ',' csv header;
COPY drivetrains           FROM '/data/Drivetrain.csv'         delimiter ',' csv header;
COPY toyota_pricing        FROM '/data/Toyota.csv'             delimiter ',' csv header;
COPY lamborghini_pricing   FROM '/data/Lamborghini.csv'        delimiter ',' csv header;
COPY ford_pricing          FROM '/data/Ford.csv'               delimiter ',' csv header;
COPY bmw_pricing           FROM '/data/BMW.csv'                delimiter ',' csv header;
COPY ferrari_pricing       FROM '/data/Ferrari.csv'            delimiter ',' csv header;
COPY honda_pricing         FROM '/data/Honda.csv'              delimiter ',' csv header;
COPY subaru_pricing        FROM '/data/Subaru.csv'             delimiter ',' csv header;
