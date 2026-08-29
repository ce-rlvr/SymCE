import sympy
from sympy import Integer, ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
# Standard rings and symbols are available for witness expressions.

def conditions(witness):
    h1 = False
    neg_q = False
    
    # 1. Tuple (R, I)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            h1 = True
            if R == I:
                neg_q = True
            elif hasattr(I, 'is_whole_ring'):
                if callable(I.is_whole_ring) and I.is_whole_ring():
                    neg_q = True
                elif not callable(I.is_whole_ring) and I.is_whole_ring:
                    neg_q = True
            elif isinstance(I, (int, Integer)) and abs(int(I)) == 1:
                neg_q = True
            elif isinstance(I, (list, tuple, set)) and (1 in I or -1 in I or Integer(1) in I or Integer(-1) in I):
                neg_q = True
            elif isinstance(I, str) and I.strip().lower() in ['r', '1', 'whole ring', 'zz', 'z', 'unit ideal']:
                neg_q = True
            return [h1, neg_q]
    except Exception:
        pass

    # 2. Integer (representing the ideal nZ in Z)
    try:
        if isinstance(witness, (int, Integer)):
            h1 = True
            if abs(int(witness)) == 1:
                neg_q = True
            return [h1, neg_q]
    except Exception:
        pass

    # 3. SymPy Ideal
    try:
        if hasattr(witness, 'is_whole_ring'):
            h1 = True
            if callable(witness.is_whole_ring) and witness.is_whole_ring():
                neg_q = True
            elif not callable(witness.is_whole_ring) and witness.is_whole_ring:
                neg_q = True
            return [h1, neg_q]
    except Exception:
        pass

    # 4. SymPy Ring / Domain (representing the unit ideal R in R)
    try:
        if (hasattr(witness, 'is_Ring') and witness.is_Ring) or witness in [ZZ, QQ]:
            h1 = True
            neg_q = True
            return [h1, neg_q]
    except Exception:
        pass

    # 5. List/Set of generators
    try:
        if isinstance(witness, (list, set)):
            h1 = True
            if 1 in witness or -1 in witness or Integer(1) in witness or Integer(-1) in witness:
                neg_q = True
            return [h1, neg_q]
    except Exception:
        pass

    # 6. String representation
    try:
        if isinstance(witness, str):
            h1 = True
            if witness.strip().lower() in ['r', '1', 'whole ring', 'zz', 'z', 'unit ideal']:
                neg_q = True
            return [h1, neg_q]
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a two-sided ideal of R",
    "¬Q: There is no ring S and surjective ring homomorphism f: R -> S with ker(f) = I"
]

N_HYP = 1
NEG_Q_INDEX = 1