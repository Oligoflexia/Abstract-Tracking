CREATE TABLE People (
    PersonID INTEGER PRIMARY KEY,
    prefix TEXT,
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT,
    post_nominals TEXT,
    role TEXT
);

CREATE TABLE Abstracts (
    AbstractID INTEGER PRIMARY KEY,
    title TEXT,
    authors BLOB, -- Just for human reference
    summary BLOB,
    pop_size INTEGER,
    year INTEGER,
    FOREIGN KEY(first_author) REFERENCES People(PersonID)
);

CREATE TABLE Conferences (
    ConferenceID INTEGER PRIMARY KEY,
    conference_name TEXT,
    location TEXT,
    start_date TEXT, -- YYYY-MM-DD
    end_date TEXT, -- YYYY-MM-DD
    organization TEXT
);

CREATE TABLE Attendances (
    ConferenceID INTEGER,
    PersonID INTEGER,
    role TEXT,
    PRIMARY KEY (ConferenceID, PersonID),
    FOREIGN KEY(PersonID) REFERENCES People(PersonID),
    FOREIGN KEY(ConferenceID) REFERENCES Conferences(ConferenceID)
);

CREATE TABLE Authorship (
    PersonID INTEGER,
    AbstractID INTEGER,
    role TEXT CHECK (status IN ('First Author', 'Co-First Author', 'Co-Author', 'Lab PI')),
    PRIMARY KEY (PersonID, AbstractID),
    FOREIGN KEY(PersonID) REFERENCES People(PersonID),
    FOREIGN KEY(AbstractID) REFERENCES Abstracts(AbstractID)
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
    FOREIGN KEY(PersonID) REFERENCES People(PersonID)
);

CREATE TABLE Submissions (
    internal_ID TEXT,
    ConferenceID INTEGER,
    AbstractID INTEGER,
    SubmitterID INTEGER,
    section TEXT,
    status TEXT CHECK (status IN ('Submitted', 'Draft', 'Draft Collection', 'Draft Analysis')),
    result TEXT,
    FOREIGN KEY(ConferenceID) REFERENCES Conferences(ConferenceID),
    FOREIGN KEY(AbstractID) REFERENCES Abstracts(AbstractID),
    FOREIGN KEY(SubmitterID) REFERENCES People(PersonID),
);