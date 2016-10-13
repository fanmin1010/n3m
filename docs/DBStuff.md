### Before beginning it may be useful to look through the docs of some tools.
 * [Documentation for Alembic (database migration tool)](http://alembic.zzzcomputing.com/en/latest/)
 * [Documentation for SqlAlchemy (used in writing migrations)](http://docs.sqlalchemy.org/en/latest/)

### Using the migration tool
From the repository root run the following:
```
python manage.py db --help
```
All of the commands to make changes to the database post-docker-install will start with python manage.py db. For the most part this is a mapping to the functionaliy of alembic. The output of --help is as follows:
```
Perform database migrations

positional arguments:
  {upgrade,heads,merge,migrate,stamp,show,current,edit,init,downgrade,branches,history,revision}
    upgrade             Upgrade to a later version
    heads               Show current available heads in the script directory
    merge               Merge two revisions together. Creates a new migration
                        file
    migrate             Alias for 'revision --autogenerate'
    stamp               'stamp' the revision table with the given revision;
                        don't run any migrations
    show                Show the revision denoted by the given symbol.
    current             Display the current revision for each database.
    edit                Edit current revision.
    init                Creates a new migration repository
    downgrade           Revert to a previous version
    branches            Show current branch points
    history             List changeset scripts in chronological order.
    revision            Create a new revision file.

optional arguments:
  -?, --help            show this help message and exit
```
While this help menu is good it is still a bit confusing. So, I will explain a few of the basics here. 


### Migrations
For our purpose a migration can be thought of as a file that contains the instructions to perform incremental, reversible changes to our database. To clarify, a migration contains instructions that can be executed to make changes to the database as well as the instructions required to undo the changes to the database.

To better understand this concept follow these instructions (replacing table names, columns, etc. with your own choices). From the application root apply the existing migrations first and then create a new migration by issuing the following commands:
```
python manage.py db upgrade
python manage.py db revision --rev-id table-name-and-modification
```

As you can see from the output this creates a file in migrations/versions/table-name-and-modification_.py. So open that file up and you will have the following:
```
"""empty message                                                                                                                                                                   
                                     
Revision ID: table-name-and-modification                                     
Revises: ed657e16ce20                                     
Create Date: 2016-10-13 01:48:38.484806                                     
                                     
"""                                     
                                     
# revision identifiers, used by Alembic.                                     
revision = 'table-name-and-modification'                                     
down_revision = 'ed657e16ce20'                                     
                                     
from alembic import op                                     
import sqlalchemy as sa                                     
                                     
                                     
def upgrade():                                     
    pass                                     
                                     
                                     
def downgrade():                                                                                                                                                                   
    pass    
```

So, whats important is the upgrade and downgrade functions which are used for moving the database forward (adding tables, columns etc.) and rolling those changes back. Here we'll add a new table foo with id and value columns. Note that sometimes tables are no longer needed and so dropping tables, removing columns and that type of activity are actually part of an upgrade. When this is the case please be very careful because restoring removed data is much harder than removing added data. 

```
def upgrade():
    op.create_table('foo', 
    sa.Column('id', sa.Integer(), nullable=False), 
    sa.Column('value', sa.String(length=255), nullable=True),  
    sa.PrimaryKeyConstraint('id')  
    )   

def downgrade():  
    op.drop_table('foo')  
```

### So now to apply the migration
```
python manage.py db upgrade --tag table-name-and-modification
```

### And to roll them back
```
python manage.py db downgrade --tag table-name-and-modification
```

#### That's it.

### Migrations not working?
if you get something like this when you try to use the migration tool:
```
File "/home/n3m/git/n3m/venv/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1139, in _execute_context
    context)
  File "/home/n3m/git/n3m/venv/local/lib/python2.7/site-packages/sqlalchemy/engine/default.py", line 450, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) relation "user" already exists
 [SQL: '\nCREATE TABLE "user" (\n\tid SERIAL NOT NULL, \n\temail VARCHAR(255), \n\tpassword VARCHAR(255), \n\tPRIMARY KEY (id), \n\tUNIQUE (email)\n)\n\n']
```
Simply log into the database and drop the user table. This should not happen in practice, and certainly not in a production environment, but it seems to be happening due to a conflict created during the docker run process. 
```
psql n3mdb
drop table "user";
```


