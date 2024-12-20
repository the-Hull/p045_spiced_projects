\c northwind

SET DateStyle TO ISO, DMY;

DROP TABLE IF EXISTS shippers CASCADE;
CREATE TABLE IF NOT EXISTS shippers(
    shipper_id SERIAL PRIMARY KEY,
    company_name VARCHAR( 20 ) NOT NULL,
    phone_numner VARCHAR( 20 ) NOT NULL

);

\copy shippers FROM '/home/alex/_work/p045_spiced/nlpoblano-student-code/05_week/00_data/northwind_data_clean/data/shippers.csv' DELIMITER ',' CSV HEADER; 

DROP TABLE IF EXISTS orders CASCADE;
CREATE TABLE IF NOT EXISTS orders(
    order_id SMALLINT PRIMARY KEY NOT NULL,
    customer_id VARCHAR ( 5 ) NOT NULL,
    employee_id SMALLINT NOT NULL,
    order_date TIMESTAMP,
    required_date TIMESTAMP,
    shipped_date TIMESTAMP,
    ship_via SMALLINT NOT NULL,
    freight NUMERIC NOT NULL,
    ship_name TEXT NOT NULL,
    ship_address TEXT NOT NULL,
    ship_city TEXT NOT NULL,
    ship_region TEXT,
    ship_postal_code TEXT,
    ship_country TEXT NOT NULL,

    FOREIGN KEY(employee_id)
      REFERENCES employees(employee_id), 
    FOREIGN KEY(customer_id)
        REFERENCES customers(customerID),
    FOREIGN KEY(ship_via)
        REFERENCES shippers(shipper_id)

      
);

\copy orders FROM '/home/alex/_work/p045_spiced/nlpoblano-student-code/05_week/00_data/northwind_data_clean/data/orders.csv' DELIMITER ',' CSV HEADER NULL AS 'NULL'; 






DROP TABLE IF EXISTS order_details CASCADE;
CREATE TABLE IF NOT EXISTS order_details(
    order_id SMALLINT,
    product_id SMALLINT,
    unit_price NUMERIC,
    quantity SMALLINT,
    discount NUMERIC,


    FOREIGN KEY(order_id)
      REFERENCES orders(order_id) 

);

\copy order_details FROM '/home/alex/_work/p045_spiced/nlpoblano-student-code/05_week/00_data/northwind_data_clean/data/order_details.csv' DELIMITER ',' CSV HEADER; 


DROP TABLE IF EXISTS employees CASCADE;
CREATE TABLE IF NOT EXISTS employees(
    employee_id SERIAL PRIMARY KEY,
    last_name TEXT,
    first_name TEXT,
    title TEXT,
    title_of_courtesy TEXT,
    birth_date TIMESTAMP,
    hire_date TIMESTAMP,
    address TEXT,
    city TEXT,
    region TEXT,
    postal_code TEXT,
    country TEXT,
    home_phone TEXT,
    extension TEXT,
    photo BYTEA,
    notes TEXT,
    reports_to SMALLINT,
    photo_path TEXT

);

\copy employees FROM '/home/alex/_work/p045_spiced/nlpoblano-student-code/05_week/00_data/northwind_data_clean/data/employees.csv' DELIMITER ',' CSV HEADER NULL 'NULL';

DROP TABLE IF EXISTS products CASCADE;
CREATE TABLE IF NOT EXISTS products(
    productID SERIAL PRIMARY KEY,
    productName TEXT,
    supplierID TEXT,
    categoryID TEXT,
    quantityPerUnit TEXT,
    unitPrice NUMERIC,
    unitsInStock NUMERIC,
    unitsOnOrder NUMERIC,
    reorderLevel NUMERIC,
    discontinued BOOL


);



\copy products FROM '/home/alex/_work/p045_spiced/nlpoblano-student-code/05_week/00_data/northwind_data_clean/data/products.csv' DELIMITER ',' CSV HEADER NULL 'NULL';



DROP TABLE IF EXISTS customers CASCADE;
CREATE TABLE IF NOT EXISTS customers(
    customerID VARCHAR (10) PRIMARY KEY,
    companyName TEXT,
    contactName TEXT,
    contactTitle TEXT,
    customer_address TEXT,
    city TEXT,
    region TEXT,
    postalCode TEXT,
    country TEXT,
    phone TEXT,
    fax TEXT


);



\copy customers FROM '/home/alex/_work/p045_spiced/nlpoblano-student-code/05_week/00_data/northwind_data_clean/data/customers.csv' DELIMITER ',' CSV HEADER NULL 'NULL';








DROP TABLE IF EXISTS order_totals CASCADE;
DROP TABLE IF EXISTS employee_activity CASCADE;
DROP TABLE IF EXISTS customer_activity CASCADE;






SELECT order_id,  SUM(unit_price * quantity) as total_price INTO order_totals FROM order_details GROUP BY order_id;

SELECT ord.employee_id, COUNT(ord.order_id) as total_orders, SUM(ot.total_price) as total_revenue INTO employee_activity
    FROM orders AS ord
    JOIN order_totals AS ot
    ON ord.order_id = ot.order_id
    GROUP BY ord.employee_id;


SELECT 
    COUNT(ot.order_id), 
    SUM(ot.total_price) as total_revenue,
    od.customer_id,
    MIN(cu.companyname) as companyname,
    MIN(od.ship_country) as country,
    MIN(od.ship_via) as shippername
    INTO customer_activity
    FROM order_totals AS ot
    RIGHT JOIN orders AS od ON ot.order_id = od.order_id
    LEFT JOIN customers AS cu ON od.customer_id = cu.customerid
    GROUP BY od.customer_id
    ORDER BY total_revenue DESC;

-- SELECT *, ROUND(total_revenue/total_orders, 2) AS sale_efficiency 
--     FROM employee_activity 
--     ORDER BY sale_efficiency DESC;    


-- Find the hiring age of each employee
CREATE OR REPLACE VIEW employee_age AS
SELECT 
    AGE(hire_date, birth_date) as hiring_age, 
    CONCAT(title_of_courtesy, ' ', first_name, ' ', last_name) as full_name,
    employee_id 
    FROM employees;

SELECT * FROM employee_age;


-- SELECT customer_id, AVG(freight) as freight_avg FROM orders
--     GROUP BY
--         customer_id
--     ORDER BY
--         freight_avg
--         DESC
--     LIMIT 5;
        
-- SELECT employee_id, COUNT(employee_id) as n_sales FROM orders
--     GROUP BY employee_id
--     ORDER BY employee_id;


-- SELECT customer_id, ship_address, ship_country, COUNT(customer_id) as n_purchases FROM orders
--     GROUP BY customer_id, ship_address,ship_country
--     ORDER BY n_purchases DESC
--     LIMIT 10;
