# Foundations

**Data Intensive applications** are the ones where we need to deal with a huge amount of data.  For example, typical internet companies like Google, Amazon, Twitter etc.  On the other hand, **Compute Intensive applications** are the one where the bottleneck is CPU/GPU speed.  For example, Crypto Mining, ML applications, etc. where there might just be a few thousand data points, but processing them requires huge amount of compute.

To handle Data Intensive applications we typically use **NoSQL, Message Brokers, Caches, Search Indexes, Batch Processing, Stream Processing**, and so on.  The following topics will help us understand the different techniques/concepts, and guide us in choosing the right technology to make our application scalable, highly available, and easily maintainable.

### Non-Functional Requirements
The 3 most important qualities of a Software System are (others being Security, Compliance etc.):
1. Reliability: The system should overall work fine even in the face of Hardware failures, Software Failures, or Human Errors.
2. Scalability: The system should be able to handle growing traffic, data volume, and data complexity.
3. Maintainability: It should be easy to add new features to the system, and easy to find and fix errors.

### Load Parameters
Some of the Load Parameters we ought to consider when trying to improve the non-functional aspects of a system are: 
1. Throughput: For example, Number of reads per second in Hadoop.
2. Latency: We generally calculate latency for x percentile of users.
3. Number of concurrent users
4. Read vs Write ratio
5. Cache hit ratio.

We need to carefully calculate the load parameters because our architecture will be completely different for different types of load parameters.  For example, an application serving 3 MB files for millions of users will have a completely different architecture compared to an application serving GB sized files for few users.


### Data Models
Following are some of the data models used commonly: 
1. Relational
2. Document Based
3. Graph Model
4. Some others are: Genome DB, Full Text Search DB, Immutable DBs, Big Data for physics handling petabytes, Time Series DB, Vector DB, Analytics DB etc.

To choose the correct data model for our application, we need to understand the type of data and query patterns that our application will have.

#### Document DB
- They use a tree-like structure.  For example, MongoDB, RethinkDB, CouchDB, etc. 
- Advantages:
  - They are good for **self-contained data** (one-to-many relationships) like a LinkedIn profile for a person.  It does not require joins to fetch details about a person's LinkedIn profile.  Loading this entire self-contained data in one go could provide us good performance.
  - They are good when our schema needs to change frequently, because we use schema-on-read.  For Relational DB, changing schema requires downtime, and changes could be hard.
  - They are closer to application's data structures, and we might not need an intermediary like Hibernate or ibatis.
  - The poor support of joins might not be a problem if our queries can do without joins. 
- Disadvantages:
  - They cannot represent many-to-one or many-to-many relationships well.  For example, if we need to change the name of a city then we might have to update each row in DocumentDB, compared to a single row change in Relational DB.  We can denormalize the data to support many-to-one or many-to-many relationships, but then we will have to do extra work to keep our data consistent. 

#### Relational DB
- They structure data in the form of tables, and use joins to make use of the relationships between tables.
- Advantages
  - They are good for dynamic queries using joins.  For a new query, we just need to create the new indexes.  The query optimizer will take care of retrieving the data in the correct order keeping performance in mind.  Thus it is useful to add new features.
  - They are good for many-to-one or many-to-many relationships.
  - Less data redundancy.
  - Generally supports ACID well which helps us maintain Data Integrity. 
- Disadvantages 
  - They have fixed schema, and changing schema might require downtime.
  - It might be hard to scale them.

#### Graph Models
- Graph Models are used for highly interconnected data.  For highly interconnected data, relational model is good, document model is bad, and graph model is best.
- Similar to Document DB, GraphDB also do not enforce schema unlike relational DB.  Therefore it is easier to adapt the applications with changing needs.
- Examples of GraphDB: Neo4j, and example of graph query language: SPARQL.


Note: Sometimes we need to support both relational and document db, called **Polyglot Persistence**.


## Storage and Retrieval
To retrieve data faster we use Indexes.  There are multiple ways in which we can build indexes, and each technique is optimized for certain kind of characteristics we might need.  Two of the important techniques in which storage engines use Indexes are: Log-structured and Page Oriented.

### Indexes
- Additional metadata that helps with faster data lookup.  But, we cannot use indexes everywhere because it degrades data insertion speed.
- Types of Indexes:
  - Hash based: 
    - Key-Val data is stored in an append-only log, and an offset to the data in an in-memory hashmap.  Splitting and merging of the log files are done for higher performance.
    - Advantage: It offers high performance reads, writes, and updates, if all keys can fit in the RAM.
    - Disadvantage: Bad for range queries. 
  - SSTables (Sorted String Tables):
    - We keep the key-value pairs sorted by key (using AVL trees), unlike append-only logs.  On DB crash, the data in memory might be lost, so we store this data in an append only log file which can be used for recovery.
    - Advantage: High write throughput since disk writes are sequential.
    - A similar concept is used in Cassandra and Lucene. 
  - B Trees:
    - Most popular technique, and it is not log-based unlike earlier ones.
    - Like SSTables it keeps key-value pairs sorted by key for efficient lookup and range queries but unlike Log-structured which writes to variable-sized segments sequentially, it breaks down the DB into fixed size blocks called pages and reads or writes are performed one page at a time. This choice is due to underlying hardware's design which is also arranged in fixed size blocks. 
    - Each page can be identified using an address which allows one page refer to another -- like pointers on disk. The pages can be thought to be arranged in a Tree structure (with light locks on the tree for concurrency).
    - For crash recovery, a **Write Ahead Log (WAL)** is used. 
    - Advantages:
      - B-Trees have index stored at only one place - helps with concurrency.
      - Faster for reads.
  - Multi Column indexes:
    - Multiple columns are concatenated as 1 key, and R-trees are used.  For example: Geospatial DBs, where latitude and longitude are merged as 1 key. 
  - Full Text search and Fuzzy Indexes:
    - To handle this type of searches, for example in Lucene, the in-memory SSTable like index is designed as a finite state automaton over the characters similar to a Trie, and then Levenstein automaton and Edit distance algorithms are used.


## In-memory DBs
- In-memory DBs keep small enough datasets entirely in-memory, potentially distributed across multiple machines.
- Some in-memory DBs like Memcached are intended to be used as cache, so it is acceptable to lose data on machine restart but some others offer durability using special hardware like battery-powered RAM or by keeping snapshots, or writing to logs.
- There are some Relational In-memory DBs too like Memsql, VoltDB, Oracle times-ten.

