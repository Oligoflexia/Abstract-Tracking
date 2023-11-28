CREATE TABLE People (
    PersonID INTEGER PRIMARY KEY,
    prefix TEXT,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    last_name TEXT,
    post_nominals TEXT,
    role TEXT,
);

CREATE TABLE Abstracts (
    AbstractID INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT, -- Just for human reference
    summary BLOB,
    pop_size INTEGER,
    year INTEGER,
);

CREATE TABLE Conferences (
    ConferenceID INTEGER PRIMARY KEY,
    conference_name TEXT NOT NULL,
    location TEXT,
    start_date TEXT, -- YYYY-MM-DD
    end_date TEXT, -- YYYY-MM-DD
    organization TEXT,
);

CREATE TABLE Attendances (
    ConferenceID INTEGER,
    PersonID INTEGER,
    role TEXT,
    PRIMARY KEY (ConferenceID, PersonID),
    FOREIGN KEY(PersonID) REFERENCES People(PersonID),
    FOREIGN KEY(ConferenceID) REFERENCES Conferences(ConferenceID),
);

CREATE TABLE Authorship (
    PersonID INTEGER,
    AbstractID INTEGER,
    role TEXT CHECK (status IN ('First Author', 'Co-First Author', 'Co-Author', 'Lab PI')),
    PRIMARY KEY (PersonID, AbstractID),
    FOREIGN KEY(PersonID) REFERENCES People(PersonID),
    FOREIGN KEY(AbstractID) REFERENCES Abstracts(AbstractID),
);

CREATE TABLE Presentations (
    ConferenceID INTEGER,
    AbstractID INTEGER,
    PersonID INTEGER, -- presenter
    presentation_day TEXT, -- YYYY-MM-DD
    presentation_time TEXT, -- HH:MM-HH:MM
    PRIMARY KEY (ConferenceID, AbstractID, PersonID),
    FOREIGN KEY(ConferenceID) REFERENCES Conferences(ConferenceID),
    FOREIGN KEY(AbstractID) REFERENCES Abstracts(AbstractID),
    FOREIGN KEY(PersonID) REFERENCES People(PersonID),
);

CREATE TABLE Submissions (
    SubmissionID INTEGER PRIMARY KEY,
    internal_ID TEXT,
    ConferenceID INTEGER,
    AbstractID INTEGER,
    SubmitterID INTEGER,
    section TEXT,
    status TEXT CHECK (status IN ('Submitted', 'Draft', 'Draft Collection', 'Draft Analysis')) NOT NULL,
    result TEXT,
    FOREIGN KEY(ConferenceID) REFERENCES Conferences(ConferenceID),
    FOREIGN KEY(AbstractID) REFERENCES Abstracts(AbstractID),
    FOREIGN KEY(SubmitterID) REFERENCES People(PersonID),
);

-- People
CREATE INDEX fname_idx ON People (first_name);

-- Abstracts

-- Conferences
CREATE INDEX confname_idx ON Conferences (conference_name);

-- Attendances
CREATE INDEX attd_idx ON Attendance (ConferenceID, PersonID);

-- Authorship
CREATE INDEX author_idx ON Authorship (PersonID, AbstractID);

-- Presentations
CREATE INDEX pres_idx ON Presentations (ConferenceID, PersonID);

-- Submissions
CREATE INDEX subm_idx ON Submissions (result, ConferenceID);