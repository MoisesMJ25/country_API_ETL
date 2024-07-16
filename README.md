    Coderhouse's Data Engineering (final project)
    By Moisés Marquina Juliao

      Requirements (requirements.txt file)
You need to have installed "Docker"
For email alerts you can use: mailsender, gmail, sendgrid, ...

      Description
This code gives you all the tools you need to run a specific DAG on airflow called 'country_API_ETL'

      What the DAG does?:
1. Get data of six diferent APIs from the same source -----> [https://country.io/data/]
2. Manipulate all the data transforming it to a dataframe
3. Save the data in the datawarehouse on redshift
4. Inform the success or failure of the process by sending an email with the information

       Configure your credentials
1. On the '.env' file, put your redshift credentials, and set the [EMAIL_PASSWORD] that you got from your email account (mailsender, gmail, sendgrid, ...)
2. Also, you have to set your email configuration on the 'docker-compose.yaml' [AIRFLOW_VAR_EMAIL], [AIRFLOW_VAR_TO_ADDRESS]

        Go! Open your terminal and run:
1. ´docker compose up airflow-init´
2. ´docker composu up´
