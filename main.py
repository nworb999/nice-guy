from llm_handler import start_tunnel, stop_tunnel, get_response

IMAGINATION_IP = "imagination.mat.ucsb.edu"
IMAGINATION_PORT = 11434
LOCAL_PORT = 12345
SSH_USERNAME = "emma"
SSH_KEYFILE = "~/.ssh/id_rsa"

URL = f"http://localhost:{LOCAL_PORT}/api/chat"


start_tunnel(
    remote_server=IMAGINATION_IP,
    ssh_username=SSH_USERNAME,
    ssh_pkey=SSH_KEYFILE,
    remote_port=IMAGINATION_PORT,
    local_port=LOCAL_PORT,
)

response = get_response(URL, "Hello, how are you?")
print("\n" + response + "\n")

stop_tunnel()