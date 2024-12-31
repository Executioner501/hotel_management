-- HOTEL_BRANCH Table
CREATE TABLE HOTEL_BRANCH (
    branch_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    planned_revenue DECIMAL(15, 2),
    planned_expenditure DECIMAL(15, 2)
);

-- CHEF Table
CREATE TABLE CHEF (
    ssn VARCHAR(15) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    join_date DATE NOT NULL,
    specialty_cuisine VARCHAR(50)
);

-- CHEF_ASSIGNMENT Table
CREATE TABLE CHEF_ASSIGNMENT (
    assignment_id INT PRIMARY KEY,
    branch_id INT NOT NULL,
    chef_ssn VARCHAR(15) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    FOREIGN KEY (branch_id) REFERENCES HOTEL_BRANCH(branch_id),
    FOREIGN KEY (chef_ssn) REFERENCES CHEF(ssn)
);

-- MENU_CARD Table
CREATE TABLE MENU_CARD (
    menu_id INT PRIMARY KEY,
    branch_id INT NOT NULL,
    menu_name VARCHAR(100) NOT NULL,
    last_updated DATE,
    FOREIGN KEY (branch_id) REFERENCES HOTEL_BRANCH(branch_id)
);

-- DISH Table
CREATE TABLE DISH (
    dish_id INT PRIMARY KEY,
    menu_id INT NOT NULL,
    chef_ssn VARCHAR(15) NOT NULL,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES MENU_CARD(menu_id),
    FOREIGN KEY (chef_ssn) REFERENCES CHEF(ssn)
);

-- Corrected DISH_DETAIL Table
CREATE TABLE DISH_DETAIL (
    menu_id INT PRIMARY KEY,
    cuisine_type VARCHAR(50) NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES MENU_CARD(menu_id)
);

-- FINANCIAL_RECORD Table
CREATE TABLE FINANCIAL_RECORD (
    record_id INT PRIMARY KEY,
    branch_id INT NOT NULL,
    record_date DATE NOT NULL,
    actual_revenue DECIMAL(15, 2) CHECK (actual_revenue >= 50000.00),
    actual_expenditure DECIMAL(15, 2) CHECK (actual_expenditure >= 50000.00),
    performance_notes TEXT,
    FOREIGN KEY (branch_id) REFERENCES HOTEL_BRANCH(branch_id)
);


-- Insert data into HOTEL_BRANCH
INSERT INTO HOTEL_BRANCH (branch_id, name, city, state, start_date, planned_revenue, planned_expenditure)
VALUES
(1, 'Luxury Stay', 'New York', 'NY', '2015-05-01', 500000.00, 300000.00),
(2, 'Cozy Retreat', 'Los Angeles', 'CA', '2018-08-15', 400000.00, 250000.00),
(3, 'Urban Comfort', 'Chicago', 'IL', '2020-03-10', 450000.00, 280000.00);

-- Insert data into CHEF
INSERT INTO CHEF (ssn, name, join_date, specialty_cuisine)
VALUES
('C101', 'John Doe', '2016-02-20', 'Italian'),
('C102', 'Jane Smith', '2018-11-10', 'Chinese'),
('C103', 'Carlos Vega', '2019-07-25', 'Continental');

-- Insert data into CHEF_ASSIGNMENT
INSERT INTO CHEF_ASSIGNMENT (assignment_id, branch_id, chef_ssn, start_date, end_date)
VALUES
(1, 1, 'C101', '2016-03-01', NULL),
(2, 2, 'C102', '2018-12-01', NULL),
(3, 3, 'C103', '2019-08-01', NULL),
(4, 1, 'C103', '2020-01-15', '2021-06-30');

-- Insert data into MENU_CARD
INSERT INTO MENU_CARD (menu_id, branch_id, menu_name, last_updated)
VALUES
(1, 1, 'Italian Classics', '2023-01-10'),
(2, 2, 'Chinese Delights', '2023-02-20'),
(3, 3, 'Continental Specials', '2023-03-05');

-- Insert data into DISH
INSERT INTO DISH (dish_id, menu_id, chef_ssn, name, price)
VALUES
    (1, 1, 'C101', 'Spaghetti Carbonara', 15.99),
    (2, 1, 'C101', 'Margherita Pizza', 12.49),
    (3, 2, 'C102', 'Kung Pao Chicken', 14.50),
    (4, 2, 'C102', 'Spring Rolls', 8.75),
    (5, 3, 'C103', 'Beef Stroganoff', 18.25),
    (6, 3, 'C103', 'Grilled Chicken', 16.75),
    (7, 1, 'C101', 'Lasagna', 17.50),
    (8, 1, 'C101', 'Caprese Salad', 10.00),
    (9, 2, 'C102', 'Sweet and Sour Pork', 15.00),
    (10, 2, 'C102', 'Noodles with Shrimp', 13.75),
    (11, 3, 'C103', 'Pork Schnitzel', 19.00),
    (12, 3, 'C103', 'Caesar Salad', 11.50),
    (13, 1, 'C101', 'Tiramisu', 6.50),
    (14, 2, 'C102', 'Dumplings', 9.00),
    (15, 3, 'C103', 'Apple Strudel', 8.00),
    (16, 1, 'C101', 'Risotto', 16.00),
    (17, 2, 'C102', 'Hot and Sour Soup', 7.50),
    (18, 3, 'C103', 'Sausage and Mash', 17.00),
    (19, 1, 'C101', 'Fettuccine Alfredo', 15.75),
    (20, 3, 'C103', 'Vegetarian Gnocchi', 14.00);

-- Corrected Insert data into DISH_DETAIL
INSERT INTO DISH_DETAIL (menu_id, cuisine_type)
VALUES
(1, 'Italian'),
(2, 'Chinese'),
(3, 'Continental');

-- Insert data into FINANCIAL_RECORD
INSERT INTO FINANCIAL_RECORD (record_id, branch_id, record_date, actual_revenue, actual_expenditure, performance_notes)
VALUES
(1, 1, '2023-06-30', 550000.00, 320000.00, 'Exceeded planned revenue by 10%'),
(2, 2, '2023-06-30', 390000.00, 260000.00, 'Slightly underperformed in revenue'),
(3, 3, '2023-06-30', 460000.00, 290000.00, 'Met planned expectations');
