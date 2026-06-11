-- Raw SQL Schema equivalent of the SQLAlchemy Models --
-- Used for reference or raw execution --

CREATE TABLE campaigns (
    Campaign_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Campaign_Name TEXT NOT NULL,
    Platform TEXT,
    Spend REAL,
    Revenue REAL,
    Clicks INTEGER,
    Impressions INTEGER,
    Conversions INTEGER,
    Date DATE
);

CREATE TABLE audiences (
    Audience_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Age_Group TEXT,
    Gender TEXT,
    Device TEXT,
    Location TEXT,
    Campaign_ID INTEGER,
    FOREIGN KEY (Campaign_ID) REFERENCES campaigns (Campaign_ID)
);

CREATE TABLE metrics (
    Metric_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    CTR REAL,
    CPC REAL,
    CPM REAL,
    ROAS REAL,
    Conversion_Rate REAL,
    Campaign_ID INTEGER,
    FOREIGN KEY (Campaign_ID) REFERENCES campaigns (Campaign_ID)
);
