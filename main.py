import os
import json
from memory_store import MemoryStore
from dotenv import load_dotenv
from google import genai
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please add it to your .env file.")

client = genai.Client(api_key=api_key)

conversation = []
store = MemoryStore()
store.load()

def update_conversation(conversation, role, content):
    conversation.append({
        "role": role,
        "content": content,
    })

def select_recent_messages(conversation, number_of_messages):
    return conversation[- number_of_messages:]


def extract_memories(user_prompt):
    if user_prompt.strip().endswith("?"):
        return []

    extraction_prompt = f"""
    You are a memory extraction system.

    Identify long-term personal information from the user's message.

    Rules:
    - Extract only information useful in future conversations.
    - Ignore questions, greetings, requests, and general conversation.
    - Split multiple facts into separate atomic memories.
    - Each memory must contain exactly one fact.
    - Assign an integer importance score from 1 to 10.
    - Return only valid JSON.
    - Return [] if nothing should be remembered.

    Required format:

    [
        {{
        "fact": "Lives in Glasgow",
        "importance": 8
        }}
    ]

    User message:
    {user_prompt}      
    """
    try:
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = extraction_prompt,
            config={
                "response_mime_type": "application/json",
            },
            )
        return json.loads(response.text)

    except Exception as error:
        print(f"Memory extraction failed {error}")
        return []



        

#We need these functions to build the prompt
#These functions just format the dictionaries so that we're not passing them directly to gemini


def format_conversations(recent_messages):
    formatted_conversations = "\n".join(f"{message['role']}: {message['content']}"
     for message in recent_messages )
    return  formatted_conversations

def format_memories(relevant_memories):
    formatted_memories = "\n".join(f"- {memory['fact']} (importance: {memory['importance']})"
    for memory in relevant_memories)
    return formatted_memories


def build_prompt(system_prompt, relevant_memories, recent_messages):
    conversation_text = format_conversations(recent_messages)
    memories_text = format_memories(relevant_memories)
    
    prompt = f"""

    System prompt:
    {system_prompt}

    Recent conversations:
    {conversation_text}

    Relevant memories:
    {memories_text}
    """

    return prompt



def get_response(prompt):
    try:
        response = client.models.generate_content(model = "gemini-2.5-flash", contents = prompt)
        return(response.text)

    except  Exception as error:
        print("Gemini 2.5 Flash failed. Trying fallback model...")
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        return response.text
   


#invoking all the function
def main():
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() == "quit":
            break

        system_prompt = """
        You are the smartest AI engineering tutor and AI engineering expert in the world.

        Use the relevant memories provided in the prompt when they help answer the user's question.
        Treat those memories as known facts about the user.
        Do not say you lack memory when a relevant memory is provided. 
        """
        update_conversation(conversation, "user", user_prompt)
        recent_messages = select_recent_messages(conversation, 10)
    
        extracted_memories = extract_memories(user_prompt)
    
        for memory in extracted_memories:
            if (
            isinstance(memory, dict)
            and isinstance(memory.get("fact"), str)
            and isinstance(memory.get("importance"), int)
            and 1 <= memory["importance"] <= 10):
        
                store.add_memory(
                memory["fact"], 
                memory["importance"]
            )
        store.save()

        relevant_memories = store.search(user_prompt,k=3)
        prompt = build_prompt(system_prompt, relevant_memories, recent_messages)
        print("\n========== PROMPT ==========")
        print(prompt)
        print("============================\n")
        ai_response = get_response(prompt)
        print(ai_response)
        update_conversation(conversation, "assistant", ai_response)

if __name__ == "__main__":
    main()
            




