from minimal_agent.agent import Agent


# 🔥 Dummy model (no API required)
def dummy_model(prompt):
    # super basic response
    return "42"


def run_agent(question):
    agent = Agent(
        model=dummy_model,
        tools=[]  # no tools for baseline
    )

    return agent.run(question)


# Optional test
if __name__ == "__main__":
    q = "What is 25 * 17?"
    print(run_agent(q))