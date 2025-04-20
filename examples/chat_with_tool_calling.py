from ollama import ChatResponse, chat

from main import LlmTooling


def main():
    # Initialize tooling
    LlmTooling.init()

    available_tools = LlmTooling.get_all_tools_as_callable()

    llm_model = "llama3.2:3b"

    messages = []

    while True:
        user_input = input('Chat with history :>> ')
        response: ChatResponse = chat(
            model=llm_model,
            messages=messages
                     + [
                         {'role': 'user', 'content': user_input},
                     ],
            tools=available_tools
        )
        # print(f"Q: {user_input}")
        # print(f"R: {response} \n")

        followup = LlmTooling.parse_and_call_tool_if_available(response)

        if followup and len(followup) != 0:
            for x in followup:
                messages.append(x)

            # Send back tool result to LLM
            response: ChatResponse = chat(
                model=llm_model,
                messages=messages,
                tools=available_tools  # <- directly passing the callable
            )

            #print(response['message']['content'])

        # Add the response to the messages to maintain the history
        messages += [
            {'role': 'user', 'content': user_input},
            {'role': 'assistant', 'content': response.message.content},
        ]

        print(response.message.content + '\n')


if __name__ == '__main__':
    main()
