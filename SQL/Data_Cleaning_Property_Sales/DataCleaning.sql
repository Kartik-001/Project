-- Step 1: Data Exploration and Summary

-- Count the total number of rows in the dataset
SELECT COUNT(*) FROM nashville_housing.propertysales;

-- Display the first 10 rows for initial inspection
SELECT * FROM nashville_housing.propertysales LIMIT 10;

-- Step 2: Identifying Duplicates

-- Display distinct rows to identify duplicates
SELECT DISTINCT * FROM nashville_housing.propertysales;

-- Count the number of distinct unique IDs
SELECT COUNT(DISTINCT uniqueid) FROM nashville_housing.propertysales;

-- Step 3: Data Splitting

-- Split 'propertyaddress' into 'propertyaddress' and 'propertycity'
SELECT
    propertyaddress,
    SUBSTRING(propertyaddress, 1, LOCATE(',', propertyaddress) - 1) AS propertyaddress,
    SUBSTRING(propertyaddress, LOCATE(',', propertyaddress) + 1) AS propertycity
FROM
    nashville_housing.propertysales;

-- Add 'propertysplitaddress' and 'propertysplitcity' columns to the table
ALTER TABLE nashville_housing.propertysales
ADD COLUMN propertysplitaddress VARCHAR(255),
ADD COLUMN propertysplitcity VARCHAR(255);

-- Update 'propertysplitaddress' with the portion before the comma
UPDATE nashville_housing.propertysales
SET propertysplitaddress = SUBSTRING(propertyaddress, 1, LOCATE(',', propertyaddress) - 1);

-- Update 'propertysplitcity' with the portion after the comma
UPDATE nashville_housing.propertysales
SET propertysplitcity = SUBSTRING(propertyaddress, LOCATE(',', propertyaddress) + 1);

-- Split 'owneraddress' into 'ownersplitaddress', 'ownersplitcity', and 'ownersplitstate'
SELECT
    owneraddress,
    SUBSTRING_INDEX(owneraddress, ',', 1) AS ownersplitaddress,
    SUBSTRING_INDEX(SUBSTRING_INDEX(owneraddress, ',', 2), ',', -1) AS ownersplitcity,
    SUBSTRING_INDEX(owneraddress, ',', -1) AS ownersplitstate
FROM
    nashville_housing.propertysales;

-- Add 'ownersplitaddress', 'ownersplitcity', and 'ownersplitstate' columns to the table
ALTER TABLE nashville_housing.propertysales
ADD COLUMN ownersplitaddress VARCHAR(255),
ADD COLUMN ownersplitcity VARCHAR(50),
ADD COLUMN ownersplitstate VARCHAR(50);

-- Update 'ownersplitaddress' with the first part of 'owneraddress'
UPDATE nashville_housing.propertysales
SET ownersplitaddress = SUBSTRING_INDEX(owneraddress, ',', 1);

-- Update 'ownersplitcity' with the second part of 'owneraddress'
UPDATE nashville_housing.propertysales
SET ownersplitcity = SUBSTRING_INDEX(SUBSTRING_INDEX(owneraddress, ',', -2), ',', 1);

-- Update 'ownersplitstate' with the last part of 'owneraddress'
UPDATE nashville_housing.propertysales
SET ownersplitstate = SUBSTRING_INDEX(owneraddress, ',', -1);

-- Step 4: Value Transformation

-- Change 'soldasvacant' values from 'Y' to 'Yes' and 'N' to 'No'
SELECT DISTINCT(soldasvacant), COUNT(soldasvacant)
FROM nashville_housing.propertysales
GROUP BY soldasvacant
ORDER BY 2;

UPDATE nashville_housing.propertysales
SET soldasvacant = CASE 
    WHEN soldasvacant = 'Y' THEN 'Yes'
    WHEN soldasvacant = 'N' THEN 'No'
    ELSE soldasvacant
END;

-- Step 5: Removing Duplicate Rows

-- Identify and delete duplicate rows based on specified columns
WITH rownumcte AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY parcelid, propertyaddress, saleprice, saledate, legalreference
               ORDER BY uniqueid
           ) AS row_num
    FROM nashville_housing.propertysales
)
DELETE
FROM rownumcte
WHERE row_num > 1;

-- Display the cleaned dataset with duplicates removed
WITH rownumcte AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY parcelid, propertyaddress, saleprice, saledate, legalreference
               ORDER BY uniqueid
           ) AS row_num
    FROM nashville_housing.propertysales
)
SELECT *
FROM rownumcte
WHERE row_num = 1;
