***Database Beta Haste** ---Skillbit walkthrough and writeup


QZ
One of our developers is working on a new database for storing notes inside the company, but they lost the code to actually read the database... Can you read our SQLite file to recover the data?

Download the file here.


![db1](/writeups/images/database1.png)

I started by downloading the db files for analysis

![db2](/writeups/images/database2.png)

From the challenge it's clear that we are anlyzing database files and logs
so we can utilize sqlite for our lab

We have the following options
![db3](/writeups/images/database3.png)

Now let's get started
First let's see the available databases and tables using the following command
```bash
sqlite3 databasebetahaste.db
```
Great, from the output we have following tables:
```bash
notes
users
secrets
```
![db4](/writeups/images/database4.png)

Let's look at each one of them, but interestingly, the secrets tables got my eye 👁️
1. Notes table
```bash
SELECT * FROM notes;
```
![db5](/writeups/images/database5.png)
Nothing really important from notes table

2. Users table
```bash
SELECT * FROM users;
```
here we get 
-alice
-bob
-eve
![db6](/writeups/images/database6.png)


Finally let's enumerate secrets table, it's interesting

```bash
SELECT * FROM secrets;
```
![db7](/writeups/images/database7.png)

And boom we have the metaflag
This was an easy db pentest
Glad you enjoyed

👍


