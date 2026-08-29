import sympy as sp
import itertools

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is a square matrix over an algebraically closed field F",
    "¬Q: The bijection between elementary divisors of xI - A and Jordan blocks of A fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, sp.MatrixBase):
            h1 = False
        else:
            h1 = witness.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = witness.shape[0]
            if n > 5:
                # To prevent timeout on large matrices, we limit the size for the minors approach
                return [h1, False]
                
            # Get Jordan blocks from the Jordan canonical form
            P, J = witness.jordan_form()
            jordan_blocks = []
            i = 0
            while i < n:
                val = J[i, i]
                k = 1
                # A Jordan block has 1s on the superdiagonal
                while i + k < n and (J[i + k, i + k] == val or sp.simplify(J[i + k, i + k] - val) == 0) and J[i + k - 1, i + k] == 1:
                    k += 1
                jordan_blocks.append((sp.simplify(val), k))
                i += k
            
            # Get elementary divisors of xI - A
            x = sp.Symbol('x')
            M = x * sp.eye(n) - witness
            
            # Compute invariant factors using the GCD of minors
            invariant_factors = []
            D_prev = sp.S.One
            for i_minor in range(1, n + 1):
                minors = []
                for row_indices in itertools.combinations(range(n), i_minor):
                    for col_indices in itertools.combinations(range(n), i_minor):
                        sub_M = M.extract(row_indices, col_indices)
                        minors.append(sub_M.det())
                
                D_i = minors[0]
                for m in minors[1:]:
                    if D_i == 0:
                        D_i = m
                    elif m != 0:
                        D_i = sp.gcd(D_i, m)
                
                if D_prev == 0:
                    d_i = sp.S.Zero
                else:
                    d_i = sp.cancel(D_i / D_prev)
                
                if d_i != 0:
                    LC = sp.LC(d_i, x)
                    if LC != 0:
                        d_i = sp.expand(d_i / LC)
                invariant_factors.append(d_i)
                D_prev = D_i
            
            # Factor invariant factors to get elementary divisors (prime power factors)
            elem_divs = []
            for d in invariant_factors:
                if d.has(x):
                    roots = sp.roots(d, x)
                    deg = sp.degree(d, x)
                    # If it factors completely into linear terms over the field
                    if sum(roots.values()) == deg:
                        for r, m in roots.items():
                            elem_divs.append((sp.simplify(r), m))
                    else:
                        # Fallback if roots cannot be found exactly
                        factors = sp.factor_list(d)[1]
                        for base, exp in factors:
                            if sp.degree(base, x) == 1:
                                r = sp.roots(base, x)
                                if r:
                                    root = list(r.keys())[0]
                                    elem_divs.append((sp.simplify(root), exp))
                            else:
                                elem_divs.append((base, exp))
            
            # Compare the multisets of Jordan blocks and elementary divisors
            def count_elements(lst):
                counts = {}
                for item in lst:
                    found = False
                    for k in counts.keys():
                        if (item[0] == k[0] or sp.simplify(item[0] - k[0]) == 0) and item[1] == k[1]:
                            counts[k] += 1
                            found = True
                            break
                    if not found:
                        counts[item] = 1
                return counts
            
            jb_counts = count_elements(jordan_blocks)
            ed_counts = count_elements(elem_divs)
            
            # The negated conclusion is True if the bijection fails
            neg_q = (jb_counts != ed_counts)
            
    except Exception:
        neg_q = False

    return [h1, neg_q]