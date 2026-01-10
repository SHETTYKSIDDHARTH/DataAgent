from agent.llm import llm

response = llm.invoke("Say hello in one word")
print(response.content)
