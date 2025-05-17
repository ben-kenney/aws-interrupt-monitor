import os
import requests
import time
import json
import socket

# Read configuration from environment variables
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "your_ntfy_topic")  # Default fallback if not set
NTFY_SERVER = os.getenv("NTFY_SERVER", "https://ntfy.sh")  # Default fallback if not set
NTFY_SECRET = os.getenv("NTFY_SECRET", "1234")  # Default fallback if not set
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "60"))  # Default: 60 seconds
VM_HOSTNAME = os.getenv("VM_HOSTNAME") or socket.gethostname()

def check_spot_interruption():
    """Check for Spot Instance interruption notice."""
    metadata_url = "http://169.254.169.254/latest/meta-data/spot/instance-action"
    try:
        response = requests.get(metadata_url, timeout=2)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data  # Return the interruption details
    except requests.exceptions.RequestException:
        pass
    return None

def send_ntfy_alert(message: str, secret: str, url: str, timeout: int = 10, priority: str = "high", tags: list[str] = ["cursing_face"]) -> int:
    """
    Sends a notification via ntfy service using a POST request.

    Args:
        message_text (str): The main message text to be sent.
        tags (str): Tags to categorize the notification.
        title (str): The title of the notification.
        secret (str): The secret token for authorization.
        url (str): The URL of the ntfy service endpoint.

    Returns:
        int: The HTTP response status code from the POST request.
    """
    xtags = ",".join(tags)
    # Define the headers for the POST request
    headers = {
        "X-Tags": xtags,
        "Title": f"AWS Spot Instance Interruption Alert ({VM_HOSTNAME})",
        "Authorization": f"Bearer {secret}",
        "Markdown": "yes",
        "Priority": priority,
    }

    # Send the POST request to the specified URL with the message, headers, and timeout
    response = requests.post(url, headers=headers, data=message, timeout=timeout)
    print(f"Quick ntfy with message: {message}")
    # Return the response status code for debugging purposes
    return response.status_code



def main():
    print(f"Starting Spot Instance interruption monitor (Polling every {POLL_INTERVAL} seconds)...")
    print(f"NTFY Server: {NTFY_SERVER}, Topic: {NTFY_TOPIC}")

    message = f"Starting spot instance interruption monitor. We will poll every {POLL_INTERVAL} seconds."
    send_ntfy_alert(message=message, secret=NTFY_SECRET, url=f"{NTFY_SERVER}/{NTFY_TOPIC}", tags=["desktop_computer"])

    while True:
        interruption_data = check_spot_interruption()
        if interruption_data:
            message = (
                f"Spot Instance interruption detected!\n"
                f"Action: {interruption_data['action']}\n"
                f"Time: {interruption_data['time']}"
            )
            print(message)
            send_ntfy_alert(message, secret=NTFY_SECRET, url=f"{NTFY_SERVER}/{NTFY_TOPIC}")
            break  # Exit after sending the alert
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
