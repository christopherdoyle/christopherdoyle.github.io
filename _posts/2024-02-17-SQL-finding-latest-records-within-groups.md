---
title: "SQL: finding latest records within groups"
date: 2024-02-17
---

## Setup

A common task in databases is to find the latest X within each group Y.
Let's take the [StackOverflow2010](https://www.brentozar.com/archive/2015/10/how-to-download-the-stack-overflow-database-via-bittorrent/) database,
and try o find the latest posts for each user.
The `Posts` and `Users` tables look like:

```sql
SELECT TOP 100
    Users.DisplayName,
    Posts.Title,
    Posts.CreationDate
FROM Posts
INNER JOIN Users ON Posts.OwnerUserId = Users.Id
```


| DisplayName  | Title                                                                                 | CreationDate            |
|--------------|---------------------------------------------------------------------------------------|-------------------------|
| Eggs McLaren | Convert Decimal to Double?                                                            | 2008-07-31 21:42:52.667 |
| Kevin Dente  | Percentage width child element in absolutely positioned parent on Internet Explorer 7 | 2008-07-31 22:08:08.620 |
| Kevin Dente  | NULL                                                                                  | 2008-07-31 22:17:57.883 |
| Jeff Atwood  | "How do I calculate someone's age in C#?"                                             | 2008-07-31 23:40:59.743 |
| Jeff Atwood  | Calculate relative time in C#                                                         | 2008-07-31 23:55:37.967 |
{: .big-width }

We can find the latest post for a user like this:

```sql
SELECT TOP 1
    Users.DisplayName,
    Posts.Title,
    Posts.CreationDate
FROM Posts
INNER JOIN Users ON Posts.OwnerUserId = Users.Id
WHERE Posts.OwnerUserId = ?
ORDER BY Posts.CreationDate DESC
```

But what if we want the latest post for every user?
If we take away the where clause, we still only get one row; a different tactic is needed.
<span class=marginnote>Actually, there is a way to use TOP 1 like this, more on that later.</span>

## CTE and MAX

A common solution is to use a subquery or CTE to find the MAX, then join back onto `Posts` like this:

```sql
WITH CTE_LatestPost AS (
    SELECT
        OwnerUserId,
        MaxCreationDate = MAX(CreationDate)
    FROM Posts
    GROUP BY OwnerUserId
)
SELECT
    Users.DisplayName,
    Posts.Title,
    Posts.CreationDate
FROM Posts
INNER JOIN Users ON Posts.OwnerUserId = Users.Id
INNER JOIN CTE_LatestPost
    ON Posts.OwnerUserId = CTE_LatestPost.OwnerUserId
    AND Posts.CreationDate = CTE_LatestPost.MaxCreationDate
```

This will work, but joining on `CreationDate` is not ideal as there could be two rows with the same creation date for a user --- unlikely in this dataset, but true in general.
We can ue `Id` instead, but then we are relying on `Id` increasing directly with `CreationDate`.
Depending on the dataset this might not be possible.

It's also quite slow. This query takes about 20 seconds on my laptop.
A big part of the reason for the slowness is the self-join on `Posts`.

## Temp table

Self-joins like this are generally black holes of performance for SQL Server.
It doesn't always know how to optimize the query well, it's not obvious what you are doing.
In particular it won't realize that the CTE is quite small, and that it could evaluate it first on it's own.
We can force it to do this by putting the results into a temp table:

```sql
SELECT
    OwnerUserId,
    MaxCreationDate = MAX(CreationDate)
INTO #LatestPost
FROM Posts
GROUP BY OwnerUserId

SELECT
    Users.DisplayName,
    Posts.Title,
    Posts.CreationDate
FROM Posts
INNER JOIN Users ON Posts.OwnerUserId = Users.Id
INNER JOIN #LatestPost
    ON Posts.OwnerUserId = #LatestPost.OwnerUserId
    AND Posts.CreationDate = #LatestPost.MaxCreationDate;
```

This takes even longer at 24 seconds!
Unfortunately, in this case, `#LatestPost` is rather large and takes 10 seconds to populate on its own.
In other examples, this solution can net a quick and easy performance benefit.

## Windowing Functions

