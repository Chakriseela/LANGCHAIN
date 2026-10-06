import os
from datasets import Dataset
import google.generativeai as genai
from ragas import evaluate
from ragas.llms import llm_factory
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

# 1. Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key-here"

# Configure the Gemini client
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
# Using gemini-2.0-flash as the evaluator LLM
gemini_client = genai.GenerativeModel("gemini-2.0-flash")

# Wrap the model for Ragas
evaluator_llm = llm_factory("gemini-2.0-flash", provider="google", client=gemini_client)

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

# 4. Explicitly assign the Gemini evaluator to the metrics
metrics = [
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
]

# 5. Run the evaluation passing the dataset and metrics
print("Running Ragas evaluation with Gemini...")
result = evaluate(
    dataset=dataset,
    metrics=metrics,
    llm=evaluator_llm  # Pass Gemini as the evaluating LLM
)

# 6. View the final scores
print("\nEvaluation Results:")
print(result)

# Export the results to a pandas DataFrame
df = result.to_pandas()
print("\nDetailed DataFrame Preview:")
print(df[['question', 'faithfulness', 'answer_relevancy']])
