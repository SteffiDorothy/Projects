DROP TABLE non_member;
DROP TABLE member;
DROP TABLE orders;
DROP TABLE order_items;
DROP TABLE Paid;
DROP TABLE checkout;
DROP TABLE Return_Request;
DROP TABLE customer;
DROP TABLE cart;
DROP TABLE payment_regist;
DROP TABLE Review;
DROP TABLE Account;
DROP TABLE Subscription;
DROP TABLE Preferences;
DROP TABLE Messages;
DROP TABLE Message_Type;
DROP TABLE browse;
DROP TABLE setup;
DROP TABLE leaves;
DROP TABLE login;
DROP TABLE sets;
DROP TABLE opt_in;

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
  commodityID VARCHAR(10),
  custID VARCHAR(50),
  rating NUMBER NOT NULL,
  review CLOB, 
  reviewDate DATE,
  FOREIGN KEY (commodityID) REFERENCES commodity_store(commodityID),
  FOREIGN KEY (custID) REFERENCES member(custID)
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
commodityID NUMBER, 
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
commodityID NUMBER,
PRIMARY KEY (custID, commodityID), 
FOREIGN KEY (custID) REFERENCES customer(custID),
FOREIGN KEY (commodityID) REFERENCES commodity_store(commodityID)
);

CREATE TABLE setup(
start_date DATE, 
subsciptionID NUMBER,
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
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100),
    email VARCHAR2(100),
    message CLOB
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

INSERT INTO Review (reviewID, commodityID, rating, comment, reviewDate) VALUES (1, '2001', 4, 'Good product', TO_DATE('2023-11-27', 'YYYY-MM-DD'));
INSERT INTO Review (reviewID, commodityID, rating, comment, reviewDate) VALUES (2, '2002', 5, 'Excellent product', TO_DATE('2023-11-28', 'YYYY-MM-DD'));
INSERT INTO Review (reviewID, commodityID, rating, comment, reviewDate) VALUES (3, '2003', 3, 'Average product', TO_DATE('2023-11-29', 'YYYY-MM-DD'));
INSERT INTO Review (reviewID, commodityID, rating, comment, reviewDate) VALUES (4, '3001', 2, 'Poor product', TO_DATE('2023-11-30', 'YYYY-MM-DD'));
INSERT INTO Review (reviewID, commodityID, rating, comment, reviewDate) VALUES (5, '3002', 5, 'Awesome!', TO_DATE('2023-12-01','YYYY-MM-DD'));

INSERT INTO Account (createDate, phone, password, email, username, saveditem, paypref) VALUES (TO_DATE('2023-11-15', 'YYYY-MM-DD'), 1234567890, 'pass123', 'user1@email.com', 'user1', 'item1', 'card1');
INSERT INTO Account (createDate, phone, password, email, username, saveditem, paypref) VALUES (TO_DATE('2023-11-16', 'YYYY-MM-DD'), 9876543210, 'pass456', 'user2@email.com', 'user2', 'item2', 'card2');
INSERT INTO Account (createDate, phone, password, email, username, saveditem, paypref) VALUES (TO_DATE('2023-11-17', 'YYYY-MM-DD'), 1122334455, 'pass789', 'user3@email.com', 'user3', 'item3', 'card3');
INSERT INTO Account (createDate, phone, password, email, username, saveditem, paypref) VALUES (TO_DATE('2023-11-18', 'YYYY-MM-DD'), 5566778899, 'pass101', 'user4@email.com', 'user4', 'item4', 'card4');
INSERT INTO Account (createDate, phone, password, email, username, saveditem, paypref) VALUES (TO_DATE('2023-11-19', 'YYYY-MM-DD'), 9988776655, 'pass112', 'user5@email.com', 'user5', 'item5', 'card5');

INSERT INTO Subscription (subscriptionID, commodityID, frequency, status, nextdeliverydate) VALUES (1, 102, 'monthly', 'active', TO_DATE('2023-12-15', 'YYYY-MM-DD'));
INSERT INTO Subscription (subscriptionID, commodityID, frequency, status, nextdeliverydate) VALUES (2, 103, 'weekly', 'active', TO_DATE('2023-12-22', 'YYYY-MM-DD'));
INSERT INTO Subscription (subscriptionID, commodityID, frequency, status, nextdeliverydate) VALUES (3, 104, 'monthly','inactive', TO_DATE('2023-12-29', 'YYYY-MM-DD'));
INSERT INTO Subscription (subscriptionID, commodityID, frequency, status, nextdeliverydate) VALUES (4, 101, 'weekly','active', TO_DATE('2024-01-05','YYYY-MM-DD'));
INSERT INTO Subscription (subscriptionID, commodityID, frequency, status, nextdeliverydate) VALUES (5, 105, 'monthly', 'active', TO_DATE('2024-01-12','YYYY-MM-DD'));

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

