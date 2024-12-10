import sqlite3

# Define the database path
DATABASE_PATH = "Database/apk_database.db"

# Connect to the database (creates a new one if it doesn't exist)
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Create the table for storing APK metadata with categories
cursor.execute('''
CREATE TABLE IF NOT EXISTS apks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL UNIQUE,
    category TEXT CHECK(category IN ('real', 'fake', 'test', 'other')) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Insert example categories and files
sample_data = [
    ("Instagram_360.0.0.51.192_APKPure.apk", "apks/real/Instagram_360.0.0.51.192_APKPure.apk", "real"),
    ("bitbar-sample-app.apk", "apks/fake/bitbar-sample-app.apk", "fake"),
    ("SpywareTest.apk", "apks/spyware/SpywareTest.apk", "test"),
    ("Dr. Driving_1.70_APKPure.apk", "apks/other/Dr. Driving_1.70_APKPure.apk", "other")
]

cursor.executemany('''
INSERT INTO apks (file_name, file_path, category)
VALUES (?, ?, ?)
''', sample_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database with categories created successfully. Sample data inserted.")
