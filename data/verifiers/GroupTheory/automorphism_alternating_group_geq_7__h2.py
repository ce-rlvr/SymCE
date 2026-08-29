import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import totient
import math

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 6",
    "¬Q: The automorphism group Aut(G) is not isomorphic to the symmetric group S_n"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # Extract G and n from the witness
    G = None
    n = None
    if isinstance(witness, dict):
        G = witness.get('G')
        n = witness.get('n')
    elif isinstance(witness, (tuple, list)) and len(witness) == 2:
        G, n = witness
    else:
        G = witness
        try:
            n = G.degree
        except Exception:
            pass

    # H_1: n is an integer strictly greater than 6
    try:
        h1_ok = (int(n) == n) and (n > 6)
    except Exception:
        h1_ok = False

    # ¬Q: The automorphism group Aut(G) is not isomorphic to the symmetric group S_n
    try:
        if not h1_ok or G is None:
            neg_q_ok = False
        else:
            order_G = int(G.order())
            n_int = int(n)
            
            # Any automorphism must fix the identity and permute the remaining |G|-1 elements.
            # Thus, Aut(G) is isomorphic to a subgroup of S_{|G|-1}, so |Aut(G)| <= (|G|-1)!
            # If (|G|-1)! < n!, then |Aut(G)| < |S_n|, so Aut(G) cannot be isomorphic to S_n.
            if order_G >= 1 and math.factorial(order_G - 1) < math.factorial(n_int):
                neg_q_ok = True
            else:
                # If the factorial bound doesn't catch it, check if G is cyclic
                is_cyclic = False
                try:
                    if G.is_abelian and order_G <= 1000:
                        if any(g.order() == order_G for g in G.elements):
                            is_cyclic = True
                except Exception:
                    pass
                
                if is_cyclic:
                    # For a cyclic group, |Aut(G)| = phi(|G|)
                    if totient(order_G) != math.factorial(n_int):
                        neg_q_ok = True
                    else:
                        neg_q_ok = False
                else:
                    # Check known cases where Aut(G) IS isomorphic to S_n
                    if n_int >= 7 and G.is_isomorphic(AlternatingGroup(n_int)):
                        neg_q_ok = False
                    elif n_int != 6 and G.is_isomorphic(SymmetricGroup(n_int)):
                        neg_q_ok = False
                    else:
                        # For other groups where we can't easily compute Aut(G),
                        # we return False to be safe and avoid false positives.
                        neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]