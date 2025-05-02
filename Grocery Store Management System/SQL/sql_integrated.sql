-- EMPLOYEE
-- INVENTORY MANAGER
DROP TABLE delivery;
DROP TABLE contract;
-- DROP TABLE Inventory_Order;
DROP TABLE Vendor;
drop table creates_restock;
drop table receives_restock;
drop table restock_report;
drop table creates_schedule;
drop table shift_schedule;
drop table coordinates;
drop table campaign; 
drop table employee_store;
drop table manages_store;
drop table budget_manager;
drop table store_manager;
DROP TABLE store;
drop table contactus;
drop table opt_in;
drop table sets;
drop table login;
drop table leaves;
drop table setup;
drop table browse;
drop table Message_Type;
drop table Messages;
drop table Preferences;
drop table Subscription;
drop table Account;
drop table Review;
drop table Return_Request;
drop table checkout;
drop table paid;
drop table payment_regist;
drop table order_items;
drop table orders;
drop table cart;
drop table member;
drop table non_member;
drop table customer;
DROP TABLE inventory_alerts_send;
drop table shelf_alerts_send;
drop table load_on;
drop table handle;
drop table shelf;
drop table work_record;
DROP TABLE commodity_store;
DROP TABLE monitor;
DROP TABLE inventory;
DROP TABLE employee;

CREATE TABLE employee (
    ssn VARCHAR(9),
    name VARCHAR(50),
    birthday DATE,
    salary DECIMAL(10, 2),
    position VARCHAR(20),
    password varchar(20),
    PRIMARY KEY (ssn)
);

INSERT INTO employee (ssn, name, birthday, salary, POSITION, password) VALUES
('12305456', 'Henry', TO_DATE('1989/06/04 00:00:00', 'yyyy/mm/dd hh24:mi:ss'), 70000, 'inventory_manager', 'abc');
INSERT INTO employee (ssn, name, birthday, salary, POSITION, password) VALUES
('22305456', 'Bob', TO_DATE('1995/06/04 00:00:00', 'yyyy/mm/dd hh24:mi:ss'), 70000, 'cashier', 'abc');
INSERT INTO employee (ssn, name, birthday, salary, POSITION, password) VALUES
('32305456', 'Mike', TO_DATE('1996/06/04 00:00:00', 'yyyy/mm/dd hh24:mi:ss'), 80000, 'custodian', 'abc');
INSERT INTO employee (ssn, name, birthday, salary, POSITION, password) VALUES
('42305456', 'Oliver', TO_DATE('1996/12/04 00:00:00', 'yyyy/mm/dd hh24:mi:ss'), 80000, 'stock_clerk', 'abc');

SELECT * FROM employee;


CREATE TABLE inventory(
    iid VARCHAR(10),
    location VARCHAR(30),
    PRIMARY KEY (iid)
);

INSERT INTO inventory (iid, location) VALUES ('001', '123 highland street');
INSERT INTO inventory (iid, location) VALUES ('003', '145 main street');

SELECT * FROM inventory;


CREATE TABLE monitor(
    ssn VARCHAR(9),
    iid VARCHAR(10),
    assigned_date DATE,
    PRIMARY KEY (ssn, iid),
    FOREIGN KEY (ssn) REFERENCES employee(ssn),
    FOREIGN KEY (iid) REFERENCES inventory(iid)
);

INSERT INTO monitor (ssn, iid, assigned_date) VALUES ('12305456', '001', TO_DATE('2024/08/08 00:00:00', 'yyyy/mm/dd hh24:mi:ss'));
INSERT INTO monitor (ssn, iid, assigned_date) VALUES ('12305456', '003', TO_DATE('2024/08/08 00:00:00', 'yyyy/mm/dd hh24:mi:ss'));

SELECT * FROM monitor;




CREATE TABLE commodity_store(
    commodityID varchar(10),
    name VARCHAR(50),
    price DECIMAL(10, 2),
    category VARCHAR(10),
    discount DECIMAL(10, 2),
    expDate DATE,
    quantity DECIMAL(10, 2),
    threshold DECIMAL(10, 2),
    iid VARCHAR(10) NOT NULL,
    brand VARCHAR(50),
    dietaryrestric VARCHAR(50),
    PRIMARY KEY (commodityID),
    FOREIGN KEY (iid) REFERENCES inventory(iid)
);
-- VEGETABLES
INSERT INTO commodity_store (commodityID, name, price, category, discount, expDate, quantity, threshold, iid, brand, dietaryrestric)
VALUES 
('2001', 'Spinach', 2.49, 'Vegetables', 0.1, SYSDATE + 5, 40, 10, '001', 'GreenHarvest', 'Vegan');
INSERT INTO commodity_store (commodityID, name, price, category, discount, expDate, quantity, threshold, iid, brand, dietaryrestric)
VALUES 
('2002', 'Broccoli', 2.99, 'Vegetables', 0.15, SYSDATE + 6, 35, 8, '003', 'OrganicFarm', 'Gluten-Free');
INSERT INTO commodity_store (commodityID, name, price, category, discount, expDate, quantity, threshold, iid, brand, dietaryrestric)
VALUES 
('2003', 'Bell Peppers', 3.29, 'Vegetables', 0.1, SYSDATE + 5, 50, 15, '003', 'VeggieFresh', 'Vegan');

