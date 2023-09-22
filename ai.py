from transformers import pipeline

# Load the GPT-Neo question-answering pipeline
qa_pipeline = pipeline("question-answering", model="EleutherAI/gpt-neo-1.3B")

# Ask a question and get the answer
context = "GPT-Neo is a transformer-based language model developed by EleutherAI."
question = "What is GPT-Neo?"
answer = qa_pipeline(question=question, context=context)

print(answer)