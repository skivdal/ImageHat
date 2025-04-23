# Let's implement the EXIF Conformity Score (ECS) formula and all its components in a reusable Python module.
import math

# Constants for tag support levels
SUPPORT_LEVEL_WEIGHTS = {"M": 1.0, "R": 0.6, "O": 0.3}
PENALTY_SCALE = {
    "M": lambda present, struct: 0 if not present else (1 - struct) * 1.0,
    "R": lambda present, struct: 0.5 if not present else (1 - struct) * 0.5,
    "O": lambda present, struct: 0,
    "N": lambda present, struct: 1 if present else 0,
    "J": lambda present, struct: 1 if present else 0,
    "U": lambda present, struct: 0.4 if not present else 0,
}

def get_baseline_order(tag_dict: dict) -> list[bytes]:
    """
    Sorts tag bytes to create a baseline order from a reversed tag dictionary.
    """
    return sorted(tag_dict.keys())

def calculate_header_validity(e: int, t: int, b: int) -> float:
    return 0.4 * e + 0.4 * t + 0.2 * b


def calculate_tag_validity_score(tags: list[dict]) -> float:
    N = len(tags)
    if N == 0:
        return
    penalties = []
    for tag in tags:
        type_correct = tag.get("type_valid", False)
        count_correct = tag.get("count_valid", False)
        struct_i = (int(type_correct) + int(count_correct)) / 2
        present_i = tag.get("present", False)
        support = tag.get("support_level", "O")
        penalty_func = PENALTY_SCALE.get(support, lambda present, struct: 0)
        penalty = penalty_func(present_i, struct_i)
        penalties.append(penalty)
    return 1 - sum(penalties) / N


# def calculate_tag_richness_score(tags: List[Dict]) -> float:
#     count_by_level = {"M": 0, "R": 0, "O": 0}
#     present_by_level = {"M": 0, "R": 0, "O": 0}
#     for tag in tags:
#         support = tag.get("support_level", "O")
#         present = tag.get("present", False)
#         if support in count_by_level:
#             count_by_level[support] += 1
#             if present:
#                 present_by_level[support] += 1

#     numerator = 0
#     denominator = sum(SUPPORT_LEVEL_WEIGHTS.values())
#     for level in SUPPORT_LEVEL_WEIGHTS:
#         N_x = count_by_level[level]
#         P_x = present_by_level[level]
#         w = SUPPORT_LEVEL_WEIGHTS[level]
#         richness = (P_x / N_x) if N_x > 0 else 0
#         numerator += w * richness
#     normalized_score = numerator / denominator
#     return normalized_score, numerator


def kendall_tau_distance(order: list[int]) -> float:
    n = len(order)
    total_pairs = n * (n - 1) / 2
    if total_pairs == 0:
        return 1.0
    inversions = sum(
        1 for i in range(n) for j in range(i + 1, n) if order[i] > order[j]
    )
    return 1 - inversions / total_pairs


def calculate_s_TOS(all_tags: list[int], baseline: list[bytes]) -> float:
    observed_order = [
        tag["tag_id"] for tag in sorted(all_tags, key=lambda x: x.get("order", 0))
        if tag.get("tag_id") in baseline
    ]

    baseline_filtered = [tag for tag in baseline if tag in observed_order]

    tag_to_index = {tag: i for i, tag in enumerate(baseline_filtered)}
    indexed_order = [tag_to_index[tag] for tag in observed_order if tag in tag_to_index]

    return kendall_tau_distance(indexed_order)


def calculate_w_TOS(observed: list[int], baseline: list[dict]) -> float:
    overlap = [tag for tag in observed if tag in baseline]
    if not overlap:
        return 0.0
    L = len(baseline)
    Z = len(overlap)
    distance_sum = sum(
        abs(observed.index(tag) - baseline.index(tag)) for tag in overlap
    )
    return 1 - (distance_sum / (Z * L)) if Z * L > 0 else 0.0


def calculate_ECS(header_score: float, tvs: float, tos: float) -> float:
    return 0.3 * header_score + 0.3 * tvs + 0.4 * tos