-- FRUITS
INSERT INTO commodity_store (commodityID, name, price, category, discount, expDate, quantity, threshold, iid, brand, dietaryrestric)
VALUES 
('3001', 'Bananas', 1.49, 'Fruits', 0.05, SYSDATE + 4, 60, 20, '001', 'TropiFresh', 'Vegan');
INSERT INTO commodity_store (commodityID, name, price, category, discount, expDate, quantity, threshold, iid, brand, dietaryrestric)
VALUES 
('3002', 'Apples', 2.19, 'Fruits', 0.1, SYSDATE + 6, 70, 25, '001', 'FreshFarm', 'Vegan');
INSERT INTO commodity_store (commodityID, name, price, category, discount, expDate, quantity, threshold, iid, brand, dietaryrestric)
VALUES 
('3003', 'Blueberries', 3.99, 'Fruits', 0.15, SYSDATE + 7, 40, 10, '003', 'BerryGood', 'Gluten-Free');

-- MEAT
INSERT INTO commodity_store (commodityID, name, price, category, discount, expDate, quantity, threshold, iid, brand, dietaryrestric)
VALUES 
('4001', 'Chicken Breast', 5.99, 'Meat', 0.2, SYSDATE + 4, 30, 10, '001', 'FarmFresh', 'None');
INSERT INTO commodity_store (commodityID, name, price, category, discount, expDate, quantity, threshold, iid, brand, dietaryrestric)
VALUES 
('4002', 'Ground Beef', 6.49, 'Meat', 0.1, SYSDATE + 5, 25, 8, '001', 'ButcherBlock', 'None');
INSERT INTO commodity_store (commodityID, name, price, category, discount, expDate, quantity, threshold, iid, brand, dietaryrestric)
VALUES 
('4003', 'Salmon Fillet', 8.99, 'Meat', 0.25, SYSDATE + 3, 20, 5, '003', 'SeaHarvest', 'Pescatarian');




SELECT * FROM commodity_store;

select * from commodity_store where commodityID = '001';

CREATE TABLE inventory_alerts_send(
    alertID VARCHAR(10),
    send_date DATE,
    commodityID VARCHAR(10),
    description VARCHAR(50),
    iid VARCHAR(10) NOT NULL,
    PRIMARY KEY (alertID),
    FOREIGN KEY (iid) REFERENCES inventory(iid)
);

DROP TRIGGER inventory_alerts;
CREATE TRIGGER inventory_alerts
AFTER UPDATE ON commodity_store
FOR EACH ROW
BEGIN
    IF (:new.quantity < :new.threshold) THEN
        INSERT INTO inventory_alerts_send (alertID, send_date, commodityID, description, iid)
        VALUES (dbms_random.string('p',10), SYSDATE, :new.commodityID, 'Low stock alert', :new.iid);
    END IF;
END;


UPDATE commodity_store
SET quantity = quantity - 1
WHERE commodityID = '1234567890';

SELECT * FROM inventory_alerts_send;

CREATE TABLE work_record (
    ssn VARCHAR(9),
    work_date DATE,
    type VARCHAR(10),
    device VARCHAR(10),
    PRIMARY KEY (ssn, work_date),
    FOREIGN KEY (ssn) REFERENCES employee(ssn) on delete cascade
);

SELECT  * FROM work_record;
DELETE FROM work_record;

CREATE TABLE shelf(
    shelfID VARCHAR(10),
    location VARCHAR(10),
    capacity INT,
    PRIMARY KEY (shelfID)
);

INSERT INTO shelf(shelfID, location, capacity) VALUES ('001', 'North01', 60);
INSERT INTO shelf(shelfID, location, capacity) VALUES ('002', 'South01', 50);
INSERT INTO shelf(shelfID, location, capacity) VALUES ('003', 'West01', 70);

CREATE TABLE handle(
    ssn VARCHAR(9),
    shelfID VARCHAR(10),
    PRIMARY KEY (ssn, shelfID),
    FOREIGN KEY (ssn) REFERENCES employee(ssn),
    FOREIGN KEY (shelfID) REFERENCES shelf(shelfID)
);

INSERT INTO handle(ssn, shelfID) VALUES ('42305456', '001');
INSERT INTO handle(ssn, shelfID) VALUES ('42305456', '002');
INSERT INTO handle(ssn, shelfID) VALUES ('42305456', '003');

CREATE TABLE load_on(
    shelfID VARCHAR(10),
    commodityID VARCHAR(10),
    quantity DECIMAL(10, 2),
    threshold DECIMAL(10, 2),
    PRIMARY KEY (shelfID, commodityID),
    FOREIGN KEY (shelfID) REFERENCES shelf(shelfID),
    FOREIGN KEY (commodityID) REFERENCES commodity_store(commodityID)
);

INSERT INTO load_on(shelfID, commodityID, quantity, threshold) VALUES
('001', '1234567890', 10, 2);
INSERT INTO load_on(shelfID, commodityID, quantity, threshold) VALUES
('002', '12305456', 20, 5);

CREATE TABLE shelf_alerts_send(
    id varchar(10),
    send_date DATE,
    commodityID VARCHAR(10),
    description VARCHAR(50),
    shelfID VARCHAR(10) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (shelfID) REFERENCES shelf(shelfID)
);
CREATE TRIGGER shelf_alerts
AFTER UPDATE ON load_on
FOR EACH ROW
BEGIN
    IF (:new.quantity < :new.threshold) THEN
        INSERT INTO shelf_alerts_send (id, send_date, commodityID, description, shelfID)
        VALUES (dbms_random.string('p',10), SYSDATE, :new.commodityID, 'Low stock alert', :new.shelfID);
    END IF;
END;

UPDATE load_on 
SET quantity = quantity - 9
WHERE commodityID = '1234567890';

SELECT * FROM shelf_alerts_send;