## Transaction Processing vs Analytics
- Unlike OLTP, Analytics queries scan huge number of records, but typically only reading few columns at a time. Data Warehouses are used to support these queries.
- Schemas for Analytics:
  - Star (majorly used): At the center of a Star schema is a fact-table (potentially with 100s of columns) and every row here is an event at a timestamp. Every column is either a description of the event or foreign-key references to dimensional-tables which are more details about those columns.
  - Snowflake schema: similar to Star schema but dimensional tables are further divided into sub-dimensional tables here.
- Column-Oriented Storage: In OLTP DBs entire row is stored together, so when we query, entire rows with needless columns are also loaded. On the other hand, Columnar DBs store entire columns together, and for analytics queries where we use a few columns only those columns are loaded, thus making it efficient for analysis.
  - In Columnar DBs, Data is easier to compress using bitmap encoding (saves desk space), and uncompressed using Vectorized processing (i.e. using tight loops).
- Data Cubes and Materialized views: It stores some pre-computed values that are used frequently like AVG, MIN, MAX etc. so that we don't have to compute them each time. Sometimes data is also pre-computed at a higher level of granularity so that the less granular values like MIN, MAX can be calculated along with more different types of queries. For example, we can store the count for each day, and this can support queries for daily/weekly/monthly/yearly counts.

## Encoding and Evolution
Application changes might require changes in the Data format or Schema. But to support rolling upgrade (or staged rollout -- changes to nodes in phases, not at once) we need to support Backward compatibility (new code can read old data), and Forward compatibility (old code can read data written by new code). For Backward compatibility the new code has to put in suitable logic for old data, and for Forward compatibility the code has to keep considering the new Data Format or Schema changes for a long period that will be made by future code.

Types:
- Language-Specific:
  - For example, Java's Serializable class.
  - Advantage: less additional code needs to be written.
  - Disadvantage: difficult to integrate with other languages, forward and backward compatibility issues, less efficient. 
  - Good to use for temporary situations.
- Formats used in APIs like JDBC and ODBC to send data stored in DBs over the network.
- JSON, XML, CSV and their Binary Variants:
  - Advantages: 
    - They support multiple languages, and are human-readable. Therefore they are good as data interchange formats.  
    - They are verbose but they can handle more detailed rules like an integer should be between 0 and 100.
  - Disadvantages: 
    - Ambiguity around encoding of numbers and some characters like comma in csv.
    - Schemas are complicated. 
  - The binary versions like BSON or WBXML use less space than their corresponding raw formats like JSON or XML. 
- Thrift and Protocol Buffers:
  - They make clever use of schemas for encoding which makes stored data more compact, and less compact data is faster to transfer over network or to store in disk.
  - To encode one technique that is used is called BinaryProtocol, where the encodings have no field names unlike the above ones.  Instead the encoded data contains Field Tags (Aliases) which are numbers and these numbers along with the names appear in the schema definition for compaction. The schema definition is referred to decode.  The other encoding techniques work similarly.
  - How do they handle schema evolution?
    - The unset values are omitted from the encoded record
    - Field names can be changed since only tags are referred. But, We cannot change Field Tags.
    - We can add new fields to the schema with new Field Tag numbers, and old code simply ignores this new Field Tag number since it does not know about this. For Forward compatibility, the datatype annotation tells how many bytes to skip and so the data is correctly read, and Backward compatibility works because field tags are never changed amd have the same meaning.
    - New field cannot be marked as required, although they can have a Default value. This is because old data will not have this required field.
    - Required field cannot be removed, and we cannot use this deleted tag number again because some data might still use this tag number
    - Datatype changes might cause truncation of data. 
- Avro:
  - Avro also uses a schema to specify the DataStructure using Avro IDL for humans, and a machine-readable JSON format, but it does not use any Tag Numbers. It just concatenates the values together. 
  - To parse the binary data we go in the same order as it is declared in the schema. The schema also tells the Data type. So, Encoder and Decoder should use compatible schemas because order is important.
  - To support Schema evolution, it uses compatible Reader's and Writer's Schema
  - To maintain Forward and Backward compatibility, we can only add or delete a value that has a default value, so that the default value can be used if actual value is not found in the schema where it is missing.
  - Changing the field name can be a bit tricky using aliases and this breaks Forward compatibility.
  - Writer's schema is written only at the beginning of huge files. Writing the schema definition a lot of times will reduce space savings. 
  - One advantage of Avro compared to Thrift or Protobufs is that the schema does not contain any tag numbers. Therefore Avro is friendlier for dynamically generated schemas. For example, if a column is deleted and one added in a DB schema, the writer can simply use this new schema. A old reader who reads this new schema will see that the fields of the record have changed, but since the fields are identified by name, the updated writer's schema can still be matched with the old reader's schema.
  - By contrast, in Thrift and Protobuf, the field tags would likely to be changed manually which is error prone. Even for automatic tools we need to take care of not using the already used Field Tags.

Protobufs, Avro and Thrift use a schema to describe a binary encoding format. Their schema languages are much simpler than JSON or XML which support more detailed validation rules like int should be between 0 and 100, etc. They are compact compared to the binary JSON variants, simpler to implement and use. Plus, schema evolution provides same kind of flexibility as schemaless or schema-on-read JSON DBs while also providing better guarantees about data and better tooling (to generate classes for programming, human viewing etc.).


## Modes of Dataflow
- Through DBs:
  - Different processes with different versions might be using the same DB. To support Backward Compatibility, use null for unknown fields of old rows.
  - Use Avro for schema evolution, Parquet for analytics. 
- RPCs (Remote Procedure Calls):
  - RPCs try to make remote requests look more like a local function call, but this design philosophy called Location Transparency is flawed because network requests might fail or timeout without providing any error message unlike local function calls. Plus, the client and server might be implemented in different programming languages.  For example, Java EJB, RMI, CORBA etc.
  - REST is still better for experimentation, debugging, and has better tooling. RPC is mainly used within an org, and REST in other places mainly.
  Backward and Forward compatibility is maintained based on encoding format it uses 
- Message Passing:
  - No encoding is enforced by message broker, so we are free to use an encoding that is Forward and Backward compatible. This way the clients and servers can be updated independently. 
- Distributed Actor Framework (DAF):
  - In DAF, Logic is encapsulated in the actors and communication is achieved via message passing.

