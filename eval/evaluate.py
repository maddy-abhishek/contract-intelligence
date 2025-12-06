import requests
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Setup Gemini as the "Judge"
judge_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key="YOUR_GOOGLE_API_KEY_HERE" # Hardcode or use os.getenv
)

API_URL = "http://localhost:8000/ask"

def evaluate():
    # 1. Load the Exam Questions
    with open("eval/qa_set.json", "r") as f:
        qa_pairs = json.load(f)

    total_score = 0
    
    print(f"Starting Evaluation on {len(qa_pairs)} questions...\n")

    for item in qa_pairs:
        question = item["question"]
        truth = item["ground_truth"]

        # 2. Ask YOUR System
        try:
            response = requests.post(API_URL, json={"question": question})
            response_data = response.json()
            predicted_answer = response_data.get("answer", "Error")
        except Exception as e:
            predicted_answer = f"System Error: {str(e)}"

        # 3. Ask the Judge to Grade it
        grading_prompt = f"""
        You are a strict teacher grading an exam.
        Question: {question}
        Correct Answer: {truth}
        Student Answer: {predicted_answer}

        Grade the Student Answer on a scale of 1 to 5 based on accuracy.
        Output ONLY the number (e.g., 4).
        """
        
        score_response = judge_llm.invoke(grading_prompt)
        try:
            score = int(score_response.content.strip())
        except:
            score = 1 # Fallback if LLM outputs text

        print(f"Q: {question}")
        print(f"Pred: {predicted_answer}")
        print(f"True: {truth}")
        print(f"Score: {score}/5\n")
        print("-" * 30)
        
        total_score += score

    # 4. Final Summary
    avg_score = total_score / len(qa_pairs)
    print(f"FINAL SCORE SUMMARY: {avg_score:.2f} / 5.0")

if __name__ == "__main__":
    evaluate()