SELECT *
FROM (
    SELECT A.commodityID, A.quantity, A.threshold, B.name
    FROM (SELECT commodityID, quantity, threshold FROM load_on WHERE shelfID = '001') A
    JOIN (SELECT commodityID, name FROM commodity_store) B
    ON A.commodityID = B.commodityID
) C
JOIN (
    SELECT commodityID, send_date, DESCRIPTION 
    FROM shelf_alerts_send
    WHERE shelfID = '001'
) D
ON C.commodityID = D.commodityID;

CREATE TABLE maintenance_region(
    regionID VARCHAR(10),
    location VARCHAR(10),
    area INT,
    PRIMARY KEY (regionID)
);
INSERT INTO maintenance_region(regionID, location, area) VALUES ('001', 'North01', 1);
INSERT INTO maintenance_region(regionID, location, area) VALUES ('002', 'West01', 2);
INSERT INTO maintenance_region(regionID, location, area) VALUES ('003', 'South01', 3);

CREATE TABLE maintain(
    ssn VARCHAR(9),
    regionID VARCHAR(10),
    PRIMARY KEY (ssn, regionID),
    FOREIGN KEY (ssn) REFERENCES employee(ssn),
    FOREIGN KEY (regionID) REFERENCES maintenance_region(regionID)
);
INSERT INTO maintain(ssn, regionID) VALUES ('32305456', '001');
INSERT INTO maintain(ssn, regionID) VALUES ('32305456', '002');

-- CUSTOMER

CREATE TABLE customer (
    custID varchar(50),
    primary key (custID)
);

CREATE TABLE non_member (
    custID varchar(50),
    primary key (custID),
    foreign key (custID) references customer(custID)
);

CREATE TABLE member (
    custID varchar(50),
    startDate date,
    expDate date,
    loyaltyPoints decimal(10,2),
    primary key (custID),
    foreign key (custID) references customer(custID)
);

CREATE TABLE cart(
    custID varchar(50),
    commodityID varchar(10),
    quantity int,
    add_date date,
    primary key (custID, commodityID),
    foreign key (custID) references customer(custID) on delete cascade
);

CREATE TABLE orders (
    orderID VARCHAR(10) PRIMARY KEY,
    order_date DATE,
    delivery_type VARCHAR(10) CHECK (delivery_type IN ('standard', 'express', 'pickup')),
    total_price DECIMAL(10, 2),
    orderstatus VARCHAR(20) DEFAULT 'Pending'
);

CREATE TABLE order_items(
    orderID varchar(10),
    commodityID varchar(10),
    quantity int CHECK (quantity>0),
    name varchar(50),
    primary key (orderID, commodityID),
    foreign key (orderID) references orders(orderID) on delete cascade
);

CREATE TABLE payment_regist(
    custID varchar(50),
    cardID varchar(10),
    card_type varchar(10),
    primary key (custID, cardID),
    foreign key (custID) references customer(custID) on delete cascade
);

CREATE TABLE paid(
    custID varchar(50),
    cardID varchar(10),
    orderID varchar(10),
    pay_status varchar(10),
    primary key (custID, cardID, orderID),
    foreign key (custID, cardID) references payment_regist(custID, cardID),
    foreign key (orderID) references orders(orderID)
);

CREATE TABLE checkout(
    custID varchar(50),
    orderID varchar(10),
    date_shipped date,
    primary key (custID, orderID),
    foreign key (custID) references customer(custID),
    foreign key (orderID) references orders(orderID)
);

CREATE TABLE Return_Request(
returnID NUMBER PRIMARY KEY, 
orderID varchar(10), 
returnReason CLOB, 
dateCreated DATE, 
status VARCHAR2(50),
custID varchar(50),
FOREIGN KEY(orderID) REFERENCES orders,
FOREIGN KEY (custID) REFERENCES customer(custID)
);


CREATE TABLE Review(
  reviewID NUMBER PRIMARY KEY,
  commodityID varchar(10),
  custID VARCHAR(50),
  rating NUMBER NOT NULL,
  review varchar(150), 
  reviewDate DATE
);


CREATE TABLE Account(
createDate DATE, 
phone NUMBER NOT NULL,
password VARCHAR2(50),
email VARCHAR2(50) PRIMARY KEY,
username VARCHAR2(50),
saveditem VARCHAR2(50), 
paypref VARCHAR2(50)
);

CREATE TABLE Subscription(
subscriptionID NUMBER PRIMARY KEY, 
commodityID varchar(10), 
frequency VARCHAR2(50),
status VARCHAR2(50), 
nextdeliverydate DATE,
FOREIGN KEY (commodityID) REFERENCES commodity_store(commodityID)
);

CREATE TABLE Preferences(
prefID NUMBER PRIMARY KEY, 
prefcategory VARCHAR2(50)NOT NULL, 
dietaryrestric VARCHAR2(50), 
prefbrands VARCHAR2(50)
);

CREATE TABLE Messages(
messageID NUMBER PRIMARY KEY, 
content CLOB NOT NULL, 
"date" DATE NOT NULL
);

CREATE TABLE Message_Type(
messageType VARCHAR2(255),
messageID NUMBER,
PRIMARY KEY (messageID, messageType),
FOREIGN KEY (messageID) REFERENCES Messages(messageID) ON DELETE CASCADE
);

CREATE TABLE browse(
browse_date DATE,
custID VARCHAR(50),
commodityID varchar(10),
PRIMARY KEY (custID, commodityID, browse_date), 
FOREIGN KEY (custID) REFERENCES customer(custID),
FOREIGN KEY (commodityID) REFERENCES commodity_store(commodityID)
);

