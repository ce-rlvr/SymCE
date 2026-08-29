import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, p, X_size) or (G, p).
    """
    G, p, X_size = None, None, None
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, p = witness
                if hasattr(G, 'degree'):
                    X_size = G.degree
            elif len(witness) == 3:
                G, p, X_size = witness
                if isinstance(X_size, (list, set, tuple)):
                    X_size = len(X_size)
    except Exception:
        pass

    try:
        p_val = int(p)
        if p_val != p:
            p_val = -1
    except Exception:
        p_val = -1

    # H1: G is a finite p-group
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and p_val >= 2:
            order = G.order()
            if order > 0:
                temp = order
                while temp % p_val == 0:
                    temp //= p_val
                if temp == 1:
                    h1 = True
    except Exception:
        h1 = False

    # H2: X is a finite set
    try:
        h2 = False
        try:
            x_val = int(X_size)
        except Exception:
            x_val = -1
        if x_val >= 0 and x_val == X_size:
            h2 = True
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        h3 = False
        if h2 and isinstance(G, PermutationGroup):
            if x_val >= G.degree:
                h3 = True
    except Exception:
        h3 = False

    # neg_Q: |X| \not\equiv |X^G| \pmod p
    try:
        neg_q = False
        if h1 and h2 and h3:
            fixed_count = 0
            gens = G.generators
            for i in range(x_val):
                if i < G.degree:
                    is_fixed = True
                    for g in gens:
                        if g(i) != i:
                            is_fixed = False
                            break
                    if is_fixed:
                        fixed_count += 1
                else:
                    # Points beyond G.degree are fixed by definition
                    fixed_count += 1
            
            if (x_val % p_val) != (fixed_count % p_val):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "H_2: X is a finite set",
    "H_3: G acts on X",
    "¬Q: |X| is not congruent to |X^G| mod p"
]

N_HYP = 3
NEG_Q_INDEX = 3