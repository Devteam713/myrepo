import random

def apply_entropy(text: str, level: float) -> str:
    words = text.split()
    swaps = int(len(words) * level)

    for _ in range(swaps):
        i, j = random.sample(range(len(words)), 2)
        words[i], words[j] = words[j], words[i]

    return " ".join(words)