CREATE TABLE setup(
start_date DATE, 
subscriptionID NUMBER,
custID varchar(10),
PRIMARY KEY (custID, subscriptionID),
FOREIGN KEY (custID) REFERENCES Member(custID),
FOREIGN KEY (subscriptionID) REFERENCES Subscription(subscriptionID)
);

CREATE TABLE leaves(
custID VARCHAR(10),
reviewID NUMBER,
PRIMARY KEY(custID, reviewID),
FOREIGN KEY (custID) REFERENCES Member(custID),
FOREIGN KEY(reviewID) REFERENCES Review(reviewID)
);

CREATE TABLE login(
custID VARCHAR(10),
email VARCHAR2(50),
PRIMARY KEY(custID, email),
FOREIGN KEY(custID) REFERENCES Member(custID),
FOREIGN KEY(email) REFERENCES Account(email)
);

CREATE TABLE sets(
custID VARCHAR(10),
prefID NUMBER,
PRIMARY KEY(custID, prefID),
FOREIGN KEY(custID) REFERENCES Member(custID),
FOREIGN KEY(prefID) REFERENCES Preferences(prefID)
);

CREATE TABLE opt_in(
custID VARCHAR(10),
messageID NUMBER,
PRIMARY KEY(custID, messageID),
FOREIGN KEY(custID) REFERENCES Member(custID),
FOREIGN KEY(messageID) REFERENCES Messages(messageID)
);

CREATE TABLE contactus (
    id varchar(10) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    message VARCHAR(100)
);


INSERT INTO customer (custID) VALUES ('CUST001');
INSERT INTO customer (custID) VALUES ('CUST002');
INSERT INTO customer (custID) VALUES ('CUST003');
INSERT INTO customer (custID) VALUES ('CUST004');
INSERT INTO customer (custID) VALUES ('CUST005');
INSERT INTO customer (custID) VALUES ('CUST006');
INSERT INTO customer (custID) VALUES ('CUST007');
INSERT INTO customer (custID) VALUES ('CUST008');
INSERT INTO customer (custID) VALUES ('CUST009');
INSERT INTO customer (custID) VALUES ('CUST010');

INSERT INTO non_member (custID) VALUES ('CUST001');
INSERT INTO non_member (custID) VALUES ('CUST004');
INSERT INTO non_member (custID) VALUES ('CUST005');
INSERT INTO non_member (custID) VALUES ('CUST007');
INSERT INTO non_member (custID) VALUES ('CUST008');

INSERT INTO member (custID, startDate, expDate, loyaltyPoints) VALUES ('CUST002', TO_DATE('2023-01-01', 'YYYY-MM-DD'), TO_DATE('2024-01-01', 'YYYY-MM-DD'), 100.00);
INSERT INTO member (custID, startDate, expDate, loyaltyPoints) VALUES ('CUST003', TO_DATE('2023-05-15', 'YYYY-MM-DD'), TO_DATE('2024-05-15', 'YYYY-MM-DD'), 150.50);
INSERT INTO member (custID, startDate, expDate, loyaltyPoints) VALUES ('CUST006', TO_DATE('2023-10-20', 'YYYY-MM-DD'), TO_DATE('2024-10-20', 'YYYY-MM-DD'), 200.75);
INSERT INTO member (custID, startDate, expDate, loyaltyPoints) VALUES ('CUST009', TO_DATE('2023-02-10', 'YYYY-MM-DD'), TO_DATE('2024-02-10', 'YYYY-MM-DD'), 120.25); 
INSERT INTO member (custID, startDate, expDate, loyaltyPoints) VALUES ('CUST010', TO_DATE('2023-08-01', 'YYYY-MM-DD'), TO_DATE('2024-08-01', 'YYYY-MM-DD'), 180.00);

INSERT INTO cart (custID, commodityID, quantity, add_date) VALUES ('CUST002', '101', 2, TO_DATE('2023-11-20', 'YYYY-MM-DD'));
INSERT INTO cart (custID, commodityID, quantity, add_date) VALUES ('CUST003', '102', 1, TO_DATE('2023-11-21', 'YYYY-MM-DD'));
INSERT INTO cart (custID, commodityID, quantity, add_date) VALUES ('CUST006', '103', 3, TO_DATE('2023-11-22', 'YYYY-MM-DD'));
INSERT INTO cart (custID, commodityID, quantity, add_date) VALUES ('CUST002', '104', 1, TO_DATE('2023-11-23', 'YYYY-MM-DD'));
INSERT INTO cart (custID, commodityID, quantity, add_date) VALUES ('CUST003', '105', 2, TO_DATE('2023-11-24', 'YYYY-MM-DD'));

INSERT INTO orders (orderID, order_date, delivery_type, total_price, orderstatus)
VALUES ('ORD001', TO_DATE('2023-11-22', 'YYYY-MM-DD'), 'standard', 50.00, 'Processing');

INSERT INTO orders (orderID, order_date, delivery_type, total_price, orderstatus)
VALUES ('ORD002', TO_DATE('2023-11-23', 'YYYY-MM-DD'), 'express', 120.50, 'Shipped');

INSERT INTO orders (orderID, order_date, delivery_type, total_price, orderstatus)
VALUES ('ORD003', TO_DATE('2023-11-24', 'YYYY-MM-DD'), 'pickup', 35.75, 'Delivered');

INSERT INTO orders (orderID, order_date, delivery_type, total_price, orderstatus)
VALUES ('ORD004', TO_DATE('2023-11-25', 'YYYY-MM-DD'), 'standard', 80.20, 'Pending');

