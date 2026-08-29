import sympy
from sympy import symbols, expand, Dummy, sympify, div, reduced, groebner
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

x, y, z, t, u, v = symbols('x y z t u v')

def ideal_subset(I, J, vars):
    if not J or all(expand(p) == 0 for p in J):
        return all(expand(p) == 0 for p in I)
    
    J_gens = [p for p in J if expand(p) != 0]
    if not J_gens:
        return all(expand(p) == 0 for p in I)
        
    gb = groebner(J_gens, *vars, domain='QQ')
    for p in I:
        rem = reduced(p, gb, *vars, domain='QQ')[1]
        if rem != 0:
            return False
    return True

def ideal_intersection(I, J, vars):
    I_zero = not I or all(expand(p) == 0 for p in I)
    J_zero = not J or all(expand(q) == 0 for q in J)
    if I_zero or J_zero:
        return [sympify(0)]
    
    t_dummy = Dummy('dummy_t')
    gens = [expand(t_dummy * p) for p in I] + [expand((1 - t_dummy) * q) for q in J]
    gens = [g for g in gens if g != 0]
    if not gens:
        return [sympify(0)]
        
    gb = groebner(gens, t_dummy, *vars, order='lex', domain='QQ')
    return [p for p in gb if not p.has(t_dummy)]

def ideal_quotient_principal(I, g, vars):
    if expand(g) == 0:
        return [sympify(1)]
    intersect = ideal_intersection(I, [g], vars)
    res = []
    for p in intersect:
        q, r = div(p, g, *vars, domain='QQ')
        if r == 0:
            res.append(q)
    return res

def ideal_quotient(I, J, vars):
    if not J or all(expand(j) == 0 for j in J):
        return [sympify(1)]
    
    J_gens = [j for j in J if expand(j) != 0]
    if not J_gens:
        return [sympify(1)]
        
    res = ideal_quotient_principal(I, J_gens[0], vars)
    for g in J_gens[1:]:
        res = ideal_intersection(res, ideal_quotient_principal(I, g, vars), vars)
    return res

def ideal_multiply(I, J):
    if not I or not J:
        return [sympify(0)]
    return [expand(p * q) for p in I for q in J]

def ideal_equality(I, J, vars):
    return ideal_subset(I, J, vars) and ideal_subset(J, I, vars)

def conditions(witness):
    try:
        I, J = witness
    except Exception:
        return [False, False]
        
    try:
        from sympy import Expr
        if not isinstance(I, (list, tuple)) or not isinstance(J, (list, tuple)):
            h1 = False
        else:
            h1 = all(isinstance(p, (Expr, int)) for p in list(I) + list(J))
    except Exception:
        h1 = False

    try:
        vars_set = set()
        for p in list(I) + list(J):
            if hasattr(p, 'free_symbols'):
                vars_set.update(p.free_symbols)
        vars = sorted(list(vars_set), key=lambda s: s.name)
        
        if not vars:
            # If there are no variables, the elements are constants (e.g. in QQ or ZZ).
            # These rings are PIDs/fields where the property always holds, so the conjecture cannot fail.
            neg_q = False
        else:
            subset = ideal_subset(I, J, vars)
            quotient = ideal_quotient(I, J, vars)
            prod = ideal_multiply(J, quotient)
            divides = ideal_equality(prod, I, vars)
            
            neg_q = not (subset == divides)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "¬Q: I ⊆ J is not equivalent to J divides I"
]

N_HYP = 1
NEG_Q_INDEX = 1