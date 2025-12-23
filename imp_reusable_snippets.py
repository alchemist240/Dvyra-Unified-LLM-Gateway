#CASE A
from openai import OpenAI

# The only 4 lines you ever need again:
client = OpenAI(
    api_key="sk-------------", #likh yaha key
    base_url="https://dominator2414-unified-dvyra.hf.space/v1"
)

# Now just code normally:
print(client.chat.completions.create(
    model="llama-8b", # Switch models instantly here!
    messages=[{"role": "user", "content": "Hi"}]
).choices[0].message.content)


#CASE B
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key="sk-------------",          # tera litellm master key
    base_url="https://dominator2414-unified-dvyra.hf.space/v1", # Standard name
    model="deepseek-coder"                        # Standard name
)

# Usage is super clean:
print(llm.invoke("Write a binary search in Python").content)