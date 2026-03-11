import mysql.connector
import zmq
import json

def get_connection():
    conn = mysql.connector.connect(
        host='', # add host
        user='', # add username
        password='', # add password
        database='' # add database name
    )
    cursor = conn.cursor(dictionary=True)
    return conn, cursor

def overall_statistics(req):
    table = req["table"]
    conn, cursor = get_connection()

    query = f"SELECT COUNT(*) FROM {table}"

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def filtered_statistics(req):
    table = req["table"]
    filters = req.get("filters", {})
    where = ""
    vals = ()

    conn, cursor = get_connection()

    if filters:
        condition = [f"{i} = %s" for i in filters]
        where = "WHERE " + " AND ".join(condition)
        vals = tuple(filters.values())

    query = f"SELECT COUNT(*) AS total FROM {table} {where}"

    cursor.execute(query, vals)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def route_handler(req):
    action = req.get("action")

    if action == "overall_statistics":
        return overall_statistics(req)
    
    elif action == "filtered_statistics":
        return filtered_statistics(req)
    
    else:
        raise ValueError("Invalid Request")
    
def runServer():
    global context, socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")

    print("Service running on port 5556...")

    while True:
        message = socket.recv()
        request = json.loads(message.decode("utf-8"))
        result = route_handler(request)
        response = {
            "status": "success",
            "data": result
        }
        socket.send(json.dumps(response).encode("utf-8"))

if __name__ == "__main__":
    runServer()
