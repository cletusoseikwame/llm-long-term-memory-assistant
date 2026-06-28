import os
from dotenv import load_dotenv
from google import genai
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please add it to your .env file.")

client = genai.Client(api_key=api_key)

conversation = []
memory_database = []

def update_conversation(conversation, role, content):
    conversation.append({
        "role": role,
        "content": content,
    })

    return conversation

def select_recent_messages(conversation, number_of_messages):
    return conversation[- number_of_messages:]

def extract_facts(messages):
    extracted_facts =[]
    for message in messages:
        if message["role"]=="user":
            extracted_facts.append({
                "fact":message["content"]
            })
    return extracted_facts



def rate_importance(facts):
    rated_importance =[]
    for fact in facts:
        rated_importance.append({
            "fact":fact["fact"],
            "importance": 5,
        })
    return rated_importance

def store_memory(memory_database, rated_facts):
    for fact in rated_facts:
        Found = False

        for memory in memory_database:
            if memory["fact"]==fact["fact"]:
                Found = True

        if not Found:
            memory_database.append(fact)
    return memory_database
        
#keyword extractor
#It also removes stopwords
def extract_keywords(user_prompt):
    stop_words = ["a", "an", "the","is","are","you","my","for","to","can"]
    keywords = []

    for word in user_prompt.lower().split():
        word = word.replace(".","")
        word = word.replace(",","")
        word = word.replace("?","")
        word = word.replace("!","")
        if word not in stop_words:
            keywords.append(word)


    return keywords


def search_memory(memory_database, keywords):
    relevant_memories = []
    for memory in memory_database:
        for keyword in keywords:
            if keyword.lower() in memory["fact"].lower():
                relevant_memories.append(memory)
                break
    return relevant_memories



#We need these functions to build the prompt
#These functions just format the dictionaries so that we're not passing them directly to gemini


def format_conversations(recent_messages):
    formated_conversations = "\n".join(f"{message['role']}: {message['content']}"
     for message in recent_messages )
    return  formated_conversations

def format_memories(relevant_memories):
    formated_memories = "\n".join(f"- {memory['fact']}(importance:{memory['importance']})"
    for memory in relevant_memories)
    return formated_memories


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

while True:
    user_prompt = input("You: ")
    if user_prompt.lower() == "quit":
        break

    system_prompt = "You are the smartest AI engineering tutor and AI engineering expert in the world"
    conversation = update_conversation(conversation, "user", user_prompt)
    recent_messages = select_recent_messages(conversation, 10)
    facts = extract_facts(recent_messages)
    important_facts = rate_importance(facts) 
    memory_database = store_memory(memory_database, important_facts)
    extracted_keywords = extract_keywords(user_prompt)
    relevant_memories = search_memory(memory_database, extracted_keywords)
    prompt = build_prompt(system_prompt, relevant_memories, recent_messages)
    
    ai_response = get_response(prompt)
    print(ai_response)
    conversation = update_conversation(conversation, "assistant", ai_response)

            




