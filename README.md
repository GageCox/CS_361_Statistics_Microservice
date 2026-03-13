# CS_361_Statistics_Microservice
Statistics Microservice for CS361 project.
This service will return the number of entries in a database, either the total number of entries in a table or the number of entries in a table that match filters.

This microservice uses ZeroMQ as it's communication pipeline

# Request
1. Create a REQ socket
2. Connect to a port
3. Send a JSON request
4. Wait for a JSON response

Sample requests to service: 
```
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

// overall_statistics
request = {
    "action": "overall_statistics",
    "table": "movies"
}
socket.send(json.dumps(request).encode("utf-8))

// filtered_statistics
request = {
    "action": "filtered_statistics",
    "table": "movies",
    "filters": {
          "genre": "Action"
    }
}
socket.send(json.dumps(request).encode("utf-8))

// attribute_statistics
request = {
    "action": "attribute_statistics",
    "table": "movies",
    "attribute": "genre"
}
socket.send(json.dumps(request).encode("utf-8))

// attribute_statistics with filters
request = {
    "action": "attribute_statistics",
    "table": "movies",
    "attribute": "genre",
    "filters": {
        "year": 2020
    }
}
socket.send(json.dumps(request).encode("utf-8))
```
**Action:**\
    overall_statistics: Returns the count of all entries in the table\
    filtered_statistics: Returns the count of all entries in the table matching the filters\
    attribute_statistics: Returns the count of different attributes from a table\
**Table:** The name of the table you want to access\
**Filters:** Table attributes you want to filter by\
**IMPORTANT:**\
    overall_statistics doesn't accept filters\
    filtered_statistics requires a filter\
    attribute_statistics has optional filters\

# Recieve
1. Store response from socket
2. Decode JSON response

Sample code for receiving:
```
response_bytes = socket.recv()
response = json.loads(response_bytes.decode("utf-8"))
```
