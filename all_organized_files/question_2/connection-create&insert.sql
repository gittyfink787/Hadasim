CREATE TABLE connection (
    connection_id INT PRIMARY KEY,
    connection_type VARCHAR(50) NOT NULL
);

ALTER TABLE connection
ADD CONSTRAINT connection_type_unique UNIQUE (connection_type);

INSERT INTO connection (connection_id, connection_type) VALUES (1, 'Father');
INSERT INTO connection (connection_id, connection_type) VALUES (2, 'Mother');
INSERT INTO connection (connection_id, connection_type) VALUES (3, 'Brother');
INSERT INTO connection (connection_id, connection_type) VALUES (4, 'Sister');
INSERT INTO connection (connection_id, connection_type) VALUES (5, 'Son');
INSERT INTO connection (connection_id, connection_type) VALUES (6, 'Daughter');
INSERT INTO connection (connection_id, connection_type) VALUES (7, 'Husband');
INSERT INTO connection (connection_id, connection_type) VALUES (8, 'Wife');
