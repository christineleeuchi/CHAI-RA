from openai import OpenAI
import os

if __name__ == "__main__":
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # Upload OP training data
    response = client.files.create(
        file=open("op_training_data.jsonl", "rb"),  # Path to your JSONL file
        purpose="fine-tune",  # Set the purpose to 'fine-tune'
    )

    print(response)
