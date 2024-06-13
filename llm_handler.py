import requests
import json
from sshtunnel import SSHTunnelForwarder


tunnel = None


def start_tunnel(remote_server, ssh_username, ssh_pkey, remote_port, local_port):
    global tunnel
    tunnel = SSHTunnelForwarder(
        (remote_server, 22),
        ssh_username=ssh_username,
        ssh_pkey=ssh_pkey,
        remote_bind_address=("localhost", remote_port),
        local_bind_address=("localhost", local_port),
    )
    tunnel.start()
    print(f"Tunnel opened at localhost:{tunnel.local_bind_port}\n")


def stop_tunnel():
    """
    Stops the SSH tunnel
    """
    global tunnel
    if tunnel:
        tunnel.stop()
        print("SSH tunnel closed\n")


def get_response(url, prompt, model="llama3:70b", past_responses=None):
    if past_responses is None:
        history = []
    else:
        history = [
            {"role": "assistant", "content": message} for message in past_responses
        ]
    history.append({"role": "user", "content": prompt})

    data = {
        "model": model,
        "messages": history,
        "stream": False,
        
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        return response.json()["message"]["content"]
    else:
        print(f"Request failed with status code {response.status_code}\n")
        return None