INSERT INTO orders (orderID, order_date, delivery_type, total_price, orderstatus)
VALUES ('ORD005', TO_DATE('2023-11-26', 'YYYY-MM-DD'), 'express', 200.00, 'Processing');


INSERT INTO order_items (orderID, commodityID, quantity, name) VALUES ('ORD001', '101', 2, 'Product A');
INSERT INTO order_items (orderID, commodityID, quantity, name) VALUES ('ORD002', '102', 1, 'Product B');
INSERT INTO order_items (orderID, commodityID, quantity, name) VALUES ('ORD003', '103', 3, 'Product C');
INSERT INTO order_items (orderID, commodityID, quantity, name) VALUES ('ORD004', '104', 1, 'Product D');
INSERT INTO order_items (orderID, commodityID, quantity, name) VALUES ('ORD005', '105', 2, 'Product E');

INSERT INTO payment_regist (custID, cardID, card_type) VALUES ('CUST002', 'CARD001', 'VISA');
INSERT INTO payment_regist (custID, cardID, card_type) VALUES ('CUST003', 'CARD002', 'MASTERCARD');
INSERT INTO payment_regist (custID, cardID, card_type) VALUES ('CUST006', 'CARD003', 'AMEX');
INSERT INTO payment_regist (custID, cardID, card_type) VALUES ('CUST002', 'CARD004', 'DISCOVER');
INSERT INTO payment_regist (custID, cardID, card_type) VALUES ('CUST003', 'CARD005', 'VISA');

INSERT INTO paid (custID, cardID, orderID, pay_status) VALUES ('CUST002', 'CARD001', 'ORD001', 'SUCCESS');
INSERT INTO paid (custID, cardID, orderID, pay_status) VALUES ('CUST003', 'CARD002', 'ORD002', 'SUCCESS');
INSERT INTO paid (custID, cardID, orderID, pay_status) VALUES ('CUST006', 'CARD003', 'ORD003', 'SUCCESS');
INSERT INTO paid (custID, cardID, orderID, pay_status) VALUES ('CUST002', 'CARD004', 'ORD004', 'SUCCESS');
INSERT INTO paid (custID, cardID, orderID, pay_status) VALUES ('CUST003', 'CARD005', 'ORD005', 'SUCCESS');

INSERT INTO checkout (custID, orderID, date_shipped) VALUES ('CUST002', 'ORD001', TO_DATE('2023-11-24', 'YYYY-MM-DD'));
INSERT INTO checkout (custID, orderID, date_shipped) VALUES ('CUST003', 'ORD002', TO_DATE('2023-11-25', 'YYYY-MM-DD'));
INSERT INTO checkout (custID, orderID, date_shipped) VALUES ('CUST006', 'ORD003', TO_DATE('2023-11-26', 'YYYY-MM-DD'));
INSERT INTO checkout (custID, orderID, date_shipped) VALUES ('CUST002', 'ORD004', TO_DATE('2023-11-27', 'YYYY-MM-DD'));
INSERT INTO checkout (custID, orderID, date_shipped) VALUES ('CUST003', 'ORD005', TO_DATE('2023-11-28', 'YYYY-MM-DD'));

INSERT INTO Return_Request (returnID, orderID, returnReason, dateCreated, status, custID) VALUES (1, 'ORD001', 'Item damaged', TO_DATE('2023-11-26', 'YYYY-MM-DD'), 'Pending','CUST002');
INSERT INTO Return_Request (returnID, orderID, returnReason, dateCreated, status, custID) VALUES (2, 'ORD002', 'Wrong item', TO_DATE('2023-11-27', 'YYYY-MM-DD'), 'Approved','CUST003');
INSERT INTO Return_Request (returnID, orderID, returnReason, dateCreated, status, custID) VALUES (3, 'ORD003', 'Changed mind', TO_DATE('2023-11-28', 'YYYY-MM-DD'), 'Denied','CUST006');
INSERT INTO Return_Request (returnID, orderID, returnReason, dateCreated, status, custID) VALUES (4, 'ORD004', 'Defective', TO_DATE('2023-11-29', 'YYYY-MM-DD'), 'Pending','CUST002');
INSERT INTO Return_Request (returnID, orderID, returnReason, dateCreated, status, custID) VALUES (5, 'ORD005', 'Not as described', TO_DATE('2023-11-30', 'YYYY-MM-DD'), 'Approved','CUST003');

INSERT INTO Review (reviewID, commodityID, rating, review, reviewDate) VALUES (100, '2001', 4, 'Good product', TO_DATE('2023-11-27', 'YYYY-MM-DD'));
INSERT INTO Review (reviewID, commodityID, rating, review, reviewDate) VALUES (2, '3001', 5, 'Excellent product', TO_DATE('2023-11-28', 'YYYY-MM-DD'));
INSERT INTO Review (reviewID, commodityID, rating, review, reviewDate) VALUES (3, '12305456', 3, 'Average product', TO_DATE('2023-11-29', 'YYYY-MM-DD'));
INSERT INTO Review (reviewID, commodityID, rating, review, reviewDate) VALUES (4, '12305456', 2, 'Poor product', TO_DATE('2023-11-30', 'YYYY-MM-DD'));
INSERT INTO Review (reviewID, commodityID, rating, review, reviewDate) VALUES (5, '1234567890', 5, 'Awesome!', TO_DATE('2023-12-01','YYYY-MM-DD'));
select A.commodityID, A.name, A.price, A.category, A.discount, A.expDate, A.quantity, A.threshold, A.iid, AVG(B.rating)
from commodity_store A left join Review B on A.commodityID = B.commodityID
where iid = '2001'
group by A.commodityID, A.name, A.price, A.category, A.discount, A.expDate, A.quantity, A.threshold, A.iid