## Miscellaneous
- Shared Nothing Architecture: Distributing load across multiple machines (Horizontal Scaling).
- Head-of-line Blocking: Few slow requests in queue slowing the following requests, thus making it hard to find which requests to optimize for.
- Elastic Systems: Systems that can automatically scale if load increases without manual intervention; good for unpredictable loads, else manual is simpler.
- Adaptability: Agility of data systems.
- Tail latency Amplification, Monitoring response times for a running time window using approximation algorithms like forward decay, t-digest etc.
- Query Language Types: Declarative (Ex. sql), Imperative (Ex. Java, Python), Map-Reduce.
- Some data stores like Redis are also used as message queues, and some message queues like Kafka guarantee data durability like data stores.

# Distributed Data
The previous section built the foundations and the topics discussed there can be implemented on a single machine.  However, we might want to distribute our Database from a single machine to multiple machines to improve the following aspects of our application:
1. Scalability: Distributing traffic to multiple machines improve throughput.
2. Fault-Tolerance/High-Availability: Our systems should reasonably work as a whole even when a few machines fail.
3. Latency: Latency is improved by serving requests from DataCenters that are geographically closer to clients, so that the requests and responses don't have to travel half way around the world.

Distributing data across multiple machines is called **Horizontal Scaling, or Scaling Out, or Shared Nothing Architecture** (because CPUs/RAM/Disc is not shared among machines). There are some fundamental problems that we need to handle with Distributed Systems like: Replica Consistency, Availability, Durability, and Latency, among others.

A different approach to scaling to higher load is to use a single more powerful machine with lots of storage and RAM (called **Vertical Scaling or Scaling up**), but the problem with this is that the cost grows faster than a linear function here.

Depending on our application, either Vertical or Horizontal scaling can work better for us i.e. there's no one silver bullet.

Distributing data across nodes is commonly achieved either using Replication, or Partitioning, or a combination of both.

## Replication
Replication means keeping a copy of the same data on multiple machines. Replication is simple, except that we need to handle changes to the replicated data too, and that makes it challenging to achieve.

### Leaders and Followers
Every write to the Database needs to be processed by all the replicas. The most common solution to achieve this is called **Leader-based replication (or Active-Passive or Master-Slave)**. Here, one of the replicas is designated as the leader (or master, primary etc.) and all writes go to this replica only. The other replicas are called **followers (or read-replicas, slaves, secondaries, hot standbys etc.)**.

Whenever the leader receives a new write, it writes it to its local storage and also send these changes to the followers as part of a **Replication Log or Change Stream**. The followers use this log to write all the data in the same order as they were processes on the leader. Here the client must write to the leader, but read can be requested from any replica.

This is the default behaviour in many DBs like MySQL, MongoDB etc. This is not only used in DBs but also distributed message brokers like Kafka for high available queues, and some network file systems and replicated block devices.

This pattern is useful for web applications where number of reads is far more compared to write -- reads can be served from multiple replicas.

### Synchronous vs Asynchronous Replication
- Synchronous
  - The leader waits for the follower's confirmation before reporting success to the client and before making the write visible to the other clients.
  - Advantage: The follower is guaranteed to have an up-to-date copy of the data.
  - Disadvantage: The leader must block all writes till the synchronous replica responds, which it does typically in <1s, but could take more time due to network delays or while recovering from a crash. 
- Asynchronous
  - The leader sends the write messages to the followers and reports success to the client, without waiting for a confirmation from the followers.
  - Advantage: Even if all followers fail, the leader can support writes.
  - Disadvantage: Not durable, because if leader fails then non-replicated writes are lost even if they are confirmed to the client.
  - Eventual Consistency: Data may not be immediately updated in the follower nodes, but eventually the followers catch up after the Replication Lag Time. 
- In synchronous replication, any one node outage can halt the entire system, so in practice typically 1 follower is made synchronous and others as asynchronous (semi-synchronous mode). If the synchronous node become slow or fails, then another asynchronous follower is made synchronous. 
- To setup new followers, take a snapshot of the leader at some point in time when it was consistent (using log sequence number or binlog coordinates for example), copy that consistent snapshot to the followers, and then the followers can request and perform all writes since the snapshot.

### How to Handle node outages?
- When followers fail: After coming back up, followers can request changes from their leader starting from the time that is in its write change log. The write change log tells the follower the write after which it crashed.
- When leaders fail, We can use the Failover process.  Choose a new leader if existing leader is dead. To choose a new leader we can use an election algorithm, or using a previously chosen Controller node. However this can lead to a Consensus Problem, a topic discussed later on.
- Problems with Failover:
  - In async replication, we might have to discard the writes of the old leader which were not synched to avoid conflicts and it could be dangerous.
  - Split Brain Problem: Both the old and new reader thinks that they are the only leader, causing lost writes or conflicts.

### Techniques to implement Replication on Leader-based systems
- Statement Based:
  - Leader logs every write statement that it executes. Ex. INSERT, UPDATE commands in relational DBs
  - Problems: Non deterministic functions like now(), datetime() gives different values when ran in different machines; also some problems with triggers and stored r=procedures. 
- Write Ahead Log (WAL):
  - Problem: WAL is expressed in a low level (like bytes), so changing storage engines or DB versions become difficult. 
- Logical (Row based): 
  - Here change granularity is at row level, and the process is called **Change Data Capture**.  This can also be used to send data to other places like a warehouse. 
- Trigger Based:
  - This is done at the application level unlike the above ones, and it provides flexibility if we want to only replicate subset of the data.

### Replication Lag Anomalies
The lag time in replicating the data can confuse users if they query from a node that has not received the new data.

Workarounds:
- Read your own writes (Read after write consistency): For the user who wrote the data, read it back from the leader, otherwise they might think that the data is lost.  For other users, they can read from the replicated nodes. 
- Monotonic Reads: User will not see old data after having seen recent data once.  To achieve this, we can make the user read from the same replica by keeping a map of ip and hostname for example. 
- Consistent Prefix Reads: Causally Dependent things like Question and Answer should appear in the same order.  To achieve this, we can make the causally dependent things to be written to the same node, or use algorithms to handle these things.

