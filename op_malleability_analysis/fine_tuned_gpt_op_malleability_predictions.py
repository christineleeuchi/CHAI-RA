from openai import OpenAI
import os
import json
import random

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def predict_and_explain(title, op_text):
    prediction = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::BG4r7eCl",
        messages=[
            {
                "role": "system",
                "content": f'You are a person who has the following mindset: "{title} {op_text}"',
            },
            {
                "role": "user",
                "content": "Are you likely to changed your mindset if presented with strong counterarguments?",
            },
        ],
    )
    prediction_response = prediction.choices[0].message.content

    explanation = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": f'You are a person who has the following mindset: "{title} {op_text}"',
            },
            {
                "role": "user",
                "content": f"Give a rating score from 0.0 to 1.0 for each of the following: valence, dominance, "
                f'intensity, and concreteness of the following argument "{title} {op_text}" for each quarter '
                f"of the argument's text",
            },
        ],
    )
    explanation_response = explanation.choices[0].message.content
    return prediction_response, explanation_response


if __name__ == "__main__":
    with open("../cmv_dataset/op_task/heldout_op_data.jsonlist") as file:
        lines = file.readlines()
        sample_size = 500
        test_op_lines = random.sample(lines, sample_size)
        for i in range(0, len(test_op_lines)):
            print(f"Predicting OP {i} ...")
            test_op_line = test_op_lines[i]
            op_json = json.loads(test_op_line)
            post_title = op_json["title"]
            post_text = op_json["selftext"]
            expected_malleability = (
                "Expected yes, likely to change mind."
                if op_json["delta_label"]
                else "Expected no, unlikely to change mind."
            )
            gpt_response, gpt_explanation = predict_and_explain(post_title, post_text)
            with open(
                f"op_gpt_predictions_and_explanations/heldout_op_{i}.txt", "w"
            ) as out:
                out.write(
                    f"{expected_malleability} GPT responded: {gpt_response}\n{gpt_explanation}\n\n"
                )
            print(f"Finished predicting OP {i}")