INSERT INTO Account (createDate, phone, password, email, username, saveditem, paypref) VALUES (TO_DATE('2023-11-15', 'YYYY-MM-DD'), 1234567890, 'pass123', 'user1@email.com', 'user1', 'item1', 'card1');
INSERT INTO Account (createDate, phone, password, email, username, saveditem, paypref) VALUES (TO_DATE('2023-11-16', 'YYYY-MM-DD'), 9876543210, 'pass456', 'user2@email.com', 'user2', 'item2', 'card2');
INSERT INTO Account (createDate, phone, password, email, username, saveditem, paypref) VALUES (TO_DATE('2023-11-17', 'YYYY-MM-DD'), 1122334455, 'pass789', 'user3@email.com', 'user3', 'item3', 'card3');
INSERT INTO Account (createDate, phone, password, email, username, saveditem, paypref) VALUES (TO_DATE('2023-11-18', 'YYYY-MM-DD'), 5566778899, 'pass101', 'user4@email.com', 'user4', 'item4', 'card4');
INSERT INTO Account (createDate, phone, password, email, username, saveditem, paypref) VALUES (TO_DATE('2023-11-19', 'YYYY-MM-DD'), 9988776655, 'pass112', 'user5@email.com', 'user5', 'item5', 'card5');

INSERT INTO Subscription (subscriptionID, commodityID, frequency, status, nextdeliverydate) VALUES (1, '1234567890', 'monthly', 'active', TO_DATE('2023-12-15', 'YYYY-MM-DD'));
INSERT INTO Subscription (subscriptionID, commodityID, frequency, status, nextdeliverydate) VALUES (2, '12305456', 'weekly', 'active', TO_DATE('2023-12-22', 'YYYY-MM-DD'));
INSERT INTO Subscription (subscriptionID, commodityID, frequency, status, nextdeliverydate) VALUES (3, '1234567890', 'monthly','inactive', TO_DATE('2023-12-29', 'YYYY-MM-DD'));
INSERT INTO Subscription (subscriptionID, commodityID, frequency, status, nextdeliverydate) VALUES (4, '12305456', 'weekly','active', TO_DATE('2024-01-05','YYYY-MM-DD'));
INSERT INTO Subscription (subscriptionID, commodityID, frequency, status, nextdeliverydate) VALUES (5, '12305456', 'monthly', 'active', TO_DATE('2024-01-12','YYYY-MM-DD'));

INSERT INTO Preferences (prefID, prefcategory, dietaryrestric, prefbrands) VALUES (1, 'food', 'vegetarian', 'Brand A');
INSERT INTO Preferences (prefID, prefcategory, dietaryrestric, prefbrands) VALUES (2, 'clothing', 'organic', 'Brand B');
INSERT INTO Preferences (prefID, prefcategory, dietaryrestric, prefbrands) VALUES (3, 'electronics', null, 'Brand C');
INSERT INTO Preferences (prefID, prefcategory, dietaryrestric, prefbrands) VALUES (4, 'books', null, 'Brand D');
INSERT INTO Preferences (prefID, prefcategory, dietaryrestric, prefbrands) VALUES (5, 'toys', null, 'Brand E');

INSERT INTO Messages (messageID, content, "date") VALUES (1, 'Welcome to our store!', TO_DATE('2023-11-17', 'YYYY-MM-DD'));
INSERT INTO Messages (messageID, content, "date") VALUES (2, 'New arrivals!', TO_DATE('2023-11-18', 'YYYY-MM-DD'));
INSERT INTO Messages (messageID, content, "date") VALUES (3, 'Sale ends soon!', TO_DATE('2023-11-19', 'YYYY-MM-DD'));
INSERT INTO Messages (messageID, content, "date") VALUES (4, 'Free shipping this weekend!', TO_DATE('2023-11-20', 'YYYY-MM-DD'));
INSERT INTO Messages (messageID, content, "date") VALUES (5, 'Your order has shipped!', TO_DATE('2023-11-21', 'YYYY-MM-DD'));

INSERT INTO Message_Type (messageType, messageID) VALUES ('Announcement', 1);
INSERT INTO Message_Type (messageType, messageID) VALUES ('Promotion', 2);
INSERT INTO Message_Type (messageType, messageID) VALUES ('Promotion', 3);
INSERT INTO Message_Type (messageType, messageID) VALUES ('Shipping', 4);
INSERT INTO Message_Type (messageType, messageID) VALUES ('Shipping', 5);

INSERT INTO browse (browse_date, custID, commodityID) VALUES (TO_DATE('2023-11-18', 'YYYY-MM-DD'), 'CUST002', '1234567890');
INSERT INTO browse (browse_date, custID, commodityID) VALUES (TO_DATE('2023-11-19', 'YYYY-MM-DD'), 'CUST003', '12305456');
INSERT INTO browse (browse_date, custID, commodityID) VALUES (TO_DATE('2023-11-20', 'YYYY-MM-DD'), 'CUST006', '1234567890');
INSERT INTO browse (browse_date, custID, commodityID) VALUES (TO_DATE('2023-11-21', 'YYYY-MM-DD'), 'CUST002', '12305456');
INSERT INTO browse (browse_date, custID, commodityID) VALUES (TO_DATE('2023-11-22', 'YYYY-MM-DD'), 'CUST003', '12305456');