### Multi-Leader Replication (Master-Master or Active/Active)
- In Multi-Leader replication, writes are allowed in multiple nodes, and the leaders need to behave as leaders and followers simultaneously.  This is more robust than single-leader replication because the system remains up even if one leader goes down.  
- Problem: We need to handle concurrent writes when the same data is being updated in multiple nodes.
- Handling Write Conflicts:
  - Avoidance: Try to make all writes to the same record go to the same node. 
  - Last Write Wins: Attach a unique monotonically increasing ID to each write and store the latest value.  The problem is that it might lead to data loss.  Ex. used by Cassandra. 
  - Custom Logic: Handle using custom logic either during read (ex. prompting user to re-insert the data), or during write (ex. Bucardo). 
  - Further Research: Conflict-Free Replicated Datatypes (CRDTs), Mergeable Persistent Data Structures, Operational Transformation algorithm etc.

#### Multiple Leader replication topologies
1. All-to-All
2. Circular: writes forwarded to neighbour along with own writes
3. Star: A designated node sends write to all nodes.


### Leaderless Replication
- In these systems, there are no leaders and all the nodes can accept writes. These systems are also called Dynamo-style because Amazon used it for DynamoDB.
- To catchup on the writes after a node goes down, 2 methods are used:
  - Read Repair: When a client makes a read from several nodes in parallel, it can detect and correct stale data, if any. 
  - Anti-entropy: A background process continuously looks for and corrects stale data in an unordered fashion.
- Detecting Concurrent Writes: Include a version number with each key which increases with each write.  Use **Version Vectors** when multiple nodes are writing, and these version vectors keep all version numbers for all nodes that are writing.
- Quorums are used to make sure that the latest data is read. If there are n replicas, then the write must be processed by at least w nodes, and reads must be processed by at least r nodes.  
  - So, Dynamo-style DBs are used in situations which can tolerate Eventual Consistency. To achieve stronger guarantees in Dynamo-style systems we need transactions or consensus. 
  - If nodes go down then we can use **Sloppy Quorums** to temporarily hold data in a temporarily designated node.

## Partitioning (also called Sharding/region/vnode/tablet)
- Partitioning/Sharding is required to achieve scalability, especially when storing and processing data on a single machine remains no longer feasible. 
- Normally, partitions are defined in such a way that each record/document/row lives in exactly one partition. In effect, each partition is a mini Database of its own, even though it can support operations that can touch multiple partitions at the same time. 
- Partitioning is usually coupled with Replication for Fault-Tolerance. A node may store more than 1 partitions, and typically the leader and followers live on different nodes. 
- Request routing is done via Round Robin (request randomly sent to node and redirection is used to find the correct node) or using a central coordinator like Zookeeper.

### Partition Strategies (Goal - Distribute keys fairly among nodes)
- Partition data randomly to random machines: 
  - Problem: We might have to query all partitions in parallel because we might not know where the queried key lives.
- By Key-ranges:
  - Each partition keeps a contiguous range of keys, and we also keep track of which ranges belong to which partition.
  - Disadvantage: Risk of hotspots if the application often access keys that are closer in the sort order.
  - This technique is used by BigTable, HBase, MongoDB etc. 
- Keys generated using Hash:
  - Choose the hash function properly to ensure fair data distribution.
  - We can then store the ranges of these Hash values using the Key-Range partitioning technique. The partition boundaries can be evenly spaced or chosen pseudo-randomly (Consistent Hashing).
  - Consistent Hashing randomly chooses partition boundaries to avoid central control or distributed consensus which are hard to achieve.
  - Disadvantage: Range queries perform bad because the storage order is lost.
  - Note: If there are many reads and writes for the same key, for example for a celebrity, add a 2 digit random number to the key so that the same key is distributed to multiple partitions.

### Partition of Secondary Indexes
A secondary index does not identify a row uniquely, but it is used to search for a particular value in a row/document efficiently. For example, all articles related to Travel.

There are 2 main ways to partition a DB with secondary indexes:
- Document Partitioned (local index): Secondary indexes are stored in the same partition as the Primary key and the actual document.  Ex: MongoDB
  - Disadvantage: Reads must read all partitions. 
- Term Partitioned: A global index covers data in all partitions (which can be further partitioned).  Here reads become fast, but writes might become slow. 

### Rebalancing Partitions
Rebalancing might be required when a node fails or we add more resources to handle increased load or datasize. This might require us to shift the load from one node to another, while continuing to support reads and writes.

Strategies:
- hash mod n: In this strategy we simply put the keys in node x where x = (hash(key) modulus n).  
  - Disadvantage: If number of nodes (n) changes, then we might have to move around a lot of keys. 
- Fixed number of partitions: Here we create more partitions than required and assign multiple partitions to each node. If a new node joins then it takes a few partitions from each node to create an even distribution. 
- Dynamic: Partitions are created dynamically. If a partition exceed some threshold size then it is divided into two halves, and small partitions are merged. Ex: HBase 
- Partitions proportional to number of nodes:
  - In this strategy, the size of partitions grow proportional to the size of the dataset, but when we increase the number of nodes the size of partitions become smaller again. When a new node joins the cluster it chooses a fixed number of partitions and takes half of the values from these. Averaging over a large number of times keeps the partition sizes even. For example, Cassandra.


## Transactions
Transactions are useful to simplify applications by handling partial writes and race conditions.

### ACID
- Atomicity: All writes in the transaction either happen or not.  If a node fails halfway in a transaction, the writes written so far must be discarded.
- Consistency: DB should be consistent before and after a transaction. For example, credit and debit amount must match. It can be achieved using Triggers for example.
- Isolation: When multiple transactions are running concurrently, the end result should be as if when they ran serially.
- Durability: Once a transaction commits, all data is written and never lost, even if there's hardware failure. It can be done by writing to non-volatile memory, or using a Write Ahead Log for recovery.

Systems that do not maintain ACID are sometimes called BASE (Basically Available, Soft State, and Eventual Consistency).

### Single-Object Writes
Atomicity and Isolation also apply when a single object is changed. For example, if node fails in between writing a 100kb JSON file.  

Atomicity can be achieved using:
1. Using a log for crash recovery
2. locks
3. Removing operations doing read-modify-write cycle
4. Compare-and-Set operation which allows write only when it is not being concurrently modified (** light-weight transaction**)

### Multi-Object Transactions
Multi-object transactions are required if several pieces of data needs to be kept in sync. They need to determine which Read and Write operations belong to the same transaction. 

### Isolation Levels
1. Read committed (Weak)
2. Snapshot Isolation (Weak)
3. Serializable (Strong): Only Serializable Isolation protects us from all these race conditions.

