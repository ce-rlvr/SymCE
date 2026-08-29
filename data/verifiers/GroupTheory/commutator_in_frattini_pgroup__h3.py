import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite p-group",
    "¬Q: The commutator subgroup G' is not a subgroup of the Frattini subgroup Φ(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Parse the witness
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            G = witness.get('G')
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            if isinstance(witness[0], PermutationGroup):
                G, p = witness
            else:
                p, G = witness
        elif isinstance(witness, PermutationGroup):
            G = witness
            order = G.order()
            factors = sympy.factorint(order)
            if len(factors) == 1:
                p = list(factors.keys())[0]
            elif order == 1:
                p = 2
            else:
                p = 0
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: G is a finite p-group
    try:
        if not isinstance(G, PermutationGroup):
            h2 = False
        else:
            order = G.order()
            if order == 1:
                h2 = True
            else:
                factors = sympy.factorint(order)
                h2 = (list(factors.keys()) == [p])
    except Exception:
        h2 = False

    # ¬Q: G' is NOT a subgroup of Φ(G)
    # By Wielandt's theorem, for any finite group G, the commutator subgroup G' 
    # is contained in the Frattini subgroup Φ(G) if and only if G is nilpotent.
    # Therefore, G' is NOT a subgroup of Φ(G) iff G is NOT nilpotent.
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            if hasattr(G, 'is_nilpotent'):
                val = G.is_nilpotent
                if callable(val):
                    is_nilp = val()
                else:
                    is_nilp = val
            else:
                lcs = G.lower_central_series()
                is_nilp = (lcs[-1].order() == 1)
            neg_q = not is_nilp
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]