import os
import uuid
from memgpt.config import MemGPTConfig
from memgpt.metadata import MetadataStore
from memgpt.cli.cli import create_default_user_or_exit
from memgpt.agent import Agent, save_agent

def user_message(agent_id: str, message: str) -> Union[List[Dict], Tuple[List[Dict], int]]:
    return send_message(agent_id, message, role="user")

def get_tools(agent_state, ms):
    tools = []
    for tool_name in agent_state.tools:
        tool = ms.get_tool(tool_name, agent_state.user_id)
        if tool is None:
            print(f"{tool} not found.")
        tools.append(tool)
    return tools

def initialize(agent):
    config = MemGPTConfig.load()
    ms = MetadataStore(config)
    user = create_default_user_or_exit(config, ms)

    persona = ms.get_persona(name=agent, user_id= uuid.UUID('00000000-0000-0000-0000-8c42e67ca299'))
    agent_state = ms.get_agent(agent_name=agent, user_id=user.id)
    human = config.human

    llm_config = config.default_llm_config
    embedding_config = config.default_embedding_config
    model = llm_config.model
    model_wrapper = llm_config.model_wrapper

    tools = get_tools(agent_state=agent_state, ms=ms)
    breakpoint()
    memgpt_agent = Agent(agent_state=agent_state, tools=tools)

    print('Got!')

if __name__ == "__main__":
    initialize(agent="yuki")