import sympy

# Top-level setup
ZZ = sympy.S.Integers

def conditions(witness) -> list[bool]:
    # Extract C from witness
    C = None
    if isinstance(witness, dict):
        C = witness.get('C', witness.get('c', witness.get('ideals', None)))
    if C is None:
        if isinstance(witness, tuple):
            if len(witness) >= 1:
                C = witness[0]
        else:
            C = witness

    try:
        C_list = list(C)
    except Exception:
        return [False, False, False, False]

    # Check if all elements are integers (representing ideals in ZZ)
    try:
        is_zz = all(isinstance(val, (int, sympy.Integer)) for val in C_list)
    except Exception:
        is_zz = False

    # H_1: R is a commutative ring with identity
    # We interpret integer witnesses as ideals in ZZ, which is a commutative ring with identity.
    h1 = is_zz

    # H_2: C is a non-empty set of prime ideals of R
    # In ZZ, an ideal (n) is prime iff |n| is prime or n = 0.
    try:
        if is_zz:
            h2 = len(C_list) > 0 and all(sympy.isprime(abs(int(val))) or int(val) == 0 for val in C_list)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: U is the union of all prime ideals in C
    # This is true by definition of our interpretation of the witness.
    h3 = h1

    # ¬Q: U is not a prime ideal of R
    # In ZZ, the union of prime ideals is an ideal iff there is a unique maximal element among them.
    # Since non-zero prime ideals in ZZ are maximal, the union of multiple distinct non-zero prime ideals
    # is never an ideal, and thus not a prime ideal.
    try:
        if is_zz:
            distinct = set(abs(int(val)) for val in C_list if int(val) != 0)
            neg_q = len(distinct) > 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: C is a non-empty set of prime ideals of R",
    "H_3: U is the union of all prime ideals in C",
    "¬Q: U is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3