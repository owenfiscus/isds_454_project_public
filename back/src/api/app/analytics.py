def full_pull(manu1,manu2,drivetrain,transmission):
    query = '''
            select * from(
            (SELECT manufacturers.manufacturer,{0}_pricing.model,{0}_pricing.msrp_price,{0}_pricing.city_mpg,{0}_pricing.highway_mpg,{0}_pricing.horsepower,{0}_pricing.fuel_tank_size
            FROM {0}_pricing 
            JOIN manufacturers ON {0}_pricing.manufacturer_id = manufacturers.manufacturer_id 
            JOIN transmissions ON {0}_pricing.transmission_id = transmissions.transmission_id 
            JOIN drivetrains ON {0}_pricing.drivetrain_id = drivetrains.drivetrain_id
            where drivetrains.drivetrain_type = '{2}'
            and transmissions.transmission_type = '{3}'
            )
            UNION ALL
            (SELECT manufacturers.manufacturer,{1}_pricing.model,{1}_pricing.msrp_price,{1}_pricing.city_mpg,{1}_pricing.highway_mpg,{1}_pricing.horsepower,{1}_pricing.fuel_tank_size
            FROM {1}_pricing 
            JOIN manufacturers ON {1}_pricing.manufacturer_id = manufacturers.manufacturer_id 
            JOIN transmissions ON {1}_pricing.transmission_id = transmissions.transmission_id 
            JOIN drivetrains ON {1}_pricing.drivetrain_id = drivetrains.drivetrain_id
            where drivetrains.drivetrain_type = '{2}'
            and transmissions.transmission_type = '{3}'
            ) 
            ) AS TOP;
            '''.format(manu1,manu2,drivetrain,transmission)
    return query

def manu_pull(manu1,manu2):
    query = '''
            select * from(
            (SELECT manufacturers.manufacturer,{0}_pricing.model,{0}_pricing.msrp_price,{0}_pricing.city_mpg,{0}_pricing.highway_mpg,{0}_pricing.horsepower,{0}_pricing.fuel_tank_size
            FROM {0}_pricing 
            JOIN manufacturers ON {0}_pricing.manufacturer_id = manufacturers.manufacturer_id 
            JOIN transmissions ON {0}_pricing.transmission_id = transmissions.transmission_id 
            JOIN drivetrains ON {0}_pricing.drivetrain_id = drivetrains.drivetrain_id
            )
            UNION ALL
            (SELECT manufacturers.manufacturer,{1}_pricing.model,{1}_pricing.msrp_price,{1}_pricing.city_mpg,{1}_pricing.highway_mpg,{1}_pricing.horsepower,{1}_pricing.fuel_tank_size
            FROM {1}_pricing 
            JOIN manufacturers ON {1}_pricing.manufacturer_id = manufacturers.manufacturer_id 
            JOIN transmissions ON {1}_pricing.transmission_id = transmissions.transmission_id 
            JOIN drivetrains ON {1}_pricing.drivetrain_id = drivetrains.drivetrain_id
            ) 
            ) AS TOP;
            '''.format(manu1,manu2)
    return query

def drive_pull(manu1,manu2,drivetrain):
    query = '''
            select * from(
            (SELECT manufacturers.manufacturer,{0}_pricing.model,{0}_pricing.msrp_price,{0}_pricing.city_mpg,{0}_pricing.highway_mpg,{0}_pricing.horsepower,{0}_pricing.fuel_tank_size
            FROM {0}_pricing 
            JOIN manufacturers ON {0}_pricing.manufacturer_id = manufacturers.manufacturer_id 
            JOIN transmissions ON {0}_pricing.transmission_id = transmissions.transmission_id 
            JOIN drivetrains ON {0}_pricing.drivetrain_id = drivetrains.drivetrain_id
            where drivetrains.drivetrain_type = '{2}'
            )
            UNION ALL
            (SELECT manufacturers.manufacturer,{1}_pricing.model,{1}_pricing.msrp_price,{1}_pricing.city_mpg,{1}_pricing.highway_mpg,{1}_pricing.horsepower,{1}_pricing.fuel_tank_size
            FROM {1}_pricing 
            JOIN manufacturers ON {1}_pricing.manufacturer_id = manufacturers.manufacturer_id 
            JOIN transmissions ON {1}_pricing.transmission_id = transmissions.transmission_id 
            JOIN drivetrains ON {1}_pricing.drivetrain_id = drivetrains.drivetrain_id
            where drivetrains.drivetrain_type = '{2}'
            ) 
            ) AS TOP;
            '''.format(manu1,manu2,drivetrain)
    return query

def transmission_pull(manu1,manu2,transmission):
    query = '''
            select * from(
            (SELECT manufacturers.manufacturer,{0}_pricing.model,{0}_pricing.msrp_price,{0}_pricing.city_mpg,{0}_pricing.highway_mpg,{0}_pricing.horsepower,{0}_pricing.fuel_tank_size
            FROM {0}_pricing 
            JOIN manufacturers ON {0}_pricing.manufacturer_id = manufacturers.manufacturer_id 
            JOIN transmissions ON {0}_pricing.transmission_id = transmissions.transmission_id 
            JOIN drivetrains ON {0}_pricing.drivetrain_id = drivetrains.drivetrain_id
            where transmissions.transmission_type = '{2}'
            )
            UNION ALL
            (SELECT manufacturers.manufacturer,{1}_pricing.model,{1}_pricing.msrp_price,{1}_pricing.city_mpg,{1}_pricing.highway_mpg,{1}_pricing.horsepower,{1}_pricing.fuel_tank_size
            FROM {1}_pricing 
            JOIN manufacturers ON {1}_pricing.manufacturer_id = manufacturers.manufacturer_id 
            JOIN transmissions ON {1}_pricing.transmission_id = transmissions.transmission_id 
            JOIN drivetrains ON {1}_pricing.drivetrain_id = drivetrains.drivetrain_id
            where transmissions.transmission_type = '{2}'
            ) 
            ) AS TOP;
            '''.format(manu1,manu2,transmission)
    return query