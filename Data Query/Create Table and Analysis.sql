-- Create Transaction Table
CREATE TABLE transaction(
	TransactionID character(50),
	CustomerID character(50),
	Date date,
	ProductID character(50),
	Price numeric,
	Qty numeric,
	TotalAmount numeric,
	StoreID character(50)
);

-- Create Store Table
CREATE TABLE store(
	StoreID character(50),
	StoreName character(50),
	GroupStore character(50),
	Type character(50),
	Latitude numeric,
	Longitude numeric,
	primary key (StoreID)
);

-- Create Customer Table
CREATE TABLE customer(
	CustomerID character(50),
	Age numeric,
	Gender character(50),
	MaritalStatus character(50),
	Income numeric,
	primary key (CustomerID)
);

-- Imputate missing value in Maritalstatus
UPDATE CUSTOMER SET MARITALSTATUS = 'Not Mentioned'
WHERE MARITALSTATUS IS NULL;

-- REPLACE 0 Female and  1 Male in Gender
ALTER TABLE CUSTOMER
ALTER COLUMN GENDER TYPE character(20);

UPDATE CUSTOMER SET GENDER = 'Female'
WHERE GENDER = '0' ;

UPDATE CUSTOMER SET GENDER = 'Male'
WHERE GENDER = '1' ;

-- Create Product Table
CREATE TABLE product(
	ProductID character(50),
	ProductName character(50),
	Price numeric,
	primary key (ProductID)
);

-- Define table relation
ALTER TABLE transaction ADD FOREIGN KEY (customerid) REFERENCES customer (customerid) 
	,ADD FOREIGN KEY (productid) REFERENCES product (productid)
	,ADD FOREIGN KEY (storeid) REFERENCES store (storeid);

-- Berapa rata-rata umur customer jika dilihat dari marital statusnya ?
SELECT MARITALSTATUS, ROUND(AVG(AGE),2) AVG_AGE
FROM CUSTOMER 
GROUP BY MARITALSTATUS
ORDER BY AVG_AGE;

-- Berapa rata-rata umur customer jika dilihat dari gender nya ?
SELECT GENDER, ROUND(AVG(AGE),2) AVG_AGE
FROM CUSTOMER 
GROUP BY GENDER
ORDER BY AVG_AGE;

-- Tentukan nama store dengan total quantity terbanyak!
SELECT S.STORENAME, SUM(T.QTY) TOTAL_QTY
FROM TRANSACTION T LEFT JOIN STORE S ON T.STOREID = S.STOREID
GROUP BY S.STORENAME
ORDER BY TOTAL_QTY DESC LIMIT 1;

-- Tentukan nama produk terlaris dengan total amount terbanyak!
SELECT P.PRODUCTNAME, SUM(T.TOTALAMOUNT) TOTAL_AMOUNT
FROM TRANSACTION T LEFT JOIN PRODUCT P ON T.PRODUCTID = P.PRODUCTID
GROUP BY P.PRODUCTNAME
ORDER BY TOTAL_AMOUNT DESC LIMIT 1;
