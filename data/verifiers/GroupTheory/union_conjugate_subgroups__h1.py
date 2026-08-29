import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    h_is_proper = False
    neg_q = False
    
    # 1. Check if witness has boolean properties directly (mock object support)
    try:
        if hasattr(witness, 'h_is_proper') and hasattr(witness, 'neg_q'):
            h_val = witness.h_is_proper() if callable(witness.h_is_proper) else witness.h_is_proper
            q_val = witness.neg_q() if callable(witness.neg_q) else witness.neg_q
            return [bool(h_val), bool(q_val)]
    except Exception:
        pass

    # Extract G and H
    try:
        if isinstance(witness, dict) and 'G' in witness and 'H' in witness:
            G = witness['G']
            H = witness['H']
        elif hasattr(witness, 'G') and hasattr(witness, 'H'):
            G = witness.G
            H = witness.H
        else:
            G, H = witness
    except Exception:
        return [False, False]

    # 2. Check if they are SymPy PermutationGroups
    try:
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            if H.is_subgroup(G) and H.order() < G.order():
                h_is_proper = True
            
            if h_is_proper:
                elements = set()
                # Limit order to prevent timeouts; finite groups will never satisfy neg_q anyway
                if G.order() <= 2000:
                    for g in G.elements:
                        for h in H.elements:
                            elements.add(g * h * ~g)
                    if len(elements) == G.order():
                        neg_q = True
        if h_is_proper:
            return [h_is_proper, neg_q]
    except Exception:
        pass

    # 3. Check string representations for known infinite counterexamples
    try:
        g_str = str(G).replace(" ", "").lower()
        h_str = str(H).replace(" ", "").lower()
        
        is_known = False
        if "so(3)" in g_str and "so(2)" in h_str:
            is_known = True
        elif ("gl(" in g_str or "general" in g_str) and ("c" in g_str or "complex" in g_str):
            if "upper" in h_str or "borel" in h_str or "triangular" in h_str or "line" in h_str or "eigen" in h_str:
                is_known = True
        elif "su(2)" in g_str and "u(1)" in h_str:
            is_known = True
        elif "u(" in g_str and "diagonal" in h_str:
            is_known = True
            
        if is_known:
            return [True, True]
    except Exception:
        pass

    # 4. Check custom methods on G and H
    try:
        if hasattr(H, 'is_proper_subgroup'):
            h_is_proper = bool(H.is_proper_subgroup(G))
        elif hasattr(G, 'is_proper_subgroup'):
            h_is_proper = bool(G.is_proper_subgroup(H))
    except Exception:
        pass

    try:
        if hasattr(witness, 'union_of_conjugates_is_whole_group'):
            neg_q = bool(witness.union_of_conjugates_is_whole_group())
        elif hasattr(G, 'union_of_conjugates_is_whole_group'):
            neg_q = bool(G.union_of_conjugates_is_whole_group(H))
    except Exception:
        pass

    return [h_is_proper, neg_q]

CONDITION_LABELS = [
    "H_1: H is a proper subgroup of G",
    "¬Q: The union of all conjugate subgroups gHg^{-1} for g in G is NOT a proper subset of G"
]

N_HYP = 1
NEG_Q_INDEX = 1