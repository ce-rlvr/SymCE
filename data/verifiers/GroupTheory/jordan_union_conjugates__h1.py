import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    h1_ok = False
    neg_q_ok = False
    
    # 1. Try to evaluate as a tuple of SymPy groups
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
            if hasattr(G, 'is_group') and hasattr(H, 'is_group'):
                h1_ok = H.is_subgroup(G) and H.order() < G.order()
                
                # Jordan's theorem holds for all finite groups.
                # Thus, for any finite group, the union of conjugates is ALWAYS a proper subset.
                if h1_ok and G.order() < float('inf'):
                    neg_q_ok = False
    except Exception:
        pass

    # 2. Try to evaluate as a custom object with attributes
    if not h1_ok:
        try:
            h1_ok = bool(witness.is_proper_subgroup)
        except Exception:
            pass
    if not neg_q_ok:
        try:
            neg_q_ok = bool(witness.union_of_conjugates_equals_G)
        except Exception:
            pass

    # 3. Try to evaluate as a dictionary with explicit boolean flags
    if not h1_ok:
        try:
            if isinstance(witness, dict) and 'is_proper_subgroup' in witness:
                h1_ok = bool(witness['is_proper_subgroup'])
        except Exception:
            pass
    if not neg_q_ok:
        try:
            if isinstance(witness, dict) and 'union_of_conjugates_equals_G' in witness:
                neg_q_ok = bool(witness['union_of_conjugates_equals_G'])
        except Exception:
            pass

    # 4. Try to evaluate as a string, tuple of strings, or dict with string values (known infinite counterexamples)
    try:
        s = ""
        if isinstance(witness, str):
            s = witness.lower()
        elif isinstance(witness, tuple) and len(witness) == 2 and all(isinstance(x, str) for x in witness):
            s = (witness[0] + " " + witness[1]).lower()
        elif isinstance(witness, dict) and 'G' in witness and 'H' in witness:
            s = (str(witness['G']) + " " + str(witness['H'])).lower()
            
        if s:
            # SO(3) and SO(2)
            if ("so(3)" in s or "so3" in s) and ("so(2)" in s or "so2" in s):
                h1_ok = True
                neg_q_ok = True
            # GL(n, C) and upper triangular / Borel subgroup
            elif "gl" in s and ("upper triangular" in s or "borel" in s):
                h1_ok = True
                neg_q_ok = True
            # SU(2) and U(1)
            elif "su(2)" in s and "u(1)" in s:
                h1_ok = True
                neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a proper subgroup of G",
    "¬Q: The union of all conjugates of H in G is not strictly a proper subset of G (i.e., it equals G)"
]

N_HYP = 1
NEG_Q_INDEX = 1