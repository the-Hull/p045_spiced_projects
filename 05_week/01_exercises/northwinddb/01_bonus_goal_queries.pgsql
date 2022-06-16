-- Get the names and the quantities in stock for each product.
-- SELECT (productname, unitsinstock) FROM products;

-- Get a list of current products (Product ID and name).
-- SELECT (productid, productname) FROM products;


-- Get a list of the most and least expensive products (name and unit price).
-- SELECT productid, unitprice FROM products
--     WHERE unitprice = (select MIN(unitprice) FROM products) OR unitprice = (select MAX(unitprice) FROM products)
-- ;

-- Get products that cost less than $20.
-- SELECT productid, productname, unitprice FROM products
--     WHERE products.unitprice < 20;

-- -- Get products that cost between $15 and $25.
-- SELECT productname, unitprice FROM products
--     WHERE unitprice BETWEEN 15 AND 25;

-- Get products above average price.
-- SELECT productname, unitprice FROM products
--     WHERE unitprice > (select AVG(unitprice) FROM products);

-- Find the ten most expensive products.
-- SELECT productname, unitprice FROM products
--     ORDER BY unitprice DESC
--     LIMIT 10;

-- Get a list of discontinued products (Product ID and name).
-- SELECT productname, discontinued FROM products
--     WHERE discontinued = true;

-- Count current and discontinued products.
-- SELECT COUNT(productname), discontinued FROM products
--     GROUP BY discontinued;

-- Find products with less units in stock than the quantity on order.
SELECT productname, unitsonorder, unitsinstock FROM products
    WHERE unitsonorder > unitsinstock;

-- Find the customer who had the highest order amount

-- Get orders for a given employee and the according customer

-- Find the hiring age of each employee

-- Create views and/or named queries for some of these queries

