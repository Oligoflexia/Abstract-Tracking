TO-DO:

Project Critical:
- [ ] Bugs / Errors
    - [ ] (SQLExplorer) Handle SQL commands that do not return a table
    - [ ] (Data File Upload) Should open to user root
    - [ ] (App) Error notifications when no DB selected
    - [ ] (App) Correct internal vs external imports
    - [ ] (App) find out why inheritance isn't working between parent -> SecondaryWindow
    - [ ] (App) error messages showing behind opened window
    - [ ] (CSVEntry) window resizing to conferences table (or scrollbar)
    - [ ] (CSVEntry) AttributeError if opening app without DB selected
    - [ ] (CSVEntry) ValueError if opening app without spreadsheet selected
    - [ ] (CSVEntry) Selecting a conference exits out the main application
    - [ ] (CSVEntry) Add a scrollbar to Conferences table

- [ ] (CSV Entry) first author handling on abstract CSV record entry
- [ ] (CSV Entry) CSV sanity checks
- [ ] (CSV Entry) non 2-word name handling for People
- [ ] (DBExplorer) Create UI elements for viewing tables
- [ ] (DBExplorer) Implement UI elements to create, delete, and update
    - [ ] individual records
    - [ ] tables (hide behind advanced setting?)
- [ ] (Settings) hiding destructive DB operations
- [ ] (Settings) remember last DB
- [ ] (App) disallow multiple instances of the apps


Eventually:
- [ ] unit testing
- [ ] automated back-ups of database
- [ ] app deployment (Docker?)
- [ ] function to spit db -> CSV
- [ ] consider moving utils, config, data, docs into app module

- [ ] Documentation
    - [ ] public SQLExplorer
    - [ ] public DBExplorer
    - [ ] public Application
    - [ ] internal Docstrings
    - [ ] review dependencies / backwards compatability
    - [ ] Figure out the proper standard for .pyi type hints

- [ ] Formatting / Refactoring
    - [ ] PEP8 Compliance
- [ ] Review license and privacy information


Time Permitting:
- [ ] UI aesthetics improvements
    - [ ] button icons
    - [ ] ttkbootstrap themes?
    - [ ] banner legibility on different OS
    - [ ] considtent padding