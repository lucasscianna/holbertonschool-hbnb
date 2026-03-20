-- ============================================================
-- HBnB — Données initiales
-- ============================================================

-- Admin user (password = admin1234 hashé avec bcrypt)
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$V1nXsNHRBal/Uqs2yBnG2eRIaOwl2HgNPJF7klEmq0ItHUDS3KZbq',
    TRUE
);

-- Amenities
INSERT INTO amenities (id, name) VALUES
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'WiFi'),
    ('b2c3d4e5-f6a7-8901-bcde-f01234567891', 'Swimming Pool'),
    ('c3d4e5f6-a7b8-9012-cdef-012345678912', 'Air Conditioning');