INSERT INTO browse (browse_date, custID, commodityID) VALUES (TO_DATE('2023-11-18', 'YYYY-MM-DD'), 'CUST002', 101);
INSERT INTO browse (browse_date, custID, commodityID) VALUES (TO_DATE('2023-11-19', 'YYYY-MM-DD'), 'CUST003', 102);
INSERT INTO browse (browse_date, custID, commodityID) VALUES (TO_DATE('2023-11-20', 'YYYY-MM-DD'), 'CUST006', 103);
INSERT INTO browse (browse_date, custID, commodityID) VALUES (TO_DATE('2023-11-21', 'YYYY-MM-DD'), 'CUST002', 104);
INSERT INTO browse (browse_date, custID, commodityID) VALUES (TO_DATE('2023-11-22', 'YYYY-MM-DD'), 'CUST003', 105);

INSERT INTO setup (start_date, subsciptionID, custID) VALUES (TO_DATE('2023-11-19', 'YYYY-MM-DD'), 1, 'CUST003');
INSERT INTO setup (start_date, subsciptionID, custID) VALUES (TO_DATE('2023-11-20', 'YYYY-MM-DD'), 2, 'CUST006');
INSERT INTO setup (start_date, subsciptionID, custID) VALUES (TO_DATE('2023-11-21', 'YYYY-MM-DD'), 3, 'CUST002');
INSERT INTO setup (start_date, subsciptionID, custID) VALUES (TO_DATE('2023-11-22', 'YYYY-MM-DD'), 4, 'CUST003');
INSERT INTO setup (start_date, subsciptionID, custID) VALUES (TO_DATE('2023-11-23', 'YYYY-MM-DD'), 5, 'CUST006');

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

CREATE OR REPLACE TRIGGER update_order_total
AFTER INSERT OR UPDATE ON Order_Items
FOR EACH ROW
BEGIN
    UPDATE Orders
    SET total_price = (
        SELECT SUM(oi.quantity * p.price)
        FROM Order_Items oi
        JOIN Commodity_Store p ON oi.commodityID = p.commodityID
        WHERE oi.orderID = :NEW.orderID
    )
    WHERE orderID = :NEW.orderID;
END;
/

CREATE OR REPLACE TRIGGER reduce_commodity_store_quantity
AFTER INSERT ON Order_Items
FOR EACH ROW
BEGIN
    UPDATE commodity_store
    SET quantity = quantity - :NEW.quantity
    WHERE commodityID = :NEW.commodityID;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20001, 'Commodity ' || :NEW.commodityID || ' not found in commodity_store.');
END;
/

CREATE OR REPLACE TRIGGER update_loyalty_points
AFTER INSERT ON Paid
FOR EACH ROW
DECLARE
    v_total_price DECIMAL(10, 2);
    v_loyalty_points NUMBER;
BEGIN
    SELECT total_price INTO v_total_price
    FROM Orders
    WHERE orderID = :NEW.orderID;
    v_loyalty_points := FLOOR(v_total_price / 10);
    UPDATE Member
    SET loyaltyPoints = loyaltyPoints + v_loyalty_points
    WHERE custID = :NEW.custID;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20001, 'Order or Member not found.');
END;
/

INSERT INTO Customer (custID)
VALUES ('TESTMEM1');


INSERT INTO Member (custID, startDate, expDate, loyaltyPoints)
VALUES ('TESTMEM1', TO_DATE('2023-01-01', 'YYYY-MM-DD'), TO_DATE('2024-01-01', 'YYYY-MM-DD'), 100);

INSERT INTO Orders (orderID, order_date, delivery_type, total_price, orderstatus)
VALUES ('TESTORD1', TO_DATE('2023-12-05', 'YYYY-MM-DD'), 'standard', 50.00, 'Processing');

INSERT INTO Payment_Regist (custID, cardID, card_type)
VALUES ('TESTMEM1', 'CARDTEST', 'VISA');
INSERT INTO Payment_Regist (custID, cardID, card_type)
VALUES ('TESTMEM1', 'CARDTEST2', 'VISA');

INSERT INTO Paid (custID, cardID, orderID, pay_status)
VALUES ('TESTMEM1', 'CARDTEST', 'TESTORD1', 'SUCCESS');

SELECT loyaltyPoints FROM Member WHERE custID = 'TESTMEM1';

INSERT INTO Paid (custID, cardID, orderID, pay_status)
VALUES ('TESTMEM1', 'CARDTEST2', 'TESTORD1', 'SUCCESS');

INSERT INTO Paid (custID, cardID, orderID, pay_status)
VALUES ('TESTMEM1', 'CARDTEST3', 'NON', 'SUCCESS');
