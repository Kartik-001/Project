import csv
import json
import mysql.connector
from datetime import datetime

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

# CSV file path
csv_file = 'Nashville_Housing_Data.csv'

# Connect to MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Create the MySQL table (if it doesn't exist)
create_table_sql = """
CREATE TABLE IF NOT EXISTS PropertySales (
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

# Read and insert data from the CSV file
with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        sale_date = datetime.strptime(row['SaleDate'], '%B %d, %Y').date()
        acreage = float(row['Acreage']) if row['Acreage'] else None
        land_value = int(row['LandValue']) if row['LandValue'] else None
        building_value = int(row['BuildingValue']) if row['BuildingValue'] else None
        total_value = int(row['TotalValue']) if row['TotalValue'] else None
        year_built = int(row['YearBuilt']) if row['YearBuilt'] else None
        bedrooms = int(row['Bedrooms']) if row['Bedrooms'] else None
        full_bath = int(row['FullBath']) if row['FullBath'] else None
        half_bath = int(row['HalfBath']) if row['HalfBath'] else None

        # Remove dollar sign and spaces and comma, and then convert SalePrice to an integer
        sale_price = int(row['SalePrice'].replace('$', '').replace(' ', '').replace(',',''))

        insert_sql = """
        INSERT INTO PropertySales (
            UniqueID, ParcelID, LandUse, PropertyAddress, SaleDate, SalePrice, LegalReference, SoldAsVacant,
            OwnerName, OwnerAddress, Acreage, TaxDistrict, LandValue, BuildingValue, TotalValue, YearBuilt,
            Bedrooms, FullBath, HalfBath
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (
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
        connection.commit()

# Close the database connection
connection.close()

print("Data insertion completed.")
