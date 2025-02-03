# Introduction

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

## Miscellaneous
- Shared Nothing Architecture: Distributing load across multiple machines (Horizontal Scaling).
- Head-of-line Blocking: Few slow requests in queue slowing the following requests, thus making it hard to find which requests to optimize for.
- Elastic Systems: Systems that can automatically scale if load increases without manual intervention; good for unpredictable loads, else manual is simpler.
- Adaptability: Agility of data systems.
- Tail latency Amplification, Monitoring response times for a running time window using approximation algorithms like forward decay, t-digest etc.
- Query Language Types: Declarative (Ex. sql), Imprative (Ex. Java, Python), Map-Reduce

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
- Advantages: They support multiple languages, and are human-readable. They are good as data interchange formats.
- Disadvantages: Ambiguity around encoding of numbers and some characters like comma in csv, Schemas are complicated.
The binary versions like BSON or WBXML use less space than their corresponding raw formats like JSON or XML.