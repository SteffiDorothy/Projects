drop table inventory_alerts_send;
drop table load_on;
drop table commodity_store;
drop table monitor;
drop table inventory;
drop table shelf_alerts_send;
drop table handle;
drop table shelf;
drop table maintain;
drop table maintenance_region;
drop table custodian_work_record;
drop table maintenance_record;
drop table cashier_asigned_to;
drop table cash_desk;
drop table inventory_manager;
drop table stock_clerk;
drop table custodian;
drop table work_record;
drop table employee;

CREATE TABLE employee (
    ssn VARCHAR(9),
    name VARCHAR(50),
    birthday DATE,
    salary DECIMAL(10, 2),
    PRIMARY KEY (ssn)
);

CREATE TABLE work_record (
    ssn VARCHAR(9),
    work_date DATE,
    type VARCHAR(10),
    device VARCHAR(10),
    PRIMARY KEY (ssn, work_date),
    FOREIGN KEY (ssn) REFERENCES employee(ssn) on delete cascade
);

CREATE TABLE custodian (
    ssn VARCHAR(9),
    PRIMARY KEY (ssn),
    FOREIGN KEY (ssn) REFERENCES employee(ssn)
);

CREATE TABLE stock_clerk (
    ssn VARCHAR(9),
    PRIMARY KEY (ssn),
    FOREIGN KEY (ssn) REFERENCES employee(ssn)
);

CREATE TABLE inventory_manager (
    ssn VARCHAR(9),
    PRIMARY KEY (ssn),
    FOREIGN KEY (ssn) REFERENCES employee(ssn)
);

CREATE TABLE cash_desk (
    desk_id VARCHAR(3),
    location VARCHAR(10),
    PRIMARY KEY (desk_id)
);

CREATE TABLE cashier_asigned_to (
    ssn VARCHAR(9),
    desk_id VARCHAR(3) NOT NULL,
    assigned_date DATE,
    PRIMARY KEY (ssn),
    FOREIGN KEY (desk_id) REFERENCES cash_desk(desk_id)
);

CREATE TABLE maintenance_record (
    recordID varchar(10),
    maintain_date DATE,
    type VARCHAR(10),
    description VARCHAR(50),
    PRIMARY KEY (recordID)
);

CREATE TABLE custodian_work_record(
    ssn VARCHAR(9),
    recordID VARCHAR(10),
    PRIMARY KEY (ssn, recordID),
    FOREIGN KEY (ssn) REFERENCES custodian(ssn),
    FOREIGN KEY (recordID) REFERENCES maintenance_record(recordID)
);

CREATE TABLE maintenance_region(
    regionID VARCHAR(10),
    location VARCHAR(10),
    area INT,
    PRIMARY KEY (regionID)
);

CREATE TABLE maintain(
    ssn VARCHAR(9),
    regionID VARCHAR(10),
    PRIMARY KEY (ssn, regionID),
    FOREIGN KEY (ssn) REFERENCES custodian(ssn),
    FOREIGN KEY (regionID) REFERENCES maintenance_region(regionID)
);

CREATE TABLE shelf(
    shelfID VARCHAR(10),
    location VARCHAR(10),
    capacity INT,
    PRIMARY KEY (shelfID)
);

CREATE TABLE handle(
    ssn VARCHAR(9),
    shelfID VARCHAR(10),
    PRIMARY KEY (ssn, shelfID),
    FOREIGN KEY (ssn) REFERENCES stock_clerk(ssn),
    FOREIGN KEY (shelfID) REFERENCES shelf(shelfID)
);

CREATE TABLE shelf_alerts_send(
    id varchar(10),
    send_date DATE,
    commodityID VARCHAR(10),
    description VARCHAR(50),
    shelfID VARCHAR(10) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (shelfID) REFERENCES shelf(shelfID)
);

CREATE TABLE inventory(
    iid VARCHAR(10),
    location VARCHAR(10),
    PRIMARY KEY (iid)
);

