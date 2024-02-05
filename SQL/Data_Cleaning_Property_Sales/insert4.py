import csv
import json
import mysql.connector
from datetime import datetime
import time

# Read the configuration file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Extract MySQL connection parameters
mysql_config = config.get('mysql')

# MySQL database configuration
db_config = {
    'host': mysql_config.get('host'),
    'user': mysql_config.get('user'),
    'password': mysql_config.get('password'),
    'database': 'nashville_housing',  # Change to your database name
}

# CSV file path (change to the path of your CSV file)
csv_file = 'Nashville_Housing_Data.csv'

# Table name where you csv file data to be added
table_name = 'PropertySales2'

# Connect to MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Create the MySQL table (if it doesn't exist)
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    UniqueID INT NOT NULL PRIMARY KEY,
    ParcelID VARCHAR(50) NOT NULL,
    LandUse VARCHAR(50) NOT NULL,
    PropertyAddress VARCHAR(255) NOT NULL,
    SaleDate DATE NOT NULL,
    SalePrice INT NOT NULL,
    LegalReference VARCHAR(255) NOT NULL,
    SoldAsVacant VARCHAR(5) NOT NULL,
    OwnerName VARCHAR(255) NOT NULL,
    OwnerAddress VARCHAR(255) NOT NULL,
    Acreage DECIMAL(5, 2),
    TaxDistrict VARCHAR(50) NOT NULL,
    LandValue INT,
    BuildingValue INT,
    TotalValue INT,
    YearBuilt INT,
    Bedrooms INT,
    FullBath INT,
    HalfBath INT
);
"""
cursor.execute(create_table_sql)
connection.commit()

# Capture the start time for measuring execution time
start_time = time.time()

# Define the SQL statement for inserting data, and use "INSERT IGNORE" to skip duplicate entries
insert_sql = f"""
INSERT IGNORE INTO {table_name} (
    UniqueID, ParcelID, LandUse, PropertyAddress, SaleDate, SalePrice, LegalReference, SoldAsVacant,
    OwnerName, OwnerAddress, Acreage, TaxDistrict, LandValue, BuildingValue, TotalValue, YearBuilt,
    Bedrooms, FullBath, HalfBath
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Read and insert data from the CSV file into the table in batches
batch_size = 1000  # Adjust the batch size as needed
batch_data = []

with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        try:
            # Data conversion and formatting
            sale_date = datetime.strptime(row['SaleDate'], '%B %d, %Y').date() if row['SaleDate'] else None
            acreage = float(row['Acreage']) if row['Acreage'] else None
            land_value = int(row['LandValue']) if row['LandValue'] else None
            building_value = int(row['BuildingValue']) if row['BuildingValue'] else None
            total_value = int(row['TotalValue']) if row['TotalValue'] else None
            year_built = int(row['YearBuilt']) if row['YearBuilt'] else None
            bedrooms = int(row['Bedrooms']) if row['Bedrooms'] else None
            full_bath = int(row['FullBath']) if row['FullBath'] else None
            half_bath = int(row['HalfBath']) if row['HalfBath'] else None
            sale_price = int(row['SalePrice'].replace('$', '').replace(' ', '').replace(',', ''))

            # Append the data to the batch
            batch_data.append((
                int(row['UniqueID']),
                row['ParcelID'],
                row['LandUse'],
                row['PropertyAddress'],
                sale_date,
                sale_price,
                row['LegalReference'],
                row['SoldAsVacant'],
                row['OwnerName'],
                row['OwnerAddress'],
                acreage,
                row['TaxDistrict'],
                land_value,
                building_value,
                total_value,
                year_built,
                bedrooms,
                full_bath,
                half_bath
            ))

            # Execute the batch insert if the batch size is reached
            if len(batch_data) >= batch_size:
                cursor.executemany(insert_sql, batch_data)
                connection.commit()
                batch_data = []

        except mysql.connector.errors.IntegrityError:
            # Handle integrity error (duplicate entry) by continuing to the next row
            pass

    # Insert any remaining rows into the table
    if batch_data:
        cursor.executemany(insert_sql, batch_data)
        connection.commit()

# Capture the end time
end_time = time.time()
# Calculate the execution time
execution_time = end_time - start_time

# Close the database connection
connection.close()

# Print completion message and execution time
print("Data insertion completed.")
print(f"Execution time: {execution_time} seconds")
