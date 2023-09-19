# Stock_Exchange_Scalable
This is a program that achieved the functionality of Stock exchange, and also could be scalable with multiple process to improve the performance

# **ECE 568 – HW4 danger log:**

Name: Fan Yang(fy62), Shiyang Pan(sp645)

> ==NOTE==: For the first time you run *docker-compose up* it may take several times to load, and after that, you SHOULD shutdown the docker, and run another time, which will make the server run normally. This is due to the setup of the postgres database, only happens at the first time, and will not influence following run of docker compose up. 

## General points:

1. For the ORM we use to manipulate the database, which is *sqlalchemy*, it has its own syntax for a database transaction called **Session** which is a class bind with the **engine** connected to the database. Each time we do a database transaction, we should set up a indivitual **session** object to *add* or *commit*. Originally we using one session and passing into different transaction, which will cause the problem, that the previous exception happens in the session, but not be flushed, and another session is committed, an inside exception is thrown, which will cause the exception giving inclear error message for clients. However, even in this previous version, this error will not make our server down. Further, we change to create a **new session** object for each operation to ensure the session is seperate for each transaction.  In addition, as we are setting the server to multiprocess, so we need to **dispose** the engine for each process setup, and this is included in the *Pool* intializer. 
2. To ensure the safe modification to the database, we need to have the lock for manipulating row and tuple. However the ORM we used, which will be covered in **Scalability** section, may run into ***dead lock*** situations. We have to do the session.commit() to unlock it. Especially, in some cases, we will detect some illegal situations, and raise the exception to get rid of the current modification, but the lock may be remained, and another request coming in and try to modify it which will cause the dead lock. 
3. Although our scalability tests which will mention in the next section, we have already cover all the operations in the **client_test.py**, but if you would like to try out the server ==outside the docker==, please set up the engine for a local database, setting in **utils.py**. 
4. ![image-20230406184728373](/Users/yangfan/Library/Application Support/typora-user-images/image-20230406184728373.png)
5. For our testing below, we are not running in one time server running, as the testcases are the same but under different conditions. If the server does not restart, it won’t drop the database, so the requests in the testcases will receive the error like the account exists. In this case it doesn’t perform any transaction to the database, which will run less time than the first execution. You may not be able to reproduce our tests results. 
6. The **unit_tests.py** mentioned in the **Functionality** part will provide a bunch of testcases that involves all kinds of potential results according to the specification, Feel free to try out. This is running outside of the docker by it self, so please change the database. 

## Scalability

As mentioned in the scalability write up, to make our server to be capable to handel multiple concurrent requests, we need to achieve parallelism in our server. As the python could make use of performance through multi-threading, we need to use pre-forked processes with the help of multiprocessing pool. The detailed performance and scalability results is given in the writeup, here we want to elaborate the implementation a bit further. 

As we are doing multiple concurrent update and modification to the database. We originally tried to make the database isolation level to **Serializable isolation**, but this will dramastically degrade our performance, so instead of that, we need to change the serializable isolation to the default of the postgres, which is the **Read Committed isolation**, but there will be phantom read in the implementation of our results. For example, if two concurrent requests want to add the same symbol to an account who doesn’t already have this stock, they will both try to write a new tuple into this user. However, as specified in our database design, the primary key for this *Position* relation is the *user_id + symbol_name*, so postgres will throw the exception. To solve this problem, we use our try except block to catch this exception, and do a rollback, which will result in a right position addition. Additionally, if we are trying to modify one tuple that is already exsiting in the database, we have to ensure this database transaction is atomic, otherwise we may lost updates. For the ORM we used to manipulate the operation to postgres is *sqlalchemy*, which supports a **Row-level lock** by using the syntax **with_for_update**. Most cases, this will help us to do database transactions. However the database relational design, make ordering transaction involved two tables update and different rows updating. There will be lost update even we doing this with the row-level lock. As a result, we introduce the process lock for the ordering transaction, this is not helpful for scalability but this could make sure correctness very well, at the same time we could make sure the parallism for other operations. 

As for the multiple core utilizition, we used taskset, by speicying the number 0, 0-1, 0-3, we could set the cores we want our server to run on. The results and analysis are given in the writeup. 

```linux
taskset -c 0-1 server.py
```



## Functionality correctness of scalability test:

For the functionality of our stock server, we have fullfilled the requirement, and we have unit tests for each database transaction, additionally with the combined unit test by integrating the parser. All these tests are located in the **unit_test.py** in *src* directory, this is a file that you can modify which unit test you want to run in the main function and run independently to see the results.  

Additional, we have set up a **print.py** file which could also be ran directly, which will print the database information including all the account information and transaction out. This is easy for you to check the database information. 

For the functionality correctness of the testcases given in the scalability writeups, here we will presented the results. This could be reproduce by specifying the corresponding parameters in **server.py** **client.py**, and also set the taskset command when running the **server.py**. As the tests setup given in the setup that:

> To test this scalability, we construct a scenario for stock creation. By specifying several total users, all the odd id users will create their account information with a balance of 10000 and create two symbol called “TELSA” and “X”, with the shares number 0 and 100 respectively. They will also place their two buy orders each with the symbol of TELSA and 50 amount, 100 dollars. On the contrary, all the even id users will create their account with 0 balance, and a “TESLA” symbol with 100 amounts. Similarly, they will place a sell order with “TESLA” symbol, with 100 shares and 100 dollars. 
>
> These two parts are ensuring the functionality of the transaction matching, after the running, the result of the accounts information should be that the odd users should have a 0 balance, and have 100 shares of TESLA, at the same time the even users will own the 10000 balance, and 0 shares. As the orders are matched together, so the balance and shares will be flipped for the odd and even users.

As the scalability tests given on different condition, here we will only present the results of 10 users running  on serilizable and concurrent requests: The left 1/3 is the running server, and the middle is the print of the database, before and and after client connected, the right is the running time of the client. To make the running time more accurate, we disable the request and response printing, you could enable this in **client_test.py** additionally with the other property like number of users and concurrent or searlize.  

Concurrent Test:

<img src="/Users/yangfan/Downloads/concurrent.png" alt="concurrent" style="zoom: 33%;" />

<img src="/Users/yangfan/Downloads/serialize_setup.png" alt="serialize_setup" style="zoom: 33%;" />

You may need to close the server, and rerun the server, then run the modified the client_test. As the client won’t help you drop the tables. 

Searializable Test:

<img src="/Users/yangfan/Downloads/searilzable.png" alt="searilzable" style="zoom:33%;" />

<img src="/Users/yangfan/Downloads/concurrent_setup.png" alt="concurrent_setup" style="zoom:33%;" />

From the results, we could see that the database is given as expected, and concurrent test is 0.2s faster than the serializable test. 
