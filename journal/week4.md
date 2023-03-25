# Week 4 — Postgres and RDS
## Task 1: To provision RDS Postgres Instance. Run the following  commands.
```
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username cruddurroot\
  --master-user-password xxxxxxxxxx\
  --allocated-storage 20 \
  --availability-zone us-east-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
```
Now compose up.Then open AWS Console and make sure the RDS,we created is there and the database is available.
![Dbimage](week4_images/DBinstance.jpg)
## Task 2: Connect with the Postgres database by running Bash scripts.
` psql -U postgres --host localhost `
### Step 1: Create database,select postgres bash.
`CREATE database cruddur;`

![Dbimage](week4_images/CreateDB.jpg)

 ### Step 2: Now create a folder under directory "backend-flask/db" then create a file "schema.sql"
```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
DROP TABLE IF EXISTS public.users;

DROP TABLE IF EXISTS public.activities;
CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text NOT NULL,
  handle text NOT NULL,
  email text NOT NULL,
  cognito_user_id text NOT NULL,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
CREATE TABLE public.activities (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  reply_to_activity_uuid integer,
  expires_at TIMESTAMP,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```
### Step 3: Run this command on the terminal.
` psql cruddur < db/schema.sql -h localhost -U postgres `
![Dbimage](week4_images/SchemaSql.jpg)
### Step 4: Set environment variable for the connection URL.

` export CONNECTION_URL="postgresql://postgres:xxxxx@127.0.0.1:5432/cruddur" `

 `gp env  CONNECTION_URL="postgresql://postgres:xxxxx@127.0.0.1:5432/cruddur"`

To make sure the env var is set:
`env | grep CONNECTION_URL`
### Step 5: Set environment variable for production.

`export PROD_CONNECTION_URL="postgresql://cruddurroot:xxxxxx@database endpoint:5432/cruddur"`

`gp env PROD_CONNECTION_URL="postgresql://cruddurroot:xxxxxx@database endpoint:5432/cruddur"`
To make sure the env var is set run:
`env | grep PROD_CONNECTION_URL`

### Step 6: Create a bash file under directory "backend-flask/bin/db-drop" to drop the database.
```
#! /usr/bin/bash
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-drop"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "DROP DATABASE IF EXISTS cruddur;"
```
Now on terminal test: ./bin/db-create
Result: permission denied 
To grant permission for read,write & execution operations:
Run:  `chmod u+x bin/db-create`
Run:   `ls -l ./bin`
Run:  ` chmod +x bin/db-drop`
Run:   `ls -l ./bin`
Run:   `./bin/db-drop`
Result:  DROP DATABASE
### Step 7: Create a bash file under directory " backend-flask/bin/db-create" to create databse.
```
#! /usr/bin/bash
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-create"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
echo "db-create"
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "CREATE database cruddur;"
```
To grant permission for read,write & execution operations:
Run:  ` chmod +x bin/db-drop`
Run:   `ls -l ./bin`
Run:   `./bin/db-create`
Result:  CREATE DATABASE
### Step 8: Create a bash file under directory "backend-flask/bin/db-schema-load" to load the schema.
```
#! /usr/bin/bash
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-schema-load"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
schema_path="$(realpath .)/db/schema.sql"
echo $schema_path

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi
psql $URL cruddur < $schema_path
```
To grant permission for read,write & execution operations:
Run:   `chmod u+x bin/db-schema-load`
 Run:   `ls -l ./bin`
Run:   `./bin/db-schema-load`
Result:  CREATE Extension
Run:   `./bin/db-schema-load prod '
Result:  Running production

![Dbimage](week4_images/Schemaload.jpg)

### Step 8: Create a SQL Query file under directory "backend-flask/db/schema.sql"
```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;
CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text NOT NULL,
  handle text NOT NULL,
  email text NOT NULL,
  cognito_user_id text NOT NULL,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
