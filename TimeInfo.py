import zmq
import requests
from datetime import datetime, timezone

def get_utc_time():
    try:
        url = "https://timeapi.io/api/Time/current/zone"
        params = {"timeZone": "UTC"}

        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        if 'dateTime' in data:
            return data['dateTime']
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error getting timestamp: {e}")
        return None


def get_current_time(request_data):

    try:
        utc_dt = datetime.now(timezone.utc)
        utc_time_str = utc_dt.isoformat()

        local_dt = utc_dt.astimezone()
        local_time_str = local_dt.isoformat()

        api_time_str = get_utc_time()

        return {
            "api_type": "TIME_INFO",
            "status": "success",
            "time_info": {
                "utc_time": utc_time_str,
                "local_time": local_time_str,
                "utc_api_time": api_time_str
            }
        }

    except Exception as e:
        return {
            "api_type": "TIME_INFO",
            "status": "error",
            "response": {
                "error": f"Failed to get time information: {str(e)}"
            }
        }


if __name__ == "__main__":
    result = {}

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5557")

    print("TimeInfo Microservice is running on port 5557...")

    while True:
        try:
            message = socket.recv_json()
            print(f"Received request: {message}")

            api_type = message.get("api_type", "").strip()

            if api_type == "TIME_INFO":
                result = get_current_time(message)
            else:
                result = {
                    "api_type": "ERROR",
                    "status": "error",
                    "message": f"Unknown API type: {api_type}"
                }

            print(f"Sending response: {result}")
            socket.send_json(result)

        except Exception as e:
            error_result = {
                "api_type": "ERROR",
                "status": "error",
                "message": f"Server error: {str(e)}"
            }
            print(f"Error processing request: {e}")
            socket.send_json(error_result)