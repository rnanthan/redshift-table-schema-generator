**Amazon Redshift Table Schema Generator**

Redshift is used as a centralised repository to store data from different sources in a unified schema and structure to create a single source of truth. 
We often get CSV extracts from third-party systems and stored it in S3 data lake and 
then copied to Redshift Database using Redshift COPY command. Before copying, we have to manually create tables in Redshift database to load CSV data. 
This utility, Amazon Redshift Table Schema Generator, enables you to generate the table schema and automate the table creation in Redshift. The following diagram describes the steps. 

<img width="1064" alt="image" src="https://user-images.githubusercontent.com/4962048/214752672-454e4f7f-f959-43e3-9a0b-b423b5f3fdf8.png">

**1. Upload CSVs**

You can upload load CSV files into S3 data lake using AWS console or AWS cli or via scripts.

**2. Run Table Schema Generator script** 

_Prerequisites_

_Use the CloudFormation [template](https://github.com/rnanthan/redshift-table-schema-generator/blob/main/cloudFormation/template.yml) to create ssm parameters, S3 and IAM roles.
You need to provide Redshift connection parameters and S3 bucket name as CloudFormation parameters. Provisioning Redshift Database is out of scope and you have to make sure it already created._

Set the following environment variable

    export AWS_PROFILE=<AWS Profile>  ## Make sure you created AWS profile with right aws_access_key_id and aws_secret_access_key
    export ENV=local  ## set to local if you are running the script locally. 

Install Python libs 

    pip3 install -r requirements.txt

Run the schema generator script. You have to provide CSV filename in S3 bucket and table name as arguments. Schema name is optional and if it is not provided, table will be create under default schema, public.

    python3 table_schema_generator.py <CSV filename in S3> <table_name> -s <schema_name>

This script will generate SQL for creating table. Script will find the best datatypes, VARCHAR length, DISTKEY and SORTKEY based on the data.

Generated output will be stored ./output location and feel free to edit if you want to change anything. 


**3. Run Create Table Script**

Run the create table script as follows. It will create the table in Redshift database.

    python3 create_table.py 

**4. Copy the CSV data in S3 to the table created in Redshift database.** 

You can use the following command to copy the data. CloudFormation [template](https://github.com/rnanthan/redshift-table-schema-generator/blob/main/cloudFormation/template.yml) create IAM role and you can get the RedshiftCopyRole ANR from CloudFormation stack output.

    COPY <schema_name>.<table_name> from
    's3://<s3 bucket name>/<object key>'
    iam_role <RedshiftCopyRole ARN>
    IGNOREHEADER 1
    CSV;