Now we use [`ROW_NUMBER`](https://learn.microsoft.com/en-us/sql/t-sql/functions/row-number-transact-sql?view=sql-server-ver16).
This keeps track of the row number within each group that we specify, in some order that we specify.
Since we order by `CreationDate DESC`, if we look at just `RN = 1`, then we have the latest occurrences.
This also avoids draws, though the draw winner is arbitrary and non-deterministic.
We could order by another (unique) column as well (such as `Id`) to solve this.


```sql
WITH CTE_LatestPost AS (
    SELECT
        OwnerUserId,
        Title,
        CreationDate,
        RN = ROW_NUMBER() OVER (
            PARTITION BY OwnerUserId
            ORDER BY CreationDate DESC
        )
    FROM Posts
)
SELECT
    Users.DisplayName,
    CTE_LatestPost.Title,
    CTE_LatestPost.CreationDate
FROM CTE_LatestPost
INNER JOIN Users ON CTE_LatestPost.OwnerUserId = Users.Id
WHERE CTE_LatestPost.RN = 1
```

This takes only 12 seconds.

The advantage of this query is that we don't need a self-join.
In the first query, we are joining `Posts` onto `Posts`.
Here we can select all the columns from `Posts` that we need inside the CTE, so there is no need to join back.


## With Ties + Windowing Function

Perhaps you feel needing a CTE/subquery is still a bit cumbersome.
Here is a solution in a single query that uses the `ROW_NUMBER` partitioning with `TOP 1 WITH TIES` to give us the latest within each group.

```sql
SELECT TOP 1 WITH TIES
    Users.DisplayName,
    Posts.Title,
    Posts.CreationDate
FROM Posts
INNER JOIN Users ON Posts.OwnerUserId = Users.Id
ORDER BY ROW_NUMBER() OVER (
    PARTITION BY Posts.OwnerUserId
    ORDER BY Posts.CreationDate DESC
)
```

`TOP 1 WITH TIES` gives us the latest from the `ORDER BY`, and if there are ties for first place then it gives us all of them.
Our `ORDER BY` is designed to give ties, it will rank the latest post for each `OwnerUserId` as joint first in the `ORDER BY`.

This is a slightly slower solution at about 14 seconds.

### Adding an index

Until now, the only index on `Posts` was a unique index on `Id`, which we are not using.

Let's create an index for our workload:

```sql
CREATE NONCLUSTERED INDEX IX_Posts_CreationDate
    ON Posts (CreationDate)
    INCLUDE (Title, OwnerUserId)
```

Rerunning the timing tests we get:

* Naive: 7.4 seconds
* Temp table: 3.1 seconds
* Windowing: 3.3 seconds
* With Ties: 4.6 seconds


## Looking closer: IO usage

The temp table solution is slightly faster than our windowing solution.
Now let's compare their IO usage using [`SET STATISTICS TIME`](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-statistics-io-transact-sql?view=sql-server-ver16):

```text
Table 'Posts'. Scan count 6, logical reads 24809, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table 'Users'. Scan count 0, logical reads 785856, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table 'Posts'. Scan count 1, logical reads 24547, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table '#LatestPost_________________________________________________________________________________________________________000000000004'. Scan count 1, logical reads 681, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
```

```text
Table 'Posts'. Scan count 6, logical reads 24781, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table 'Users'. Scan count 6, logical reads 7769, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
```

So while the temp table solution is quicker, it's hiting the tables significantly harder.
On the other hand, the CPU times (measure of CPU load) of the temp table is much lower than the windowing function.
Overall this is a tradeoff between CPU and IO.
Which method is faster will depend on the particular workflow and hardware.
Which method is *best* will depend on what else you have running on these tables.
If you are already IO constrained, it might be preferable to take a slightly slower overall query that has much lower CPU load.


## Further refinement: temp table indexes

We can get another small benefit (about 2.5 second total time) by adding a primary key to our temp table:

```sql
CREATE TABLE #LatestPost (
    OwnerUserId int NOT NULL PRIMARY KEY,
    MaxCreationDate datetime NOT NULL
)

INSERT INTO #LatestPost (OwnerUserId, MaxCreationDate)
SELECT
    OwnerUserId,
    MaxCreationDate = MAX(CreationDate)
FROM Posts
GROUP BY OwnerUserId

SELECT
    Users.DisplayName,
    Posts.Title,
    Posts.CreationDate
FROM Posts
INNER JOIN Users ON Posts.OwnerUserId = Users.Id
INNER JOIN #LatestPost
    ON Posts.OwnerUserId = #LatestPost.OwnerUserId
    AND Posts.CreationDate = #LatestPost.MaxCreationDate;
```

We could also add an index on MaxCreationDate but this probably won't have a huge impact because of the time required to build it.
Sometimes the cost of adding a primary key is also not worth it, again it depends on workload.

This leads to my final thought on optimizing this solution: engineering.
Compared to other solutions, we now have a solution which is 3 statements (`CREATE`, `INSERT`, `SELECT`) compared to 1 (`SELECT`).
It is also a bit harder to maintain: we need to keep the temp table schema in sync with the `Posts` table, in other words our solution is more tightly coupled to the source tables.
The `WITH TIES` solution is slick and concise, but how many people on your team will understand it?
These things might not matter in a toy problem, but if this strategy is used extensively, it can become burdonsome to maintain.
It can also lead to errors: if `CreationDate` is changed from a `datetime` to a `date` (it is called a `Date`, but this *is* encoding a time; in other datasets, particularly older ones, it is not uncommon to see pure dates in a `datetime` column), and the temp table schema is not updated, then you are know adding a small cast to the insert, and another cast to the join in the select.
Sometimes this penalty is imperceptible, but it could have a bigger impact then the savings of this solution.
The best solution is not always the one that is quickest right now, and sometimes a slightly worse solution is better in the long run.
