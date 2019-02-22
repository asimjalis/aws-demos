# DAX

## DAX in VPC

<img src="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/images/dax_high_level.png">

## Replication

How does DAX use multiple nodes?

- DAX designates one of the nodes as the master.
- The other nodes are read replicas.
- Reads can be served by the master or a replica.
- Writes can only be served by the master.
- Updates to the master are asynchronously replicated to the replicas.
- If the master fails, a replica is promoted to become the next master.
- The best practice is to deploy the master and replicas in different
  availability zones for high-availability.

## Caching

How does DAX cache reads and writes?

- DAX has two caches: item cache and query cache.
- It caches all GetItem calls and writes into its item cache.
- It caches all queries into its query cache. 

## Invalidation

How does DAX invalidate its caches?

- DAX invalidates cache entries using the TTL setting for the cache.
- It also uses LRU to invalidate entries when it needs to free space.
- DAX uses separate TTL and LRU settings for the item and query caches.

## DAX Caches

<img src="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/images/dax-item-cache.png">

## Strongly Consistent Reads

How does DAX handle strongly consistent reads?

- DAX passes strongly consistent reads to DynamoDB.
- DAX handles eventually consistent reads based on its cache.
- If it does not find the item in its cache it fetches it from DynamoDB.
- If it does not find it in DynamoDB it caches the missing value and returns it.
- This is called *negative caching*.

## DAX vs DynamoDB Perf

How is DAX's performance compared to DynamoDB?

- DAX's eventually consistent reads are faster than DynamoDB.
- Instead of milliseconds, DAX lookups take microseconds.
- DAX's writes as well as strongly consistent reads are slower than calling DynamoDB directly.
- This is because they are passed to DynamoDB and so require an extra hop.

## Write Perf

How can we speed up DAX writes?

- By default DAX will write-through the data.
- This means reads is fast but writes have extra network hop and so more latency.
- If you want to reduce write latency you can write directly to DynamoDB (write-around).
- This will lead to stale data in the cache until it expires through TTL.

## Write-Around

<img src="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/images/dax-consistency-alice-bob.png">

## References

- [DAX Concepts](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.concepts.html)
- [DAX Consistency Models](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.consistency.html)