These isolation levels are characterized by various types of race conditions like Dirty Reads, Dirty Writes, Read Skew, Lost Updates, Write Skew, Phantom reads etc. Different isolation levels guarantee different levels of race conditions that we can avoid.  Applications can make use of these isolation level guarantees provided by the DB to keep its code simple.

#### Read Committed
- It guarantees no dirty reads (only committed data is read) and no dirty writes (while writing we only overwrite committed data).
- Transactions running at read committed isolation level usually delays the second concurrent write until the first transaction commits or aborts.
- Problem: Read Committed isolation level however still does not prevent lost updates when a txn modifies after a txn's read but before it's write.
- Most commonly, DBs prevent dirty writes by allowing only 1 transaction to acquire row-level locks.  Read locks cannot acquire lock until write finished.


#### Snapshot Isolation and Repeatable Read
- Read committed isolation suffers from an anomaly called 'Non Repeatable Read' or 'Read Skew'. This happens in the following scenario when we just get unlucky with our read timings. If we read the data again, then we will see correct and consistent data.
![read_skew.png](../images/read_skew.png)
- Snapshot isolation is the most common solution to this problem, where each transaction reads from a consistent state of the DB - each transaction sees all data that was committed at the start of the transaction. It does not care if that transaction has committed during the actual read; it just uses the value that was at the start of the txn. 
- Snapshot Isolation implementations typically use write locks to prevent dirty writes, but reads do not require locks. 

#### Preventing Lost Updates
The problem of Lost Updates can occur in a read-modify-write cycle where a value is first read, then updated (potentially based on the previous read), and then written. For example, an account balance is read, updated based on the value and written back. In this scenario one of the writes might be lost because the 2nd write does not consider the first modification.

Solutions:
1. Atomic writes: Many DBs provide atomic update operations using UPDATE keyword.  Atomic writes takes locks or uses a single thread.
2. Explicit Locking: Application explicitly locks all objects that are going to be updated using the 'FOR UPDATE' clause which locks all objects returned by a select query. 
3. Automatically detecting Lost updates: Above methods are sequential. This method allows the transactions to execute in parallel and if a lost update is detected then abort the transaction.
4. Compare and Set: This atomic operation allows update to happen if the value hasn't yet change since you last read it.
5. Conflict Resolution and Replication: This is used for multi-leader or leaderless replications, which allows concurrent writes to happen and resolve at application level while reading (among other techniques discussed later).

#### Write Skew and Phantoms
Write Skews can occur for example in the following figure where a check is made based on some global condition, but then the write itself can change the global condition for other txns running concurrently. In the following figure, it is expected that count never becomes 0, but it can become 0 nonetheless with txns operating concurrently.
![write_skew.png](../images/write_skew.png)

Solutions to Write Skew:
1. Atomic single-object solutions does not help because multiple objects are involved.
2. Implement constraints using multiple objects if possible, for example using triggers or materialized views etc.
3. If using serializable isolation level is not possible, then next best option is to use 'FOR UPDATE' clause to lock rows on which the transaction depends.

#### Serializability
Techniques to implement Serializable Isolation:
- Actual Serial Execution
  - Here one transaction is executed one at a time serially on a single thread.
  - Disadvantage: It's throughput is limited to a single CPU core. 
- 2 Phase Locking (2PL):
  - Several transactions are allowed to read concurrently as long as no transaction is writing to it. Exclusive locks are required for writes.
  - This is in contrast to Snapshot Isolation where readers and writers never block each other. This difference makes 2PL overcome all the race conditions discussed earlier including lost updates and write skew.
  - To read, a Txn must obtain a shared lock. To write, a Txn must obtain an exclusive lock. 
  - Predicate Locks:  Predicate Locks are used to stop Phantoms causing Write Skew.  It works similar to shared/exclusive lock but the locks does not belong to an object/row, it belongs to all objects that match a search condition.  Predicate Locks do not perform well, and so Index-range Locks are used more commonly.
  - Index-Range Locks: Here a greater set of predicates is matched. This approximation of the search condition is attached to one of the indexes (either the room_id or time index). Now, if another txn wants to modify this same overlapping condition then it will see the shared lock on the index, and consequently it will wait for that lock to be released. 
- Serializable Snapshot Isolation (SSI):
  - 2PC implementations like 2 phase locking don't perform well, and serial executions do not scale well. 
  - SSI provides full serializability with a small performance penalty compared to Snapshot Isolation. SSI is new, so its adoption is still not widespread. 
  - Compared to 2 phase locking or serializable executions which are pessimistic, this is an optimistic algorithm. Instead of blocking if something dangerous could happen, txns continue anyway hoping that everything will turn out good in the end. When a txn wants to commit the DB checks whether isolation was violated, and if so, the txn is aborted and has to be retried. Only txns that executed serially are allowed to commit.


# Problems with Distributed Systems
Distributed Systems are hard because it works with unreliable network, and we can't even know if something succeeded for sure because the response might be lost.  Also, we need to keep running Distributed Systems as a whole even if some nodes fail.  In contrast, in High Performance Computing we can kill the job if something fails and restart it from some snapshot.
1. Detecting Faults: Detecting faults might be achieved using **timeouts** but we need to set it properly.
2. Unreliable Clocks: Even using sophisticated systems like **Network Time Protocol (NTP)** might still have some seconds of variation with the actual clock.  So it becomes difficult to find which event occurred first if clocks in 2 machines are not in sync.  Logical Clocks based on incrementing counters are a safer alternative for ordering events rather than the unreliable time-of-day quartz clock. Logical clocks do not measure time, just the order of events.
3. Process Pauses: Long process pauses can be bad if process pauses after acquiring lock for something (like Leader Lock).  To deal with it we can plan processes like Garbage Collection which takes a long time at regular intervals.
4. Fencing Locks: On wakeup from process pause the old leader might still think that it is the new leader, but the Quorum decided to replace the process-paused leader already.  To overcome this split-brain (multiple leaders), we can attach a monotonically increasing ID to each locks, and this value can be used to decide the latest leader.
5. Byzantine Faults: A system is Byzantine Fault Tolerant if it continues to operate correctly even if some of the nodes are malfunctioning and not obeying the protocol, or if malicious attackers are interfering the network.  Protection from Byzantine Faults might require hardware support. For web apps we can use input validation to prevent it. In peer-to-peer network where there is no central authority, Byzantine Faults may occur more frequently.

