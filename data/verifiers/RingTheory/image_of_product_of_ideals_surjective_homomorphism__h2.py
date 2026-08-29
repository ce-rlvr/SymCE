import sympy
import sympy.combinatorics
import sympy.matrices

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_ring(R):
    # We support Z/nZ represented as an integer n > 0
    return isinstance(R, int) and R > 0

def is_ideal(I, R):
    if not is_ring(R):
        return False
    if not isinstance(I, (set, list, tuple)):
        return False
    I = set(I)
    if not I.issubset(set(range(R))):
        return False
    if not I:
        return False
    # Check additive subgroup
    for a in I:
        for b in I:
            if (a + b) % R not in I:
                return False
    # Check absorbing property
    for a in I:
        for r in range(R):
            if (a * r) % R not in I:
                return False
    return True

def _additive_closure(subset, mod):
    closure = set(subset)
    added = True
    while added:
        added = False
        new_elements = set()
        for a in closure:
            for b in closure:
                c = (a + b) % mod
                if c not in closure:
                    new_elements.add(c)
        if new_elements:
            closure.update(new_elements)
            added = True
    return closure

def product_of_ideals(I, J, R):
    prods = set((a * b) % R for a in I for b in J)
    return _additive_closure(prods, R)

def apply_f(f, X):
    if isinstance(f, dict):
        return set(f[x] for x in X)
    elif isinstance(f, (list, tuple)):
        return set(f[x] for x in X)
    else:
        return set(f(x) for x in X)

def product_of_subsets(A, B, S):
    prods = set((a * b) % S for a in A for b in B)
    return _additive_closure(prods, S)

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        R = witness.get('R')
        S = witness.get('S')
        I = witness.get('I')
        J = witness.get('J')
        f = witness.get('f')
    elif isinstance(witness, (list, tuple)) and len(witness) == 5:
        R, S, I, J, f = witness
    else:
        try:
            R = witness.R
            S = witness.S
            I = witness.I
            J = witness.J
            f = witness.f
        except AttributeError:
            return [False, False, False, False]

    # H_1: R and S are rings
    try:
        h1 = is_ring(R) and is_ring(S)
    except Exception:
        h1 = False

    # H_2: I is an ideal of R
    try:
        h2 = is_ideal(I, R)
    except Exception:
        h2 = False

    # H_3: J is an ideal of R
    try:
        h3 = is_ideal(J, R)
    except Exception:
        h3 = False

    # ¬Q: f(IJ) != f(I)f(J)
    try:
        IJ = product_of_ideals(I, J, R)
        f_IJ = apply_f(f, IJ)
        f_I = apply_f(f, I)
        f_J = apply_f(f, J)
        f_I_f_J = product_of_subsets(f_I, f_J, S)
        
        neg_q = (f_IJ != f_I_f_J)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "¬Q: f(IJ) != f(I)f(J)"
]

N_HYP = 3
NEG_Q_INDEX = 3