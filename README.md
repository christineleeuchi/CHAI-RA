# Introduction
I will be replicating the experiment and analysis of persuasive argument prediction from the Reddit ChangeMyMind subreddit based on the findings of Chenhao Tan's work: https://chenhaot.com/papers/changemyview.html.

# Set-up
Download the cmv dataset from the website linked above.\
Parse the persuasive pairs and OP data into .jsonl training files that we will use to train our GPT models.\
Upload training files through OpenAI API.\
Fine-tune GPT-4o-mini models to identity if counterarguments are persuasive and if OP's beliefs are malleable.\
Run the GPT models against heldout test data.\
Parse GPT predictions of test data and graph quarterly linguistic scores.

