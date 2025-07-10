from langchain.memory import ConversationBufferMemory

# Create shared memory store (placeholder – wire to Redis/Firestore in production)
def get_memory():
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)