# Linearizability
- One of the strongest consistency models.  Eventual Consistency is a weak guarantee because it does not say anything about when a data would be eventually available.
- In Eventual Consistency 2 different replicas may provide different answers if one of them is lagging behind and this can confuse the users. Linearizability gives only one response. It is also called Atomic/Strong/Immediate/External Consistency. The basic idea is to make a system appear as if there is only one copy of the data and all operations on it are atomic.
- Unlike Serializability, Linearizability does not group operations together. The read and write request could be independent and thus write skew cannot happen. A DB may provide both Serializability and Linearizability, and this combination is called strict-serializability or strong one-copy serializability. Implementations of Serializability based on 2 phase locking or actual serializability are typically linearizable, but Snapshot Isolation Serializability does not guarantee that.
- Linearizability is useful for Leader Election, reliable counter increments etc.
- Implementation: If only a single node holds one copy of the data and all operations on this is atomic, then it might be lost/inaccessible if the node fails - and hence not fault tolerant. The most common way to make a system fault-tolerant is to use replication. Here's a discussion of if replication can be made linearizable:
  - Single-Leader Replication: They are potentially linearizable if we read from the leader or from the synchronous followers. 
  - Consensus Algorithms 
  - Multi-Leader Replication: Linearizable even if network interruption happens between 2 datacenters, because the clients just needs to connect to it's "home" datacenter. 
  - Leaderless Replications are probably not linearizable because of concurrency issues. 
  - Strict Quorums: Strict Quorums are not linearizable due to variable networks delays; and because the reads may read from different set of nodes.   It is possible to make dynamo-style quorums at the cost of reduced performance; a reader must perform read repair synchronously and a writer must read the latest state of quorum before sending its writes. But this makes only read and write linearizable, not compare-and-set.

# The CAP Theorem
Choose any 2 between Consistency, Availability, and Partition Tolerance. Since Partition tolerance is beyond our control we need to choose one of the other 2.

## Sequence Number Ordering
We can use sequence numbers to order events. They are counters which is incremented on every operation. Thus, every operation has an unique sequence number and we can always compare two sequence numbers. We can create sequence numbers that is consistent with causality. For single-leader the leader can simply assign a monotonically increasing number to each operation in the replication log, and the followers can simply use this order. For leaderless and multi-leader systems, we use Lamport Timestamps.

Lamport Timestamps are a pair of (counter, nodeId). 

## Distributed Transactions and Consensus
Consensus is required for Leader Election and Atomic commit. 
- 2 Phase Commit (2PC):
  - It is the most common way of solving the problem of atomic commit. On single machines atomic commit is achieved using Write Ahead Log and recovering using it in case of failures, but in distributed systems, the commit may happen in some nodes but not in others due to different reasons, thus making data inconsistent across nodes. 
  - 2PC achieves atomic commit across multiple machines i.e. either all nodes commit or abort. Here the commit/abort process is split into 2 phases. It uses a Coordinator or Transaction Manager. 
  - A 2PC txn begins with the app reading and writing data on multiple DB nodes (called participants), as normal. When the application is ready to commit, the coordinator begins Phase 1: it sends a prepare message to all nodes asking them if they can commit or not. If it hears all say yes then it sends a commit message to all in phase 2 and the commit happens, else aborts. 
- Three-phase commit (3PC): 2PC is blocking because participants need to wait for coordinator recovery and during that time no one can read/write because the rows are locked. 3PC is non-blocking but it assumes bounded delay of network. 
- Epoch-Numbering: Within each epoch the leader is unique.


## Membership and Coordination Services
- Zookeeper, etcd etc. are "distributed key-value services" or "coordination and configuration services". They are designed to hold small amounts of data that can fit entirely in memory (although they still write to disk for durability). This small amount of data is replicated across all nodes using a fault-tolerant total order broadcast algorithm.
- Zookeper uses fencing token to handle process pauses. Client maintains a long-lived session with Zookeeper and they occasionally bounce heartbeats and in this way Zookeeper make sure if a node is dead. Normally data kept in zookeeper is slow changing like alive_nodes+their-ip. It also offers service discovery.


# Derived Data
Derived data is derived from system of records, also called source of truth. For example, Cache (derived from underlying data), Predictions derived from usage logs etc.

## Types of Systems:
1. Services (online): Client sends requests to servers and waits for their response. Primary measure of performance is response time.
2. Batch processing (offline): These systems run periodically and take a huge amount of input, runs it for minutes or hours and produces output. Primary measure of performance is throughput (i.e. the time it takes to crunch the input of a certain size).
3. Stream processing (near real-time or nearline): It is somewhere between online and offline systems. Like batch processing it takes input and produces output (rather than responding to requests). However a stream job operates on an even shortly after it happened, unlike batch which operates on a fixed input set. It requires stream systems to have lower latency than batch systems, but they are built on top of batch systems.

