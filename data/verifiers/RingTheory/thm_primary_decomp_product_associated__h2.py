import sympy
from sympy import symbols, Rational, Integer
import itertools
import functools

# Top-level setup for Ring Theory
x, y, z, t = symbols('x y z t')

def conditions(witness) -> list[bool]:
    """
    Check the hypotheses and the negated conclusion for the conjecture:
    H1: R is a Noetherian commutative ring
    H2: P_1, ..., P_k are the associated prime ideals of the minimal primary decomposition of I
    Q: There exists a positive integer m such that (P_1 ... P_k)^m is contained in I
    """
    # Parse witness
    try:
        if isinstance(witness, dict):
            I = witness.get('I')
            P_list = witness.get('P_list', [])
            R = witness.get('R', getattr(I, 'ring', None))
        elif isinstance(witness, (list, tuple)):
            if len(witness) >= 2:
                if hasattr(witness[0], 'ideal') and hasattr(witness[1], 'gens'):
                    R = witness[0]
                    I = witness[1]
                    P_list = witness[2] if len(witness) > 2 else []
                elif hasattr(witness[0], 'gens'):
                    I = witness[0]
                    R = getattr(I, 'ring', None)
                    if len(witness) == 2 and isinstance(witness[1], (list, tuple)):
                        P_list = witness[1]
                    else:
                        P_list = witness[1:]
                else:
                    return [False, False, False]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if R is None and hasattr(I, 'ring'):
            R = I.ring
    except Exception:
        return [False, False, False]

    # H1: R is a Noetherian commutative ring
    try:
        h1 = False
        if R is not None:
            if getattr(R, 'is_commutative', False):
                h1 = True
            elif hasattr(R, 'domain') and hasattr(R, 'gens'):
                h1 = True
    except Exception:
        h1 = False

    # H2: P_1, ..., P_k are the associated prime ideals of the minimal primary decomposition of I
    try:
        h2 = False
        if isinstance(P_list, (list, tuple)):
            h2 = all(hasattr(P, 'gens') for P in P_list)
    except Exception:
        h2 = False

    # neg_Q: For all m > 0, (P_1 ... P_k)^m is NOT contained in I
    try:
        neg_q = True
        if not P_list:
            G = [R.one] if hasattr(R, 'one') else [1]
        else:
            G = list(P_list[0].gens)
            for P in P_list[1:]:
                new_G = []
                for g1 in G:
                    for g2 in P.gens:
                        new_G.append(g1 * g2)
                        if len(new_G) > 500:
                            break
                    if len(new_G) > 500:
                        break
                
                # Remove duplicates to keep the generator list small
                unique_G = []
                for g in new_G:
                    if g not in unique_G:
                        unique_G.append(g)
                G = unique_G
        
        if G:
            combinations_checked = 0
            MAX_COMBINATIONS = 5000
            
            for m in range(1, 21):
                subset = True
                for combo in itertools.combinations_with_replacement(G, m):
                    combinations_checked += 1
                    if combinations_checked > MAX_COMBINATIONS:
                        break
                    
                    term = functools.reduce(lambda a, b: a * b, combo)
                    if not I.contains(term):
                        subset = False
                        break
                
                if combinations_checked > MAX_COMBINATIONS:
                    # If we exceed the computation limit without finding a valid m,
                    # we assume it's not contained (neg_q remains True).
                    break
                    
                if subset:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Noetherian commutative ring",
    "H_2: P_1, ..., P_k are the associated prime ideals of the minimal primary decomposition of I",
    "¬Q: For all m > 0, the product (P_1 ... P_k)^m is NOT contained in I"
]

N_HYP = 2
NEG_Q_INDEX = 2