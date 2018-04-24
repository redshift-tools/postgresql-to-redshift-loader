set AWS_ACCESS_KEY_ID=***
set AWS_SECRET_ACCESS_KEY=***
set PGPASSWORD= test
set PGCLIENTENCODING=UTF8
set PGRES_CLIENT_HOME="C:\Program Files\PostgreSQL\9.5"
set REDSHIFT_CONNECT_STRING="dbname='test' port='5439' user='test' password='test' host='test.cxvkqzwtuva2.us-west-2.redshift.amazonaws.com'"

python postgresql_to_redshift_loader.py -q test_query.sql -d ","  -b testbucket -k oracle_table_export -r -p -o crime_test -m "YYYY-MM-DD HH24:MI:SS" -l 100
