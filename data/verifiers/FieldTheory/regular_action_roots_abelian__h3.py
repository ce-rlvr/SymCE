import sympy
from sympy import Symbol, factor_list, degree, RootOf, Poly
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

x = Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            f = witness[0]
        else:
            f = witness
            
        if isinstance(f, Poly):
            f = f.as_expr()
        else:
            f = sympy.sympify(f)
            
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        else:
            var = x
            
        facs = factor_list(f)[1]
        h1_ok = (len(facs) == 1 and facs[0][1] == 1 and degree(f, var) > 0)
    except Exception:
        h1_ok = False
        
    h2_ok = True
    
    try:
        n = degree(f, var)
        if n <= 1:
            neg_q_ok = False
        else:
            r = RootOf(f, 0)
            ext_facs = factor_list(f, extension=r)[1]
            splits_completely = all(degree(fac, var) == 1 for fac, mult in ext_facs)
            neg_q_ok = not splits_completely
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = ["H_1: f is irreducible", "H_2: L is splitting field", "~Q: Galois group does not act regularly"]
N_HYP = 2
NEG_Q_INDEX = 2