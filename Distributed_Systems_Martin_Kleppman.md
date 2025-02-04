# Foundations

Data Intensive applications are the ones where we need to deal with a huge amount of data.  For example, typical internet companies like Google, Amazon, Twitter etc.  On the other hand compute (CPU or GPU) intensive applications are the one where the bottleneck is CPU speed.  For example, Crypto Mining, ML applications, etc. where there might just be a few thousand data points, but processing them requires huge amount of compute.

To handle Data Intensive applications we typically use NoSQL, Message Brokers, Caches, Search Indexes, Batch Processing, Stream Processing, and so on.  The following topics will help us understand the different techniques/concepts, and guide us in choosing the right technology to make our application scalable, highly available, and easily maintainable.

## Non-Functional Requirements
The 3 most important qualities of a Software System are (others being Security, Compliance etc.):
1. Reliability: The system should overall work fine even in the face of Hardware failures, Software Failures, or Human Errors.
2. Scalability: The system should be able to handle growing traffic, data volume, data complexity.
3. Maintainability: It should be easy to add new features to the system.  Also, it should be easy to find and fix errors, if and when that occurs.

## Load Parameters
Some of the Load Parameters we ought to consider when trying to improve the non-functional aspects of a system are: Throughput (Ex. number of reads per second in Hadoop), Latency (for x percentile of users), Number of concurrent users, Read vs Write ratio, cache hit ratio, and so on.

We need to carefully calculate the load parameters because our architecture will be completely different for different types of load parameters.  For example, an application serving 3 MB files for millions of users will have a completely different architecture compared to an application serving GB sized files for few users.


## Data Models
Mainly there are 3: Relational, Document Based, Graph Model.
Some others are: Genome DB, Full Text Search DB, Immutable DBs, Big Data for physics handling petabytes, Time Series DB, Vector DB, Analytics DB etc.
It's not easy to say which data model makes our application simple.  It depends on the data and query patterns.

### Document DBs Vs Relational DBs
#### Document DB
They use a tree-like structure.  For example, MongoDB, RethinkDB, CouchDB, etc.
##### Advantages
- They are good for self-contained data (one-to-many relationships) like a LinkedIn profile for a person.  It does not require joins to fetch details about a person's LinkedIn profile.  Loading this entire self-contained data in one go could provide us good performance.
- They are good when our schema needs to change frequently, because we use schema-on-read.  For Relational DB, changing schema requires downtime, and changes could be hard.
- They are closer to application's data structures, and we might not need an intermediary like Hibernate or ibatis.
- The poor support of joins might not be a problem if our queries can do without joins.

##### Disadvantages
- They not represent many-to-one or many-to-many relationships well.  For example, if we need to change the name of a city then we might have to update each row in DocumentDB, compared to a single row change in Relational DB.  We can denormalize the data to support many-to-one or many-to-many relationships, but then we will have to do extra work to keep our data consistent.

#### Relational DB
##### Advantages
- Better for Dynamic queries using joins.  For a new query, we just need to create the new indexes.  The query optimized will take care of retrieving the data in the correct order keeping performance in mind.  Thus it is useful to add new features.
- They are good for many-to-one or many-to-many relationships.
- Less data redundancy.

##### Disadvantages
- Changing schema might require downtime.

### Graph Models
For highly interconnected data, relational is good, document model is bad, and graph model is best.  Examples of GraphDB: Neo4j, and example of graph query language: SPARQL.
Similar to Document DB, GraphDB also do not enforce schema unlike relational DB.  Therefore it is easier to adapt the applications with changing needs.

Note: Sometimes we need to support both relational and document db, called **Polyglot Persistence**.


## Storage and Retrieval
There are majorly 2 ways in which storage engines operate: Log-structured and Page Oriented.

