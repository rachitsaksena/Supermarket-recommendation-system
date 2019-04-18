# Supermarket-recommendation-system

This program detects real-time transactions on firestore and recommends items for the customer who made the transaction. The recommendations are then uploaded on firestore. The recommendation system uses cosine simliarity. 

### Requirements
1. pandas
1. numpy
1. turicreate
1. sklearn
1. firebase_admin

### Usage Instructions

Since this program detects only real-time changes, in order to get the predictions on firestore, this program must be running when the transaction is made/added on firestore. 
#### Input Format
![input](/images/input.png)
#### Output Format
![output](/images/output.png)
