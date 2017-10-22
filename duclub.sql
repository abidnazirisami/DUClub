CREATE TABLE Accounts (
    MemberID int primary key AUTO_INCREMENT,
    MemberName varchar(255),
    MemberContactNo varchar(20),
    MemberPresentAdress varchar(2555),
    MemberPermanentAdress varchar(2555),
    designation varchar(100),
    department varchar(100),
    status varchar(40),
     email varchar(100),
     password varchar(2555),
     type varchar(255) 
);


CREATE TABLE Lounge (
      LoungeID int key NOT NULL AUTO_INCREMENT,
      LoungeName varchar(255)
);

CREATE TABLE FoodItem (
      FoodID int primary key NOT NULL AUTO_INCREMENT,
      FoodName varchar(2555),
      FoodPrice int,
      weekBitmask int,
      timeBitmask int
);

INSERT INTO FoodItem (FoodName, FoodPrice, weekBitMask, timeBitmask) VALUES
( 'Chitoipitha', 10, 91001001, 91010),
('Rumaliruti', 15, 91111111, 91010),
('Beef', 70, 91111111, 90101),
('Daal', 60, 91000100, 91101),
('Vegetable', 30, 91000100, 91101),
('Daalpuri', 5, 91111111, 91010),
('Alupuri', 5, 91111111, 91010),
('Sandwich', 40, 91111111, 91010),
('Bombay Toast', 10, 91111111, 91010),
('Soup', 60, 90101011, 91010),
('Lachchi', 40, 90100100, 91111),
('Vapapitha', 5, 90100000, 91010),
('Chicken fry', 50, 90100000, 91111),
('Alu chop', 5, 90001110, 91010),
('Cholapiaju', 40, 90010000, 91010),
('Chicken grill', 120, 90010010, 90101),
('Moghlaiparatha', 50, 90001001, 91010),
('Shingara', 5, 90001001, 91010),
('Shkkabab', 60, 90001001, 90101),
('Luchi', 5, 90001001, 91010),
('Sola Batura', 20, 90000100, 91010),
('Somucha', 10, 90000100, 91010),
('Paratha', 5, 90000010, 91010),
('Chicken', 100, 91111111, 91111),
('Tea', 20, 90000000, 91111),
('coffee', 20, 91111111, 91111);

CREATE TABLE GameTable (
      GameID int primary key NOT NULL AUTO_INCREMENT,
      GameName varchar(2555),
      GameFee int
);

CREATE TABLE Admin(
      MemberID int,
      AdminID int primary key NOT NULL AUTO_INCREMENT,
      adminPassword varchar(2555),
CONSTRAINT FK_MemberID FOREIGN KEY (MemberID) REFERENCES Accounts(MemberID)
);

CREATE TABLE LoungeBooking(
      LoungeID int,
      bookingID int primary key NOT NULL AUTO_INCREMENT,
      startTime datetime,
      endTime datetime,
CONSTRAINT FK_LoungeID FOREIGN KEY (LoungeID) REFERENCES Lounge(LoungeID)
);


CREATE TABLE GameBooking(
      LoungeID int,
      GameID int,
      GLID int primary key NOT NULL AUTO_INCREMENT,
      GameStartTime datetime,
      GameEndTime datetime,
CONSTRAINT FK_GameLoungeID FOREIGN KEY (LoungeID) REFERENCES Lounge(LoungeID),

CONSTRAINT GameLID FOREIGN KEY (GameID) REFERENCES GameTable(GameID)
);

CREATE TABLE BillTable(
      LoungeID int,
      FoodID int,
      BillID int primary key NOT NULL AUTO_INCREMENT,
      MemberID int,
      Quantity int,
      Discount double(10,2),
      Date date,
     Total double(10,2),
CONSTRAINT FK_BillLoungeID FOREIGN KEY (LoungeID) REFERENCES Lounge(LoungeID),

CONSTRAINT FK_BilMemberID FOREIGN KEY (MemberID) REFERENCES Accounts(MemberID),

CONSTRAINT FK_BillFoodID FOREIGN KEY (FoodID) REFERENCES FoodItem(FoodID)

);