INSERT INTO setup (start_date, subscriptionID, custID) VALUES (TO_DATE('2023-11-19', 'YYYY-MM-DD'), 1, 'CUST003');
INSERT INTO setup (start_date, subscriptionID, custID) VALUES (TO_DATE('2023-11-20', 'YYYY-MM-DD'), 2, 'CUST006');
INSERT INTO setup (start_date, subscriptionID, custID) VALUES (TO_DATE('2023-11-21', 'YYYY-MM-DD'), 3, 'CUST002');
INSERT INTO setup (start_date, subscriptionID, custID) VALUES (TO_DATE('2023-11-22', 'YYYY-MM-DD'), 4, 'CUST003');
INSERT INTO setup (start_date, subscriptionID, custID) VALUES (TO_DATE('2023-11-23', 'YYYY-MM-DD'), 5, 'CUST006');

INSERT INTO leaves (custID, reviewID) VALUES ('CUST003', 1);
INSERT INTO leaves (custID, reviewID) VALUES ('CUST006', 2);
INSERT INTO leaves (custID, reviewID) VALUES ('CUST002', 3);
INSERT INTO leaves (custID, reviewID) VALUES ('CUST003', 4);
INSERT INTO leaves (custID, reviewID) VALUES ('CUST006', 5);

INSERT INTO login (custID, email) VALUES ('CUST003', 'user1@email.com');
INSERT INTO login (custID, email) VALUES ('CUST006', 'user2@email.com');
INSERT INTO login (custID, email) VALUES ('CUST002', 'user3@email.com');
INSERT INTO login (custID, email) VALUES ('CUST003', 'user4@email.com');
INSERT INTO login (custID, email) VALUES ('CUST006', 'user5@email.com');

INSERT INTO sets (custID, prefID) VALUES ('CUST003', 1);
INSERT INTO sets (custID, prefID) VALUES ('CUST006', 2);
INSERT INTO sets (custID, prefID) VALUES ('CUST002', 3);
INSERT INTO sets (custID, prefID) VALUES ('CUST003', 4);
INSERT INTO sets (custID, prefID) VALUES ('CUST006', 5);

INSERT INTO opt_in (custID, messageID) VALUES ('CUST003', 1);
INSERT INTO opt_in (custID, messageID) VALUES ('CUST006', 2);
INSERT INTO opt_in (custID, messageID) VALUES ('CUST002', 3);
INSERT INTO opt_in (custID, messageID) VALUES ('CUST003', 4);
INSERT INTO opt_in (custID, messageID) VALUES ('CUST006', 5);

--CREATE OR REPLACE TRIGGER update_order_total
--AFTER INSERT OR UPDATE ON Order_Items
--FOR EACH ROW
--BEGIN
--    UPDATE Orders
--    SET total_price = (
--        SELECT SUM(oi.quantity * p.price)
--        FROM Order_Items oi
--        JOIN Commodity_Store p ON oi.commodityID = p.commodityID
--        WHERE oi.orderID = :NEW.orderID
--    )
--    WHERE orderID = :NEW.orderID;
--END;
--/
--
--CREATE OR REPLACE TRIGGER reduce_commodity_quantity
--AFTER INSERT ON Order_Items
--FOR EACH ROW
--BEGIN
--    UPDATE commodity_store
--    SET quantity = quantity - :NEW.quantity
--    WHERE commodityID = :NEW.commodityID;
--EXCEPTION
--    WHEN NO_DATA_FOUND THEN
--        RAISE_APPLICATION_ERROR(-20001, 'Commodity ' || :NEW.commodityID || ' not found in commodity_store.');
--END;
--/
--
--CREATE OR REPLACE TRIGGER update_loyalty_points
--AFTER INSERT ON Paid
--FOR EACH ROW
--DECLARE
--    v_total_price DECIMAL(10, 2);
--    v_loyalty_points NUMBER;
--BEGIN
--    SELECT total_price INTO v_total_price
--    FROM Orders
--    WHERE orderID = :NEW.orderID;
--    v_loyalty_points := FLOOR(v_total_price / 10);
--    UPDATE Member
--    SET loyaltyPoints = loyaltyPoints + v_loyalty_points
--    WHERE custID = :NEW.custID;
--EXCEPTION
--    WHEN NO_DATA_FOUND THEN
--        RAISE_APPLICATION_ERROR(-20001, 'Order or Member not found.');
--END;
--/
--
--INSERT INTO Customer (custID)
--VALUES ('TESTMEM1');
--
--
--INSERT INTO Member (custID, startDate, expDate, loyaltyPoints)
--VALUES ('TESTMEM1', TO_DATE('2023-01-01', 'YYYY-MM-DD'), TO_DATE('2024-01-01', 'YYYY-MM-DD'), 100);
--
--INSERT INTO Orders (orderID, order_date, delivery_type, total_price, orderstatus)
--VALUES ('TESTORD1', TO_DATE('2023-12-05', 'YYYY-MM-DD'), 'standard', 50.00, 'Processing');
--
--INSERT INTO Payment_Regist (custID, cardID, card_type)
--VALUES ('TESTMEM1', 'CARDTEST', 'VISA');
--INSERT INTO Payment_Regist (custID, cardID, card_type)
--VALUES ('TESTMEM1', 'CARDTEST2', 'VISA');
--
--INSERT INTO Paid (custID, cardID, orderID, pay_status)
--VALUES ('TESTMEM1', 'CARDTEST', 'TESTORD1', 'SUCCESS');
--
--SELECT loyaltyPoints FROM Member WHERE custID = 'TESTMEM1';
--
--INSERT INTO Paid (custID, cardID, orderID, pay_status)
--VALUES ('TESTMEM1', 'CARDTEST2', 'TESTORD1', 'SUCCESS');
--
--INSERT INTO Paid (custID, cardID, orderID, pay_status)
--VALUES ('TESTMEM1', 'CARDTEST3', 'NON', 'SUCCESS');

