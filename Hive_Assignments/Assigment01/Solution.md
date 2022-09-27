# Hive Assignment01

## DESCRIPTION

<B>This assignment includes tasks to check skills on Hive queries and HDFS</b>

### TASKS:
1. Create a internal hive table "sales_order_csv" which will store csv data sales_order_csv .. make sure to skip header row while creating table

2. Load data from hdfs path into "sales_order_csv" 

3. Create an internal hive table which will store data in ORC format "sales_order_orc"

4. Load data from "sales_order_csv" into "sales_order_orc"


#### LOADING DATA FROM HOST SYSTEM TO LFS AND THEN TO HDFS

```
hadoop fs -put akshit/sales_order_data.csv /tmp/hive_data_class2
```

#### Task1: Creating sales_order_data_csv table
```
create table sales_order_data_csv
(
ORDERNUMBER int,
QUANTITYORDERED int,
PRICEEACH float,
ORDERLINENUMBER int,
SALES float,
STATUS string,
QTR_ID int,
MONTH_ID int,
YEAR_ID int,
PRODUCTLINE string,
MSRP int,
PRODUCTCODE string,
PHONE string,
CITY string,
STATE string,
POSTALCODE string,
COUNTRY string,
TERRITORY string,
CONTACTLASTNAME string,
CONTACTFIRSTNAME string,
DEALSIZE string
)
row format delimited
fields terminated by ','
tblproperties("skip.header.line.count"="1")
; 
```
 
#### Task2: Load data from HDFS to table
```
load data inpath '/tmp/hive_data_class2/sales_order_data.csv' into table sales_order_data_csv;

```

#### Task3:  Create an internal hive table which will store data in ORC format "sales_order_orc"
```
create table sales_order_orc
(
ORDERNUMBER int,
QUANTITYORDERED int,
PRICEEACH float,
ORDERLINENUMBER int,
SALES float,
STATUS string,
QTR_ID int,
MONTH_ID int,
YEAR_ID int,
PRODUCTLINE string,
MSRP int,
PRODUCTCODE string,
PHONE string,
CITY string,
STATE string,
POSTALCODE string,
COUNTRY string,
TERRITORY string,
CONTACTLASTNAME string,
CONTACTFIRSTNAME string,
DEALSIZE string
)
stored as orc;
```


#### Task04: Load data from "sales_order_data_csv" into "sales_order_orc"
```
from sales_order_data_csv insert overwrite table sales_order_orc select *;
```


## Queries


#### 1. Calculatye total sales per year
```
select year_id, sum(sales) as total_sales from sales_order_orc group by year_id;
```
![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/Hive_Assignments/Assigment01/Screenshots/q1.PNG)


#### 2. Find a product for which maximum orders were placed
```
select PRODUCTLINE, SUM(QUANTITYORDERED) AS total_orders FROM sales_order_orc group by PRODUCTLINE ORDER BY total_orders desc LIMIT 1;
```
![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/Hive_Assignments/Assigment01/Screenshots/query2.PNG)


#### 3. Calculate the total sales for each quarter
```
select YEAR_ID as year, QTR_ID as Quarter, sum(SALES) as sale_in_quarter from sales_order_orc GROUP BY YEAR_ID,QTR_ID ;
```
![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/Hive_Assignments/Assigment01/Screenshots/QUERY3.PNG)


#### 4. In which quarter sales was minimum
```
select YEAR_ID as year, QTR_ID as Quarter, sum(SALES) as min_sales_qtr from sales_order_orc GROUP BY YEAR_ID,QTR_ID ORDER BY min_sales_qtr limit 1 ;
```
![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/Hive_Assignments/Assigment01/Screenshots/q4.PNG)

#### 5. In which country sales was maximum and in which country sales was minimum
```
select COUNTRY, sum(SALES) as total_sales from sales_order_orc group by COUNTRY order by total_sales asc limit 1 union all select COUNTRY, sum(SALES) as total_sales from sales_order_orc group by COUNTRY order by total_sales desc limit 1;
```
![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/Hive_Assignments/Assigment01/Screenshots/Q5.PNG)

#### 6.  Calculate quartelry sales for each city
```
select CITY,YEAR_ID, QTR_ID,SUM(SALES) FROM sales_order_orc group by CITY,YEAR_ID, QTR_ID;
```
![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/Hive_Assignments/Assigment01/Screenshots/q6.PNG)


#### 7.  Find a month for each year in which maximum number of quantities were sold
```
select YEAR_ID,MONTH_ID,total_sales from
(
select YEAR_ID, MONTH_ID,total_sales,dense_rank() over (partition by YEAR_ID order by total_sales desc) as rank 
from
(select YEAR_ID,MONTH_ID,sum(sales) as total_sales from sales_order_orc group by YEAR_ID,MONTH_ID)a1
)a2 
where rank =1;
```
![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/Hive_Assignments/Assigment01/Screenshots/q7.PNG)
