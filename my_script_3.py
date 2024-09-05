import uuid
import argparse
import requests
import json
import random
from agent_database import get_agent_id

# If starting fresh run these commands:
# run `memgpt quickstart`
# run `memgpt run --agent yuki` --- Ctrl + C out of the chat.

# if storage backend is postgresql:
# run `export PGVECTOR_TEST_DB_URL=postgresql+pg8000://<user>:<password>@localhost:5432/<dbname>

# run the following commands in a separate terminal before running this script:
# run `export MEMGPT_SERVER_PASS=yuki`
# run `memgpt server` 

BASE_URL = "http://localhost:8283"
TOKEN = "yuki"
AGENT_ID = uuid.UUID(get_agent_id()) # for sqlite
# AGENT_ID = uuid.UUID("25dd901c-3cc2-42ed-86ee-a3d80493b24f") # this is for postgresql.

class AgentClient:
    def __init__(self, base_url: str, token: str, agent_id: uuid.UUID):
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }
        self.agent_id = agent_id

    def send_message(self, message: str, role: str = "user", stream: bool = False):
        data = {
            "agent_id": str(self.agent_id),
            "message": message,
            "stream": stream,
            "role": role
        }
        try:
            response = requests.post(
                f"{self.base_url}/api/agents/{self.agent_id}/messages", 
                headers=self.headers, 
                json=data,
                timeout= 10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:

            return {'messages': {'error_msg': "I'm sorry, this is taking some time... Thank you for your patience."}}
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    
    def format_response(self, response: dict):
        for msg in response.get('messages', []):
            if 'internal_monologue' in msg:
                print(f"THOUGHTS: {msg['internal_monologue']}")
            elif 'function_call' in msg and 'arguments' in msg['function_call']:
                arguments = json.loads(msg['function_call']['arguments'])
                message = arguments.get('message', '')
                print(f"ASSISTANT: {message}")
            elif 'error_msg' == msg:
                print(f"ASSISTANT: {response['messages'][msg]}")

def main():
    client = AgentClient(BASE_URL, TOKEN, AGENT_ID)
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--function',
        type=str,
        default="user_chat",
        help='[user_chat|system_chat]'
    )

    parser.add_argument(
        '--passes',
        type=int,
        default=10,
        help='Number of conversations initiated by system.'
    )
    args = parser.parse_args()
    if args.function == 'user_chat':
        print("You can start chatting with the agent. Type 'STOP' to end the conversation.")
    
        while True:
            user_input = input("You: ")
            if user_input.strip().upper() == "STOP":
                print("Ending conversation.")
                break
            response = client.send_message(user_input)
            client.format_response(response)
    elif args.function == 'system_chat':
        print(f"Number of passes: {args.passes}")
        count = 0
        context = "I will perform a batch of tests where I will write a number, and you will have to tell me the next prime number"
        print("SYSTEM: ", context)
        response = client.send_message(context)
        client.format_response(response)

        while count < args.passes:
            count += 1
            random_number = f"Number is {random.randint(1, 10000)}"
            print("SYSTEM: ", random_number)
            response = client.send_message(random_number)
            client.format_response(response)
        
        print('STOP')



if __name__ == "__main__":
    main()
