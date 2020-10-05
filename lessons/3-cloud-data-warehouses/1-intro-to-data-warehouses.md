# Data Warehouse

- Operational perspective - Make it work!
- Business perspective - What is going on?

Definitions of a DWH
- a copy of transaction data specifically structured for query and analysis (KIMBALL)
- a **subject-oriented**, **integrated**, **nonvolatile* and **time-variant** collection of data in support of management's decisions (INMON)
- a system that retrives and consolidated data periodically from the source system into a dimensional or normalied data store. It is uually keeps years of history and is queried for business inteligence or other analytical activities. Is is typically updated in batches. (RAINARDI)

## Tech perspective
![Tech perspictive](images/tech_perspective.png "Tech perspective")

## Goals
- Simple to understand
- Performant
- Quality Assured
- Handles new questions well
- Secure


![Schemas](images/schemas_olap_vs_oltp.png "Schemas")

### Facts
- Numeric and Additive (99% cases)
    - Good: Comment counts, total amount for an invoice
    - Not good: invoice id, comment

### Dimensions
- Date & time
- Phisical locations
- Human roles
- Goods sold

## Operational db to Analytics

Naive ETL: From 3NF to ETL
- Query 3NF DB (Extract)
    - Join tables toghether
    - Change types
    - add new columns
- Loading
    - Insert into dfacts & dimension tables

Example [Sakila DB](https://www.jooq.org/sakila)

From
![Pagila 3NF](pagila-3nf.png "Pagila 3NF")
To
![Pagila Star](pagila-star.png "Pagila Star")

Examples - using the 3nf form we need to do a lot of DEEP joins

### Transform to star schema

**dimDate table**
- date_key composed as an integer yyyyMMDD
- use EXTRACT function for the rest of the columns (ex: EXTRACT(year FROM payment_date) )
- do some logic for identifying is_weekend

**dimCustomer table**
- denormalize
- just select fields from customer, address, city and country

**dimMovie**
- denormalize
- just select fields from film and language

**dimStore**
- denormalize
- just select from store, staff, address, city and country

**factSales**
- build the same type of date key yyyyMMDD
- select from payment, rental and inventory


ETL in our context
 - E - select fields
 - T - transformations like extract, build date_key, compute is_weekend
 - L - the insert into the new tables

Using the new schema is simpler, you don't need any deep join
```
SELECT dimMovie.title, dimDate.month, dimCustomer.city, sum(sales_amount) as revenue
FROM factSales 
JOIN dimMovie    on (dimMovie.movie_key      = factSales.movie_key)
JOIN dimDate     on (dimDate.date_key         = factSales.date_key)
JOIN dimCustomer on (dimCustomer.customer_key = factSales.customer_key)
group by (dimMovie.title, dimDate.month, dimCustomer.city)
order by dimMovie.title, dimDate.month, dimCustomer.city, revenue desc;
```
VS
```
SELECT f.title, EXTRACT(month FROM p.payment_date) as month, ci.city, sum(p.amount) as revenue
FROM payment p
JOIN rental r    ON ( p.rental_id = r.rental_id )
JOIN inventory i ON ( r.inventory_id = i.inventory_id )
JOIN film f ON ( i.film_id = f.film_id)
JOIN customer c  ON ( p.customer_id = c.customer_id )
JOIN address a ON ( c.address_id = a.address_id )
JOIN city ci ON ( a.city_id = ci.city_id )
group by (f.title, month, ci.city)
order by f.title, month, ci.city, revenue desc;
```

- The new query is not on a single table, but is just a stright forward join to get the details for each dimension
- The queries with the star schema are more performant on large datasets.

