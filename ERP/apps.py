from django.apps import AppConfig
import pyodbc as pc
import pandas as pd
import datetime

class YourAppConfig(AppConfig):
    name = 'ERP'

    def ready(self):
        """
        print('***ready to setup connection***')
        databaseName = 'sreeman_live'
        username = 'sa'
        password = 'Hemanth@123'
        server = 'DESKTOP-L57QDTP\SQLEXPRESS'
        driver= '{SQL Server Native Client 10.0}'
        CONNECTION_STRING = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+databaseName+';UID='+username+';PWD='+ password

        databaseName1 = 'suriya_live'
        username1 = 'sa'
        password1 = 'Hemanth@123'
        server1 = 'DESKTOP-L57QDTP\SQLEXPRESS'
        driver1= '{SQL Server Native Client 10.0}'
        CONNECTION_STRING2 = 'DRIVER='+driver1+';SERVER='+server1+';DATABASE='+databaseName1+';UID='+username1+';PWD='+ password1
        
        """
        print('***ready to setup connection***')
        # Set up the connections
        databaseName = 'sreeman_live'
        username = 'sa'
        password = 'sa'
        server = 'SREEMAN-NEW'
        driver = '{SQL Server Native Client 10.0}'
        CONNECTION_STRING = 'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + databaseName + ';UID=' + username + ';PWD=' + password

        databaseName1 = 'suriya_live'
        username1 = 'sa'
        password1 = 'sa'
        server1 = 'SREEMAN-NEW'
        driver1 = '{SQL Server Native Client 10.0}'
        CONNECTION_STRING2 = 'DRIVER=' + driver1 + ';SERVER=' + server1 + ';DATABASE=' + databaseName1 + ';UID=' + username1 + ';PWD=' + password1
        
        # Create/Open connections
        conn = pc.connect(CONNECTION_STRING)
        conn1 = pc.connect(CONNECTION_STRING2)

        # Execute SQL queries and create DataFrames
        sql = "SELECT * FROM DBO.Sreeman_full_data_view"
        df_sreem = pd.read_sql(sql, conn)

        sql1 = "SELECT * FROM DBO.Suriya_full_data_view"
        df_suri = pd.read_sql(sql1, conn1)

        df_sreeman = df_sreem
        df_suriya = df_suri

        df_sreeman['Company'] = 'Sreeman'
        df_suriya['Company'] = 'Suriya'

        df = pd.concat([df_sreeman, df_suriya], ignore_index=True)

        def date_ext_mon1(mon):
            datee = datetime.datetime.strptime(mon, "%Y-%m-%d")
            month = datetime.date(datee.year, datee.month, datee.day).strftime('%B')
            return month

        def date_ext_year1(year):
            datee = datetime.datetime.strptime(year, "%Y-%m-%d")
            Year = datee.year
            return Year

        def date_ext_day1(day):
            datee = datetime.datetime.strptime(day, "%Y-%m-%d")
            Day = datee.day
            return Day

        # Apply date extraction functions to the DataFrame
        df['lr_hire_date'] = df['lr_hire_date'].astype(str)
        df['YEAR'] = df['lr_hire_date'].apply(lambda x: date_ext_year1(x))
        df['MONTH'] = df['lr_hire_date'].apply(lambda x: date_ext_mon1(x))
        df['DAY'] = df['lr_hire_date'].apply(lambda x: date_ext_day1(x))

        # Make the DataFrame available for use in views
        self.df = df
