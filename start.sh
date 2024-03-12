#!bin/sh
nohup airflow scheduler &
exec airflow webserver