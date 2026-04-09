from datasets import load_dataset

# FIX THIS IMPORT BASED ON YOUR STRUCTURE
from src.minimal_agent.agent import Agent   # we'll adjust if needed


def run_agent(question):
    agent = Agent()
    return agent.run(question)


def evaluate():
    print("Loading dataset...")
    data = load_dataset("gsm8k", split="test").select(range(20))

    correct = 0

    for i, item in enumerate(data):
        q = item["question"]
        gt = item["answer"]

        pred = run_agent(q)

        is_correct = str(gt).strip() in str(pred)

        print(f"\nQ{i+1}")
        print("Q:", q)
        print("Pred:", pred)
        print("GT:", gt)
        print("Correct:", is_correct)

        if is_correct:
            correct += 1

    print("\nFINAL ACCURACY:", correct / len(data))


if __name__ == "__main__":
    evaluate()
