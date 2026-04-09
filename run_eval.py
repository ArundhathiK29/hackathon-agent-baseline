from datasets import load_dataset


# 🔥 SIMPLE BASELINE AGENT (no LLM, no dependencies)
def run_agent(question):
    return "42"   # dumb baseline


def evaluate():
    print("Loading dataset...")

    # ✅ FIXED GSM8K
    data = load_dataset("gsm8k", "main", split="test").select(range(20))

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