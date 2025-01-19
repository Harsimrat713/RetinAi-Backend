CREATE SCHEMA RetinAI_DB;
GO
CREATE TABLE kiosks (
    kioskID CHAR(36) PRIMARY KEY,
    kioskLocation CHAR(36),
    kioskStatus CHAR(36), 
    initializationDate CHAR(36)
);
CREATE TABLE sessions (
    sessionID CHAR(36) PRIMARY KEY, 
    kioskID CHAR(36),
    imageLocation CHAR(100),
    chosenImageLeft CHAR(100),
    chosenImageRight CHAR(100)
);
CREATE TABLE images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    imageName char(36),
    sessionID char(36),
    eyeSide char(10),
    cropped BOOLEAN,
    prediction char(36),
    selectedForDisp BOOLEAN
);