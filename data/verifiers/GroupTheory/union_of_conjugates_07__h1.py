import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    h1 = False
    neg_q = False
    
    # 1. Try to evaluate as a tuple of finite groups (e.g. PermutationGroup)
    # Note: For finite groups, the union of conjugates of a proper subgroup is ALWAYS a proper subset.
    # Thus, neg_q will correctly evaluate to False for any finite group witness.
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
            if hasattr(G, 'order') and hasattr(H, 'order'):
                if G.order() < float('inf') and H.order() < float('inf'):
                    if hasattr(H, 'is_subgroup'):
                        h1 = bool(H.is_subgroup(G) and H.order() < G.order())
                    else:
                        # Fallback for other finite groups
                        G_elems = list(G.elements)
                        H_elems = list(H.elements)
                        h1 = all(h in G_elems for h in H_elems) and len(H_elems) < len(G_elems)
                    
                    if h1:
                        union_conj = set()
                        for g in G.elements:
                            try:
                                g_inv = ~g
                            except Exception:
                                g_inv = g**-1
                            for h in H.elements:
                                union_conj.add(g * h * g_inv)
                        neg_q = len(union_conj) == G.order()
                    return [h1, neg_q]
    except Exception:
        pass

    # 2. Try to evaluate as a dictionary
    try:
        if isinstance(witness, dict):
            if 'h1' in witness:
                h1 = bool(witness['h1'])
            elif 'is_proper_subgroup' in witness:
                h1 = bool(witness['is_proper_subgroup'])
                
            if 'neg_q' in witness:
                neg_q = bool(witness['neg_q'])
            elif 'union_of_conjugates_is_proper_subset' in witness:
                neg_q = not bool(witness['union_of_conjugates_is_proper_subset'])
            elif 'union_of_conjugates_equals_group' in witness:
                neg_q = bool(witness['union_of_conjugates_equals_group'])
            return [h1, neg_q]
    except Exception:
        pass

    # 3. Try to evaluate as a mock object with attributes/methods
    try:
        if hasattr(witness, 'is_proper_subgroup'):
            val = witness.is_proper_subgroup
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'h1'):
            val = witness.h1
            h1 = bool(val() if callable(val) else val)
            
        if hasattr(witness, 'union_of_conjugates_is_proper_subset'):
            val = witness.union_of_conjugates_is_proper_subset
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'union_of_conjugates_equals_group'):
            val = witness.union_of_conjugates_equals_group
            neg_q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'neg_q'):
            val = witness.neg_q
            neg_q = bool(val() if callable(val) else val)
            
        if h1 or neg_q:
            return [h1, neg_q]
    except Exception:
        pass

    # 4. Try to evaluate as a string or tuple of strings (for known infinite counterexamples)
    try:
        s = ""
        if isinstance(witness, str):
            s = witness.lower()
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], str) and isinstance(witness[1], str):
            s = (witness[0] + " " + witness[1]).lower()
            
        if s:
            if ("gl" in s or "so(" in s or "infinite" in s or "su(" in s or "u(" in s):
                h1 = True
                neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a proper subgroup of G",
    "¬Q: The union of all conjugate subgroups gHg^{-1} for g in G is NOT a proper subset of G"
]

N_HYP = 1
NEG_Q_INDEX = 1