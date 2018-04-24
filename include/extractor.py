import re, os,sys
from subprocess import PIPE,Popen
import psycopg2
import cStringIO
from pprint import pprint
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
e=sys.exit

# dict g - is a calling env Globals()
opt= g['opt']
PGRES_CLIENT_HOME = g['PGRES_CLIENT_HOME']
PGPASSWORD = g['PGPASSWORD']

	
def extract(env):
	
	in_qry=open(opt.pgres_query_file, "r").read().strip().strip(';')
	db_client_dbshell=r'%s\bin\psql.exe' % PGRES_CLIENT_HOME.strip('"')
	#print db_client_dbshell
	#e(0)
	loadConf=[ db_client_dbshell ,'-U', opt.pgres_user,'-d',opt.pgres_db_name, '-h', opt.pgres_db_server]
	
	
	header_str=''
	#if opt.ora_add_header:
	#	header_str=' CSV HEADER'
	limit=''
	if opt.pgres_lame_duck>0:
		limit='LIMIT %d' % opt.pgres_lame_duck
	quote=''
	if opt.pgres_lame_duck>0:
		quote='QUOTE  \'%s\'' % opt.pgres_quote
		
	#select * from crime_test
	q="""
	COPY ((%s) %s)
TO STDOUT
WITH DELIMITER ','
CSV %s
	""" % (in_qry, limit, quote)
	#print q
	p1 = Popen(['echo', q], stdout=PIPE,stderr=PIPE,env=env)
	
	
	p2 = Popen(loadConf, stdin=p1.stdout, stdout=PIPE,stderr=PIPE)
	output=' '
	status=0
	if 0:
		while output:
			output = p2.stdout.readline()
			print output
	#e(0)
	p1.wait()
	return p2

	


	