INSERT INTO Accounts (MemberName, MemberContactNo, MemberPresentAdress, MemberPermanentAdress, designation, email) VALUES
('A A M S Arefin Siddique', '+8801700000000', 'V C Banglo', 'Dhaka','',  'email@example.com' ),
('Dr. (Mrs.) Begum Akhter Kamal', '1711282835', '', '','', 'trinatanniarush@gmail.com'),
('Dr. (Mrs.) Siddiqua Mahmuda', '9611997', '', '', '',  'hmahmuda001@hotmail.com'),
('Dr. Bismadeb Chowdhury', '1715547113', '', '','',  'bdarpi@yahoo.com'),
('Dr. Biswajit Ghosh', '11199029200', '', '','',  'bgdubd1957@gmail.com'),
('Dr. Syed Md. Shahed', '9887802', '', '','',   'bng05@gmail.com'),
('Rafique Ullah Khan', '1715150685', '', '','',  'khanrafique_ullah@yahoo.com'),
('Dr. Md. Shajahan Mia', '1715042588', '', '','',  'bng07@gmail.com'),
('Dr. Syed Azizul Huq', '1748213112', '', '','',   'bng08@gmail.com'),
('Dr. Mrs. Fatema Kawser', '1552313382', '', '','',  'bng09@gmail.com'),
('Dr. Serajul Islam (Seraj Salekin)', '1556981186','', '', '',  'serajsalekeen@gmail.com'),
('Dr. Soumitra Sekhar Dey', '1732102103', '', '','',   'scpcdu@gmail.com'),
('Dr. Baitullah Quaderee', '', '', '','',  'quaderee@yahoo.com'),
('Dr. Md. Giashuddin (Gias Shameem)', '1552341789', '', '','',  'bng11@gmail.com'),
('Dr. Nurunnaher Feayzur Nessa', '9117107', '', '','',  'naher601@gmail.com'),
('Mrs. Hosne Ara', '9668136', '','', '',  'hosneara-happy@gmail.com'),
('Dr Md. Abdus Sobhan Talukder', '1713046183', '', '','',   'bng12@gmail.com'),
('Dr. Mohammad Azam', '1552541646', '', '','',  'mazam1975@hotmail.com'),
('Mrs. Meher Niger', '1731021670', '', '','', 'junebdc@yahoo.com');


delimiter //
CREATE PROCEDURE addM (IN param1 VARCHAR(255))
BEGIN
INSERT INTO Accounts(MemberName) VALUES (param1);
END //

delimiter ;


delimiter //
CREATE PROCEDURE addMember (IN name VARCHAR(255), IN cell_no VARCHAR(20), IN presentad VARCHAR(2555), IN permanentad VARCHAR(2555), IN designation VARCHAR(100), IN dept VARCHAR(100), IN status VARCHAR(40), mail VARCHAR(100), type VARCHAR(255))
BEGIN
INSERT INTO Accounts(MemberName, MemberContactNo, MemberPresentAdress, MemberPermanentAdress, designation, department, status, email, type) VALUES (name, cell_no, presentad, permanentad, designation, dept, status, mail, type);
END //

delimiter ;


delimiter //
CREATE PROCEDURE deleteMember (IN memID int)
BEGIN
delete from Accounts
where memberID = memID;
END //

delimiter ;


delimiter //
CREATE PROCEDURE updateMember (IN memid int, IN name VARCHAR(255), IN cell_no VARCHAR(20), IN presentad VARCHAR(2555), IN permanentad VARCHAR(2555), IN designation VARCHAR(100), IN dept VARCHAR(100), IN status VARCHAR(40), mail VARCHAR(100), type VARCHAR(255))
BEGIN
update Accounts
set MemberName = name, MemberContactNo = cell_no, MemberPresentAdress = presentad, MemberPermanentAdress = permanentad, designation = designation, department = dept, status = status, email = mail , type = type
where memberID = memid;

END //

delimiter ;

delimiter //
CREATE PROCEDURE addLounge (IN name VARCHAR(255))
BEGIN
INSERT INTO Lounge(LoungeName)
VALUES (name);
END //
delimiter ;


delimiter //
CREATE PROCEDURE addLounge (IN name VARCHAR(255))
BEGIN
INSERT INTO Lounge(LoungeName)
VALUES (name);
END //
delimiter;


delimiter //
CREATE PROCEDURE deleteLounge (IN lngID int)
BEGIN
delete from Lounge
where loungeID = lngID;
END //

delimiter ;

delimiter //
CREATE PROCEDURE updateLounge (IN longeid int,IN name VARCHAR(255))
BEGIN
update Lounge
set loungeName = name
where loungeID = longeid;

END //

delimiter ;

delimiter //
CREATE PROCEDURE searchMemWithName (IN search_id VARCHAR(255))
BEGIN
select MemberID, MemberName from Accounts where MemberName like CONCAT('%', search_id, '%');
END //
delimiter ;


delimiter //
CREATE PROCEDURE searchMemWithID (IN search_id int(11))
BEGIN
select MemberID, MemberName from Accounts where MemberID = search_id;
END //
delimiter ;

delimiter //
CREATE PROCEDURE searchMemAll ()
BEGIN
select MemberID, MemberName from Accounts;
END //
delimiter ;




