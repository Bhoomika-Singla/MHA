# MHA
Music History Analysis
Flask -> Backend
React -> Frontend
MongoDB -> Database
AWS -> Cloud Provider

More services can be added(like Apache Kafka, Docker, Container)



Instructions for using the dump file

Install MongoDb to your machine following the instructions at this link
This page also has instructions on how to launch an mongodb instance
If you can install the "community-edition-@5.0" the (@6.0 version kept breaking for me)
this has given me the best results 
https://www.mongodb.com/docs/manual/administration/install-community/

if your database is running propperly you should be able to launch mongoshell and automatically connect 
run mongoshell with the 'mongosh' command and you will see a "connection string" you will need this string for the next step

Once running use the MongoDatabase Tool in bash called "mongorestore" on the dump file 
documentation on how to do that can be found here
https://www.mongodb.com/docs/database-tools/mongorestore/





