CREATE TABLE Vendor (
    vendorID VARCHAR(50),
    name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(10),
    email VARCHAR(50),
    address VARCHAR (250)
    PRIMARY KEY (vendorID),
);

CREATE TABLE Inventory_Order ( 
    inventory_orderID VARCHAR(50),
    commodityID VARCHAR(25) NOT NULL,
    product_name VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    vendorID VARCHAR(50),
    PRIMARY KEY (inventory_orderID),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID)
);

CREATE TABLE Contract (
    contractID VARCHAR(50),
    storeID VARCHAR(50) NOT NULL,
    vendorID VARCHAR(50),
    order_frequency VARCHAR(50),
    delivery_schedule VARCHAR(100),
    start_date DATE NOT NULL,
    end_date DATE,
    pricing DECIMAL(10, 2),
    PRIMARY KEY (contractID),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID)
);

CREATE TABLE Delivery (
    deliveryID VARCHAR(50),
    storeID VARCHAR(50) NOT NULL,
    vendorID VARCHAR(50),
    commodityID VARCHAR(50),
    orderdate DATE NOT NULL,
    expected_time TIME,
    discrepancy TEXT,
    received_status VARCHAR(50),
    PRIMARY KEY (deliveryID),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID)
);

CREATE TABLE Has (
    contractID VARCHAR(50) NOT NULL,
    vendorID VARCHAR(50) NOT NULL,
    PRIMARY KEY (contractID),
    FOREIGN KEY (contractID) REFERENCES Contract(contractID),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID)
);

CREATE TABLE Delivers (
    deliveryID VARCHAR(50) NOT NULL,
    vendorID VARCHAR(50) NOT NULL,
    PRIMARY KEY (deliveryID),
    FOREIGN KEY (deliveryID) REFERENCES Delivery(deliveryID),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID),
);

CREATE TABLE Sells (
    vendorID VARCHAR(50) NOT NULL,
    commodityID VARCHAR(50) NOT NULL,
    PRIMARY KEY (vendorID, commodityID),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID),
    FOREIGN KEY (commodityID) REFERENCES Commodity(commodityID)
);

CREATE TABLE Sends_Processes (
    inventory_orderID VARCHAR(50)
    vendorID VARCHAR(50) NOT NULL,
    m_ssn VARCHAR(9) NOT NULL,
    PRIMARY KEY (inventory_orderID, m_ssn, vendorID),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID),
    FOREIGN KEY (inventory_orderID) REFERENCES Inventory_Order(inventory_orderID)
    FOREIGN KEY (m_ssn) REFERENCES Store_Manager(m_ssn),
);
