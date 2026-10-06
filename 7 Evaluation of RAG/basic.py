import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

# 1. Set your OpenAI API key (used by Ragas to evaluate the data)
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"

# 2. Define your sample RAG data
data = {
    "question": [
        "What is the capital of France?",
        "Who wrote Romeo and Juliet?"
    ],
    "contexts": [
        ["Paris is the capital and most populous city of France."],
        ["William Shakespeare was an English playwright who wrote Romeo and Juliet in the 1590s."]
    ],
    "answer": [
        "The capital of France is Paris.",
        "Romeo and Juliet was written by William Shakespeare."
    ],
    "ground_truth": [
        "Paris is the capital of France.",
        "William Shakespeare wrote Romeo and Juliet."
    ]
}

# 3. Convert your dictionary into a Hugging Face Dataset
dataset = Dataset.from_dict(data)

# 4. Select the evaluation metrics you want to track
metrics = [
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
]

# 5. Run the evaluation
print("Running Ragas evaluation...")
result = evaluate(
    dataset=dataset,
    metrics=metrics
)

# 6. View the final scores
print("\nEvaluation Results:")
print(result)

# Optional: Export the results to a pandas DataFrame for deeper analysis
df = result.to_pandas()
print("\nDetailed DataFrame Preview:")
print(df[['question', 'faithfulness', 'answer_relevancy']])
