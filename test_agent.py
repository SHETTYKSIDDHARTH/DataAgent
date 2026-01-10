from agent.graph import build_graph

agent = build_graph()

while True:
    question = input(
        "Enter your question (type 'exit' to leave chat mode): "
    ).strip()

    if question.lower() == "exit":
        print("Exiting chat mode.")
        break

    result = agent.invoke({
        "question": question,
        "schema": None,
        "sql": None,
        "validation": None,
        "result": None,
        "answer": None,
        "error": None,
    })

    print("\nANSWER:")
    print(result["answer"])
    print("-" * 50)
