


                                                            <!-- Install docker and run mssql server -->


Step 1: Install Docker
    Download Docker


Step 2: Pull the SQL Server Docker Image

    Open Terminal or Command Prompt:
        Ensure Docker is running.

    Pull the MSSQL Server Docker Image:

    bash

    docker pull mcr.microsoft.com/mssql/server:2019-latest

    This command pulls the latest SQL Server 2019 image from Microsoft's container registry.

Step 3: Run the SQL Server Container

    Run the Docker Container:

    bash

    docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=Your_password123" -p 1433:1433 --name TestDB -d mcr.microsoft.com/mssql/server:2019-latest

        -e 'ACCEPT_EULA=Y': Accepts the end-user license agreement.
        -e 'SA_PASSWORD=Your_password123': Sets the password for the sa user. Make sure to use a strong password.
        -p 1433:1433: Maps port 1433 on your host to port 1433 on the container.
        --name sqlserver: Names the container sqlserver.
        -d: Runs the container in detached mode.

Step 4: Connect to SQL Server

    Download SQL Server Management Studio (SSMS):
        SQL Server Management Studio (SSMS)

    Open SSMS:
        Launch SQL Server Management Studio after installation.

    Connect to the Docker Container:
        Server Name: localhost,1433
        Authentication: SQL Server Authentication
        Login: sa
        Password: Your_password123
        Click Connect.

Step 5: Create a Database

    Create a New Database:
        In SSMS, right-click on Databases in the Object Explorer.
        Select New Database....
        Enter the database name (e.g., TestDB).
        Click OK.

Step 6: Use the Database

    Create a Table:
        Right-click on your new database (TestDB), go to Tables, and select New > Table....
        Define columns (e.g., ID, Name, Age).
        Save the table (e.g., Person).

    Insert Data:
        Open a new query window.
        Insert sample data:

        sql

    INSERT INTO TestDB.dbo.Person (Name, Age)
    VALUES ('John Doe', 30), ('Jane Smith', 25);

    Execute the query.

Query Data:

    In a new query window, select the data:

    sql

        SELECT * FROM TestDB.dbo.Person;

        Execute the query to see the results.

Step 7: Stop and Start the Container

    Stop the Container:

    bash

docker stop sqlserver

Start the Container:

bash

docker start sqlserver