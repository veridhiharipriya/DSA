from backend.preprocessing import preprocess_text


# ==========================================
# RABIN-KARP FINGERPRINTING
# ==========================================

def rabin_karp_fingerprints(text: str, window_size: int = 5):
    """
    Generate Rabin-Karp rolling-hash fingerprints
    using a fixed-size word window.
    """

    words = text.split()

    if len(words) < window_size:
        return []

    base = 257
    modulus = 1_000_000_007

    fingerprints = []

    # Calculate hash for the first window
    current_hash = 0

    for word in words[:window_size]:
        for character in word:
            current_hash = (
                current_hash * base + ord(character)
            ) % modulus

        current_hash = (
            current_hash * base + 32
        ) % modulus

    fingerprints.append({
        "hash": current_hash,
        "position": 0,
        "text": " ".join(words[:window_size])
    })

    # Generate fingerprints for remaining windows
    for i in range(1, len(words) - window_size + 1):

        window = " ".join(
            words[i:i + window_size]
        )

        window_hash = 0

        for character in window:
            window_hash = (
                window_hash * base + ord(character)
            ) % modulus

        fingerprints.append({
            "hash": window_hash,
            "position": i,
            "text": window
        })

    return fingerprints

# ==========================================
# WINNOWING
# ==========================================

def winnow(fingerprints, window_size: int = 4):
    """
    Select representative fingerprints using
    the winnowing algorithm.
    """

    if not fingerprints:
        return []

    if len(fingerprints) <= window_size:
        return fingerprints

    selected = []
    previous_position = -1

    for i in range(len(fingerprints) - window_size + 1):

        window = fingerprints[
            i:i + window_size
        ]

        # Select the fingerprint with the
        # smallest hash value in this window
        minimum = min(
            window,
            key=lambda fingerprint: fingerprint["hash"]
        )

        # Avoid selecting the same position repeatedly
        if minimum["position"] != previous_position:
            selected.append(minimum)
            previous_position = minimum["position"]

    return selected
# ==========================================
# CANDIDATE MATCHING
# ==========================================

def find_candidate_matches(winnowed1, winnowed2):
    """
    Find matching fingerprint positions between
    two submissions.
    """

    fingerprint_map = {}

    for fingerprint in winnowed1:
        fingerprint_map.setdefault(
            fingerprint["hash"], []
        ).append(fingerprint)

    matches = []

    for fingerprint in winnowed2:
        matching_fingerprints = fingerprint_map.get(
            fingerprint["hash"], []
        )

        for match in matching_fingerprints:
            matches.append({
                "submission_1_position": match["position"],
                "submission_2_position": fingerprint["position"],
                "hash": fingerprint["hash"],
                "text": fingerprint["text"]
            })

    return matches

# ==========================================
# SUFFIX ARRAY
# ==========================================

def build_suffix_array(text: str):
    """
    Build a suffix array for the given text.

    Each suffix is represented by its starting position.
    """

    suffixes = [
        (text[i:], i)
        for i in range(len(text))
    ]

    suffixes.sort()

    return [
        position
        for suffix, position in suffixes
    ]


# ==========================================
# LCP ARRAY
# ==========================================

def build_lcp_array(text: str, suffix_array):
    """
    Build the LCP (Longest Common Prefix) array.

    LCP[i] stores the length of the common prefix
    between suffix_array[i] and suffix_array[i - 1].
    """

    n = len(text)

    if n == 0:
        return []

    rank = [0] * n

    for i, suffix_position in enumerate(suffix_array):
        rank[suffix_position] = i

    lcp = [0] * n

    current_length = 0

    for i in range(n):

        current_rank = rank[i]

        if current_rank == 0:
            continue

        previous_position = suffix_array[current_rank - 1]

        while (
            i + current_length < n
            and previous_position + current_length < n
            and text[i + current_length]
            == text[previous_position + current_length]
        ):
            current_length += 1

        lcp[current_rank] = current_length

        if current_length > 0:
            current_length -= 1

    return lcp


