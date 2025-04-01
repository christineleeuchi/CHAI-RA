from openai import OpenAI
import os
import json
import random

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def predict_and_explain(op_mindset, counterargument):
    prediction = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::BGHgrQnY",
        messages=[
            {
                "role": "system",
                "content": f'You are a person who has the following mindset: "{op_mindset}"',
            },
            {
                "role": "user",
                "content": f'Does the following counterargument change your mind?: "{counterargument}"',
            },
        ],
    )
    prediction_response = prediction.choices[0].message.content

    explanation = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": f'You are a person who has the following mindset: "{op_mindset}"',
            },
            {
                "role": "user",
                "content": f"Give a rating score from 0.0 to 1.0 for each of the following: valence, dominance, "
                f"intensity, and concreteness of the following argument {counterargument} for each quarter "
                f"of the argument's text",
            },
        ],
    )
    explanation_response = explanation.choices[0].message.content
    return prediction_response, explanation_response


if __name__ == "__main__":
    with open("../cmv_dataset/pair_task/heldout_pair_data.jsonlist") as file:
        lines = file.readlines()
        sample_size = 500
        test_pairs_lines = random.sample(lines, sample_size)
        for i in range(0, len(test_pairs_lines)):
            print(f"Predicting pair {i} ...")
            test_pair_line = test_pairs_lines[i]
            pair_json = json.loads(test_pair_line)
            op_text = pair_json["op_text"]
            positive_reply = pair_json["positive"]["comments"][0]["body"]
            negative_reply = pair_json["negative"]["comments"][0]["body"]
            positive_response, positive_explanation = predict_and_explain(
                op_text, positive_reply
            )
            negative_response, negative_explanation = predict_and_explain(
                op_text, negative_reply
            )
            with open(
                f"pairs_gpt_predictions_and_explanations/heldout_pair_{i}.txt", "w"
            ) as out:
                out.write(
                    f"Expected yes, changed mind. GPT responded: {positive_response}\n{positive_explanation}\n\n"
                )
                out.write(
                    f"Expected no, did not change mind. GPT responded: {negative_response}\n{negative_explanation}\n\n"
                )
            print(f"Finished predicting pair {i}")
