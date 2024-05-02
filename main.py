from openai import AsyncOpenAI, AsyncAPIResponse
import random
from typing import List
import os
import json
import asyncio


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM = """
You are a customer service bot of SockStore Inc. Online shop of socks.
You can help customers with status of their orders.
You can only answer questions related to orders and their status.
You need to ask for the session_id before you can answer any questions.
You need customer session_id to call the API to get the order status.
"""

async def get_all_orders(session_id: str) -> List[dict]:
    # Call the API to get the orders for the customer
    if not session_id:
        return {
            "error": "No session_id provided. Please provide a session_id.",
            "status": 403,
        }

    return random.choices(
        [
            {
                "id": "1",
                "name": "red socks",
                "description": "very red very socks",
                "status": "received",
            },
            {
                "id": "2",
                "name": "blue socks",
                "description": "very blue very socks",
                "status": "shipped",
            },
            {
                "id": "3",
                "name": "green socks",
                "description": "very green very socks",
                "status": "cancelled",
            },
            {
                "id": "4",
                "name": "yellow socks",
                "description": "very yellow very socks",
                "status": "delivered",
            },
            {
                "id": "5",
                "name": "black socks",
                "description": "very black very socks",
                "status": "shipped",
            },
            {
                "id": "6",
                "name": "white socks",
                "description": "very white very socks",
                "status": "received",
            },
            {
                "id": "7",
                "name": "purple socks",
                "description": "very purple very socks",
                "status": "delivered",
            },
            {
                "id": "8",
                "name": "orange socks",
                "description": "very orange very socks",
                "status": "received",
            },
            {
                "id": "9",
                "name": "pink socks",
                "description": "very pink very socks",
                "status": "shipped",
            },
            {
                "id": "10",
                "name": "brown socks",
                "description": "very brown very socks",
                "status": "received",
            },
            {
                "id": "11",
                "name": "grey socks",
                "description": "very grey very socks",
                "status": "cancelled",
            },
            {
                "id": "12",
                "name": "cyan socks",
                "description": "very cyan very socks",
                "status": "received",
            },
            {
                "id": "13",
                "name": "magenta socks",
                "description": "very magenta very socks",
                "status": "shipped",
            },
            {
                "id": "14",
                "name": "violet socks",
                "description": "very violet very socks",
                "status": "received",
            },
            {
                "id": "15",
                "name": "indigo socks",
                "description": "very indigo very socks",
                "status": "cancelled",
            },
        ],
        k=2,
    )


def get_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "get_all_orders",
                "description": "Get all orders for a customer, with id, description, and status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "JWT token for the customer to access their orders.",
                        }
                    },
                    "required": ["session_id"],
                },
            },
        },
    ]


def is_tool_calls_required(response: AsyncAPIResponse) -> bool:
    # Check if the response requires tool calls
    return (
        response.choices[0].finish_reason == "tool_calls"
        and response.choices[0].message.tool_calls
    )


def call_tool(function_name: str, parameters: dict) -> dict:
    # Call the tool function with the provided parameters
    if type(parameters) == str:
        try:
            parameters = json.loads(parameters)
        except json.JSONDecodeError:
            pass

    if function_name == "get_all_orders":
        return get_all_orders(parameters["session_id"])


async def chat_complete(client, message_list: List[str]) -> str:
    """{
        "id": "chatcmpl-qwerefsd",
        "choices": [
            {
                "finish_reason": "tool_calls",
                "index": 0,
                "logprobs": null,
                "message": {
                    "content": "Great! Please let me retrieve your order information. Let me check your order status with the provided session ID.",
                    "role": "assistant",
                    "function_call": null,
                    "tool_calls": [
                        {
                            "id": "call_8Sm4ZEk0VIIocL6CXGAIw4EC",
                            "function": {
                                "arguments": "{\\"session_id\\":\\"qwertewefdfsdf"}",
                                "name": "get_all_orders"
                            },
                            "type": "function"
                        }
                    ]
                }
            }
        ],
        "created": 1714547383,
        "model": "gpt-3.5-turbo-0125",
        "object": "chat.completion",
        "system_fingerprint": "fp_3b956da36b",
        "usage": {
            "completion_tokens": 93,
            "prompt_tokens": 234,
            "total_tokens": 327
        }
    }"""
    model = "gpt-3.5-turbo"
    response = await client.chat.completions.create(
        model=model,
        messages=message_list,
        tools=get_tools(),
    )

    tool_responses_list = []
    if is_tool_calls_required(response):
        for tool_call in response.choices[0].message.tool_calls:
            tool_responses_list.append(
                await call_tool(tool_call.function.name, tool_call.function.arguments)
            )

    if tool_responses_list:
        message_list.append(
            {
                "role": "system",
                "content": str(tool_responses_list),
            }
        )
        response = await client.chat.completions.create(
            model=model,
            messages=message_list,
            tools=get_tools(),
        )

    return response


if __name__ == "__main__":
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    message_list = [
        {
            "role": "system",
            "content": SYSTEM,
        }
    ]
    while True:
        message = input("You: ")
        if message == "exit":
            break
        message_list.append(
            {
                "role": "user",
                "content": message,
            }
        )
        response = asyncio.run(chat_complete(client, message_list))
        msg = response.choices[0].message.content

        message_list.append(
            {
                "role": "assistant",
                "content": msg,
            }
        )

        print(f"Assistant: {msg}")