### Indexes
Additional metadata that helps with faster data lookup.  But, we cannot use indexes everywhere because it degrades data insertion speed.
Types of Indexes:
1. Hash based: 
- Key-Val data is stored in append-only log, and an offset to the data in an in-memory hashmap.  Splitting and merging of the log files are done for higher performance.
- Advantage: It offers high performance reads, writes, and updates if all keys can fit in the RAM.
- Disadvantage: Bad for range queries.
2. SSTables (Sorted String Tables):
- We keep the key-value pairs sorted by key (using AVL trees), unlike append-only logs.  On DB crash, the data in memory might be lost, so we store this data in an append only log file which can be used for recovery.
- Advantage: High write throughput since disk writes are sequential.
- A similar concept is used in Cassandra and Lucene.
3. B Trees:
- Most popular and is not log-based unlike earlier ones.
- Like SSTables it keeps key-value pairs sorted by key for efficient lookup and range queries but unlike Log-structured which writes to variable-sized segments sequentially, it breaks down the DB into fixed size blocks called pages and reads or writes are performed one page at a time. This choice is due to underlying hardware's design which is also arranged in fixed size blocks. Each page can be identified using an address which allows one page refer to another -- like pointers on disk. The pages can be thought to be arranged in a Tree structure (with light locks on the tree for concurrency).
- For crash recovery, a Write Ahead Log (WAL) is used.
4. Multi Column indexes:
- Multiple columns are concatenated as 1 key, and R-trees are used.  For example: Geospatial DBs, where latitude and longitude are merged as 1 key.
5. Full Text search and Fuzzy Indexes:
- To handle this type of searches, for example in Lucene, the in-memory SSTable like index is designed as a finite state automaton over the characters similar to a Trie, and then Levenstein automaton and Edit distance algorithms are used.

#### B-Trees vs LSM-Tress
- LSM-Trees are faster for writes whereas B-Trees are thought to be faster for reads.
- B-Trees have index stored at only one place - helps with concurrency.

## In-memory DBs
In-memory DBs keep small enough datasets entirely in-memory, potentially distributed across multiple machines.
Some in-memory DBs like Memcached are intended to be used as cache, so it is acceptable to lose data on machine restart but some others offer durability using special hardware like battery-powered RAM or by keeping snapshots, or writing to logs.
There are some Relational In-memory DBs too like Memsql, VoltDB, Oracle times-ten.

## Transaction Processing vs Analytics
- Unlike OLTP, Analytics queries scan huge number of records, but typically only reading few columns at a time. Data Warehouses are used to support these queries.
- Schemas for Analytics:
  - Star (majorly used): At the center of a Star schema is a fact-table (potentially with 100s of columns) and every row here is an event at a timestamp. Every column is either a description of the event or foreign-key references to dimensional-tables which are more details about those columns like product details, country_id details etc. 
  - Snowflake schema: similar to Star schema but dimensional tables are further divided into sub-dimensional tables here.
- Column-Oriented Storage: In OLTP DBs entire row is stored together, so when we query entire rows with needless columns are also loaded. On the other hand, Columnar DBs store entire columns together, and for analytics queries where we use a few columns only those columns are loaded, thus making it efficient for analysis.
  - They are compressed using bitmap encoding to save desk space, and uncompressed using Vectorized processing (i.e. using tight loops).
- Data Cubes and Materialized views: It stores some pre-computed values that are used frequently like AVG, MIN, MAX etc. so that we don't have to compute them each time. Sometimes data is also pre-computed at a higher level of granularity so that the less granular values like MIN, MAX can be calculated along with more different types of queries. For example, we can store the count for each day, and this can support queries for daily/weekly/monthly/yearly counts.

## Encoding and Evolution
Application changes might require changes in the Data format or Schema. But, to support rolling upgrade (or staged rollout -- changes to nodes in phases, not at once) we need to support Backward compatibility (new code can read old data), and Forward compatibility (old code can read data written by new code). For Backward compatibility the new code has to put in suitable logic for old data, and for Forward compatibility the code has to keep considering the new Data Format or Schema changes for a long period that will be made by future code.

Types:
1. Language-Specific:
- Advantage: less additional code
- Disadvantage: difficult to integrate with other languages, forward and backward compatibility issues, less efficient.
- For example, Java's Serializable class. 
- Good to use for temporary situations.
2. Formats used in APIs like JDBC and ODBC to send data stored in DBs over the network.
3. JSON, XML, CSV and their Binary Variants:
- Advantages: They support multiple languages, and are human-readable. They are good as data interchange formats.  Also, they are verbose but they can handle more detailed rules like an integer should be between 0 and 100.
- Disadvantages: Ambiguity around encoding of numbers and some characters like comma in csv, Schemas are complicated.
The binary versions like BSON or WBXML use less space than their corresponding raw formats like JSON or XML.
4. Thrift and Protocol Buffers:
- Both of them uses a schema using which data is encoded.
- To encode one technique is BinaryProtocol, where the encodings have no field names unlike the above ones.  Instead the encoded data contains Field Tags (Aliases) which are numbers and these numbers along with the names appear in the schema definition for compaction. The schema definition is referred to decode.  The other encoding techniques work similarly.
- How do they handle schema evolution?
  - The unset values are omitted from the encoded record
  - Field names can be changed since only tags are referred. But, We cannot change Field Tags.
  - We can add new fields to the schema with new Field Tag numbers, and old code simply ignores this new Field Tag number since it does not know about this. For Forward compatibility, the datatype annotation tells how many bytes to skip and so the data is correctly read, and Backward compatibility works because field tags are never changed amd have the same meaning.
  - New field cannot be marked as required, although they can have a Default value. This is because old data will not have this required field.
  - Required field cannot be removed, and we cannot use this deleted tag number again because some data might still use this tag number
  - Datatype changes might cause truncation of data.
