import uuid
import requests
import json

# If starting fresh run these commands:
# run `memgpt quickstart`
# run `memgpt run --agent yuki` --- Ctrl + C out of the chat.

# run the following commands in a separate terminal before running this script:
# run `export MEMGPT_SERVER_PASS=yuki`
# run `memgpt server` 

BASE_URL = "http://localhost:8283"
TOKEN = "yuki"


# TODO: Agent ID is different for different systems or instances of Yuki. Handle updating the Agent ID accordingly.
# AGENT_ID = uuid.UUID(<agent_id>)


class AgentClient:
    def __init__(self, base_url: str, token: str, agent_id: uuid.UUID):
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json"
        }
        self.agent_id = agent_id

    def send_message(self, message: str, role: str = "user", stream: bool = False):
        data = {
            "agent_id": str(self.agent_id),
            "message": message,
            "stream": stream,
            "role": role
        }
        response = requests.post(f"{self.base_url}/api/agents/{self.agent_id}/messages", headers=self.headers, json=data)
        if response.status_code != 200:
            raise ValueError(f"Failed to send message: {response.text}")
        return response.json()
    
    def format_response(self, response: dict):
        for msg in response.get('messages', []):
            if 'internal_monologue' in msg:
                print(f"THOUGHTS: {msg['internal_monologue']}")
            elif 'function_call' in msg and 'arguments' in msg['function_call']:
                arguments = json.loads(msg['function_call']['arguments'])
                message = arguments.get('message', '')
                print(f"ASSISTANT: {message}")

def main():
    client = AgentClient(BASE_URL, TOKEN, AGENT_ID)
    print("You can start chatting with the agent. Type 'STOP' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        if user_input.strip().upper() == "STOP":
            print("Ending conversation.")
            break

        response = client.send_message(user_input)
        client.format_response(response)


if __name__ == "__main__":
    main()
