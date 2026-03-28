"""
Helper function for managing chat
"""

from numpy import append
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def get_system_prompt(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    system_prompt_path = "./system-prompt.txt"
    with open(system_prompt_path) as f:
        system_prompt = f.read()
    messages.append(
        {
            "role": "system",
            "content": system_prompt,
        }
    )
    return messages


def stream_model_response(
    messages: list[dict[str, str]], write_funct=print, model="gpt-4o"
) -> list[dict[str, str]]:
    # only include 'role' and 'content' for each message
    messages_filtered = [
        {"role": message["role"], "content": message["content"]} for message in messages
    ]
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    response = write_funct(stream)
    messages.append({"role": "assistant", "content": response})
    return messages
