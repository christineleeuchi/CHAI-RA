import re

if __name__ == "__main__":
    linguistic_traits = ["valence", "dominance", "intensity", "concreteness"]
    sample_size = 500
    persuasive_argument_quarter_scores = {
        linguistic_trait: [] for linguistic_trait in linguistic_traits
    }
    non_persuasive_argument_quarter_scores = {
        linguistic_trait: [] for linguistic_trait in linguistic_traits
    }
    for i in range(0, sample_size):
        pairs_response_file = open(
            f"pairs_gpt_predictions_and_explanations/heldout_pair_{i}.txt"
        )
        lines = pairs_response_file.readlines()
        linguistic_scores_text = "".join(lines[2:])
        all_scores = re.findall(r"\d+\.\d+", linguistic_scores_text)
        start_of_second_response = linguistic_scores_text.find("Expected no")
        if (
            linguistic_scores_text.find("Summary Scores:") < start_of_second_response
            or linguistic_scores_text.find("Summary of Scores:")
            < start_of_second_response
        ):
            all_scores = all_scores[0:16] + all_scores[32:]
        if len(all_scores) < 32:
            continue
        for index, linguistic_trait in enumerate(linguistic_traits):
            persuasive_argument_quarter_scores[linguistic_trait].append(
                [all_scores[4 * j + index] for j in range(len(linguistic_traits))]
            )
            non_persuasive_argument_quarter_scores[linguistic_trait].append(
                [all_scores[16 + 4 * j + index] for j in range(len(linguistic_traits))]
            )
        pairs_response_file.close()

    for linguistic_trait in linguistic_traits:
        # Write linguistic quarter scores for persuasive arguments
        with open(
            f"pairs_linguistics_scores/{linguistic_trait}/persuasive_quarter_scores.csv",
            "w",
        ) as out:
            out.write("first,second,third,fourth\n")
            for scores in persuasive_argument_quarter_scores[linguistic_trait]:
                out.write(",".join(scores) + "\n")
        # Write linguistic quarter scores for non-persuasive arguments
        with open(
            f"pairs_linguistics_scores/{linguistic_trait}/non_persuasive_quarter_scores.csv",
            "w",
        ) as out:
            out.write("first,second,third,fourth\n")
            for scores in non_persuasive_argument_quarter_scores[linguistic_trait]:
                out.write(",".join(scores) + "\n")
