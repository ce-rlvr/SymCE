import sympy
from sympy import symbols, Rational, Integer
import itertools
import math
import functools

# Top-level setup
x, y, z = symbols('x y z')

def normalize_witness(witness):
    if isinstance(witness, dict) and 'n' in witness:
        n = witness['n']
        add = witness['add']
        mul = witness['mul']
        I = witness['I']
    elif isinstance(witness, (tuple, list)) and len(witness) == 4:
        n, add, mul, I = witness
    else:
        elements = list(witness.elements)
        add_func = witness.add
        mul_func = witness.mul
        I_elems = list(witness.ideal)
        n = len(elements)
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        def get_val(f, u, v):
            if isinstance(f, dict):
                return f[(u, v)]
            elif callable(f):
                return f(u, v)
            else:
                return f[u][v]
                
        add_table = [[elem_to_idx[get_val(add_func, u, v)] for v in elements] for u in elements]
        mul_table = [[elem_to_idx[get_val(mul_func, u, v)] for v in elements] for u in elements]
        I_idx = [elem_to_idx[u] for u in I_elems]
        return n, add_table, mul_table, I_idx

    def to_table(f):
        if isinstance(f, dict):
            return [[f[(i, j)] for j in range(n)] for i in range(n)]
        elif callable(f):
            return [[f(i, j) for j in range(n)] for i in range(n)]
        else:
            return f

    return n, to_table(add), to_table(mul), list(I)

def conditions(witness):
    try:
        n, add, mul, I = normalize_witness(witness)
    except Exception:
        return [False, False, False, False]
        
    try:
        # Find zero
        zero = None
        for i in range(n):
            if all(add[i][j] == j and add[j][i] == j for j in range(n)):
                zero = i
                break
                
        if zero is None:
            return [False, False, False, False]
            
        # Check if R is a ring
        is_ring = True
        for i in range(n):
            if not is_ring: break
            for j in range(n):
                if not is_ring: break
                for k in range(n):
                    if add[add[i][j]][k] != add[i][add[j][k]]: 
                        is_ring = False; break
                    if mul[mul[i][j]][k] != mul[i][mul[j][k]]: 
                        is_ring = False; break
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: 
                        is_ring = False; break
                    if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: 
                        is_ring = False; break
                        
        for i in range(n):
            if not is_ring: break
            for j in range(n):
                if add[i][j] != add[j][i]: 
                    is_ring = False; break
                    
        for i in range(n):
            if not is_ring: break
            has_inv = False
            for j in range(n):
                if add[i][j] == zero:
                    has_inv = True
                    break
            if not has_inv: 
                is_ring = False; break

        # Check if I is an ideal
        is_ideal = is_ring
        if is_ideal:
            if zero not in I:
                is_ideal = False
            for u in I:
                if not is_ideal: break
                for v in I:
                    if add[u][v] not in I:
                        is_ideal = False; break
                inv_u = None
                for v in range(n):
                    if add[u][v] == zero:
                        inv_u = v
                        break
                if inv_u not in I:
                    is_ideal = False; break
                for r in range(n):
                    if mul[u][r] not in I:
                        is_ideal = False; break
                    if mul[r][u] not in I:
                        is_ideal = False; break

        h1 = is_ideal
        h2 = is_ideal  # \pi is canonical projection, well-defined if I is an ideal
        h3 = is_ring   # Z(R) is the center of R, well-defined if R is a ring

        if not is_ideal:
            return [h1, h2, h3, False]

        # Compute Z(R)
        Z_R = []
        for i in range(n):
            is_center = True
            for j in range(n):
                if mul[i][j] != mul[j][i]:
                    is_center = False
                    break
            if is_center:
                Z_R.append(i)

        # Compute R/I
        def get_coset(r):
            return frozenset(add[r][u] for u in I)

        cosets = set(get_coset(r) for r in range(n))

        # Compute Z(R/I)
        Z_R_mod_I = set()
        for C in cosets:
            is_center = True
            for D in cosets:
                r = next(iter(C))
                s = next(iter(D))
                if get_coset(mul[r][s]) != get_coset(mul[s][r]):
                    is_center = False
                    break
            if is_center:
                Z_R_mod_I.add(C)

        # Compute \pi(Z(R))
        pi_Z_R = set(get_coset(z_elem) for z_elem in Z_R)

        # Conclusion: \pi(Z(R)) is contained in Z(R/I)
        conclusion = pi_Z_R.issubset(Z_R_mod_I)
        neg_q = not conclusion

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: \\pi: R -> R/I is the canonical projection",
    "H_3: Z(R) is the center of R",
    "¬Q: The image \\pi(Z(R)) is not contained in the center of R/I"
]

N_HYP = 3
NEG_Q_INDEX = 3