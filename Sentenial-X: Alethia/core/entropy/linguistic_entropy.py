import random


class LinguisticEntropyEngine:
    """
    Applies controlled linguistic instability.
    """

    def apply(self, text: str, entropy_level: float) -> str:
        if entropy_level <= 0:
            return text

        words = text.split()
        swaps = int(len(words) * entropy_level)

        for _ in range(swaps):
            i, j = random.sample(range(len(words)), 2)
            words[i], words[j] = words[j], words[i]

        return " ".join(words)