5. Avro:
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
1. Through DBs:
- Different processes with different versions might be using the same DB. To support Backward Compatibility, use null for unknown fields of old rows.
- Use Avro for schema evolution, Parquet for analytics.
2. RPCs (Remote Procedure Calls):
- RPCs try to make remote requests look more like a local function call, but this design philosophy called Location Transparency is flawed because network requests might fail or timeout without providing any error message unlike local function calls. Plus, the client and server might be implemented in different programming languages.  For example, Java EJB, RMI, CORBA etc.
- REST is still better for experimentation, debugging, and has better tooling. RPC is mainly used within an org, and REST in other places mainly.
Backward and Forward compatibility is maintained based on encoding format it uses
3. Message Passing:
- No encoding is enforced by message broker, so we are free to use an encoding that is Forward and Backward compatible. This way the clients and servers can be updated independently.
4. Distributed Actor Framework (DAF):
- In DAF, Logic is encapsulated in the actors and communication is achieved via message passing.

## Miscellaneous
- Shared Nothing Architecture: Distributing load across multiple machines (Horizontal Scaling).
- Head-of-line Blocking: Few slow requests in queue slowing the following requests, thus making it hard to find which requests to optimize for.
- Elastic Systems: Systems that can automatically scale if load increases without manual intervention; good for unpredictable loads, else manual is simpler.
- Adaptability: Agility of data systems.
- Tail latency Amplification, Monitoring response times for a running time window using approximation algorithms like forward decay, t-digest etc.
- Query Language Types: Declarative (Ex. sql), Imprative (Ex. Java, Python), Map-Reduce.
- Some data stores like Redis are also used as message queues, and some message queues like Kafka guarantee data durability like data stores.

# Distributed Data
We might want to distribute our Database from a single machine to multiple machines because it improves the following aspects of our application:

1. Scalability: Distributing traffic to multiple machines improve throughput.
2. Fault-Tolerance/High-Availability: Our systems should reasonably work as a whole even when a few machines fail.
3. Latency: Latency is improved by serving requests from DataCenters that are geographically closer to clients, so that the requests and responses don't have to travel half way around the world.

Distributing data across multiple machines is called Horizontal Scaling, or Scaling Out, or Shared Nothing Architecture (because CPUs/RAM/Disc is not shared among machines). There are some fundamental problems that we need to handle with Distributed Systems like: Replica Consistency, Availability, Durability, and Latency, among others.

A different approach to scaling to higher load is to use a single more powerful machine with lots of storage and RAM (called Vertical Scaling or Scaling up), but the problem with this is that the cost grows faster than a linear function here.

Depending on our application, either Vertical or Horizontal scaling can work better for us i.e. there's no one silver bullet.

Distributing data across nodes is commonly achieved either using Replication, or Partitioning, or a combination of both.

## Replication
Replication means keeping a copy of the same data on multiple machines. Replication is simple except that we need to handle changes to the replicated data too, and that makes it challenging to achieve.

### Leaders and Followers
Every write to the Database needs to be processed by all the replicas. The most common solution to achieve this is called Leader-based replication (or Active-Passive or Master-Slave). Here, one of the replicas is designated as the leader (or master, primary etc.) and all writes go to this replica only. The other replicas are called followers (or read-replicas, slaves, secondaries, hot standbys etc.).

Whenever the leader receives a new write, it writes it to its local storage and also send these changes to the followers as part of a Replication Log or Change Stream. The followers use this log to write all the data in the same order as they were processes on the leader. Here the client must write to the leader, but read can be requested from any replica.

This is the default behaviour in many DBs like MySQL, MongoDB etc. This is not only used in DBs but also distributed message brokers like Kafka for high available queues, and some network file systems and replicated block devices.