# ==========================================
# COMMON PASSAGE EXTRACTION
# ==========================================
def find_common_passages(text1: str, text2: str, min_length: int = 5):
    """
    Find common passages between two submissions
    using word-level comparison.

    Only the longest non-overlapping matches are kept.
    """

    words1 = text1.split()
    words2 = text2.split()

    matches = []

    for i in range(len(words1)):

        for j in range(len(words2)):

            match_length = 0

            while (
                i + match_length < len(words1)
                and
                j + match_length < len(words2)
                and
                words1[i + match_length]
                == words2[j + match_length]
            ):
                match_length += 1

            if match_length >= min_length:

                matches.append({
                    "start1": i,
                    "start2": j,
                    "length": match_length
                })

    # Longest matches first
    matches.sort(
        key=lambda match: match["length"],
        reverse=True
    )

    selected_matches = []

    used_words1 = set()
    used_words2 = set()

    for match in matches:

        start1 = match["start1"]
        start2 = match["start2"]
        length = match["length"]

        range1 = set(
            range(start1, start1 + length)
        )

        range2 = set(
            range(start2, start2 + length)
        )

        # Skip if this passage overlaps
        # with a longer passage already selected.
        if range1.intersection(used_words1):
            continue

        if range2.intersection(used_words2):
            continue

        selected_matches.append(match)

        used_words1.update(range1)
        used_words2.update(range2)

    common_passages = []

    for match in selected_matches:

        start1 = match["start1"]
        length = match["length"]

        passage_words = words1[
            start1:start1 + length
        ]

        passage_text = " ".join(
            passage_words
        )

        common_passages.append({
            "submission_1_passage": passage_text,
            "submission_2_passage": passage_text,
            "length": length
        })

    return common_passages

# ==========================================
# MAIN PLAGIARISM ANALYSIS
# ==========================================
def analyze_submissions(text1: str, text2: str):
    """
    Analyze two submissions and calculate
    their similarity.
    """

    # -----------------------------
    # STEP 1: Preprocess text
    # -----------------------------

    processed_text1 = preprocess_text(text1)
    processed_text2 = preprocess_text(text2)

    # -----------------------------
    # STEP 2: Rabin-Karp
    # -----------------------------

    fingerprints1 = rabin_karp_fingerprints(
        processed_text1
    )

    fingerprints2 = rabin_karp_fingerprints(
        processed_text2
    )

    # -----------------------------
    # STEP 3: Winnowing
    # -----------------------------

    winnowed1 = winnow(
        fingerprints1
    )

    winnowed2 = winnow(
        fingerprints2
    )

    # -----------------------------
    # STEP 4: Candidate matching
    # -----------------------------

    candidate_matches = find_candidate_matches(
        winnowed1,
        winnowed2
    )

    # -----------------------------
    # STEP 5: Find common passages
    # -----------------------------

    common_passages = find_common_passages(
        processed_text1,
        processed_text2,
        min_length=5
    )

    # -----------------------------
    # STEP 6: Calculate similarity
    # -----------------------------

    words1 = processed_text1.split()
    words2 = processed_text2.split()

    length1 = len(words1)
    length2 = len(words2)

    if length1 == 0 or length2 == 0:

        similarity_percentage = 0.0

    else:

        total_common_words = sum(
            passage["length"]
            for passage in common_passages
        )

        smaller_document_length = min(
            length1,
            length2
        )

        similarity_percentage = (
            total_common_words
            / smaller_document_length
        ) * 100

        similarity_percentage = min(
            similarity_percentage,
            100.0
        )

    # -----------------------------
    # STEP 7: Return result
    # -----------------------------

    return {
        "submission_1": processed_text1,
        "submission_2": processed_text2,

        "fingerprints_1": len(
            fingerprints1
        ),

        "fingerprints_2": len(
            fingerprints2
        ),

        "winnowed_1": len(
            winnowed1
        ),

        "winnowed_2": len(
            winnowed2
        ),

        "common_fingerprints": len(
            candidate_matches
        ),

        "candidate_matches": candidate_matches,

        "similarity_percentage": round(
            similarity_percentage,
            2
        ),

        "common_passages": common_passages
    }