## Batch Processing
- Unix Pipelines: Unix tools process GBs of log files in seconds.  It automatically parallelizes to all CPU cores, and handles data greater than memory size by spilling into disk.
- Map Reduce:
  - MapReduce is a programming framework using which we can write code to process large datasets in a distributed filesystem like HDFS.  It can be used to create search indexes like Lucene or to precompute ML recommendations.
  - Data processing pattern:
    - Read a set of input files and break it down into records. For example, each record is a line in a log file.
    - Call the mapper function to extract a key and a value from each input record.
    - Sort all the key-value pairs by key. This step is implicit, and mapper always sorts the output before giving it to the reducer.
    - Call the reducer function to iterate over the sorted key-value pairs. Since the keys are sorted, so some calculations like uniq becomes easy on memory.
  - If we want to sort by the count, then we need a second sorting stage which we can implement by writing a second MapReduce job and using the output of the first job as the input for the second job.
  - The parallelization of MapReduce is based on partitioning: the input to the job is typically a directory in HDFS, and each file or fileblock within the input directory is considered to be a separate partition that can be processed by a separate map task. Each input file is typically hundreds of megabytes in size.
  - Sort-Merge Joins: It is used when we need to join data from 2 datasets.  Here, 2 sets of mappers produce the key-value pairs for each dataset and keep them together.  Then the reducer function can be called for each key once to produce the final output.
    - For example, 2 mappers process over click and user_profile datasets and puts the user_id+click_type and user_id+user_age together sorted by user_id.  The reducer function can be called for each userId once, and it can store the first row (age) in a local variable, and iterating over the click_event, outputting pairs of viewed-url and viewer-age-in-years.  Subsequent MapReduce jobs can then calculate the distribution of viewer ages by URL and sort it.
  - Hot Keys: 
    - Bringing all values with the same key to the same place might break for 'hot keys' (ex. celebrities) and might lead to data skew (or hotspots) i.e. one reducer might have significantly more data than others. Since MapReduce jobs are complete only when all of its mappers and reducers have completed, any subsequent jobs might have to wait for the slowest reducer before they can start. 
    - If a join input has a hot key, there are a few algorithms we can use to compensate. For example, the skewed join method in pig runs a sampling first to determine which keys are hot. For Hive, we need to explicitly mention the hot key in the metadata. Grouping happens in 2 stages: the first grouping makes the output more compact, and the 2nd grouping works on this compacted data.
  - Map side joins:
    - The previous approach is called reduce-side joins which do not assume anything about the data distribution. Reduce-side joins may be quite expensive. 
    - Map-side joins work if we can make some assumptions about the data. These jobs have no reducers and no sorting. It's just one mapper reading one input file block from the distributed file system and writing one output to the file system. 
    - Techniques:
      - Broadcast Hash Joins: It works when a big dataset needs to be joined with a small dataset which is small enough to be entirely loaded in the memory of each mapper. We can load entirely into memory or on a read-only index on the local disk, which doesn't require it to fit this into memory. 
      - Partitioned Hash Joins:  If the inputs to the map-side joins are partitioned in the same way, then the hash join can be applied to each partition independently. For example, the data in click_event and user_data partitioned ny the last digit of their user_id.  These are also called bucketed map joins in Hive. 
      - Map-side merge joins:  It works if the input dataset is not only partitioned in the same way, but also sorted based on the same key. Here, it doesn't matter if the inputs don't fit in memory because merging is done same as the reducer. 
    - The output of reduce-side join is partitioned and sorted by key, but for map-side join the output is sorted and partitioned in the same way as the input. Map-side join also makes assumption of the data layout. Number of partitions, etc. can affect performance.
  - Hadoop vs Distributed DBs:
    - Data type: Distribute DBs need to decide on a schema beforehand, whereas in Hadoop we can simply dump the data, and later we can figure out how to process the raw data. This is possible because of the general purpose MapReduce and HDFS. Also, HDFS simply stores sequences of bytes which can be anything like images, videos, texts, sensor data etc. 
    - Processing models: MPPs use sql syntax and are limited in expression, whereas Hadoop is general purpose. We cannot write ML algos easily with SQL, but we can write them using Mapreduce. 
    - Handling Fault Tolerance: MapReduce can handle fault tolerance better because data is written to disk, and reruns can run from these intermediate steps. In Distributed DBs data is kept in memory, so rerunning cannot start from intermediate steps. It is designed this way because Distributed DBs need to respond within minutes, whereas Hadoop jobs can run for days. 
- Beyond MapReduce:  MapReduce is robust and can handle humongous amounts of data (albeit slowly) and on multi-tenant systems with frequent task terminations. On the other hand it might be slower than other tools which does not write intermediate results to files.
  - MapReduce writing intermediate files to disk makes it slow sometimes. So several new execution engines were created like Spark and Flink (called dataflow engines). They handle the entire workflow as one job rather than dividing them into subjobs.
  - High level APIs like spark, hive etc. can optimize joins by changing the join order for example so that less amount of data is required to be in memory.  They can also make use of column-oriented storage to load only the required columns.  They use vectorized execution for faster execution, by using tight inner loops for example to make use of CPU cache while running loops, and avoiding function calls. 
- Graphs and Iterative Processing:
  - Batch processing on graphs is often used in ML algorithms like recommendation engines or ranking systems (like pagerank).  Many Graph algorithms work by traversing one vertex/edge at a time (in iterations) until some termination condition is met.  
  - The Pregel Processing Model: It is also called the Pregel model, based on Google's paper named Pregel.  It works by message passing between vertices.  In each iteration we need to pass the messages to only a subset of the vertices, so it works efficiently compared to MapReduce which processes every row in each iteration. 
  - Apache Giraph, Spark's GraphX API etc.

## Stream Processing
- In batch processing the input is of finite size, so the batch process knows when it has finished reading all data. For data coming continuously like user clicks, batch processes partitions the data artificially into fixed chunks. For example, running the batch process at the end of each day. 
- In batch processing, output data is reflected after a delay which might be slow for many cases. To reduce the delay, we can process the data at the end of every second or continuously, abandoning the concept of time slices and processing every event as it happens. This is the idea behind Stream Processing.
- Transmitting Even Streams: In stream processing a record is most commonly called an event, which is an immutable self contained object that contains the details of something happening at some point of time. An event usually contains a timestamp. 
  - An event is generated once by a producer (or publisher) and potentially processed by multiple consumers (or subscribers). Events are usually grouped in topics. 
  - In batch processing the consumers polls the DB to get the data that has arrived since it last checked. But for streaming this polling can be expensive, and so usually the consumers are notified when a new event occurs.
- Messaging Systems: Specialized systems to notify consumers of a new event. 
  - Direct communication channels like a unix pipe or TCP can connect only one producer to one consumer, whereas messaging systems require multiple producers to be able to send messages to a topic, and multiple consumers to consume from that topic. 
  - Within the publish/subscribe model, there are different strategies based on the following different situations:
  - What happens if producer sends messages faster than the consumer can process them? 
    - In this case there are 3 options: drop messages, buffer messages in a queue, backpressure (block producer from sending more messages).   In queue, what happens if queue can no longer fit in memory? does it crash, does it write to disk (and if yes then does disk access degrade performance)? 
  - What happens in nodes crash or go offline? Are the messages lost? 
    - Durability of messages has a cost of writing to disk and replication. If we can afford to lost some messages then we can get a higher throughput and low latency.
  - Some message brokers participate in 2-phase commit, making them similar to DBs, but unlike DBs they delete messages once processed (work with the assumption that there will be less data).  Also, unlike DB they can notify clients when data changes.