This pattern is useful for web applications where number of reads is far more compared to write -- reads can be served from multiple replicas.

### Synchronous vs Asynchronous Replication
#### Synchronous
- The leader waits for the follower's confirmation before reporting success to the client and before making the write visible to the other clients.
- Advantage: The follower is guaranteed to have an up-to-date copy of the data.
- Disadvantage: The leader must block all writes till the synchronous replica responds, which it does typically in <1s, but could take more time due to network delays or while recovering from a crash.

#### Asynchronous
- The leader sends the write messages to the followers and reports success to the client, without waiting for a confirmation from the followers.
- Advantage: Even if all followers fail, the leader can support writes.
- Disadvantage: Not durable, because if leader fails then non-replicated writes are lost even if they are confirmed to the client.
- Eventual Consistency: Data may not be immediately updated in the follower nodes, but eventually the followers catch up after the Replication Lag Time.

In synchronous replication, any one node outage can halt the entire system, so in practice typically 1 follower is made synchronous and others as asynchronous (semi-synchronous mode). If the synchronous node become slow or fails, then another asynchronous follower is made synchronous.

To setup new followers, take a snapshot of the leader at some point in time when it was consistent (using log sequence number or binlog coordinates for example), copy that consistent snapshot to the followers, and then the followers can request and perform all writes since the snapshot.

### How to Handle node outages?
- When followers fail: After coming back up, followers can request changes from their leader starting from the time that is in its write change log. The write change log tells the follower the write after which it crashed.
- When leaders fail, We can use the Failover process.  Choose a new leader if existing leader is dead. To choose a new leader we can use an election algorithm, or using a previously chosen Controller node. However this can lead to a Consensus Problem, a topic discussed later on.
- Problems with Failover:
  - In async replication, we might have to discard the writes of the old leader which were not synched to avoid conflicts and it could be dangerous.
  - Split Brain Problem: Both the old and new reader thinks that they are the only leader, causing lost writes or conflicts.

### Techniques to implement Replication on Leader-based systems
1. Statement Based:
- Leader logs every write statement that it executes. Ex. INSERT, UPDATE commands in relational DBs
- Problems: Non deterministic functions like now(), datetime() gives different values when ran in different machines; also some problems with triggers and stored r=procedures.
2. Write Ahead Log (WAL):
- Problem: WAL is expressed in a low level (like bytes), so changing storage engines or DB versions become difficult.
3. Logical (Row based):
- Here change granularity is at row level, and the process is called **Change Data Capture**.  This can also be used to send data to other places like a warehouse.
4. Trigger Based:
- This is done at the application level unlike the above ones, and it provides flexibility if we want to only replicate subset of the data.

### Replication Lag Anomalies
The lag time in replicating the data can confuse users if they query from a node that has not received the new data.

Workarounds:
1. Read your own writes (Read after write consistency): For the user who wrote the data, read it back from the leader, otherwise they might think that the data is lost.  For other users, they can read from the replicated nodes.
2. Monotonic Reads: User will not see old data after having seen recent data once.  To achieve this, we can make the user read from the same replica by keeping a map of ip and hostname for example.
3. Consistent Prefix Reads: Causally Dependent things like Question and Answer should appear in the same order.  To achieve this, we can make the causally dependent things to be written to the same node, or use algorithms to handle these things.

### Multi-Leader Replication (Master-Master or Active/Active)
- In Multi-Leader replication, writes are allowed in multiple nodes, and the leaders need to behave as leaders and followers simultaneously.  This is more robust than single-leader replication because the system remains up even if one leader goes down.  
- Problem: We need to handle concurrent writes when the same data is being updated in multiple nodes.
- Handling Write Conflicts:
1. Avoidance: Try to make all writes to the same record go to the same node.
2. Last Write Wins: Attach a unique monotonically increasing ID to each write and store the latest value.  The problem is that it might lead to data loss.  Ex. used by Cassandra.
3. Custom Logic: Handle using custom logic either during read (ex. prompting user to re-insert the data), or during write (ex. Bucardo).
4. Further Research: Conflict-Free Replicated Datatypes (CRDTs), Mergeable Persistent Data Structures, Operational Transformation algorithm etc.

#### Multiple Leader replication topologies
1. All-to-All
2. Circular: writes forwarded to neighbour along with own writes
3. Star: A designated node sends write to all nodes.


