import sympy
from sympy import Symbol, Expr
from sympy.abc import x, y, z
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

def extract_witness(witness):
    x_sym = Symbol('x')
    
    if isinstance(witness, dict):
        R_vars = witness.get('R_vars', None)
        I_gens = witness.get('I_gens', witness.get('I', None))
        x_val = witness.get('x', x_sym)
        if I_gens is None:
            return None, None, None
        if R_vars is None:
            R_vars = list(set().union(*(getattr(p, 'free_symbols', set()) for p in I_gens)))
        return R_vars, I_gens, x_val

    if isinstance(witness, tuple):
        if len(witness) == 3:
            return witness[0], witness[1], witness[2]
        elif len(witness) == 2:
            if isinstance(witness[1], Symbol) or isinstance(witness[1], str):
                I_gens = witness[0]
                x_val = witness[1] if isinstance(witness[1], Symbol) else Symbol(witness[1])
                R_vars = list(set().union(*(getattr(p, 'free_symbols', set()) for p in I_gens)))
                return R_vars, I_gens, x_val
            else:
                R_vars = witness[0]
                I_gens = witness[1]
                return R_vars, I_gens, x_sym
        elif len(witness) == 1:
            I_gens = witness[0]
            R_vars = list(set().union(*(getattr(p, 'free_symbols', set()) for p in I_gens)))
            return R_vars, I_gens, x_sym

    try:
        I_gens = list(witness)
        R_vars = list(set().union(*(getattr(p, 'free_symbols', set()) for p in I_gens)))
        return R_vars, I_gens, x_sym
    except Exception:
        return None, None, None

def conditions(witness):
    try:
        R_vars, I_gens, x_val = extract_witness(witness)
    except Exception:
        return [False, False]
        
    if R_vars is None or I_gens is None or x_val is None:
        return [False, False]
        
    try:
        if not isinstance(I_gens, (list, tuple, set)):
            return [False, False]
        for p in I_gens:
            if not hasattr(p, 'free_symbols') and not isinstance(p, (int, float)):
                return [False, False]
    except Exception:
        return [False, False]
        
    try:
        x_val = x_val if isinstance(x_val, Symbol) else Symbol(str(x_val))
        R_vars_sym = []
        seen = set()
        for v in R_vars:
            v_sym = v if isinstance(v, Symbol) else Symbol(str(v))
            if v_sym not in seen:
                seen.add(v_sym)
                R_vars_sym.append(v_sym)
        R_vars = R_vars_sym
    except Exception:
        return [False, False]

    # H1: I is an ideal of R
    # Any valid list of polynomials generates an ideal in the polynomial ring Q[R_vars].
    h1 = True
    
    # neg_Q: R[x]/<I, x> is NOT isomorphic to R/I
    # If x is a new variable (not in R_vars), R[x]/<I, x> is isomorphic to R/I, so the conclusion holds (neg_Q = False).
    # If x is already in R_vars, R[x] is just R. For a Noetherian ring R, R/<I, x> is isomorphic to R/I 
    # if and only if x is in I. Thus, the conclusion fails (neg_Q = True) iff x is NOT in I.
    try:
        if x_val not in R_vars:
            neg_q = False
        else:
            non_zero_gens = [g for g in I_gens if g != 0]
            if not non_zero_gens:
                neg_q = True
            else:
                G = sympy.groebner(non_zero_gens, *R_vars)
                rem = G.reduce(x_val)[1]
                neg_q = (rem != 0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = ['H_1: I is an ideal of R', 'not Q: The factor ring is not isomorphic to R/I']
N_HYP = 1
NEG_Q_INDEX = 1