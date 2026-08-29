import sympy
from sympy import symbols

# Top-level setup
x, y, z = symbols('x y z')
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    witness must have:
    - rings: list or dict of ring objects
    - transitions: dict mapping (i, j) to a function f(x)
    - limit: ring object
    - limit_maps: list or dict of functions phi_i(x)
    - (optional) I: list of indices
    - (optional) leq: function leq(i, j)
    
    Each ring object must have:
    - elements: list of elements
    - zero: the zero element
    - one: the one element
    - add(a, b): function returning a + b
    - mul(a, b): function returning a * b
    """
    
    def is_ring(R):
        try:
            elements = R.elements
            zero = R.zero
            if zero not in elements: return False
            for a in elements:
                if R.add(a, zero) != a: return False
                if R.add(zero, a) != a: return False
                if not any(R.add(a, b) == zero for b in elements): return False
                for b in elements:
                    if R.add(a, b) not in elements: return False
                    if R.mul(a, b) not in elements: return False
                    if R.add(a, b) != R.add(b, a): return False
            for a in elements:
                for b in elements:
                    for c in elements:
                        if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)): return False
                        if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)): return False
                        if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): return False
                        if R.mul(R.add(a, b), c) != R.add(R.mul(a, c), R.mul(b, c)): return False
            return True
        except Exception:
            return False

    def is_integral_domain(R):
        try:
            elements = R.elements
            zero = R.zero
            one = R.one
            if one not in elements: return False
            if one == zero: return False
            for a in elements:
                if R.mul(a, one) != a: return False
                if R.mul(one, a) != a: return False
                for b in elements:
                    if R.mul(a, b) != R.mul(b, a): return False
                    if a != zero and b != zero and R.mul(a, b) == zero: return False
            return True
        except Exception:
            return False

    def check_h1(witness):
        try:
            if hasattr(witness, 'I'):
                I = witness.I
                leq = witness.leq
                rings = witness.rings
                limit_maps = witness.limit_maps
            else:
                I = list(range(len(witness.rings)))
                leq = lambda i, j: i <= j
                rings = {i: witness.rings[i] for i in I}
                limit_maps = {i: witness.limit_maps[i] for i in I}
                
            transitions = witness.transitions
            limit = witness.limit
            
            if len(I) == 0: return False
            
            # Check directed set properties
            for i in I:
                if not leq(i, i): return False
                for j in I:
                    for k in I:
                        if leq(i, j) and leq(j, k) and not leq(i, k): return False
            for i in I:
                for j in I:
                    if not any(leq(i, k) and leq(j, k) for k in I): return False
                    
            # Check rings
            for i in I:
                if not is_ring(rings[i]): return False
            if not is_ring(limit): return False
            
            # Check transitions
            for i in I:
                for j in I:
                    if leq(i, j):
                        if (i, j) not in transitions: return False
                        f = transitions[(i, j)]
                        R_i = rings[i]
                        R_j = rings[j]
                        for a in R_i.elements:
                            for b in R_i.elements:
                                if f(R_i.add(a, b)) != R_j.add(f(a), f(b)): return False
                                if f(R_i.mul(a, b)) != R_j.mul(f(a), f(b)): return False
                                
            for i in I:
                f_ii = transitions[(i, i)]
                for a in rings[i].elements:
                    if f_ii(a) != a: return False
                    
            for i in I:
                for j in I:
                    for k in I:
                        if leq(i, j) and leq(j, k):
                            f_ij = transitions[(i, j)]
                            f_jk = transitions[(j, k)]
                            f_ik = transitions[(i, k)]
                            for a in rings[i].elements:
                                if f_jk(f_ij(a)) != f_ik(a): return False
                                
            # Check direct limit properties
            for i in I:
                for j in I:
                    if leq(i, j):
                        f_ij = transitions[(i, j)]
                        phi_i = limit_maps[i]
                        phi_j = limit_maps[j]
                        for a in rings[i].elements:
                            if phi_j(f_ij(a)) != phi_i(a): return False
                            
            for x in limit.elements:
                found = False
                for i in I:
                    phi_i = limit_maps[i]
                    if any(phi_i(a) == x for a in rings[i].elements):
                        found = True
                        break
                if not found: return False
                
            for i in I:
                phi_i = limit_maps[i]
                for a in rings[i].elements:
                    for b in rings[i].elements:
                        if phi_i(a) == phi_i(b):
                            found = False
                            for j in I:
                                if leq(i, j):
                                    f_ij = transitions[(i, j)]
                                    if f_ij(a) == f_ij(b):
                                        found = True
                                        break
                            if not found: return False
                        else:
                            for j in I:
                                if leq(i, j):
                                    f_ij = transitions[(i, j)]
                                    if f_ij(a) == f_ij(b): return False
                                    
            for i in I:
                phi_i = limit_maps[i]
                R_i = rings[i]
                for a in R_i.elements:
                    for b in R_i.elements:
                        if phi_i(R_i.add(a, b)) != limit.add(phi_i(a), phi_i(b)): return False
                        if phi_i(R_i.mul(a, b)) != limit.mul(phi_i(a), phi_i(b)): return False
                        
            return True
        except Exception:
            return False

    def check_h2(witness):
        try:
            if hasattr(witness, 'I'):
                if isinstance(witness.rings, dict):
                    rings_list = witness.rings.values()
                else:
                    rings_list = witness.rings
            else:
                rings_list = witness.rings
            for R in rings_list:
                if not is_integral_domain(R): return False
            return True
        except Exception:
            return False

    def check_neg_q(witness):
        try:
            limit = witness.limit
            return not is_integral_domain(limit)
        except Exception:
            return False

    return [check_h1(witness), check_h2(witness), check_neg_q(witness)]

CONDITION_LABELS = [
    "H_1: {R_i, f_{ij}} is a directed system of rings over a directed set I",
    "H_2: For every i in I, R_i is an integral domain",
    "¬Q: The direct limit is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2