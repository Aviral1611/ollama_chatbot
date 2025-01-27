from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import tkinter as tk
from tkinter import scrolledtext

template = '''
Answer the questions below precisely and with reasoning. Use the following personality: {personality}.

Here is the conversation history : {context}

Question: {question}

Answer:


'''

model = OllamaLLM(model='llama3.2')
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def chatbot_app():
    # Initialize variables
    context = ''
    personality = "smart"  # Default personality

    def send_question():
        nonlocal context, personality

        question = question_entry.get()
        if not question.strip():
            return

        # Clear the input field
        question_entry.delete(0, tk.END)

        if question.lower() == 'quit':
            app.destroy()
            return

        # Get response from the model
        result = chain.invoke({"context": context, "question": question, "personality": personality})

        # Update the chat history
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"You: {question}\n")
        chat_history.insert(tk.END, f"AI ({personality}): {result}\n\n")
        chat_history.config(state=tk.DISABLED)
        chat_history.see(tk.END)

        # Update the context
        context += f"\nUser: {question}\nAI ({personality}): {result}"

        # Log the conversation
        with open("conversation_log.txt", "a") as log:
            log.write(f"User: {question}\nAI ({personality}): {result}\n")

    def set_personality(p):
        nonlocal personality
        personality = p
        personality_label.config(text=f"Personality: {personality.capitalize()}")

    # Initialize the app
    app = tk.Tk()
    app.title("Chatbot App")
    app.configure(bg="black")

    # Chat history display
    chat_history = scrolledtext.ScrolledText(app, state=tk.DISABLED, wrap=tk.WORD, width=60, height=20, bg="black", fg="white")
    chat_history.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    # Personality selection
    personality_label = tk.Label(app, text=f"Personality: {personality.capitalize()}", bg="black", fg="white")
    personality_label.grid(row=1, column=0, padx=10, pady=5)

    tk.Button(app, text="Funny", command=lambda: set_personality("funny"), bg="gray", fg="white").grid(row=1, column=1, padx=5, pady=5)
    tk.Button(app, text="Sarcastic", command=lambda: set_personality("sarcastic"), bg="gray", fg="white").grid(row=1, column=2, padx=5, pady=5)
    tk.Button(app, text="Gen Z", command=lambda: set_personality("genz"), bg="gray", fg="white").grid(row=1, column=3, padx=5, pady=5)
    tk.Button(app, text="Smart", command=lambda: set_personality("smart"), bg="gray", fg="white").grid(row=1, column=4, padx=5, pady=5)

    # Question entry
    question_entry = tk.Entry(app, width=50, bg="black", fg="white", insertbackground="white")
    question_entry.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    # Send button
    send_button = tk.Button(app, text="Send", command=send_question, bg="gray", fg="white")
    send_button.grid(row=2, column=3, padx=10, pady=10)

    # Run the app
    app.mainloop()

if __name__ == "__main__":
    chatbot_app()
