from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = '''
Answer the questions below precisely and with reasoning. Use the following personality: {personality}.

Here is the conversation history : {context}

Question: {question}

Answer:


'''

model = OllamaLLM(model='llama3.2')
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ''
    personality = "smart"  # Default personality

    print("Welcome! Choose the personality of the bot (funny, sarcastic, genz, smart):")
    while True:
        chosen_personality = input("Personality (or press Enter to keep 'smart'): ").lower()
        if chosen_personality in ['funny', 'sarcastic', 'genz', 'smart']:
            personality = chosen_personality
            print(f"Personality set to {personality}!")
        elif chosen_personality and chosen_personality not in ['funny', 'sarcastic', 'genz', 'smart']:
            print("Invalid choice. Please choose from funny, sarcastic, genz, or smart.")

        print("Ask a question or type 'quit' to exit.")
        question = input("You: ")
        if question.lower() == 'quit':
            break

        # Pass the chosen personality to the model
        result = chain.invoke({"context": context, "question": question, "personality": personality})
        print("Model:", result)

        # Update the context
        context += f"\nUser: {question}\nAI ({personality}): {result}"

        # Save the conversation to a log file
        with open("conversation_log.txt", "a") as log:
            log.write(f"User: {question}\nAI ({personality}): {result}\n")

if __name__ == "__main__":
    handle_conversation()