### Leaderless Replication
- In these systems, there are no leaders and all the nodes can accept writes. These systems are also called Dynamo-style because Amazon used it for DynamoDB.
- To catchup on the writes after a node goes down, 2 methods are used:
1. Read Repair: When a client makes a read from several nodes in parallel, it can detect and correct stale data, if any.
2. Anti-entropy: A background process continuously looks for and corrects stale data in an unordered fashion.
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
1. Random: 
- Problem: We might have to query all partitions in parallel because we might not know where the queried key lives.
2. By Key-ranges:
- Each partition keeps a contiguous range of keys, and we also keep track of which ranges belong to which partition.
- Disadvantage: Risk of hotspots if the application often access keys that are closer in the sort order.
- This technique is used by BigTable, HBase, MongoDB etc.
3. Keys generated using Hash:
- Choose the hash function properly to ensure fair data distribution.
- We can then store the ranges of these Hash values using the Key-Range partitioning technique. The partition boundaries can be evenly spaced or chosen pseudo-randomly (Consistent Hashing).
- Consistent Hashing randomly chooses partition boundaries to avoid central control or distributed consensus which are hard to achieve.
- Disadvantage: Range queries perform bad because the storage order is lost.
- Note: If there are many reads and writes for the same key, for example for a celebrity, add a 2 digit random number to the key so that the same key is distributed to multiple partitions.

### Partition of Secondary Indexes
A secondary index does not identify a row uniquely, but it is used to search for a particular value in a row/document efficiently. For example, all articles related to Travel.

There are 2 main ways to partition a DB with secondary indexes:
1. Document Partitioned (local index): Secondary indexes are stored in the same partition as the Primary key and the actual document.  Ex: MongoDB
- Disadvantage: Reads must read all partitions.
2. Term Partitioned: A global index covers data in all partitions (which can be further partitioned).  Here reads become fast, but writes might become slow. 

### Rebalancing Partitions
Rebalancing might be required when a node fails or we add more resources to handle increased load or datasize. This might require us to shift the load from one node to another, while continuing to support reads and writes.

Strategies:
1. hash mod n: In this strategy we simply put the keys in node x where x = (hash(key) modulus n).  
- Disadvantage: If number of nodes (n) changes, then we might have to move around a lot of keys. 
2. Fixed number of partitions: Here we create more partitions than required and assign multiple partitions to each node. If a new node joins then it takes a few partitions from each node to create an even distribution.
3. Dynamic: Partitions are created dynamically. If a partition exceed some threshold size then it is divided into two halves, and small partitions are merged. Ex: HBase
4. Partitions proportional to number of nodes:
In this strategy, the size of partitions grow proportional to the size of the dataset, but when we increase the number of nodes the size of partitions become smaller again. When a new node joins the cluster it chooses a fixed number of partitions and takes half of the values from these. Averaging over a large number of times keeps the partition sizes even. For example, Cassandra.


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
1. Actual Serial Execution
- Here one transaction is executed one at a time serially on a single thread.
- Disadvantage: It's throughput is limited to a single CPU core. 
2 Phase Locking (2PL):
- Several transactions are allowed to read concurrently as long as no transaction is writing to it. Exclusive locks are required for writes.
- This is in contrast to Snapshot Isolation where readers and writers never block each other. This difference makes 2PL overcome all the race conditions discussed earlier including lost updates and write skew.
- To read, a Txn must obtain a shared lock. To write, a Txn must obtain an exclusive lock. 
- Predicate Locks:  Predicate Locks are used to stop Phantoms causing Write Skew.  It works similar to shared/exclusive lock but the locks does not belong to an object/row, it belongs to all objects that match a search condition.  Predicate Locks do not perform well, and so Index-range Locks are used more commonly.
- Index-Range Locks: Here a greater set of predicates is matched. This approximation of the search condition is attached to one of the indexes (either the room_id or time index). Now, if another txn wants to modify this same overlapping condition then it will see the shared lock on the index, and consequently it will wait for that lock to be released.
3. Serializable Snapshot Isolation (SSI):
- 2PC implementations like 2 phase locking don't perform well, and serial executions do not scale well. 
- SSI provides full serializability with a small performance penalty compared to Snapshot Isolation. SSI is new, so its adoption is still not widespread. 
- Compared to 2 phase locking or serializable executions which are pessimistic, this is an optimistic algorithm. Instead of blocking if something dangerous could happen, txns continue anyway hoping that everything will turn out good in the end. When a txn wants to commit the DB checks whether isolation was violated, and if so, the txn is aborted and has to be retried. Only txns that executed serially are allowed to commit.