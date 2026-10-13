
CREATE TABLE drivers (
    driver_id SERIAL PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE transport_collections (
    id SERIAL PRIMARY KEY,
    driver_id INTEGER NOT NULL REFERENCES drivers(driver_id) ON DELETE CASCADE,
    vehicle_number VARCHAR(20) NOT NULL,
    collection_date DATE NOT NULL,
    morning_trips INTEGER NOT NULL,
    evening_trips INTEGER NOT NULL,
    morning_collection NUMERIC(10, 2) NOT NULL,
    evening_collection NUMERIC(10, 2) NOT NULL,
    fuel_expense NUMERIC(10, 2) NOT NULL,
    other_expense NUMERIC(10, 2) NOT NULL,
    total_trips INTEGER NOT NULL,
    total_collection NUMERIC(10, 2) NOT NULL,
    total_expense NUMERIC(10, 2) NOT NULL,
    net_collection NUMERIC(10, 2) NOT NULL,
    report_file TEXT
);

INSERT INTO drivers (driver_name, phone_number) VALUES
('Arun Kumar', '9876543210'),
('Karthik Raj', '9876543211');