-- STORE MANAGER

CREATE TABLE store (
storeID VARCHAR(9) NOT NULL,
name VARCHAR(50),
address varchar(50),
phone_number varchar(10),
PRIMARY KEY (storeID)
);

--Store Manager
CREATE TABLE store_manager (
m_ssn VARCHAR(9),
storeID VARCHAR(9) NOT NULL,
name VARCHAR(50),
salary DECIMAL(10, 2),
birthday DATE,
PRIMARY KEY (m_ssn),
FOREIGN KEY (storeID) REFERENCES store (storeID)
);


--Manages Budget
CREATE TABLE budget_manager (
budgetID VARCHAR(9),
m_ssn VARCHAR(9) NOT NULL,
category VARCHAR(50),
amount DECIMAL(10, 2),
year VARCHAR(4),
PRIMARY KEY (budgetID),
FOREIGN KEY (m_ssn) REFERENCES store_manager (m_ssn)
);


--Manages Store
CREATE TABLE manages_store (
storeID VARCHAR(9),
m_ssn VARCHAR(9) NOT NULL,
name VARCHAR(50),
address VARCHAR(50),
phone_number VARCHAR(11),
PRIMARY KEY (storeID),
FOREIGN KEY (m_ssn) REFERENCES store_manager (m_ssn)
);


--Employee Store
CREATE TABLE employee_store (
ssn VARCHAR(9),
storeID VARCHAR(9),
since DATE,
PRIMARY KEY (ssn, storeID),
FOREIGN KEY (ssn) REFERENCES employee (ssn),
FOREIGN KEY (storeID) REFERENCES manages_store (storeID)
);

--Campaign
CREATE TABLE campaign (
campaignID VARCHAR(9),
campaign_name VARCHAR(50),
start_date DATE,
end_date DATE,
commodity_category VARCHAR(10),
PRIMARY KEY (campaignID)
);

--Coordinates
CREATE TABLE coordinates (
campaignID VARCHAR(9),
m_ssn VARCHAR(9),
PRIMARY KEY (campaignID, m_ssn),
FOREIGN KEY (campaignID) REFERENCES campaign,
FOREIGN KEY (m_ssn) REFERENCES store_manager
);

CREATE TABLE shift_schedule (
ssn VARCHAR(9),
name VARCHAR(50),
shift_date DATE,
hr_start VARCHAR(5),
hr_end VARCHAR(5),
station VARCHAR(20),
PRIMARY KEY (ssn, shift_date),
FOREIGN KEY (ssn) REFERENCES employee (ssn) ON DELETE CASCADE
);

--Creates Schedule
CREATE TABLE creates_schedule (
m_ssn VARCHAR(9),
shift_date DATE,
ssn VARCHAR(9),
PRIMARY KEY (m_ssn, shift_date, ssn),
FOREIGN KEY (m_ssn) REFERENCES store_manager (m_ssn),
FOREIGN KEY (ssn, shift_date) REFERENCES shift_schedule (ssn, shift_date),
FOREIGN KEY (ssn) REFERENCES employee (ssn)
);

CREATE TABLE restock_report (
reportID VARCHAR(9),
commodityID VARCHAR(10),
quantity DECIMAL (10, 2),
PRIMARY KEY (reportID)
);

--Receives
CREATE TABLE receives_restock (
m_ssn VARCHAR(9),
reportID VARCHAR(9),
PRIMARY KEY (m_ssn, reportID),
FOREIGN KEY (m_ssn) REFERENCES store_manager (m_ssn),
FOREIGN KEY (reportID) REFERENCES restock_report (reportID)
);

--Creates restock
CREATE TABLE creates_restock (
ssn VARCHAR(9),
reportID VARCHAR(9),
report_created_date DATE,
PRIMARY KEY (ssn, reportID),
FOREIGN KEY (ssn) REFERENCES employee (ssn),
FOREIGN KEY (reportID) REFERENCES restock_report (reportID)
);

-- VENDOR
CREATE TABLE Vendor (
    vendorID varchar(50),
    name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(10),
    email VARCHAR(50),
    address VARCHAR (250),
    PRIMARY KEY (vendorID)
);

--CREATE TABLE Inventory_Order ( 
--    commodityID VARCHAR(25) NOT NULL,
--    product_name VARCHAR(50) NOT NULL,
--    quantity INT NOT NULL,
--    price DECIMAL(10, 2) NOT NULL,
--    vendorID VARCHAR(50),
--    PRIMARY KEY (inventory_orderID) VARCHAR(50),
--    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID)
--);

CREATE TABLE Contract (
    storeID VARCHAR(50) NOT NULL,
    vendorID VARCHAR(50),
    order_frequency VARCHAR(50),
    delivery_schedule VARCHAR(100),
    start_date DATE NOT NULL,
    end_date DATE,
    pricing DECIMAL(10, 2),
    contractID VARCHAR(50),
    PRIMARY KEY (contractID),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID)
);

CREATE TABLE Delivery (
    storeID VARCHAR(50) NOT NULL,
    vendorID VARCHAR(50),
    commodityID VARCHAR(50),
    orderdate DATE NOT NULL,
    expected_time date,
    discrepancy varchar(50),
    received_status VARCHAR(50),
    deliveryID varchar(50),
    PRIMARY KEY (deliveryID),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID)
);





