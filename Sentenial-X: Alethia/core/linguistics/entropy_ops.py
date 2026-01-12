import random

def apply_entropy(text: str, level: float) -> str:
    """
    Randomly shuffle words based on entropy level to degrade semantic coherence.
    """
    words = text.split()
    n_swaps = max(1, int(len(words) * level))

    for _ in range(n_swaps):
        i, j = random.sample(range(len(words)), 2)
        words[i], words[j] = words[j], words[i]

    return " ".join(words)
