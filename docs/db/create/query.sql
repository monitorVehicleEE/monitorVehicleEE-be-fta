-- CREATE TABLE users (
--     id BIGSERIAL PRIMARY KEY,

--     code VARCHAR(50),

--     status INT DEFAULT 0,
--     -- 0: New
--     -- 1: Active
--     -- 2: Suspended
--     -- 10: Deleted

--     type INT DEFAULT 200,
--     -- 100: Staff
--     -- 200: User
--     -- 300: Guest

--     email VARCHAR(250),
--     username VARCHAR(250),
--     password VARCHAR(250),
--     avatar VARCHAR(250),

--     fullname VARCHAR(100),

--     date_new TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     date_mod TIMESTAMP
-- );

-- CREATE TABLE otps (
--     id BIGSERIAL PRIMARY KEY,

--     email VARCHAR(250) NOT NULL,

--     otp_code VARCHAR(6) NOT NULL,

--     is_used INTEGER DEFAULT 0,

--     expire_at TIMESTAMP NOT NULL,

--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
-- CREATE INDEX idx_otps_email ON otps(email);
-- CREATE TABLE cameras (
--     id BIGSERIAL PRIMARY KEY,

--     code VARCHAR(50) NOT NULL UNIQUE,

--     name VARCHAR(100) NOT NULL,

--     location VARCHAR(250),

--     camera_role INTEGER NOT NULL,

--     source_type VARCHAR(20) NOT NULL,

--     source_path VARCHAR(500) NOT NULL,

--     last_active_time TIMESTAMP,

--     status INTEGER DEFAULT 1,

--     date_new TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

--     date_mod TIMESTAMP
-- );
-- CREATE TABLE vehicle_types (
--     id SERIAL PRIMARY KEY,

--     code VARCHAR(50) UNIQUE NOT NULL,

--     name VARCHAR(100) NOT NULL,

--     description VARCHAR(255),

--     status INTEGER DEFAULT 1
-- );

-- CREATE TABLE vehicles (
--     id BIGSERIAL PRIMARY KEY,

--     plate VARCHAR(20) NOT NULL UNIQUE,

--     type VARCHAR(50),

--     is_internal BOOLEAN DEFAULT FALSE,

--     status INTEGER DEFAULT 1,

--     date_new TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

--     date_mod TIMESTAMP
-- );

-- CREATE TABLE access_rules (
--     id BIGSERIAL PRIMARY KEY,

--     plate VARCHAR(20) NOT NULL,

--     rule_type VARCHAR(20) NOT NULL,

--     description VARCHAR(250),

--     valid_from TIMESTAMP,

--     valid_to TIMESTAMP,

--     status INTEGER DEFAULT 1,

--     date_new TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

--     date_mod TIMESTAMP
-- );

-- CREATE INDEX idx_access_rules_plate
-- ON access_rules(plate);


-- CREATE TABLE vehicle_events (
--     id BIGSERIAL PRIMARY KEY,

--     camera_id BIGINT NOT NULL,
--     plate VARCHAR(20),

--     event_type VARCHAR(20) NOT NULL, -- IN, OUT, DETECTED
--     vehicle_type_id BIGINT,

--     vehicle_confidence NUMERIC(5,2),
--     plate_confidence NUMERIC(5,2),

--     image_path VARCHAR(500),
--     plate_image_path VARCHAR(500),

--     bbox JSONB,

--     status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
--     event_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     date_new TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

--     CONSTRAINT fk_vehicle_event_camera
--         FOREIGN KEY (camera_id)
--         REFERENCES cameras(id),

-- 	   CONSTRAINT fk_vehicle_event_vehicle_type
--     	   FOREIGN KEY (vehicle_type_id)
--         REFERENCES vehicle_types(id)
-- );


-- CREATE INDEX idx_vehicle_events_plate
-- ON vehicle_events(plate);

-- CREATE TABLE vehicle_sessions (
--     id BIGSERIAL PRIMARY KEY,

--     plate VARCHAR(20),

--     in_event_id BIGINT,

--     out_event_id BIGINT,

--     in_time TIMESTAMP NOT NULL,

--     out_time TIMESTAMP,

--     duration_seconds INTEGER,

--     in_camera_id BIGINT NOT NULL,

--     out_camera_id BIGINT,

--     status VARCHAR(20) NOT NULL,

--     date_new TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

--     date_mod TIMESTAMP,

--     CONSTRAINT fk_session_in_event
--         FOREIGN KEY (in_event_id)
--         REFERENCES vehicle_events(id),

--     CONSTRAINT fk_session_out_event
--         FOREIGN KEY (out_event_id)
--         REFERENCES vehicle_events(id),

--     CONSTRAINT fk_session_in_camera
--         FOREIGN KEY (in_camera_id)
--         REFERENCES cameras(id),

--     CONSTRAINT fk_session_out_camera
--         FOREIGN KEY (out_camera_id)
--         REFERENCES cameras(id)
-- );