import json

from src.navigate_skartner.tools import tools
from src.openai_client import openai_client

GPT_MODEL = "gpt-3.5-turbo-0613"


def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})


def use_assistant_message(messages, assistant_message):
    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            messages.append({"role": "function", "tool_call_id": tool_call.id,
                            "name": tool_call.function.name, "arguments": tool_call.function.arguments,  "content": ""})
    else:
        return {"role": assistant_message.role, "content": assistant_message.content}


def pop_arguments_key(messages):
    new_messages = json.loads(json.dumps(messages))
    for message in new_messages:
        if 'arguments' in message:
            message.pop('arguments')
    return new_messages


def navigate_skartner(user_message: str):
    messages.append({"role": "user", "content": user_message})
    chat_response = chat_completion_request(
        pop_arguments_key(messages), tools=tools
    )
    assistant_message = chat_response.choices[0].message
    use_assistant_message(messages, assistant_message)
    return assistant_message
