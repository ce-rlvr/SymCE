import math
from sympy import Integer, ZZ, QQ

# Top-level setup for standard objects
Z = 'Z'

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should represent a ring R, a list of ideals, and a list of elements.
    For simplicity and standard counterexamples, we support R = Z.
    Witness formats accepted:
      - (ring, ideals, elements)
      - (ideals, elements)  # implicitly assumes ring is Z
      - {'ring': 'Z', 'ideals': [...], 'elements': [...]}
    """
    # Parse witness
    try:
        if hasattr(witness, 'ring') and hasattr(witness, 'ideals') and hasattr(witness, 'elements'):
            ring = witness.ring
            ideals = witness.ideals
            elements = witness.elements
        elif isinstance(witness, dict):
            ring = witness.get('ring', 'Z')
            ideals = witness.get('ideals', [])
            elements = witness.get('elements', [])
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                ring, ideals, elements = witness
            elif len(witness) == 2:
                ring = 'Z'
                ideals, elements = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a ring with identity
    try:
        h1 = ring in ['Z', ZZ, 'ZZ']
    except Exception:
        h1 = False

    # H_2: I_1, I_2, ..., I_n are ideals of R
    try:
        parsed_ideals = []
        for I in ideals:
            if isinstance(I, (int, Integer)):
                parsed_ideals.append(int(I))
            elif isinstance(I, (list, tuple)) and len(I) == 1 and isinstance(I[0], (int, Integer)):
                # Accept principal ideal generators wrapped in a tuple/list
                parsed_ideals.append(int(I[0]))
            else:
                raise ValueError
        h2 = len(parsed_ideals) > 0
    except Exception:
        h2 = False

    # H_3: x_1, x_2, ..., x_n are elements of R
    try:
        parsed_elements = []
        for x in elements:
            if isinstance(x, (int, Integer)):
                parsed_elements.append(int(x))
            else:
                raise ValueError
        h3 = len(parsed_elements) == len(parsed_ideals) and len(parsed_elements) > 0
    except Exception:
        h3 = False

    # ¬Q: There does not exist an element x in R such that x ≡ x_k (mod I_k) for all k
    try:
        neg_q = False
        if h1 and h2 and h3:
            # By the Chinese Remainder Theorem for Z, a system of congruences
            # x = x_i (mod m_i) has a solution if and only if
            # x_i = x_j (mod gcd(m_i, m_j)) for all pairs i, j.
            solution_exists = True
            for i in range(len(parsed_ideals)):
                for j in range(i + 1, len(parsed_ideals)):
                    g = math.gcd(abs(parsed_ideals[i]), abs(parsed_ideals[j]))
                    if g != 0:
                        if (parsed_elements[i] - parsed_elements[j]) % g != 0:
                            solution_exists = False
                            break
                    else:
                        # If gcd is 0, both ideals are (0), so elements must be exactly equal
                        if parsed_elements[i] != parsed_elements[j]:
                            solution_exists = False
                            break
                if not solution_exists:
                    break
            
            # The conclusion FAILS if there is NO solution
            neg_q = not solution_exists
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: I_1, I_2, ..., I_n are ideals of R",
    "H_3: x_1, x_2, ..., x_n are elements of R",
    "¬Q: There does not exist an element x in R such that x ≡ x_k (mod I_k) for all k"
]

N_HYP = 3
NEG_Q_INDEX = 3