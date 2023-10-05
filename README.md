# Bank Transaction API

This is a simple REST API for executing transactions between bank accounts.

## Prerequisites

- Python 3.9.13
- Flask 1.1.2
- SQLite 3.39.3

## Getting Started
I have run the code locally on my computer, but you can make a viritual environment if you want. 
You'll have to install the Prerequirements as mentioned over. 

I have tested my code using the Postman Desktop application. 

The application will be usually be accessible at http://127.0.0.1:5001/api/executeTransaction by default(for mac).
To run code simply run 
```
python banking.py
```
Open postman and type in the web address that you get in your terminal + api/executeTransaction
Change the request type to POST. 
Navigate to the "body" tab under the weblink and open it. Then tap the "raw" button. To the right set the type to JSON. 
In this space you can insert your JSON file. Under I've provided an example JSON. 

For accessing the database simply write: 
```
sqlite3 bank_data.db
```
To check the content of the database
```
SELECT * FROM accounts;
```
Then send your POST request in Postman and retype the SELECT statement and you'll see that the sums have changed.  

## Example JSON

- **POST /api/executeTransaction**: Execute financial transactions between multiple bank accounts.
    ```
    {
    "transactions": [
        {
            "sourceAccount": {
                "id": 1,
                "name": "Account1",
                "availableCash": 100.0
            },
            "destinationAccount": {
                "id": 2,
                "name": "Account2",
                "availableCash": 50.0
            },
            "registeredTime": 1633595048,
            "executedTime": 1633595050,
            "cashAmount": 25.0
        },
        {
            "sourceAccount": {
                "id": 2,
                "name": "Account2",
                "availableCash": 50.0
            },
            "destinationAccount": {
                "id": 3,
                "name": "Account3",
                "availableCash": 200.0
            },
            "registeredTime": 1633595049,
            "executedTime": 1633595051,
            "cashAmount": 30.0
        },
        {
            "sourceAccount": {
                "id": 3,
                "name": "Account3",
                "availableCash": 200.0
            },
            "destinationAccount": {
                "id": 4,
                "name": "Account4",
                "availableCash": 75.0
            },
            "registeredTime": 1633595050,
            "executedTime": 1633595052,
            "cashAmount": 40.0
        },
        {
            "sourceAccount": {
                "id": 4,
                "name": "Account4",
                "availableCash": 75.0
            },
            "destinationAccount": {
                "id": 5,
                "name": "Account5",
                "availableCash": 120.0
            },
            "registeredTime": 1633595051,
            "executedTime": 1633595053,
            "cashAmount": 20.0
        },
        {
            "sourceAccount": {
                "id": 5,
                "name": "Account5",
                "availableCash": 120.0
            },
            "destinationAccount": {
                "id": 6,
                "name": "Account6",
                "availableCash": 90.0
            },
            "registeredTime": 1633595052,
            "executedTime": 1633595054,
            "cashAmount": 15.0
        },
        {
            "sourceAccount": {
                "id": 6,
                "name": "Account6",
                "availableCash": 90.0
            },
            "destinationAccount": {
                "id": 1,
                "name": "Account1",
                "availableCash": 100.0
            },
            "registeredTime": 1633595053,
            "executedTime": 1633595055,
            "cashAmount": 35.0
        }
    ]
    }
    ```
    Example response:
    ```json
    {
        "success": true
    }
    ```
