import json
import random

MALLEABLE = (
    "Yes, I am likely to change my mindset if presented with strong counterarguments."
)
UNMALLEABLE = "No, I am not likely to change my mindset if presented with strong counterarguments."

if __name__ == "__main__":
    with open("../cmv_dataset/op_task/train_op_data.jsonlist") as file:
        lines = file.readlines()
        sample_size = 200
        sampled_ops = random.sample(lines, sample_size)
        with open("op_training_data.jsonl", "w") as out:
            for op in sampled_ops:
                op_json = json.loads(op)
                title = op_json["title"]
                op_text = op_json["selftext"]
                delta_label = op_json["delta_label"]
                changed_mind = MALLEABLE if delta_label else UNMALLEABLE
                op_training_json = {
                    "messages": [
                        {
                            "role": "system",
                            "content": f'You are a person who has the following mindset: "{title} {op_text}".',
                        },
                        {
                            "role": "user",
                            "content": "Are you likely to changed your mindset if presented with strong "
                            "counterarguments?",
                        },
                        {
                            "role": "assistant",
                            "content": changed_mind,
                        },
                    ]
                }
                out.write(json.dumps(op_training_json) + "\n")
