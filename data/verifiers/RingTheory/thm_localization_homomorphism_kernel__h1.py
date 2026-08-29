import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def contains(lst, item):
    for x in lst:
        if x == item:
            return True
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be provided as:
      - A tuple (R_elements, S_elements) where elements support + and * (e.g., SymPy matrices)
      - A tuple (R_elements, add_func, mul_func, zero_elem, S_elements)
    """
    try:
        if len(witness) == 2:
            R_elements, S_elements = witness
            R_elements = list(R_elements)
            S_elements = list(S_elements)
            if not R_elements:
                return [False, False, False]
            
            def add(x, y): return x + y
            def mul(x, y): return x * y
            zero = R_elements[0] - R_elements[0]
            
        elif len(witness) == 5:
            R_elements, add_func, mul_func, zero_elem, S_elements = witness
            R_elements = list(R_elements)
            S_elements = list(S_elements)
            add = add_func
            mul = mul_func
            zero = zero_elem
        else:
            return [False, False, False]
            
        # Remove duplicates to ensure clean set-like operations
        unique_R = []
        for r in R_elements:
            if not contains(unique_R, r):
                unique_R.append(r)
        R_elements = unique_R

        unique_S = []
        for s in S_elements:
            if not contains(unique_S, s):
                unique_S.append(s)
        S_elements = unique_S

        # H_1: S is a multiplicatively closed subset of R
        # We also implicitly verify that R is a valid ring (closed under + and *)
        h1 = True
        for a in R_elements:
            for b in R_elements:
                if not contains(R_elements, add(a, b)):
                    h1 = False
                    break
                if not contains(R_elements, mul(a, b)):
                    h1 = False
                    break
            if not h1:
                break
                
        if h1:
            if not contains(R_elements, zero):
                h1 = False
            else:
                for a in R_elements:
                    if add(a, zero) != a or add(zero, a) != a:
                        h1 = False
                        break

        if h1:
            for s in S_elements:
                if not contains(R_elements, s):
                    h1 = False
                    break
        if h1:
            for a in S_elements:
                for b in S_elements:
                    if not contains(S_elements, mul(a, b)):
                        h1 = False
                        break
                        
        # H_2: f is the natural ring homomorphism defined by f(r) = r/1
        # This is a definitional hypothesis.
        h2 = True
        
        # ¬Q: The kernel of f is NOT {r in R | sr = 0 for some s in S}
        # First, compute K = {r in R | sr = 0 for some s in S}
        K = []
        for r in R_elements:
            for s in S_elements:
                if mul(s, r) == zero:
                    if not contains(K, r):
                        K.append(r)
                    break
                    
        # Compute ker(f) for the finite ring R.
        # ker(f) is the smallest ideal I such that S maps to units in R/I.
        # For finite rings, this is equivalent to finding the smallest ideal I 
        # such that for all s in S, sx in I implies x in I, and xs in I implies x in I.
        ker_f = [zero]
        changed = True
        while changed:
            changed = False
            new_elements = []
            for s in S_elements:
                for x in R_elements:
                    if not contains(ker_f, x):
                        if contains(ker_f, mul(s, x)) or contains(ker_f, mul(x, s)):
                            new_elements.append(x)
            
            if new_elements:
                I_new = list(ker_f)
                added_last_round = []
                for nx in new_elements:
                    if not contains(I_new, nx):
                        I_new.append(nx)
                        added_last_round.append(nx)
                
                # Generate the ideal closed under addition and multiplication by R
                closed = False
                while not closed:
                    closed = True
                    new_this_round = []
                    
                    for a in added_last_round:
                        for b in I_new:
                            sm1 = add(a, b)
                            if not contains(I_new, sm1) and not contains(new_this_round, sm1):
                                new_this_round.append(sm1)
                            sm2 = add(b, a)
                            if not contains(I_new, sm2) and not contains(new_this_round, sm2):
                                new_this_round.append(sm2)
                                
                    for a in added_last_round:
                        for r in R_elements:
                            p1 = mul(r, a)
                            if not contains(I_new, p1) and not contains(new_this_round, p1):
                                new_this_round.append(p1)
                            p2 = mul(a, r)
                            if not contains(I_new, p2) and not contains(new_this_round, p2):
                                new_this_round.append(p2)
                                
                    if new_this_round:
                        I_new.extend(new_this_round)
                        added_last_round = new_this_round
                        closed = False
                        
                if len(I_new) > len(ker_f):
                    ker_f = I_new
                    changed = True
                    
        # Since K is always a subset of ker_f by construction, 
        # they are unequal if and only if their sizes differ.
        neg_q = (len(ker_f) != len(K))
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: f is the natural ring homomorphism defined by f(r) = r/1",
    "¬Q: The kernel of f is not {r in R | sr = 0 for some s in S}"
]

N_HYP = 2
NEG_Q_INDEX = 2