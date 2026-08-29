import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should ideally be a tuple (G, p), but if only G is provided,
    p is inferred as |G| // 2.
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        G, p = witness
    else:
        G = witness
        try:
            p = G.order() // 2
        except Exception:
            return [False, False]
            
    # H_1: p is an odd prime
    try:
        h1_ok = bool(sympy.isprime(p) and (p % 2 != 0))
    except Exception:
        h1_ok = False
        
    # neg_Q: The number of Sylow 2-subgroups of G is NOT exactly p
    try:
        order = G.order()
        if order % 2 != 0:
            # If the order is odd, the Sylow 2-subgroup is the trivial subgroup (order 1)
            # and there is exactly 1 such subgroup.
            n_2 = 1
        else:
            # Find one Sylow 2-subgroup
            P = G.sylow_subgroup(2)
            P_elements = list(P.generate_dimino())
            
            # Find all conjugate subgroups g^-1 * P * g
            conjugates = set()
            for g in G.generate_dimino():
                conj = frozenset(~g * x * g for x in P_elements)
                conjugates.add(conj)
                
            n_2 = len(conjugates)
            
        neg_q_ok = bool(n_2 != p)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "¬Q: The number of Sylow 2-subgroups of G is not exactly p"
]

N_HYP = 1
NEG_Q_INDEX = 1