CREATE TABLE monitor(
    ssn VARCHAR(9),
    iid VARCHAR(10),
    assigned_date DATE,
    PRIMARY KEY (ssn, iid),
    FOREIGN KEY (ssn) REFERENCES inventory_manager(ssn),
    FOREIGN KEY (iid) REFERENCES inventory(iid)
);

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
    PRIMARY KEY (commodityID),
    FOREIGN KEY (iid) REFERENCES inventory(iid)
);

CREATE TABLE load_on(
    shelfID VARCHAR(10),
    commodityID VARCHAR(10),
    quantity DECIMAL(10, 2),
    threshold DECIMAL(10, 2),
    PRIMARY KEY (shelfID, commodityID),
    FOREIGN KEY (shelfID) REFERENCES shelf(shelfID),
    FOREIGN KEY (commodityID) REFERENCES commodity_store(commodityID)
);

CREATE TABLE inventory_alerts_send(
    alertID VARCHAR(10),
    send_date DATE,
    commodityID VARCHAR(10),
    description VARCHAR(50),
    iid VARCHAR(10) NOT NULL,
    PRIMARY KEY (alertID),
    FOREIGN KEY (iid) REFERENCES inventory(iid)
);

CREATE TRIGGER inventory_alerts
AFTER UPDATE ON commodity_store
FOR EACH ROW
BEGIN
    IF (:new.quantity < :new.threshold) THEN
        INSERT INTO inventory_alerts_send (alertID, send_date, commodityID, description, iid)
        VALUES (dbms_random.string('p',10), SYSDATE, :new.commodityID, 'Low stock alert', :new.iid);
    END IF;
END;

CREATE TRIGGER shelf_alerts
AFTER UPDATE ON load_on
FOR EACH ROW
BEGIN
    IF (:new.quantity < :new.threshold) THEN
        INSERT INTO shelf_alerts_send (id, send_date, commodityID, description, shelfID)
        VALUES (dbms_random.string('p',10), SYSDATE, :new.commodityID, 'Low stock alert', :new.shelfID);
    END IF;
END;

-- test oracle trigger
SELECT * FROM inventory_alerts_send;

INSERT INTO inventory(iid, location)
VALUES ('003', '123_MainSt');

INSERT INTO commodity_store(commodityID, name, price, category, discount, expDate, quantity, threshold, iid)
VALUES ('1234567890', 'bread', 4.46, 'bread', 1, SYSDATE + 30, 20, 20, '003');

UPDATE commodity_store
SET quantity = quantity - 1
WHERE commodityID = '1234567890';

SELECT * FROM inventory_alerts_send;

CREATE TRIGGER inventory_alerts
AFTER UPDATE ON commodity_store
FOR EACH ROW
BEGIN
    IF (:new.quantity < :new.threshold) THEN
        INSERT INTO inventory_alerts_send (alertID, send_date, commodityID, description, iid)
        VALUES (dbms_random.string('p',10), SYSDATE, :new.commodityID, 'Low stock alert', :new.iid);
    END IF;
END;

for postgresql
CREATE OR REPLACE FUNCTION alert()
RETURNS TRIGGER AS $commodity_store$
   BEGIN
      IF (new.quantity < new.threshold) THEN
        INSERT INTO inventory_alerts_send (alertID, send_date, commodityID, description, iid)
        VALUES (substring(random()::text, 1, 10), now(), new.commodityID, 'Low stock alert', new.iid);
        return new;
      END IF;
   END;
$commodity_store$ LANGUAGE plpgsql;

CREATE TRIGGER inventory_alerts
AFTER UPDATE ON commodity_store
FOR EACH ROW
EXECUTE PROCEDURE alert();

SELECT send_date, commodityID, description, iid  FROM inventory_alerts_send;

INSERT INTO inventory(iid, location)
VALUES ('003', '123_MainSt');

INSERT INTO commodity_store(commodityID, name, price, category, discount, expDate, quantity, threshold, iid)
VALUES ('1234567890', 'bread', 4.46, 'bread', 1, now(), 20, 20, '003');

UPDATE commodity_store
SET quantity = quantity - 1
WHERE commodityID = '1234567890';

SELECT send_date, commodityID, description, iid FROM inventory_alerts_send;