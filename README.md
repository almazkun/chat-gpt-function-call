# chat-gpt-function-call

Quick example on how to use OpenAI Function Call API with ChatGPT. https://platform.openai.com/docs/assistants/tools/function-calling

## Setup
1. Provide your OpenAI API key in the `.env` file.
    ```bash
    cp '.env copy' .env
    ```

1. Activate the virtual environment.
    ```bash
    pipenv install
    pipenv shell
    ```

1. Run the script.
    ```bash
    python main.py
    ```

## Example
```bash
python main.py
You: hi!
Assistant: Hello! To assist you, please provide me with your session ID.
You: e901e9102ej091d21ndnnd1n2d
Assistant: Order 2: Status - Shipped
Order 3: Status - Cancelled
You:
```