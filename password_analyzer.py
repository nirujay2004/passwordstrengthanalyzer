import math, re
from typing import List, Tuple, Optional

def calculate_password_strength(password: str) -> float:
    """Advanced password strength calculation with enhanced entropy estimation."""
    if not password:
        return 0.0

    length = len(password)
    character_set_sizes: List[int] = []
    character_checks: List[Tuple[callable, int]] = [
        (str.isupper, 26),
        (str.islower, 26),
        (str.isdigit, 10),
        (lambda c: not c.isalnum(), 32),
    ]

    character_set_sizes = [
        size for check, size in character_checks 
        if any(check(c) for c in password)
    ]

    char_set_size = sum(character_set_sizes)
    entropy = length * math.log2(char_set_size) if char_set_size else 0

    pattern_checks = [
        (r"(.)\1{2,}", 15),     # Repeating chars
        (r"123|abc|qwe|asdf", 15),  # Simple sequences
        (r"(?:qwerty|asdfgh)", 15),  # Keyboard patterns
        (r"(.)\1\1", 10),        # Three same chars
        (r"(..)\1", 10)          # Repeating pairs
    ]

    for pattern, penalty in pattern_checks:
        if re.search(pattern, password, re.IGNORECASE):
            entropy = max(0, entropy - penalty)

    return max(0, entropy * 0.7)

def get_password_rating(strength):
    """Rates password strength based on the calculated score."""

    ratings = [
        (30, "Very Weak"),
        (40, "Weak"),
        (50, "Moderate"),
        (60, "Strong"),
        (float('inf'), "Very Strong"),
    ]

    for threshold, rating in ratings:
        if strength < threshold:
            return rating

def format_crack_time(seconds):
    """Formats crack time into a human-readable string."""

    units = [
        (31536000, "years"),
        (86400, "days"),
        (3600, "hours"),
        (60, "minutes"),
        (1, "seconds"),
        (0.001, "milliseconds"),
    ]

    for unit_seconds, unit_name in units:
        if seconds >= unit_seconds:
            return f"{seconds / unit_seconds:.2f} {unit_name}"

def calculate_crack_time(entropy, guesses_per_second):
    """Calculates the estimated crack time based on entropy."""

    if entropy <= 0 or guesses_per_second <= 0:
        return "Infinite"  # Indicate infinite time for invalid input.

    possible_combinations = 2**entropy #calculate combinations.
    crack_time_seconds = possible_combinations / guesses_per_second
    return format_crack_time(crack_time_seconds)

def check_password(password, guesses_per_second=100000000):
    """Checks password strength, rating, estimated crack time, and provides feedback."""

    strength = calculate_password_strength(password)
    rating = get_password_rating(strength)
    crack_time = calculate_crack_time(strength, guesses_per_second)

    print(f"Password: {password}")
    print(f"Password Strength (Entropy): {strength:.2f} bits")
    print(f"Password Rating: {rating}")
    print(f"Estimated Crack Time: {crack_time}")

    if strength < 40:
        print("Weak password. Suggestions:")
        if len(password) < 8:
            print("- Increase password length (at least 8 characters).")
        if not re.search(r"[A-Z]", password):
            print("- Add uppercase letters.")
        if not re.search(r"[a-z]", password):
            print("- Add lowercase letters.")
        if not re.search(r"\d", password):
            print("- Add digits.")
        if not re.search(r"[^a-zA-Z0-9]", password):
            print("- Add special characters.")
        if re.search(r"(.)\1{2,}", password) or re.search(r"123|abc|qwe|asdf|zyx|cba|fed", password, re.IGNORECASE) or re.search(r"(?:qwerty|asdfgh|zxcvbn)", password, re.IGNORECASE):
            print("- Avoid common patterns or sequences.")

    char_sets = []
    if re.search(r"[A-Z]", password):
        char_sets.append("Uppercase")
    if re.search(r"[a-z]", password):
        char_sets.append("Lowercase")
    if re.search(r"\d", password):
        char_sets.append("Digits")
    if re.search(r"[^a-zA-Z0-9]", password):
        char_sets.append("Special")

    if char_sets:
        print(f"Character Sets Used: {', '.join(char_sets)}\n")

# Example password checks
check_password('slimjim')
check_password('slimjim1234')
check_password('SlimJim1234!')
check_password('Q2i73-<A¤ll&')
check_password('ji"XWJp¤wGxD%Nv')
