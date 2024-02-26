# PostgreSQL Data Migration

Set of tools and scripts designed to facilitate the data migration process between PostgreSQL databases.

## Getting Started 🚀
Clone the following repository to your local folder.

***
### Pre-Prerequisites 📋
   ```
   1) Have Python 3.8 or higher installed.
   2) Have VirtualEnviroment installed.
   3) Create a .env file and place it in the project root (refer to .envExample).
   4) Create a queries.yaml file and place it in the project root. *
```
* The queries.yaml file defines SQL queries for data migration. The structure of the file is as follows:
   ```
   tables:
   <table_name>:
      queries:
         select:
   <table_name>:
      columns:
      queries:
         insert:
   ```

   #### Considerations:
   * Source Tables: Source tables must have a select section within queries that defines the SQL query to extract data.
   * Target Tables: Target tables must have an insert section within queries that defines the SQL query to insert data.
   * Columns: The columns section defines the columns to be inserted into the target table. The order of the columns must match the order of values in the insert query as they are specified using placeholders %s.

***
### Installation 🔧

Once the repository is cloned, open it in your favorite IDE and open a terminal where you will execute the following code to install the project dependencies.
```
pip install -r requirements.txt
```

***
### Ejecución 🧑‍💻
To execute the migration, you should navigate to the command line and pass the following parameters to the execution statement in the following order:

   > -id --> (initDate) Represents the Start Date to retrieve records from the Source Database (Format YYYY-MM-DD).

   > -ed --> (endDate) Represents the End Date to retrieve records from the Source Database (Format YYYY-MM-DD).

   > -to --> (tableOrigin) Represents the table from which data will be extracted from the Source Database.

   > -tt --> (tableTarget) Represents the table into which data will be inserted into the Target Database.

For each parameter, the parameter name should be followed by a space and the specified value. Example:

> -id 2019-06-20

All the parameters shown are required; if not passed in that order and in the explained format, the execution will not take place.

The file to execute to start the migration is:
```
app.py
```

Example execution statement for the simulation:
```
$ python3 app.py -id '2020-01-01' -ed '2024-01-01' -to affiliate -tt new_affiliate
```

***
## Audit 🕵️‍♂️
Each execution request to perform the simulation, whether successful or not, will be stored in a Log file that will be in the project root, which will have the following name:
```
audit.log.{fecha_ejecución}.csv
```
> Where {execution_date} --> Represents the date of creation of the .log file

This log file will be created once per day, provided the simulation request is executed, and will store the records displayed on the console for the corresponding day.

***
## Contributions
The community is invited to participate in the project development.

***
## Roadmap 📝
The project is in continuous development, and the following improvements are planned:

* Expansion of support for new database platforms.
* Development of a graphical user interface to facilitate interaction with the tool.
* Improvement and expansion of available documentation.

***
## Autor ✒️

* **Franz Suárez** - *Backend Developer* - [fsuarezr](https://github.com/fsuarezr)

🧑‍💻 with ❤️ by [fsuarezr](https://github.com/fsuarezr) 🤘 