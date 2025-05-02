drop table store_manager;
drop table budget_manager;
drop table manages_store;
drop table employee_store;
drop table campaign;
drop table coordinates;
drop table creates_schedule; 
drop table shift_schedule;
drop table receives_restock;
drop table creates_restock;
drop table restock_report;


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
FOREIGN KEY ssn REFERENCES employee (ssn),
FOREIGN KEY storeID REFERENCES manages_store (storeID)
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
PRIMARY KEY (campaignID, ssn),
FOREIGN KEY (campaignID) REFERENCES campaign,
FOREIGN KEY (m_ssn) REFERENCES store_manager
);

--Creates Schedule
CREATE TABLE creates_schedule (
m_ssn VARCHAR(9),
shift_date DATE,
ssn VARCHAR(9),
PRIMARY KEY (m_ssn, work_date, ssn),
FOREIGN KEY (m_ssn) REFERENCES store_manager (m_ssn),
FOREIGN KEY (shift_date) REFERENCES shift_schedule (shift_date),
FOREIGN KEY (ssn) REFERENCES employee (ssn)
);

--Shift Schedule
CREATE TABLE shift_schedule (
ssn VARCHAR(9),
name VARCHAR(50),
shift_date DATE,
hr_start VARCHAR(5),
hr_end VARCHAR(5),
station VARCHAR(20),
PRIMARY KEY (ssn, shift_date)
FOREIGN KEY (ssn) REFERENCES employees (ssn) ON DELETE CASCADE
);

--Receives
CREATE TABLE receives_restock (
m_ssn VARCHAR(9),
reportID VARCHAR(9),
PRIMARY KEY (m_ssn, reportID),
FOREIGN KEY (m_ssn) REFERENCES store_manager (m_ssn),
FOREIGN KEY (reportID) REFERENCES restock_report (reportID)
);


--Restock Report
CREATE TABLE restock_report (
reportID VARCHAR(9),
commodityID VARCHAR(10),
quantity DECIMAL (10, 2),
PRIMARY KEY (reportID)
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
