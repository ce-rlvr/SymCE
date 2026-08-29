import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings for witness expressions
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

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it falsifies the conclusion.
    
    The witness can be a tuple: (G, alpha) or (G, alpha, S)
    where G is a group and alpha is a mapping (dict, list of pairs, or callable).
    """
    try:
        if len(witness) == 2:
            G, alpha = witness
            S_given = None
        elif len(witness) == 3:
            G, alpha, S_given = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            elements = list(G.elements)
    except Exception:
        h1 = False

    # H_2: S is the set of all elements x \in G such that \alpha(x) = x
    try:
        if not h1:
            h2 = False
            S_computed = set()
        else:
            S_computed = set()
            for x in elements:
                if isinstance(alpha, dict):
                    if x in alpha:
                        val = alpha[x]
                    else:
                        # Fallback to check by equality
                        found = False
                        for k, v in alpha.items():
                            if k == x:
                                val = v
                                found = True
                                break
                        if not found:
                            raise ValueError(f"Mapping for {x} not found in alpha")
                elif isinstance(alpha, (list, tuple)):
                    found = False
                    for k, v in alpha:
                        if k == x:
                            val = v
                            found = True
                            break
                    if not found:
                        raise ValueError(f"Mapping for {x} not found in alpha")
                elif callable(alpha):
                    val = alpha(x)
                else:
                    raise TypeError("alpha must be a dict, list of pairs, or callable")
                
                if val == x:
                    S_computed.add(x)
            
            if S_given is not None:
                h2 = (set(S_given) == S_computed)
            else:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: S is NOT a subgroup of G
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            S_list = list(S_computed)
            if not S_list:
                neg_q = True  # The empty set is not a subgroup
            else:
                # Find the identity element in G
                identity = None
                for x in elements:
                    if x * x == x:
                        identity = x
                        break
                
                if identity not in S_computed:
                    neg_q = True
                else:
                    is_subgroup = True
                    # Check closure under group operation
                    for x in S_list:
                        for y in S_list:
                            if (x * y) not in S_computed:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                    
                    # Check closure under inverses
                    if is_subgroup:
                        for x in S_list:
                            if (x**-1) not in S_computed:
                                is_subgroup = False
                                break
                                
                    neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: S is the set of all elements x in G such that alpha(x) = x",
    "¬Q: S is not a subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2