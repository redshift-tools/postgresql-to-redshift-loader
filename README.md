# PostgreSQL-to-Redshift-Data-Loader
    Ground to cloud data integration tool
    Used for ad-hoc query data results load from PostgreSQL to Amazon-Redshift.
    Works from Windows CLI (command line).

**NOTE**: This script requires Windows PostgreSql client (_bin\psql.exe_) for data [extract](https://github.com/alexbuz/PostgreSQL_To_Redshift_Loader/blob/master/sources/include/extractor.py).

Features:
 - Loads PostgreSQL table (or query) data to Amazon-Redshift.
 - Automatically uploads compressed data to S3 before append to Redshift table.
 - AWS Access Keys are not passed as arguments. 
 - You can modify default Python [extractor.py](https://github.com/alexbuz/PostgreSQL_To_Redshift_Loader/blob/master/sources/include/extractor.py) and [loader.py](https://github.com/alexbuz/PostgreSQL_To_Redshift_Loader/blob/master/sources/include/loader.py)
 - Written using Python/boto/psycopg2/PyInstaller.


## Other scripts
  - [Oracle -> S3](https://github.com/alexbuz/Oracle_To_S3_Data_Uploader/blob/master/README.md) data loader| [TableHunter for Oracle](https://github.com/alexbuz/TableHunter-For-Oracle) | [DataWorm](https://github.com/alexbuz/DataWorm/blob/master/README.md) 
  - [Oracle -> Redshift](https://github.com/alexbuz/Oracle-To-Redshift-Data-Loader/blob/master/README.md) data loader
  - [MySQL -> Redshift](https://github.com/alexbuz/MySQL_To_Redshift_Loader/blob/master/README.md) data loader
  - [CSV -> Redshift](https://github.com/alexbuz/CSV_Loader_For_Redshift/blob/master/README.md) data loader
  - [EC2 Metcics Plotter](https://github.com/alexbuz/EC2_Metrics_Plotter/blob/master/README.md)
  - [Oracle->Oracle](https://github.com/alexbuz/TabZilla/blob/master/README.md) data loader.
  - [Oracle->MySQL](https://github.com/alexbuz/Oracle-to-MySQL-DataMigrator/blob/master/README.txt) data loader.
  - [CSV->S3](https://github.com/alexbuz/S3_File_Uploader/blob/master/README.md) data uploader.

## Purpose

- Stream/pipe/load PostgreSQL table data to Amazon-Redshift.

## How it works
- Tool connects to source PostgreSQL DB and opens data pipe for reading.
- Data stream is compressed and pumped to S3 using multipart upload.
- Optional upload to Reduced Redundancy storage (not RR by default).
- Optional "make it public" after upload (private by default).
- If S3 bucket doesn't exists it will be created.
- You can control the region where new bucket is created.
- Streamed data can be tee'd (dumped on disk) during load.
- If not set, S3 Key defaulted to input query file name.
- Data is loaded to Redshift from S3 using COPY command
- Target Redshift table has to exist
- It's a Python/boto/psycopg2 script
	* Boto S3 docs: http://boto.cloudhackers.com/en/latest/ref/s3.html
	* psycopg2 docs: http://initd.org/psycopg/docs/
- Executable is created using [pyInstaller] (http://www.pyinstaller.org/)

## Audience

Database/ETL developers, Data Integrators, Data Engineers, Business Analysts, AWS Developers, SysOps

##Designated Environment
Pre-Prod (UAT/QA/DEV)

## Usage

```
c:\Python35-32\PROJECTS\PostgreSQL2redshift>dist\PostgreSQL_to_Redshift_loader.exe
#############################################################################
#PostgreSQL-to-Redshift Data Loader (v1.2, beta, 04/05/2016 15:11:53) [64bit]
#Copyright (c): 2016 Alex Buzunov, All rights reserved.
#Agreement: Use this tool at your own risk. Author is not liable for any damages
#           or losses related to the use of this software.
################################################################################
Usage:
  set AWS_ACCESS_KEY_ID=test_key
  set AWS_SECRET_ACCESS_KEY=test_secret_key
  set PGPASSWORD=test123
  set PGRES_CLIENT_HOME="C:\Program Files\PostgreSQL\9.5"

  set REDSHIFT_CONNECT_STRING="dbname='***' port='5439' user='***' password='***' host='mycluster.***.redshift.amazonaws.com'"  
  
  
  postgresql_to_redshift_loader.exe [<pgres_query_file>] [<pgres_col_delim>] [<pgres_add_header>] 
			    [<s3_bucket_name>] [<s3_key_name>] [<s3_use_rr>] [<s3_public>]
	
	--pgres_query_file -- SQL query to execure in source PostgreSQL db.
	--pgres_col_delim  -- CSV column delimiter for downstream(,).
	--pgres_quote	-- Enclose values in quotes (")
	--pgres_add_header -- Add header line to CSV file (False).
	--pgres_lame_duck  -- Limit rows for trial upload (1000).
	--create_data_dump -- Use it if you want to persist streamed data on your filesystem.
	
	--s3_bucket_name -- S3 bucket name (always set it).
	--s3_location	 -- New bucket location name (us-west-2)
				Set it if you are creating new bucket
	--s3_key_name 	 -- CSV file name (to store query results on S3).
		if <s3_key_name> is not specified, the PostgreSQL query filename (ora_query_file) will be used.
	--s3_use_rr -- Use reduced redundancy storage (False).
	--s3_write_chunk_size -- Chunk size for multipart upoad to S3 (10<<21, ~20MB).
	--s3_public -- Make uploaded file public (False).
	
	--red_to_table  -- Target Amazon-Redshit table name.
	--red_col_delim  -- CSV column delimiter for upstream(,).
	--red_quote 	-- Set it if input values are quoted.
	--red_timeformat -- Timestamp format for Redshift ('MM/DD/YYYY HH12:MI:SS').
	--red_ignoreheader -- skip header in input stream
	
	PostgreSQL data uploaded to S3 is always compressed (gzip).

	Boto S3 docs: http://boto.cloudhackers.com/en/latest/ref/s3.html
	psycopg2 docs: http://initd.org/psycopg/docs/

```
# Example


### Environment variables
Set the following environment variables (for all tests):

```
  set AWS_ACCESS_KEY_ID=test_key
  set AWS_SECRET_ACCESS_KEY=test_secret_key
  set PGPASSWORD=test123
  set PGRES_CLIENT_HOME="C:\Program Files\PostgreSQL\9.5"

  set REDSHIFT_CONNECT_STRING="dbname='***' port='5439' user='***' password='***' host='mycluster.***.redshift.amazonaws.com'"  
  

```

### Test load with data dump.
PostgreSQL table `crime_test` contains data from data.gov [Crime](https://catalog.data.gov/dataset/crime) dataset.
In this example complete table `crime_test` get's uploaded to Aamzon-S3 as compressed CSV file.

Contents of the file *table_query.sql*:

```
SELECT * FROM crime_test;

```
Also temporary dump file is created for analysis (by default there are no files created)
Use `-s, --create_data_dump` to dump streamed data.

If target bucket does not exists it will be created in user controlled region.
Use argument `-t, --s3_location` to set target region name

Contents of the file *test.bat*:
```
dist-64bit\PostgreSQL_to_redshift_loader.exe ^
-q table_query.sql ^
-d "," ^
-b test_bucket ^
-k postgresql_table_export ^
-r ^
-o crime_test ^
-m "DD/MM/YYYY HH12:MI:SS" ^
-s
```
Executing `test.bat`:

```
c:\Python35-32\PROJECTS\PostgreSQL2redshift>dist-64bit\PostgreSQL_to_redshift_loader.exe -q table_query.sql -d "," -b test_bucket -k postgresql_table_export -r -o crime_test -m "DD/MM/YYYY HH12:MI:SS" -s
Uploading results of "table_query.sql" to existing bucket "test_bucket"
Started reading from PostgreSQL (1.25 sec).
Dumping data to: c:\Python35-32\PROJECTS\Ora2redshift\data_dump\table_query\test_bucket\postgresql_table_export.20160408_203221.gz
1 chunk 10.0 MB [11.36 sec]
2 chunk 10.0 MB [11.08 sec]
3 chunk 10.0 MB [11.14 sec]
4 chunk 10.0 MB [11.12 sec]
5 chunk 877.66 MB [0.96 sec]
Size: Uncompressed: 40.86 MB
Size: Compressed  : 8.95 MB
Elapsed: PostgreSQL+S3    :69.12 sec.
Elapsed: S3->Redshift :3.68 sec.
--------------------------------
Total elapsed: 72.81 sec.


```

### Modifying default Redshift COPY command.
You can modify default Redshift COPY command this script is using.

Open file `include\loader.py` and modify `sql` variable on line 24.

```
	sql="""
COPY %s FROM '%s' 
	CREDENTIALS 'aws_access_key_id=%s;aws_secret_access_key=%s' 
	DELIMITER '%s' 
	FORMAT CSV %s 
	GZIP 
	%s 
	%s; 
	COMMIT;
	...
```


## Teardown
https://github.com/pydemo/teardown


## Snowpipe

https://github.com/pydemo/Snowpipe-For-SQLServer


[<img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png">](https://www.buymeacoffee.com/0nJ32Xg)









