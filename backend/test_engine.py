from backend.plagiarism_engine import analyze_submissions


submission_1 = """
Python is a popular programming language.
It is widely used for web development and data science.
Students use Python to build applications and solve problems.
"""


submission_2 = """
Python is a popular programming language.
It is widely used for web development and machine learning.
Students use Python to build applications and solve problems.
"""


result = analyze_submissions(
    submission_1,
    submission_2
)


print("\n========== VERITEXT ENGINE TEST ==========\n")

print(
    "Similarity:",
    result["similarity_percentage"],
    "%"
)

print(
    "Submission 1 Fingerprints:",
    result["fingerprints_1"]
)

print(
    "Submission 2 Fingerprints:",
    result["fingerprints_2"]
)

print(
    "Submission 1 Winnowed:",
    result["winnowed_1"]
)

print(
    "Submission 2 Winnowed:",
    result["winnowed_2"]
)

print(
    "Common Fingerprints:",
    result["common_fingerprints"]
)

print("\n========== COMMON PASSAGES ==========\n")

for passage in result["common_passages"]:
    print(
        "Passage:",
        passage["submission_1_passage"]
    )

    print(
        "Length:",
        passage["length"]
    )

    print("--------------------------------------")

print("\n========================================\n")