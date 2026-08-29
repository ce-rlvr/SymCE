import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Standard group theory objects for potential witnesses
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide both the group G and the parameter p.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    # H_1: G is a finite cyclic group
    try:
        h1 = isinstance(G, PermutationGroup) and G.is_cyclic
        if callable(h1):
            h1 = h1()
    except Exception:
        h1 = False
        
    # neg_Q: The Sylow p-subgroup of G is NOT unique and cyclic
    # This will be True if p is not a prime (since the Sylow p-subgroup is undefined),
    # or if it exists but fails to be unique or cyclic.
    try:
        if not isprime(p):
            neg_q = True
        else:
            if not isinstance(G, PermutationGroup):
                neg_q = True
            else:
                S = G.sylow_subgroup(p)
                
                unique = True
                s_order = S.order() if callable(S.order) else S.order
                if s_order > 1:
                    for g in G.generators:
                        g_inv = ~g
                        for h in S.generators:
                            if (g * h * g_inv) not in S:
                                unique = False
                                break
                        if not unique:
                            break
                
                cyclic = S.is_cyclic
                if callable(cyclic):
                    cyclic = cyclic()
                
                concl = unique and cyclic
                neg_q = not concl
    except Exception:
        # If evaluating the Sylow p-subgroup fails for any reason, the conclusion fails.
        neg_q = True

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "¬Q: The Sylow p-subgroup of G is not unique and cyclic"
]

N_HYP = 1
NEG_Q_INDEX = 1