**Amazon Redshift Table Schema Generator**

Redshift is used as a centralised repository that stores data from different sources in a unified schema and structure to create a single source of truth. 
We often get CSV extracts from third-party systems and stored it in S3 data lake and 
then copied to Redshift Database using Redshift COPY command. Before copying, we have to create tables in Redshift database to load CSV data. 
This utility, Amazon Redshift Table Schema Generator, enables you to generate the table schema and you can automate the table creation in Redshift using 
this tool. 