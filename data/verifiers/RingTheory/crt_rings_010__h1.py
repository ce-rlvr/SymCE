import sympy
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
# Counterexample: R = 2Z / 12Z
# Elements: 0, 2, 4, 6, 8, 10 mapped to indices 0, 1, 2, 3, 4, 5
R_add = [[(i + j) % 6 for j in range(6)] for i in range(6)]
R_mul = [[(2 * i * j) % 6 for j in range(6)] for i in range(6)]
I_ideal = [0, 2, 4] # corresponds to {0, 4, 8}
J_ideal = [0, 3]    # corresponds to {0, 6}

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I + J = R",
    "H_3: I \\cap J = \\{0\\}",
    "¬Q: There does not exist a unique idempotent e in R such that I = <1-e> and J = <e>"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, dict):
            R_add_w = witness['add']
            R_mul_w = witness['mul']
            I_w = witness['I']
            J_w = witness['J']
        else:
            R_add_w, R_mul_w, I_w, J_w = witness
            
        if hasattr(R_add_w, 'tolist'):
            R_add_w = R_add_w.tolist()
        if hasattr(R_mul_w, 'tolist'):
            R_mul_w = R_mul_w.tolist()
            
        n = len(R_add_w)
        elements = list(range(n))
        
        # Find zero element
        zero = None
        for i in elements:
            if all(R_add_w[i][j] == j for j in elements) and all(R_add_w[j][i] == j for j in elements):
                zero = i
                break
        if zero is None:
            return [False, False, False, False]
            
        # Check if R is a valid ring
        is_abelian_add = all(R_add_w[i][j] == R_add_w[j][i] for i in elements for j in elements)
        is_assoc_add = all(R_add_w[R_add_w[i][j]][k] == R_add_w[i][R_add_w[j][k]] for i in elements for j in elements for k in elements)
        has_inv_add = all(any(R_add_w[i][j] == zero for j in elements) for i in elements)
        is_assoc_mul = all(R_mul_w[R_mul_w[i][j]][k] == R_mul_w[i][R_mul_w[j][k]] for i in elements for j in elements for k in elements)
        is_dist_left = all(R_mul_w[i][R_add_w[j][k]] == R_add_w[R_mul_w[i][j]][R_mul_w[i][k]] for i in elements for j in elements for k in elements)
        is_dist_right = all(R_mul_w[R_add_w[i][j]][k] == R_add_w[R_mul_w[i][k]][R_mul_w[j][k]] for i in elements for j in elements for k in elements)
        
        if not (is_abelian_add and is_assoc_add and has_inv_add and is_assoc_mul and is_dist_left and is_dist_right):
            return [False, False, False, False]
            
        # H1: I and J are ideals of R
        def is_ideal(S):
            if not S: return False
            if zero not in S: return False
            for a in S:
                for b in S:
                    if R_add_w[a][b] not in S: return False
            for a in S:
                inv_a = next(x for x in elements if R_add_w[a][x] == zero)
                if inv_a not in S: return False
            for a in S:
                for r in elements:
                    if R_mul_w[r][a] not in S: return False
                    if R_mul_w[a][r] not in S: return False
            return True
            
        h1 = is_ideal(I_w) and is_ideal(J_w)
        
        # H2: I + J = R
        sums = set()
        for a in I_w:
            for b in J_w:
                sums.add(R_add_w[a][b])
        h2 = (sums == set(elements))
        
        # H3: I \cap J = {0}
        h3 = (set(I_w).intersection(set(J_w)) == {zero})
        
        # Conclusion: There exists a unique idempotent e in R such that I = <1-e> and J = <e>
        # If R lacks an identity, 1-e is undefined, so the conclusion fails.
        one = None
        for i in elements:
            if all(R_mul_w[i][j] == j for j in elements) and all(R_mul_w[j][i] == j for j in elements):
                one = i
                break
                
        def ideal_generated_by(x):
            gen = {x}
            while True:
                new_gen = set(gen)
                for a in gen:
                    inv_a = next(k for k in elements if R_add_w[a][k] == zero)
                    new_gen.add(inv_a)
                    for b in gen:
                        new_gen.add(R_add_w[a][b])
                    for r in elements:
                        new_gen.add(R_mul_w[r][a])
                        new_gen.add(R_mul_w[a][r])
                if len(new_gen) == len(gen):
                    break
                gen = new_gen
            return gen

        if one is None:
            neg_q = True
        else:
            valid_e_count = 0
            for e in elements:
                if R_mul_w[e][e] == e:
                    inv_e = next(x for x in elements if R_add_w[e][x] == zero)
                    one_minus_e = R_add_w[one][inv_e]
                    
                    ideal_e = ideal_generated_by(e)
                    ideal_one_minus_e = ideal_generated_by(one_minus_e)
                    
                    if set(I_w) == ideal_one_minus_e and set(J_w) == ideal_e:
                        valid_e_count += 1
            
            neg_q = (valid_e_count != 1)
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]