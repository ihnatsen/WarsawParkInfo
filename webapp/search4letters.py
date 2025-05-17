def search_for_letter(sequence: str, letters='aeiou') -> set:
    return set(letters).intersection(set(sequence))
