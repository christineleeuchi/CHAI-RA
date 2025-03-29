from openai import OpenAI
import os

if __name__ == "__main__":
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Fine-tune OP malleability model
    response = client.fine_tuning.jobs.create(
        training_file="file-KeNPVt5D12L2VkcWXZYngC", model="gpt-4o-mini-2024-07-18"
    )

    print(response)
