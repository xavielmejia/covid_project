/* Table creation COVID database */
USE COVID
GO
CREATE TABLE covidCountries
(
	id INT IDENTITY(1,1),
	name VARCHAR(255),
	slug VARCHAR(255),
	iso2 VARCHAR(10),
	createdDate date
)
GO
CREATE TABLE covidCases
(
	id INT IDENTITY(1,1),
	countryName VARCHAR(255),
	countryCode VARCHAR(255),
	province VARCHAR(255),
	city VARCHAR(255),
	cityCode VARCHAR(255),
	latitutde VARCHAR(255),
	longitude VARCHAR(255),
	confirmed VARCHAR(255),
	deaths VARCHAR(255),
	recovered VARCHAR(255),
	active VARCHAR(255),
	date varchar(255),
	createdDate date
)
