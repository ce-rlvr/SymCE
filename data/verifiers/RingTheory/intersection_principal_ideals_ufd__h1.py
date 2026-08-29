import sympy
from sympy import ZZ, QQ, Rational, Integer
from sympy.abc import x, y, z, w

def verify_ring_axioms(n, add, mul):
    # Commutativity
    for i in range(n):
        for j in range(i, n):
            if add[i][j] != add[j][i]: return False
            if mul[i][j] != mul[j][i]: return False
            
    # Associativity and Distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                
    # Additive identity
    zero = -1
    for z in range(n):
        if all(add[i][z] == i for i in range(n)):
            zero = z
            break
    if zero == -1: return False
    
    # Multiplicative identity
    one = -1
    for o in range(n):
        if all(mul[i][o] == i for i in range(n)):
            one = o
            break
    if one == -1: return False
    
    # Additive inverses
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False
        
    return True

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample.
    The witness can be provided in two formats:
    1. A finite ring tuple: (n, add_table, mul_table, a, b)
    2. A SymPy ring tuple: (R, a, b)
    """
    # 1. Try finite ring tuple
    if isinstance(witness, tuple) and len(witness) == 5 and isinstance(witness[0], int):
        try:
            n, add, mul, a, b = witness
            if not (isinstance(n, int) and 0 < n <= 128):
                pass
            elif verify_ring_axioms(n, add, mul):
                zero = -1
                for z in range(n):
                    if all(add[i][z] == i for i in range(n)):
                        zero = z
                        break
                
                h1 = (a != zero) and (b != zero)
                
                ideal_a = set(mul[a][i] for i in range(n))
                ideal_b = set(mul[b][i] for i in range(n))
                intersection = ideal_a.intersection(ideal_b)
                
                is_principal = False
                for g in range(n):
                    ideal_g = set(mul[g][i] for i in range(n))
                    if ideal_g == intersection:
                        is_principal = True
                        break
                        
                neg_q = not is_principal
                return [bool(h1), bool(neg_q)]
        except Exception:
            pass

    # 2. Try SymPy ring tuple
    try:
        R, a, b = witness
        h1 = (a != R.zero) and (b != R.zero)
        
        I_a = R.ideal(a)
        I_b = R.ideal(b)
        I_int = I_a.intersect(I_b)
        
        try:
            l = R.lcm(a, b)
            I_lcm = R.ideal(l)
            neg_q = (I_int != I_lcm)
        except Exception:
            # If lcm fails or is not implemented, check if the intersection is principal.
            # If it is not principal, then it cannot be equal to (lcm(a, b)).
            is_principal = False
            if hasattr(I_int, 'gens'):
                gens = I_int.gens
                if len(gens) == 1:
                    is_principal = True
                else:
                    for gen in gens:
                        try:
                            if R.ideal(gen) == I_int:
                                is_principal = True
                                break
                        except Exception:
                            pass
            else:
                # Fallback to avoid false positives if we can't inspect generators
                is_principal = True 
                
            neg_q = not is_principal
            
        return [bool(h1), bool(neg_q)]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "¬Q: The intersection (a) ∩ (b) is not equal to the principal ideal (lcm(a, b))"
]

N_HYP = 1
NEG_Q_INDEX = 1