- Direct Communication: It works for certain specialized situations but the application has to take care when messages are lost.  For example, UDP multicast (for low latency systems like finance), Brokerless messaging services like ZeroMQ, StatsD, HTTP/RPC.
- When multiple consumers read messages from the same topic, 2 main patterns of messaging are used:
  - Load Balancing: Each message is delivered to one arbitrary consumer.  This pattern is useful when the message processing is heavy, and we want to add more consumers to increase parallelization. 
  - Fanout: Each message is delivered to all of the consumers.
  - Combination of Load Balancing and Fanout.
  - Acknowledgements and Redelivery: Consumers might crash. So brokers wait for the consumers to tell them once it has finished processing before removing the message from the queue. If it does not wait then messages can be lost. If message is processed but acknowledgement is lost, then message is redelivered for consumer processing. Handling this case requires atomic commit protocol. This redelivery along with load balancing can make the consumers receive the messages in a different order. To avoid this issue we can use a different queue per consumer (not load balancing), if message ordering is important.
- Partitioned Logs: Log-based message brokers stores the message, but without increasing the latency too much (reading from the log is slower compared to in-memory read). This is required because otherwise once a message is wrongly deleted, it is lost forever.
  - Producer appends messages to an append-only log and consumer reads from a certain offset of this log.  The log is partitioned across multiple machines.
  - Sequence number is used for each message.  This sequence number provides ordering within a single partition, but there's no such guarantee across partitions.
  - Ex: Apache Kafka.
  - Even though these systems write msgs to disk they can process millions of messages per second using partitions and replication for fault-tolerance.
  - The log based approach typically supports fan out because several consumers can independently read the logs without affecting each other. To achieve load balancing across a group of consumers, instead of assigning individual messages to consumer clients, the broker can assign entire partitions to nodes in the consumer group.
  - Typically when a consumer has been assigned a log partition, it reads the messages in the log partition sequentially in a simple single-threaded manner, but this method has some downsides:
    - The number of nodes sharing the topic cannot be greater than the number of partitions. 
    - If a single message is low to process, it holds up the processing of subsequent msgs in that partition. 
  - Thus in situations where messages may be expensive to process and we want to parallelize processing on a msg-by-msg basis, and where msg ordering is not important, the JMS/AMQP style is preferred. But where high msg throughput, and short msg processing time, and msg ordering required, the log-based approach works well.
  - Only appending might lead to running out of disk space. So, we partition the logs into segments and periodically clean/archive the older segments. But if the consumers are slow, then it might still point to the deleted segments, but this is very unlikely practically with monitoring tools and all. However this does not affect other consumers. This is also unlike traditional msg brokers which keeps msgs in memory and uses space. 
  - Also unlike JMS/AMQP style, processing and acknowledging is a destructive process where msgs are deleted once acknowledged. However log-based approach writes the msg, and we can configure a consumer to consume from a random offset. So, it allows for more experimentation and easy recovery from faults.
- Change Data Capture:
  - To read DB logs and replicate the changes in a different system, for example to keep the DB and cache in sync. It is especially beneficial if the changes are made available as a stream immediately after they are written. Ex. LinkedIn's Databus, and MongoRiver for MongoDB. CDC is async and thus fast for writes but problems with replication lag may apply. 
  - To add a new system, it can read the entire log history to construct its state. But, reading the entire history can take a lot of time, so we use log compaction. This compaction feature is supported by Kafka. 
  - To support CDC, DBs are also providing APIs. Ex. Kafka connect.
- Event Sourcing: Similar to CDC, Event Sourcing stores application changes as log of change events. But Event Sourcing uses this idea at the level of application. In CDC, the DBs are mutable and we can update/delete records. In Event Sourcing the application logic is built on the basis of immutable events. Ex: EventStore
- Partitioning and Parellalization works similar to MapReduce and dataflow engines. The one crucial difference is that a stream never ends. So sorting does not make sense and sort-merge joins do not work. Streaming jobs also use a different fault-tolerance mechanism. We can restart batch jobs if it fails, but a streaming job that has been running for years might not be feasible to run from the start.
- Uses of Stream Processing 
  - Monitoring in fraud detection or financial systems. 
  - Complex Event Processing: It allows us to specify rules to search for certain patterns of events in a stream. Ex: SQLstream
  - Stream Analytics: aggregation, statistics, probabilistic algorithms like bloom filters, approx percentiles.  Ex: Apache Storm, Spark Streaming, Kafka Streams, Flink.
  - Maintaining Materialized views like caches, indexes etc.
  - Message Passing and RPC: Ex. using Apache Storm's distributed RPC which match user queries with stream events and return results to the users who queried.
- Stragler events: Events that occurred in a particular window might arrive late due to network problems or queues. We can ignore them if they are less in number or recalculate the values.
- Types of Windows to calculate aggregations 
  - Tumbling Window: These are of fixed length and every event belongs to exactly one window. 
  - Hopping window: It also has fixed length but it allows windows to overlap for smoothing. Ex. a 5 minute hopping window with a 1 minute tumble will look like 10:00:00 to 10:05:00 and next window will look like 10:01:00 to 10:06:00 
  - Sliding Window: it contains all events which occurred within some interval of each other. Ex: a 5 min window will have events from 10:01:00 to 10:06:00 in the same window because they are <5 minutes apart. In Tumbling and Hoping windows these objects won't belong to the same window. 
  - Session Window: unlike others, this does not have a fixed window or duration. Instead it groups all activities for the same user for example user clicks on a website. When the user becomes inactive for some time this eindow is closed. It is used for webpage analytics.
- Stream Joins:
  - New events may come anytime and this makes joins harder in streams. 
  - Types of stream joins:
    - Stream-stream join (window join): Events are joined based on sessionId for example. 
    - stream-table join (stream enrichment): For every event a DB is queried to find more info about that event's userId for example. This info DB can be called as a remote call, or loaded into the computer where the stream processor is running. To keep the table updated, we can use change data capture. 
    - table-table join (materialized view maintenance): Streams are collected in tables and joined.
- Fault Tolerance of stream operators:
  - Using Microbatching and Checkpointing:
    - Microbatching is breaking streams into blocks and treat each batch like a miniature batch process. This is used in spark streaming. 
    - Apache Flink ocassionally writes the state in durable storage, and recover from there.
  - Atomic Commits: Make the side effects run only once if the task succeeds using techniques like 'Exactly once message processing' discussed earlier, or 2 phase commit. In restricted environments this can be achieved efficiently.
  - Idempotence: Make ops idempotent so that even if the operation is run many times, the effect happens only once.  Even if the operation is not naturally idempotent like click counter, it can be made idempotent with some metadata. 
  - Rebuilding state after failure: Any stream process that requires a state - counter, windowed aggregations like sum, any tables and indexes used for joins - must ensure state recovery after failure. Keep state local to the stream processor machine and replicate it periodically. This ensures no message loss.