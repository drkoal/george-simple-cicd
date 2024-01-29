# George Automation Server

George Automation Server helps the developer with CICD in local
projects between multiple machines on local environment with Gitlab. 
Allows the execution of scripts, 
downloading projects and executing SQL when pushes to your repositories. 
It is a software with low requirements that facilitates certain repetitive tasks in 
simulation of productive environments.

If you have your own Gitlab and wants to have your easy-setup cicd software,
George can help you.

## Configuration

The configuration file is named
    
    george.yml

The configuration file must be:

    host-ip: [machine-ip]
    host-port: [port-ip]

## Pipelines

On the *pipelines* folder will be all the processes defined. If the user wants
create a new pipelines using the API, a new file will appear here.

All the pipelines can be defined manually on this folder or using the API explained
on this document.

    name: Pipeline-Name
    url: http://0.0.0.0/user/repository
    branch: branch-name     
    actions:
      - name: action-example-1
        command: COPY /target/path/of/machine
      - name: action-example-2
        command: RUN /target/path/of/file/to/run.sh_bat
      - name: action-example-3
        command: SQL /folder/with/sql-files/to/run
        options:
          connection: sqlite
          host: /Example/path/database.db

The commands accepted are:

    COPY [path]: Clone the repository to the path defined

    RUN [file]: Runs the file defined

    SQL [directory]: Runs all the .sql files on the directory defined

The connections accepted are: 

### sqlite

    options:
      connection: sqlite
      host: /Example/path/database.db

### postgresql

    options:
      connection: postgresql
      host: ip
      user: username
      password: password
      database: database
      schema: schema


### mysql

    options:
      connection: mysql
      host: ip
      user: username
      password: password
      database: database

## Endpoints

### /

[*Method: POST*]

When receives a push from Gitlab and, if a pipeline is configured on this 
repository and branch,
the pipeline will start to execute all the actions defined.

### get_pipelines

[*Method: GET*]

Receives all the pipelines configured on George server.

### new_pipeline

[*Method: POST*]

Creates a new pipeline, creating the new file and reloading all the pipelines.
It needs a JSON Body on the request as the example:

    {
        "name":"name-pipeline-and-new-file",
        "url": "http://ip/user/project",
        "branch": "branch-name",
        "actions": [
            {"name": "action-1-name", "command":"COMMAND target"},
            {"name": "action-2-name", "command":"SQL folder", "options":{"connection":"sqlite", "path":"example.db"}}
        ]
    }








