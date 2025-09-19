import sqlite3

DATABASE_PATH = 'health_services.db'

def add_new_clinic(name, address, latitude, longitude, services):
    """Adds a new clinic to the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clinics (name, address, latitude, longitude, services) VALUES (?, ?, ?, ?, ?)",
        (name, address, latitude, longitude, services)
    )
    conn.commit()
    conn.close()
    print(f"Added new clinic: {name}")

def update_clinic_address(clinic_name, new_address):
    """Updates the address of an existing clinic."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clinics SET address = ? WHERE name = ?",
        (new_address, clinic_name)
    )
    conn.commit()
    conn.close()
    print(f"Updated address for clinic: {clinic_name}")

def delete_clinic(clinic_name):
    """Deletes a clinic from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM clinics WHERE name = ?",
        (clinic_name,)
    )
    conn.commit()
    conn.close()
    print(f"Deleted clinic: {clinic_name}")

if __name__ == '__main__':
    # --- Example Usage ---

    # 1. Add a new clinic
    # add_new_clinic("Wellness Clinic", "45 Health St, Bengaluru", 12.9141, 74.8569, "General, Physiotherapy")

    # 2. Update an existing clinic's address (uncomment to run)
    # update_clinic_address("New Life Medical Center", "555 Basavanagudi St, Jayanagar")

    # 3. Delete a clinic (uncomment to run)
    # delete_clinic("Mobile Mercy Unit Alpha")

    print("Script finished. Check your 'health_services.db' file for changes.")