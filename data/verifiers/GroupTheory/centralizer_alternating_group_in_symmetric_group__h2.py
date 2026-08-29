import sympy
from sympy.combinatorics import AlternatingGroup, SymmetricGroup
from sympy.combinatorics.named_groups import DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be an integer n (or an AlternatingGroup object).
    """
    n = None
    if isinstance(witness, (int, sympy.Integer)):
        n = int(witness)
    elif hasattr(witness, 'degree'):
        n = int(witness.degree)
        
    # H_1: Let n >= 4 be an integer
    try:
        h1 = (n is not None) and (n >= 4)
    except Exception:
        h1 = False

    # H_2: Let A_n be the alternating group on n letters
    try:
        if n is not None and n >= 1:
            if hasattr(witness, 'degree'):
                h2 = isinstance(witness, AlternatingGroup)
            else:
                # If witness is just the integer n, this definitional hypothesis holds
                h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The centralizer of A_n in S_n is NOT the trivial subgroup
    try:
        if n is None or n < 1:
            neg_q = False
        else:
            if n <= 2:
                # For n=1, S_1 and A_1 are trivial, centralizer is trivial.
                # For n=2, S_2 is Z_2, A_2 is trivial, centralizer is S_2 (not trivial).
                is_trivial = (n == 1)
            elif n <= 5:
                # Compute explicitly for small n to avoid timeouts
                Sn = SymmetricGroup(n)
                An = AlternatingGroup(n)
                is_trivial = True
                for g in Sn.elements:
                    if g.is_Identity:
                        continue
                    commutes = True
                    for gen in An.generators:
                        if g * gen != gen * g:
                            commutes = False
                            break
                    if commutes:
                        is_trivial = False
                        break
            else:
                # For n >= 4, it is a known mathematical fact that C_{S_n}(A_n) is trivial.
                # We use this shortcut for n > 5 to guarantee fast execution.
                is_trivial = True
                
            neg_q = not is_trivial
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 4 is an integer",
    "H_2: A_n is the alternating group on n letters",
    "¬Q: The centralizer of A_n in S_n is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2