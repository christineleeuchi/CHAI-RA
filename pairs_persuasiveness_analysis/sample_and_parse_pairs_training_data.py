import json
import random

if __name__ == "__main__":
    with open("../cmv_dataset/pair_task/train_pair_data.jsonlist") as file:
        lines = file.readlines()
        sample_size = 200
        sampled_pairs = random.sample(lines, sample_size)
        with open("pairs_training_data.jsonl", "w") as out:
            for pair in sampled_pairs:
                pair_json = json.loads(pair)
                op_text = pair_json["op_text"]
                positive_reply = pair_json["positive"]["comments"][0]["body"]
                negative_reply = pair_json["negative"]["comments"][0]["body"]
                positive_training_json = {
                    "messages": [
                        {
                            "role": "system",
                            "content": f'You are a person who has the following mindset: "{op_text}".',
                        },
                        {
                            "role": "user",
                            "content": f'Does the following counterargument change your mind?: "{positive_reply}"',
                        },
                        {
                            "role": "assistant",
                            "content": "Yes, the provided counterargument changes my mind",
                        },
                    ]
                }
                negative_training_json = {
                    "messages": [
                        {
                            "role": "system",
                            "content": f'You are a person who has the following mindset: "{op_text}".',
                        },
                        {
                            "role": "user",
                            "content": f'Does the following counterargument change your mind?: "{negative_reply}"',
                        },
                        {
                            "role": "assistant",
                            "content": "No, the provided counterargument does not change my mind",
                        },
                    ]
                }
                out.write(json.dumps(positive_training_json) + "\n")
                out.write(json.dumps(negative_training_json) + "\n")
