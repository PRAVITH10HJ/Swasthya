import sqlite3

DATABASE_FILE = 'health_services.db'

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# Drop the table if it exists to start fresh
cursor.execute("DROP TABLE IF EXISTS clinics")

# Create the 'clinics' table
cursor.execute('''
CREATE TABLE clinics (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    services TEXT
);
''')

# --- 10 Sample Clinics in Bengaluru ---
clinics_to_add = [
    ('Hope Clinic', '123 Health St, Majestic', 12.9767, 77.5713, 'General, Pediatric'),
    ('Community Care Center', '456 Wellness Ave, Indiranagar', 12.9784, 77.6408, 'General, Dental'),
    ('Unity Health Services', '789 Unity Rd, Koramangala', 12.9352, 77.6245, 'Emergency, General'),
    ('SafeHands Medical', '101 Mercy Ln, Jayanagar', 12.9231, 77.5822, 'General, Maternity'),
    ('Bengaluru Health Hub', '212 Brigade Rd, Ashok Nagar', 12.9719, 77.6074, 'General, Pharmacy'),
    ('Displaced Peoples Clinic', '333 Relief Rd, Marathahalli', 12.9569, 77.7011, 'Trauma, General'),
    ('Mobile Mercy Unit Alpha', 'Near KR Market', 12.9600, 77.5730, 'Mobile Clinic, First Aid'),
    ('New Life Medical Center', '555 Basavanagudi St', 12.9421, 77.5711, 'General, Vaccinations'),
    ('Hebbal Health Point', '876 Outer Ring Rd, Hebbal', 13.0358, 77.5970, 'General'),
    ('Whitefield Community Clinic', '990 ITPL Main Rd, Whitefield', 12.9839, 77.7499, 'General, Pediatric')
]

# Insert the data
cursor.executemany('''
INSERT INTO clinics (name, address, latitude, longitude, services) VALUES (?, ?, ?, ?, ?);
''', clinics_to_add)

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Database '{DATABASE_FILE}' created and populated with {len(clinics_to_add)} clinics.")