# IlmarIntelligence
This file contains my solution for the coding assignement shared by Ilmar Intelligence

## Solution

/*Write a query to pull back the most recent redemption count, by redemption date, for the date range 2023-10-30 to 2023-11-05, for retailer "ABC Store". Your result should have 2 columns and 7 rows (one row per day in the date range). Provide the query and then using your query result, provide answers to the following questions.*/


CREATE TEMPORARY TABLE weeklyTransactionTbl AS
/*Asumming that having multiple rows for same store and same redemption date is caused due data duplicate and we only need the latest record as per the createdatetime.*/
WITH red_ByDay as ( 
SELECT retailerId, redemptionDate, redemptionCount, row_number() over (PARTITION BY retailerId, redemptionDate ORDER BY createDateTime DESC) AS logging
FROM TblRedemptions_ByDay
WHERE redemptionDate BETWEEN '2023-10-30' AND '2023-11-05' -- Applying the date filter within the CTE
ORDER BY redemptionDate DESC, id -- Sort the table to optimize the join
)

SELECT retailerId, retailerName, redemptionCount, redemptionDate
FROM red_ByDay AS red_day
INNER join (SELECT DISTINCT id, retailerName FROM tblRetailers WHERE retailername = 'ABC Store') AS retailers -- Filtering for the desired store in the inner table for optimization.
ON red_day.retailerId = retailers.id
WHERE logging = 1
ORDER BY redemptionDate DESC, id
;

-- Which date had the least number of redemptions and what was the redemption count?
SELECT redemptionDate, redemptionCount AS minRedemptions
FROM weeklyTransactionTbl
WHERE redemptionCount in (SELECT MIN(redemptionCount) FROM weeklyTransactionTbl)

redemptionDate	min Redemptions
2023-11-05	3702


-- Which date had the most number of redemptions and what was the redemption count?
SELECT redemptionDate, redemptionCount AS maxRedemptions
FROM weeklyTransactionTbl
WHERE redemptionCount in (SELECT MAX(redemptionCount) FROM weeklyTransactionTbl)
redemptionDate	maxRedemptions
2023-11-04	5224


What was the createDateTime for each redemptionCount in questions 1 and 2?

-- What was the createDateTime for each redemptionCount in questions 1 and 2?
WITH maxMinRedemption as (
SELECT retailerId, retailerName, redemptionDate, redemptionCount, 'minRedemptions' AS redemptionType
FROM weeklyTransactionTbl
WHERE redemptionCount in (SELECT MIN(redemptionCount) FROM weeklyTransactionTbl)

UNION 

SELECT retailerId, retailerName, redemptionDate, redemptionCount, 'maxRedemptions' AS redemptionType
FROM weeklyTransactionTbl
WHERE redemptionCount in (SELECT MAX(redemptionCount) FROM weeklyTransactionTbl))

SELECT redSummary.redemptionDate, redSummary.redemptionCount, redSummary.redemptionType, createDateTime
FROM maxMinRedemption AS redSummary
INNER JOIN ( SELECT retailerId, redemptionDate, redemptionCount, createDateTime, row_number() over (PARTITION BY retailerId, redemptionDate ORDER BY createDateTime DESC) AS logging 
            FROM TblRedemptions_ByDay) bigTable
ON redSummary.retailerId = bigTable.retailerId  
AND redSummary.redemptionDate = bigTable.redemptionDate
AND redSummary.redemptionCount = bigTable.redemptionCount
WHERE bigTable.logging = 1

 ![Capture](https://github.com/kami71539/IlmarIntelligence/assets/49458424/413ad1c7-b25e-4238-a824-332331d28712)

Is there another method you can use to pull back the most recent redemption count, by
redemption date, for the date range 2023-10-30 to 2023-11-05, for retailer "ABC Store"?
In words, describe how you would do this (no need to write a query, unless you’d like to).

Change 1 - I could use Lead or Lag function partitioning on the basis of retail id, redemptionDate, and sorting by createdatetime (asc/desc depending on lead or lag) and keep only the rows where lead/lag is null.
Change 2- I could have used subquery instead of with clause and reduced the query length.
Change 3 - I could have used left join instead of inner join and applied filter on retailer name outside the join.
