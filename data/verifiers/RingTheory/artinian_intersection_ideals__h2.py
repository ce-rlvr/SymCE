import sympy
from sympy import symbols, Dummy, Poly, groebner
from sympy.abc import x, y, z, t, u, v, w
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_artinian_poly(I_gens, vars):
    if not vars:
        return True
    try:
        G = groebner(I_gens, *vars)
        if len(G) == 1 and G[0].is_constant() and G[0] != 0:
            return True
        for var in vars:
            has_pure_power = False
            for g in G:
                p = Poly(g, *vars)
                lm = p.LM()
                v_idx = vars.index(var)
                if lm[v_idx] > 0 and all(lm[i] == 0 for i in range(len(vars)) if i != v_idx):
                    has_pure_power = True
                    break
            if not has_pure_power:
                return False
        return True
    except Exception:
        return False

def intersect_ideals(I_gens, J_gens, vars):
    t_dummy = Dummy('t')
    tI = [t_dummy * p for p in I_gens]
    _1tJ = [(1 - t_dummy) * p for p in J_gens]
    try:
        G = groebner(tI + _1tJ, t_dummy, *vars, order='lex')
        intersection_gens = []
        for g in G:
            if t_dummy not in g.free_symbols:
                intersection_gens.append(g)
        return intersection_gens
    except Exception:
        return []

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R, I, J = witness
            elif len(witness) == 2:
                I, J = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        from sympy import Integer
        if isinstance(I, (int, Integer)) and isinstance(J, (int, Integer)):
            I = int(I)
            J = int(J)
            h1 = True
            h2 = (I != 0)
            h3 = (J != 0)
            import math
            I_cap_J = abs(I * J) // math.gcd(I, J) if I and J else 0
            q = (I_cap_J != 0)
            return [h1, h2, h3, not q]
            
        if isinstance(I, (list, tuple)) and isinstance(J, (list, tuple)):
            I = list(I)
            J = list(J)
            vars_set = set()
            for p in I + J:
                if hasattr(p, 'free_symbols'):
                    vars_set.update(p.free_symbols)
            vars_list = sorted(list(vars_set), key=lambda sym: sym.name)
            
            if not vars_list:
                return [True, True, True, False]
                
            h1 = True
            h2 = is_artinian_poly(I, vars_list)
            h3 = is_artinian_poly(J, vars_list)
            
            I_cap_J = intersect_ideals(I, J, vars_list)
            q = is_artinian_poly(I_cap_J, vars_list)
            
            return [h1, h2, h3, not q]
            
        return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: The quotient ring R/I is Artinian",
    "H_3: The quotient ring R/J is Artinian",
    "¬Q: The quotient ring R/(I \\cap J) is not Artinian"
]

N_HYP = 3
NEG_Q_INDEX = 3