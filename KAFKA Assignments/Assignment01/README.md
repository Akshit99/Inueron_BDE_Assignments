# Assignment01 of Kafka

## This assignment is done to test skills on:
-  Creating Kafka topics and Schema registry 
-  Create Producer and Consumers read from CSV data
-  Testing multiple consumer groups/ single groups


## 1. Create one kafka topic named as "restaurent-take-away-data" with 3 partitions

![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/KAFKA%20Assignments/Assignment01/screenshots/Kafka-topic.PNG?raw=true "Create Topic")

## 2. Setup key (string) & value (json) schema in the confluent schema registry

Json Schema
https://github.com/Akshit99/Inueron_BDE_Assignments/blob/79957bafbe1b6a0c8eba2a68008e9f98dd154b6a/KAFKA%20Assignments/Assignment01/schema.json#L1-L34

key-schema
```
"string"
```

 ## 3. Write a kafka producer program to read data records from restaurent data csv file. *Read the latest version of schema and schema_str from schema registry.*

#### **Reading schema from Schema registry**

https://github.com/Akshit99/Inueron_BDE_Assignments/blob/ae4e57301b4b5ee69895954ba2be1eb7a6ed68e7/KAFKA%20Assignments/Assignment01/restaurants_producer.py#L109-L119

## 4. From producer code, publish data in Kafka Topic one by one and use dynamic key while publishing the records into the Kafka Topic
```
python restaurants_producer.py
```

![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/KAFKA%20Assignments/Assignment01/screenshots/producer.PNG?raw=true)

## 5. Write kafka consumer code and create two copies of same consumer code and save it with different names. Test two scenarios with your consumer code:
#### a. Use different groupID in each consumer and check total number of records printed
#### b. Use same groupID in both consumer and check total number of records printed

https://github.com/Akshit99/Inueron_BDE_Assignments/blob/ae4e57301b4b5ee69895954ba2be1eb7a6ed68e7/KAFKA%20Assignments/Assignment01/restaurant_consumers1.py#L72-L76
https://github.com/Akshit99/Inueron_BDE_Assignments/blob/ae4e57301b4b5ee69895954ba2be1eb7a6ed68e7/KAFKA%20Assignments/Assignment01/restaurant_consumers2.py#L77-L81
Both these cases were tested by changing GroupId to:

### Different Groups Case:  "G2" , "G3"

Consumer1 
![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/KAFKA%20Assignments/Assignment01/screenshots/dg_consumer1.PNG?raw=true)
Consumer2
![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/KAFKA%20Assignments/Assignment01/screenshots/dg_consumer2.PNG?raw=true)
---

### Same Groups Case: "G1" , "G1"

Consumer1
![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/KAFKA%20Assignments/Assignment01/screenshots/sg_consumer1.PNG?raw=true)

Consumer2 
![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/KAFKA%20Assignments/Assignment01/screenshots/sg_consumer2.PNG?raw=true)

---
## Findings:
- When different groups were passed, Each consumer will read all the partitions simulataneously as there is no restriction on them of being in the same group. So both end up printing same Total records : 74817
- When same groups were passed, Each consumer is assigned a specific set of partition and it can only consume message from that specific partition. So there was a split between both consumer and both ended up reading unique records. 

 - Consumer1 printed : 24795 records  
 - Consumer2 printed: 50022 records 
 - Total: 74817 (same as one consumer of different groups)
  
---

## 6. Write another kafka consumer to read data from kafka topic and from the consumer code create one csv file "output.csv" and append consumed records output.csv file.

https://github.com/Akshit99/Inueron_BDE_Assignments/blob/a2099af2bd525e10a7777f30664199e2a805aeb8/KAFKA%20Assignments/Assignment01/restaurant_consumers_to_csv.py#L75-L98

### Logic for closing consumer once partition is read(No more messages)
- Create a empty_poll_counter variable outside your while loop.
- Increased the counter every time poll() fetches 0 records from Kafka Brokers.
- Reset the counter to 0 if the poll() extracts records
- If counter == 20(threshold), then break out of loop and close the consumer.

![alt text](https://github.com/Akshit99/Inueron_BDE_Assignments/blob/main/KAFKA%20Assignments/Assignment01/screenshots/df.PNG?raw=true)


## Conclusion:
- Kafka Basics were successfully executed with Topic Creation, Schema Registry Connections, Producer, Consumer, Consumer groups, Reading and Writing csv data from KAFKA.
