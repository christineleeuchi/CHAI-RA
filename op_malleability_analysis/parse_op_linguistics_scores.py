import re

if __name__ == "__main__":
    linguistic_traits = ["valence", "dominance", "intensity", "concreteness"]
    sample_size = 500
    malleable_op_quarter_scores = {
        linguistic_trait: [] for linguistic_trait in linguistic_traits
    }
    non_malleable_op_quarter_scores = {
        linguistic_trait: [] for linguistic_trait in linguistic_traits
    }
    for i in range(0, sample_size):
        op_response_file = open(
            f"op_gpt_predictions_and_explanations/heldout_op_{i}.txt"
        )
        lines = op_response_file.readlines()
        linguistic_scores_text = "".join(lines[2:])
        all_scores = re.findall(r"0\.\d+|0\.0\b|1\.0\b", linguistic_scores_text)
        if len(all_scores) < 16:
            continue
        if "Expected yes" in lines[0]:
            for index, linguistic_trait in enumerate(linguistic_traits):
                malleable_op_quarter_scores[linguistic_trait].append(
                    [all_scores[4 * j + index] for j in range(len(linguistic_traits))]
                )
        elif "Expected no" in lines[0]:
            for index, linguistic_trait in enumerate(linguistic_traits):
                non_malleable_op_quarter_scores[linguistic_trait].append(
                    [all_scores[4 * j + index] for j in range(len(linguistic_traits))]
                )
        op_response_file.close()

    for linguistic_trait in linguistic_traits:
        # Write linguistic quarter scores for malleable op mindsets
        with open(
            f"op_linguistics_scores/{linguistic_trait}/malleable_quarter_scores.csv",
            "w",
        ) as out:
            out.write("first,second,third,fourth\n")
            for scores in malleable_op_quarter_scores[linguistic_trait]:
                out.write(",".join(scores) + "\n")
        # Write linguistic quarter scores for non-malleable op mindsets
        with open(
            f"op_linguistics_scores/{linguistic_trait}/non_malleable_quarter_scores.csv",
            "w",
        ) as out:
            out.write("first,second,third,fourth\n")
            for scores in non_malleable_op_quarter_scores[linguistic_trait]:
                out.write(",".join(scores) + "\n")
