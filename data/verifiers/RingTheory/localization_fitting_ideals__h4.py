import math
import itertools
from sympy import Matrix, expand, gcd, simplify, fraction, eye, zeros, symbols, groebner, reduced

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
x, y, z = symbols('x y z')

class IdealMembershipError(Exception):
    pass

def in_ideal(elem, generators, provided_vars=None):
    if provided_vars is not None and len(provided_vars) > 0:
        vars = provided_vars
    else:
        free_symbols = set()
        if hasattr(elem, 'free_symbols'):
            free_symbols.update(elem.free_symbols)
        for g in generators:
            if hasattr(g, 'free_symbols'):
                free_symbols.update(g.free_symbols)
        vars = list(free_symbols)
        
    if not vars:
        if not generators:
            return elem == 0
        g = generators[0]
        for gen in generators[1:]:
            g = gcd(g, gen)
        if g == 0:
            return elem == 0
        try:
            return (elem % g) == 0
        except Exception:
            try:
                return fraction(simplify(elem / g))[1] == 1
            except Exception:
                raise IdealMembershipError()
    else:
        if not generators:
            return expand(elem) == 0
        if expand(elem) == 0:
            return True
        try:
            gb = groebner(generators, *vars)
            rem = reduced(elem, gb, *vars)[1]
            return expand(rem) == 0
        except Exception:
            raise IdealMembershipError()

def fitting_ideal(A, k):
    m = A.rows
    n = A.cols
    size = m - k
    if size <= 0:
        return [1]
    if size > min(m, n):
        return [0]
    
    row_indices = list(itertools.combinations(range(m), size))
    col_indices = list(itertools.combinations(range(n), size))
    minors = []
    for rows in row_indices:
        for cols in col_indices:
            submatrix = A[list(rows), list(cols)]
            minors.append(submatrix.det())
    return minors

def conditions(witness) -> list[bool]:
    res = [False, False, False, False]
    try:
        if not isinstance(witness, dict):
            w = {}
            for attr in ['A', 'S', 'S_generator', 'k', 'vars', 'R_is_commutative']:
                if hasattr(witness, attr):
                    w[attr] = getattr(witness, attr)
            witness = w

        A = witness.get('A')
        S = witness.get('S', [])
        S_gen = witness.get('S_generator', None)
        k = witness.get('k', 0)
        vars = witness.get('vars', [])
        
        # H1: R is a commutative ring
        res[0] = bool(witness.get('R_is_commutative', True))
        
        # H2: M is a finitely presented R-module
        res[1] = isinstance(A, Matrix)
        
        # H3: S is a multiplicatively closed subset of R
        if S_gen is not None:
            res[2] = True
        elif S:
            has_one = any(expand(s - 1) == 0 for s in S)
            if has_one:
                closed = True
                for s1 in S:
                    for s2 in S:
                        if not any(expand(s1*s2 - s) == 0 for s in S):
                            closed = False
                            break
                    if not closed:
                        break
                res[2] = closed
        else:
            res[2] = False
            
        # neg_Q: Fitt_k(S^{-1}M) != S^{-1}Fitt_k(M)
        if res[1] and res[2]:
            I_A = fitting_ideal(A, k)
            I_B = I_A  # S^{-1}M is canonically presented by the same matrix A over S^{-1}R
            
            if S_gen is not None:
                def check_subset_gen(I1, I2, f):
                    for elem in I1:
                        found = False
                        for p in range(6):
                            if in_ideal((f**p)*elem, I2, vars):
                                found = True
                                break
                        if not found:
                            return False
                    return True
                eq = check_subset_gen(I_A, I_B, S_gen) and check_subset_gen(I_B, I_A, S_gen)
            else:
                def check_subset(I1, I2):
                    for elem in I1:
                        found = False
                        for s in S:
                            if in_ideal(s*elem, I2, vars):
                                found = True
                                break
                        if not found:
                            return False
                    return True
                eq = check_subset(I_A, I_B) and check_subset(I_B, I_A)
                
            res[3] = not eq
            
    except Exception:
        pass
        
    return res

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is a finitely presented R-module",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: Fitt_k(S^{-1}M) != S^{-1}Fitt_k(M)"
]

N_HYP = 3
NEG_Q_INDEX = 3