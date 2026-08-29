import itertools

# Top-level setup: Standard finite rings represented by their moduli.
# A ring Z/n1Z x Z/n2Z x ... is represented by the tuple (n1, n2, ...).
# Elements are tuples of integers (x1, x2, ...) where 0 <= xi < ni.
Z2 = (2,)
Z3 = (3,)
Z4 = (4,)
Z5 = (5,)
Z6 = (6,)
Z8 = (8,)
Z2xZ2 = (2, 2)
Z2xZ3 = (2, 3)
Z2xZ2xZ2 = (2, 2, 2)

def get_elements(moduli):
    if not moduli:
        return [(0,)]
    ranges = [range(m) for m in moduli]
    return list(itertools.product(*ranges))

def add_elements(x, y, moduli):
    return tuple((a + b) % m for a, b, m in zip(x, y, moduli))

def mul_elements(x, y, moduli):
    return tuple((a * b) % m for a, b, m in zip(x, y, moduli))

def is_ideal(subset, moduli):
    if not subset:
        return False
    elements = get_elements(moduli)
    subset_set = set(subset)
    if not subset_set.issubset(set(elements)):
        return False
    zero = tuple(0 for _ in moduli)
    if zero not in subset_set:
        return False
    # Closed under addition
    for a in subset:
        for b in subset:
            if add_elements(a, b, moduli) not in subset_set:
                return False
    # Closed under scalar multiplication (absorbing property)
    for a in subset:
        for r in elements:
            if mul_elements(a, r, moduli) not in subset_set:
                return False
    return True

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness should be a dictionary with keys:
      'R': tuple of moduli for ring R
      'S': tuple of moduli for ring S
      'I': list of elements (tuples) in ideal I
      'J': list of elements (tuples) in ideal J
      'f': dict, list of pairs, or callable mapping elements of R to elements of S
    """
    try:
        R_moduli = witness['R']
        S_moduli = witness['S']
        I = witness['I']
        J = witness['J']
        f = witness['f']
    except Exception:
        return [False, False, False, False]

    # H_1: Let R and S be rings.
    try:
        h1 = isinstance(R_moduli, (list, tuple)) and len(R_moduli) > 0 and isinstance(S_moduli, (list, tuple)) and len(S_moduli) > 0
        h1 = h1 and all(isinstance(m, int) and m > 0 for m in R_moduli)
        h1 = h1 and all(isinstance(m, int) and m > 0 for m in S_moduli)
    except Exception:
        h1 = False

    # H_2: Let I and J be ideals of R.
    try:
        h2 = is_ideal(I, R_moduli) and is_ideal(J, R_moduli)
    except Exception:
        h2 = False

    # H_3: Assume I and J are comaximal in R.
    try:
        R_elements = set(get_elements(R_moduli))
        sum_IJ = set(add_elements(i, j, R_moduli) for i in I for j in J)
        h3 = (sum_IJ == R_elements)
    except Exception:
        h3 = False

    # ¬Q: The image ideals f(I) and f(J) are NOT comaximal in S (or fail to be ideals).
    try:
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        elif isinstance(f, (list, tuple)) and all(isinstance(item, (list, tuple)) and len(item) == 2 for item in f):
            f_dict = dict(f)
            f_func = lambda x: f_dict[x]
        else:
            f_func = f
            
        R_elements = set(get_elements(R_moduli))
        S_elements = set(get_elements(S_moduli))
        
        # Verify f maps R to S
        for r in R_elements:
            if f_func(r) not in S_elements:
                raise ValueError("f must map R to S")
                
        f_I = list(set(f_func(x) for x in I))
        f_J = list(set(f_func(x) for x in J))
        
        if not is_ideal(f_I, S_moduli):
            neg_q = True
        elif not is_ideal(f_J, S_moduli):
            neg_q = True
        else:
            sum_fIfJ = set(add_elements(x, y, S_moduli) for x in f_I for y in f_J)
            neg_q = (sum_fIfJ != S_elements)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: I and J are ideals of R",
    "H_3: I and J are comaximal in R",
    "¬Q: The image ideals f(I) and f(J) are not comaximal in S (or not ideals)"
]

N_HYP = 3
NEG_Q_INDEX = 3