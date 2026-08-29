import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_finitely_generated(grp):
    if hasattr(grp, 'is_finitely_generated'):
        val = grp.is_finitely_generated
        return val() if callable(val) else val
    if isinstance(grp, dict) and 'is_finitely_generated' in grp:
        return grp['is_finitely_generated']
    
    if isinstance(grp, PermutationGroup):
        return True
        
    cls_name = type(grp).__name__
    if cls_name in ('FpGroup', 'FreeGroup'):
        return True
    return False

def has_solvable_word_problem(grp):
    if hasattr(grp, 'has_solvable_word_problem'):
        val = grp.has_solvable_word_problem
        return val() if callable(val) else val
    if isinstance(grp, dict) and 'has_solvable_word_problem' in grp:
        return grp['has_solvable_word_problem']
    
    if isinstance(grp, PermutationGroup):
        return True
        
    cls_name = type(grp).__name__
    if cls_name in ('FreeGroup',):
        return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            G, H = witness[0], witness[1]
        elif isinstance(witness, dict) and 'G' in witness and 'H' in witness:
            G, H = witness['G'], witness['H']
        elif hasattr(witness, 'G') and hasattr(witness, 'H'):
            G, H = witness.G, witness.H
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(is_finitely_generated(G))
    except Exception:
        h1 = False

    try:
        h2 = bool(has_solvable_word_problem(G))
    except Exception:
        h2 = False

    try:
        h3 = bool(has_solvable_word_problem(H))
    except Exception:
        h3 = False

    try:
        prod_swp = None
        if isinstance(witness, dict):
            if 'GxH' in witness:
                prod_swp = has_solvable_word_problem(witness['GxH'])
            elif 'G_times_H' in witness:
                prod_swp = has_solvable_word_problem(witness['G_times_H'])
        else:
            if hasattr(witness, 'GxH'):
                prod_swp = has_solvable_word_problem(witness.GxH)
            elif hasattr(witness, 'G_times_H'):
                prod_swp = has_solvable_word_problem(witness.G_times_H)
        
        if prod_swp is None:
            # Deduce: G x H has a solvable word problem in the standard sense 
            # iff both are finitely generated and have solvable word problems.
            prod_swp = is_finitely_generated(G) and is_finitely_generated(H) and \
                       has_solvable_word_problem(G) and has_solvable_word_problem(H)
                       
        neg_q = not bool(prod_swp)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: G has a solvable word problem",
    "H_3: H has a solvable word problem",
    "¬Q: The direct product G × H does not have a solvable word problem"
]

N_HYP = 3
NEG_Q_INDEX = 3