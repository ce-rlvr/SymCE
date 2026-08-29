import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings that the witness expression may reference.
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
D6 = DihedralGroup(6)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(witness, PermutationGroup) and witness.is_finite
    except Exception:
        h1_ok = False

    # H_2: The order of G is p^2 q
    # Note: The dropped hypothesis was "p and q are distinct primes". 
    # Without it, p and q could be any integers, or p=q. 
    # We check if there exist integers p > 1, q > 1 such that |G| = p^2 * q.
    # To be a valid counterexample to the exact phrasing, we must find *some* p, q 
    # where the conclusion fails. We will just check if the order can be written as p^2 q
    # for some primes p, q (even if not distinct, though if p=q it's p^3).
    # Wait, if p and q must be primes, we extract them.
    try:
        if not h1_ok:
            h2_ok = False
            p, q = None, None
        else:
            order = witness.order()
            factors = sympy.factorint(order)
            h2_ok = False
            p, q = None, None
            
            # Check if order is exactly p^2 * q for primes p, q
            if len(factors) == 2:
                p1, e1 = list(factors.items())[0]
                p2, e2 = list(factors.items())[1]
                if e1 == 2 and e2 == 1:
                    h2_ok = True
                    p, q = p1, p2
                elif e1 == 1 and e2 == 2:
                    h2_ok = True
                    p, q = p2, p1
            elif len(factors) == 1:
                # If p = q, order is p^3
                p1, e1 = list(factors.items())[0]
                if e1 == 3:
                    h2_ok = True
                    p, q = p1, p1
    except Exception:
        h2_ok = False
        p, q = None, None

    # neg_Q: NEITHER the Sylow p-subgroup NOR the Sylow q-subgroup is normal in G
    try:
        if not h2_ok or p is None or q is None:
            neg_q_ok = False
        else:
            # Check if Sylow p-subgroup is normal
            sylow_p_normal = False
            try:
                sylow_p = witness.sylow_subgroup(p)
                sylow_p_normal = sylow_p.is_normal(witness)
            except Exception:
                pass
            
            # Check if Sylow q-subgroup is normal
            sylow_q_normal = False
            try:
                sylow_q = witness.sylow_subgroup(q)
                sylow_q_normal = sylow_q.is_normal(witness)
            except Exception:
                pass
            
            # The conclusion is "Either Sylow p is normal or Sylow q is normal"
            # Negation: NEITHER is normal
            neg_q_ok = not (sylow_p_normal or sylow_q_normal)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is p^2 q",
    "¬Q: Neither the Sylow p-subgroup nor the Sylow q-subgroup is normal in G"
]

N_HYP = 2
NEG_Q_INDEX = 2