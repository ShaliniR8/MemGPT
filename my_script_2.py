from memgpt import create_client
import uuid
# Connect to the server as a user
client = create_client()

# Send a message to the agent
messages = client.user_message(agent_id=uuid.UUID("4d64be10-418a-460c-a5de-c4815aea910f"), message="Hello, yuki!")
# Create a helper that sends a message and prints the assistant response only
def send_message(message: str):
    """
    sends a message and prints the assistant output only.
    :param message: the message to send
    """
    response = client.user_message(agent_id=uuid.UUID("4d64be10-418a-460c-a5de-c4815aea910f"), message=message).messages
    # breakpoint()
    for r in response:
        # Can also handle other types "function_call", "function_return", "function_message"
        if "assistant_message" in r:
            print("ASSISTANT:", r["assistant_message"])
        elif "internal_monologue" in r:
            print("THOUGHTS:", r["internal_monologue"])

# Send a message and see the response
send_message("Please introduce yourself and tell me about your abilities!")

# curl
# curl --request POST --url http://localhost:8283/api/agents --header "accept: application/json" --header "authorization: Bearer mc7tWi2C9B_n5wyhOINadg" --header "content-type: application/json" --data "{\"config\": {\"name\": \"yuki\", \"preset\": \"memgpt_chat\", \"human\": \"User\", \"persona\": \"yuki\"}}"

