from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = '''
Answer the questions below.

Here is the conversation history : {context}

Question: {question}

Answer:


'''

model = OllamaLLM(model='llama3.2')
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def handle_conversation():
    context=''
    print("Welcome")
    while True:
        question = input("You: ")
        if question.lower() == 'quit':
            break

        result = chain.invoke({"context": "context", "question" : question})
        print("Model:",result)
        context += f"\nUser:{question}\nAI:{result}"


if __name__== "__main__":
    handle_conversation()