CREATE TABLE public.activities (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  reply_to_activity_uuid integer,
  expires_at TIMESTAMP,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```
![Dbimage](week4_images/UserActivities.jpg)

### Step 9: Create a bash file under directory "backend-flask/bin/db-connect" 
```
#! /usr/bin/bash
if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi
psql $URL 
psql $CONNECTION_URL
```
To grant permission for read,write & execution operations:
Run:   `chmod u+x bin/db-connect`
 Run:   `ls -l ./bin`
Run:   `./bin/db-connect`
Result: you will be able connect to the database "cruddur" run,  " \l , \dt " so,you can see users and activities table in the database.

![Dbimage](week4_images/Production.jpg)

### Step 10: Create a bash file under directory "backend-flask/bin/db-seed" 
```
#! /usr/bin/bash
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-seed"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
seed_path="$(realpath .)/db/seed.sql"
echo $seed_path
psql $CONNECTION_URL cruddur < $seed_path
```
![Dbimage](week4_images/seed.jpg)

### Step 11: Create a SQL Query file under directory "backend-flask/db/seed.sql"
```
INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown' ,'MOCK'),
  ('Andrew Bayko', 'bayko' ,'MOCK');
INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
```
To grant permission for read,write & execution operations:

RUN:  `chmod u+x ./bin/db-schema-load`
Run:  `./bin/db-seed`

Results: INSERT 0 2,INSERT 0 1

### Step 12: Connect with the database.

RUN: `./bin/db-connect`

cruddur#: \dt  to see tables

cruddur#: `SELECT * FROM activities;`
### Step 13: Create a bash file under directory "backend-flask/bin/db-sessions"
```
#! /usr/bin/bash
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-sessions"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi
NO_DB_URL=$(sed 's/\/cruddur//g' <<<"$URL")
psql $NO_DB_URL -c "select pid as process_id, \
       usename as user,  \
       datname as db, \
       client_addr, \
       application_name as app,\
       state \
from pg_stat_activity;"
```
To grant permission for read,write & execution operations:

RUN:  `chmod u+x ./bin/db-sessions`

Run: `./bin/db-sessions`

![Dbimage](week4_images/Session.jpg)

### Step 14: Create a bash file under directory "backend-flask/bin/db-setup"
```
#! /usr/bin/bash
-e # it will stop if fails,on any point
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-setup"
printf "${CYAN}=== ${LABEL}${NO_COLOR}\n"
bin_path="$(realpath .)/bin"
source "$bin_path/db-drop"
source "$bin_path/db-create"
source "$bin_path/db-schema-load"
source "$bin_path/db-seed"
```
To grant permission for read,write & execution operations:

RUN: `chmod u+x ./bin/db-setup`

Run: `./bin/db-setup`

## Task 3: Install Postgres Driver.

### Step 1: open requirements.txt add these drivers.

```
  psycopg[binary]
  psycopg[pool]

```
then cd into backend directory and run: 

 `pip install -r requirements.txt`

### Step 2: now create a file under lib/db.py
```
from psycopg_pool import ConnectionPool
import os
def query_wrap_object(template):
  sql = f"""
  (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
  {template}
  ) object_row);
  """
   return sql
def query_wrap_array(template):
  sql = f"""
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
  {template}
  ) array_row);
  """
   return sql
connection_url = os.getenv("postgresql://postgres:xxxxx@127.0.0.1:5432/cruddur")
pool = ConnectionPool(connection_url)
```
### Step 3: Now set the Connection URL environment variable in docker compose file

 `CONNECTION_URL: "postgresql://postgres:xxxxxx@127.0.0.1:5432/cruddur"`

### Step 4: Open backend-flask/services/homeactivities and add the following code.
```
from lib.db import pool, query_wrap_object, query_wrap_array
class HomeActivities
  def run(cognito_user_id=None):
  sql = query_wrap_array("""
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      ORDER BY activities.created_at DESC
      """)
print(sql)
with pool.connection() as conn:
   with conn.cursor() as cur:
          cur.execute(sql)

          # this will return a tuple
          # the first field being the data
          json = cur.fetchone()
          print(json[0])
  return json[0]
  return results 
```
### Step 5: Try to connect with the database with the following command.

`psql $CONNECTION_URL`

Result: cannot connect need to update the security group on our RDS to allow inbound traffic on AWS Console.

## Task 4: First,Set the gitpod IP as environment variable to connect with Gitpod.

 `echo $GITPOD_IP`

 `export GITPOD_IP=$(curl ifconfig.me)`

## Task 5: Update security group.

### Step 1: Create a bash file under directory "backend-flask/bin/rds-update-sg-rule". The following bash file is set to update the dynamic gitpod IP address on the RDS security group so we can be able to connect with RDS each time.
```
#! /usr/bin/bash
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="rds-update-sg-rule"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description=GITPOD,IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
```
### Step 2: Now again try to connect with postgres after update TCP rule:

`"psql $CONNECTION_URL"`

Result sucessfully connected. to "cruddur"  database.

## Task 6: Create Congito Trigger with lamda to insert user into database.

### Step 1: Open AWS Console search for lambda from Services on the top left side of the console then click on create function.
### Step 2: Now on the gitpod,go to the backend-flask/aws/json create a folder "lamda" add file "cruddur-post-confirmtion.py". This should be the same name of your lamda that you create on console.Add the following lamda trigger code.

```
import json
import psycopg2
import os
def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('userAttributes')
    print('user')
    user_display_name     = user['user']
    user_email            = user['email']
    user_handle           = user['preferred_username']
    user_cognito_id       = user['sub']
    try:
         sql = f"""
 		INSERT INTO public.users (
		   display_name,
               email,
               handle,
               cognito_user_id
               )
          VALUES(%s,%s,%s,%s)
           """
         print('SQL Statement------')
         print(sql)
         conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
         cur = conn.cursor()
         params = [
           user_display_name,
           user_email,
           user_handle,
           user_cognito_id
         ]
         cur.execute(sql,param)
         conn.commit() 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')
return event
```

![Dbimage](week4_images/lambdafn.jpg)

### Step 3: Go to the lambda function and deploy the above code and the set permissions for the lambda apply custom policy as well,set VPC,set environement variable for lambda and add layer.
for attaching custom policy write the following JSON:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeNetworkInterfaces",
                "ec2:CreateNetworkInterface",
                "ec2:DescribeInstances",
                "ec2:AttachNetworkInterface",
                "ec2:DeleteNetworkInterface"
            ],
            "Resource": "*"
        }
    ]
}
```
![Dbimage](week4_images/Policy.jpg)

for adding psycopg2 security layer to the lambda:

`arn:aws:lambda:us-east-1:898466741470:layer:psycopg2-py38:2`

## Task 7: Create new activities with a database insert.
### Step 1: Add the following code into backend-flask/services/create_activity. 
```
from lib.db import db
  def create_activity(handle, message, expires_at):
    sql = db.template('activities','create')
    uuid = db.query_commit(sql,{
      'handle': handle,
      'message': message,
      'expires_at': expires_at
    })
    return uuid
  def query_object_activity(uuid):
    sql = db.template('activities','object')
    return db.query_object_json(sql,{
      'uuid': uuid
    })
```
### Step 2: open file backend-flask/lib/db.py
```
from psycopg_pool import ConnectionPool
import os
import re
import sys
from flask import current_app as app
class Db:
  def __init__(self):
    self.init_pool()

  def template(self,args):
    pathing = list((app.root_path,'db','sql',) + args)
    pathing[-1] = pathing[-1] + ".sql"
    template_path = os.path.join(pathing)
    green = '\033[92m'
    no_color = '\033[0m'
    print("\n")
    print(f'{green} Load SQL Template: {template_path} {no_color}')

    with open(template_path, 'r') as f:
      template_content = f.read()
    return template_content

  def init_pool(self):
    connection_url = os.getenv("postgresql://postgres:xxxxxx@127.0.0.1:5432/cruddur")
    self.pool = ConnectionPool(connection_url)
  # we want to commit data such as an insert
  # be sure to check for RETURNING in all uppercases
  def print_params(self,params):
    blue = '\033[94m'
    no_color = '\033[0m'
    print(f'{blue} SQL Params:{no_color}')
    for key, value in params.items():
      print(key, ":", value)

  def print_sql(self,title,sql):
    cyan = '\033[96m'
    no_color = '\033[0m'
    print(f'{cyan} SQL STATEMENT-[{title}]------{no_color}')
    print(sql)
  def query_commit(self,sql,params={}):
    self.print_sql('commit with returning',sql)

    pattern = r"\bRETURNING\b"
    is_returning_id = re.search(pattern, sql)

    try:
      with self.pool.connection() as conn:
        cur =  conn.cursor()
        cur.execute(sql,params)
        if is_returning_id:
          returning_id = cur.fetchone()[0]
        conn.commit() 
        if is_returning_id:
          return returning_id
    except Exception as err:
      self.print_sql_err(err)
  # when we want to return a json object
  def query_array_json(self,sql,params={}):
    self.print_sql('array',sql)

    wrapped_sql = self.query_wrap_array(sql)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql,params)
        json = cur.fetchone()
        return json[0]
  # When we want to return an array of json objects
  def query_object_json(self,sql,params={}):

    self.print_sql('json',sql)
    self.print_params(params)
    wrapped_sql = self.query_wrap_object(sql)

    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql,params)
        json = cur.fetchone()
        if json == None:
          "{}"
        else:
          return json[0]
  def query_wrap_object(self,template):
    sql = f"""
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    """
    return sql
  def query_wrap_array(self,template):
    sql = f"""
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    """
    return sql
  def print_sql_err(self,err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno
    # print the connect() error
    print ("\npsycopg ERROR:", err, "on line number:", line_num)
    print ("psycopg traceback:", traceback, "-- type:", err_type)
    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
db = Db()
```
### Step 3: Create a folder under directory "backend-flask/db/sql/activities" create a file "create_activity.sql" add the following code.
```
INSERT INTO public.activities (
  user_uuid,
  message,
  expires_at
)
VALUES (
  (SELECT uuid 
    FROM public.users 
    WHERE users.handle = %(handle)s
    LIMIT 1
  ),
  %(message)s,
  %(expires_at)s
) RETURNING uuid;
```
### Step 4: Create a folder under directory "backend-flask/db/sql/activities" create a file "object.sql" add the following code.
```
SELECT
  activities.uuid,
  users.display_name,
  users.handle,
  activities.message,
  activities.created_at,
  activities.expires_at
FROM public.activities
INNER JOIN public.users ON users.uuid = activities.user_uuid 
WHERE 
  activities.uuid = %(uuid)s
```
### Step 5: Create a folder under directory "backend-flask/db/sql/activities" create a file "home.sql" add the following code.
```
SELECT
  activities.uuid,
  users.display_name,
  users.handle,
  activities.message,
  activities.replies_count,
  activities.reposts_count,
  activities.likes_count,
  activities.reply_to_activity_uuid,
  activities.expires_at,
  activities.created_at
FROM public.activities
LEFT JOIN public.users ON users.uuid = activities.user_uuid
ORDER BY activities.created_at DESC
```
