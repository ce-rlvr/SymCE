import sympy
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup for potential witness expressions
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

def eval_word(word, mapping, target_group):
    if hasattr(word, 'is_identity') and word.is_identity:
        return target_group.identity
    
    if hasattr(word, 'array_form'):
        arr = word.array_form
    elif hasattr(word, 'word') and hasattr(word.word, 'array_form'):
        arr = word.word.array_form
    else:
        raise ValueError("Unsupported word type")

    sym_mapping = {}
    for g, val in mapping.items():
        if hasattr(g, 'array_form'):
            sym = g.array_form[0][0]
        elif hasattr(g, 'word') and hasattr(g.word, 'array_form'):
            sym = g.word.array_form[0][0]
        else:
            raise ValueError("Unsupported generator type")
        sym_mapping[sym] = val

    res = target_group.identity
    for sym, exp in arr:
        val = sym_mapping[sym]
        res = res * (val ** exp)
    return res

def conditions(witness):
    try:
        # The witness is expected to be a tuple: (F, R, r_dict, s_dict)
        # where r_dict is a mapping from F's generators to R (the retraction)
        # and s_dict is a mapping from R's generators to F (the section)
        F, R, r_dict, s_dict = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a free group
    try:
        h1 = isinstance(F, FreeGroup)
    except Exception:
        h1 = False

    # H_2: There exists a retraction homomorphism from F onto R
    try:
        h2 = True
        # Check r_dict maps F's generators to R
        for gen in F.generators:
            if gen not in r_dict:
                h2 = False
                break
            if r_dict[gen].group != R:
                h2 = False
                break
        
        # Check s_dict maps R's generators to F
        if h2:
            for gen in R.generators:
                if gen not in s_dict:
                    h2 = False
                    break
                if s_dict[gen].group != F:
                    h2 = False
                    break
        
        # Check relators of R for s_dict (if R is an FpGroup)
        if h2 and hasattr(R, 'relators'):
            for rel in R.relators:
                if eval_word(rel, s_dict, F) != F.identity:
                    h2 = False
                    break

        # Check r(s(x)) = x for all generators of R
        if h2:
            for gen in R.generators:
                s_val = s_dict[gen]
                r_s_val = eval_word(s_val, r_dict, R)
                if r_s_val != gen:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: R is not a free factor of F
    try:
        if R == F:
            neg_q = False
        else:
            # If R is a separate group object, it is not a subgroup of F, 
            # and therefore cannot be a free factor of F.
            if hasattr(R, 'generators') and len(R.generators) > 0:
                if R.generators[0].group != F:
                    neg_q = True
                else:
                    neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: There exists a retraction homomorphism from F onto R",
    "¬Q: R is not a free factor of F (since it is not a subgroup of F)"
]

N_HYP = 2
NEG_Q_INDEX = 2