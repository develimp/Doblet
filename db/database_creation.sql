CREATE DATABASE IF NOT EXISTS sp;
USE sp;

CREATE TABLE IF NOT EXISTS category(
	id INT AUTO_INCREMENT PRIMARY KEY,
	fee DECIMAL(10, 2) NOT NULL,
	name VARCHAR(10),
	description VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS family(
	id INT AUTO_INCREMENT PRIMARY KEY,
	discount DECIMAL(10, 2) NOT NULL,
	isDirectDebited BOOLEAN
);

CREATE TABLE IF NOT EXISTS member(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	surname VARCHAR(100) NOT NULL,
	birthdate DATE NOT NULL,
	gender ENUM('M', 'F'),
	dni VARCHAR(10),
	address VARCHAR(100),
	phoneNumber VARCHAR(15),
	isRegistered BOOLEAN,
	familyFk INT NOT NULL,
	categoryFk INT NOT NULL,
	email VARCHAR(50),
	CONSTRAINT member_family_FK
	FOREIGN KEY(familyFk)
	REFERENCES family(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
	CONSTRAINT member_category_FK
	FOREIGN KEY(categoryFk)
	REFERENCES category(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS fallaYear(
	code INT PRIMARY KEY,
	created DATE,
	finished DATE
);

CREATE TABLE IF NOT EXISTS movement(
	id INT AUTO_INCREMENT PRIMARY KEY,
	transactionDate DATE NOT NULL,
	amount DECIMAL(10, 2) NOT NULL,
	idType INT NOT NULL,
	idConcept INT NOT NULL,
	fallaYearFk INT NOT NULL,
	memberFk INT NOT NULL,
	description VARCHAR(100),
	receiptNumber INT,
	CONSTRAINT movement_member_FK
	FOREIGN KEY(memberFk)
	REFERENCES member(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
	CONSTRAINT movement_fallaYear_FK
	FOREIGN KEY(fallaYearFk)
	REFERENCES fallaYear(code)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS membershipHistory(
	id INT AUTO_INCREMENT PRIMARY KEY,
	fallaYearFk INT NOT NULL,
	position VARCHAR(30) NOT NULL,
	falla VARCHAR(50) NOT NULL,
	memberFk INT NOT NULL,
	CONSTRAINT membershipHistory_fallaYear_FK
	FOREIGN KEY(fallaYearFk)
	REFERENCES fallaYear(code)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
	CONSTRAINT membershipHistory_member_FK
	FOREIGN KEY(memberFk)
	REFERENCES member(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS summaryMembersFallaYear(
	id INT AUTO_INCREMENT PRIMARY KEY,
	fallaYearFk INT NOT NULL,
	memberFk INT NOT NULL,
	assignedFee DECIMAL(10, 2) NOT NULL,
	assignedLottery DECIMAL(10, 2) NOT NULL,
	assignedRaffle DECIMAL(10, 2) NOT NULL,
	payedFee DECIMAL(10, 2) NOT NULL,
	payedLottery DECIMAL(10, 2) NOT NULL,
	payedRaffle DECIMAL(10, 2) NOT NULL,
	difference DECIMAL(10, 2) AS (
		assignedFee + assignedLottery + assignedRaffle - 
		(payedFee + payedLottery + payedRaffle)
	) VIRTUAL,
	CONSTRAINT summaryMembersFallaYear_fallaYear_FK
	FOREIGN KEY(fallaYearFk)
	REFERENCES fallaYear(code)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
	CONSTRAINT summaryMembersFallaYear_member_FK
	FOREIGN KEY(memberFk)
	REFERENCES member(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS lottery(
	id INT AUTO_INCREMENT PRIMARY KEY,
	lotteryId INT NOT NULL,
	lotteryName VARCHAR (30) NOT NULL,
	assigned DATE DEFAULT CURRENT_DATE,
	fallaYearFk INT NOT NULL,
	memberFk INT NOT NULL,
	ticketsMale INT,
	ticketsFemale INT,
	ticketsChildish INT,
	tenthsMale INT,
	tenthsFemale INT,
	tenthsChildish INT,
	isAssigned BOOLEAN,
	price DECIMAL(10, 2) AS (
		(ticketsMale * 4) + (ticketsFemale * 4) + (ticketsChildish * 4) +
		(tenthsMale * 20) + (tenthsFemale * 20) + (tenthsChildish * 20)
	) VIRTUAL,
	benefit DECIMAL(10, 2) AS (
		ticketsMale + ticketsFemale + ticketsChildish +
		(tenthsMale * 3) + (tenthsFemale * 3) + (tenthsChildish * 3)
	) VIRTUAL,
	CONSTRAINT lottery_fallaYear_FK
	FOREIGN KEY(fallaYearFk)
	REFERENCES fallaYear(code)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
	CONSTRAINT lottery_member_FK
	FOREIGN KEY(memberFk)
	REFERENCES member(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS balance(
	memberFk INT PRIMARY KEY,
	feeAssigned DECIMAL(10, 2) NOT NULL,
	feePayed DECIMAL(10, 2) NOT NULL,
	lotteryAssigned DECIMAL(10, 2) NOT NULL,
	lotteryPayed DECIMAL(10, 2) NOT NULL,
	raffleAssigned DECIMAL(10, 2) NOT NULL,
	rafflePayed DECIMAL(10, 2) NOT NULL,
	CONSTRAINT balance_member_FK
	FOREIGN KEY(memberFk)
	REFERENCES member(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS partner(
	id INT AUTO_INCREMENT PRIMARY KEY,
	memberFk INT NOT NULL,
	name VARCHAR(50) NOT NULL,
	surname VARCHAR(100) NOT NULL,
	birthdate DATE NOT NULL,
	dni VARCHAR(10),
	fallaYearFk INT NOT NULL,
	CONSTRAINT partner_member_FK
	FOREIGN KEY(memberFk)
	REFERENCES member(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
	CONSTRAINT partner_fallaYear_FK
	FOREIGN KEY(fallaYearFk)
	REFERENCES fallaYear(code)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS worker(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	surname VARCHAR(100) NOT NULL,
	dni VARCHAR(10),
	job VARCHAR(50),
	fallaYearFk INT NOT NULL,
	CONSTRAINT worker_fallaYear_FK
	FOREIGN KEY(fallaYearFk)
	REFERENCES fallaYear(code)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS supplier(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	nif VARCHAR(10),
	address VARCHAR(100),
	phoneNumber VARCHAR(15),
	email VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS supplierAccount(
	id INT AUTO_INCREMENT PRIMARY KEY,
	accountNumber VARCHAR(24) NOT NULL,
	supplierFk INT NOT NULL,
	CONSTRAINT supplierAccount_supplier_FK
	FOREIGN KEY(supplierFk)
	REFERENCES supplier(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS budgetItem(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	description VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS subItem(
	id INT AUTO_INCREMENT PRIMARY KEY,
	budgetItemFk INT NOT NULL,
	name VARCHAR(50) NOT NULL,
	description VARCHAR(100) NOT NULL,
	CONSTRAINT subItem_budgetItem_FK
	FOREIGN KEY(budgetItemFk)
	REFERENCES budgetItem(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS buy(
	id INT AUTO_INCREMENT PRIMARY KEY,
	subItemFk INT NOT NULL,
	supplierFk INT NOT NULL,
	amount DECIMAL(10, 2) NOT NULL,
	payMethod ENUM('efectiu', 'banc') NOT NULL,
	ticketReference VARCHAR(30),
	buyed DATE DEFAULT CURRENT_DATE,
	supplierAccountFk INT NOT NULL,
	digitizedDocument VARCHAR(30),
	CONSTRAINT buy_subItem_FK
	FOREIGN KEY(subItemFk)
	REFERENCES subItem(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
	CONSTRAINT buy_supplier_FK
	FOREIGN KEY(supplierFk)
	REFERENCES supplier(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS memberStatusLog(
	id INT AUTO_INCREMENT PRIMARY KEY,
	memberFk INT NOT NULL,
	status TINYINT(1) NOT NULL,
	created DATE DEFAULT CURRENT_DATE,
	CONSTRAINT memberStatusLog_member_FK
	FOREIGN KEY(memberFk)
	REFERENCES member(id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);