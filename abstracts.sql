CREATE TABLE Conference (
    conference_ID INTEGER PRIMARY KEY,
    start_date TEXT, -- YYYY-MM-DD
    end_date TEXT, -- YYYY-MM-DD
    conference_name TEXT,
    location TEXT,
    organization TEXT
);

CREATE TABLE People (
    person_ID INTEGER PRIMARY KEY,
    name TEXT, 
    role TEXT
);

CREATE TABLE Attended (
    c_id INTEGER,
    p_id INTEGER,
    PRIMARY KEY (c_id, p_id),
    FOREIGN KEY(p_id) REFERENCES People(person_ID),
    FOREIGN KEY(c_id) REFERENCES Conference(conference_ID)
);

CREATE TABLE Abstract (
    abstract_ID INTEGER PRIMARY KEY,
    internal_ID INTEGER,
    title TEXT,
    section TEXT,
    status TEXT CHECK (status IN ('Submitted', 'Draft', 'Draft Collection', 'Draft Analysis')),
    result TEXT,
    first_author INTEGER,
    submitter_ID INTEGER,
    presentation_day TEXT, -- YYYY-MM-DD
    presentation_time TEXT, -- HH:MM-HH:MM
    FOREIGN KEY(submitter_ID) REFERENCES People(person_ID),
    FOREIGN KEY(first_author) REFERENCES People(person_ID)
);

CREATE TABLE Authors (
    p_id INTEGER,
    a_id INTEGER,
    PRIMARY KEY (p_id, a_id),
    FOREIGN KEY(p_id) REFERENCES People(person_ID),
    FOREIGN KEY(a_id) REFERENCES Abstract(abstract_ID)
);

CREATE TABLE Presented (
    c_id INTEGER,
    a_id INTEGER,
    p_id INTEGER, -- presenter
    PRIMARY KEY (c_id, a_id, p_id),
    FOREIGN KEY(c_id) REFERENCES Conference(conference_ID),
    FOREIGN KEY(a_id) REFERENCES Abstract(abstract_ID),
    FOREIGN KEY(p_id) REFERENCES People(person_ID)
);