import sympy
import sympy.polys

def get_gens(I):
    if isinstance(I, (list, tuple)):
        return I
    elif hasattr(I, 'gens'):
        return I.gens
    else:
        return [I]

def ideal_contains(I1, I2):
    """Check if ideal I1 contains ideal I2 (i.e., I2 is a subset of I1)."""
    try:
        gens2 = get_gens(I2)
        if hasattr(I1, 'contains'):
            return all(I1.contains(g) for g in gens2)
        else:
            return all(g in I1 for g in gens2)
    except Exception:
        return False

def check_radical(Q, P):
    """Check if P is the radical of Q (heuristically)."""
    try:
        if not ideal_contains(P, Q):
            return False
        for g in get_gens(P):
            found = False
            for n in range(1, 15):
                if hasattr(Q, 'contains'):
                    if Q.contains(g**n):
                        found = True
                        break
                else:
                    if g**n in Q:
                        found = True
                        break
            if not found:
                return False
        return True
    except Exception:
        return False

def is_minimal_primary_decomposition(I, decomp):
    """
    decomp is a list of tuples (Q, P)
    Check if decomp is a minimal primary decomposition of I.
    """
    try:
        if not decomp:
            return False
            
        # 1. Intersection of Qs equals I
        int_Q = decomp[0][0]
        for Q, P in decomp[1:]:
            int_Q = int_Q.intersect(Q)
        if not (ideal_contains(I, int_Q) and ideal_contains(int_Q, I)):
            return False
            
        # 2. Irredundant: no Q can be omitted
        for i in range(len(decomp)):
            int_other = None
            for j in range(len(decomp)):
                if i == j:
                    continue
                if int_other is None:
                    int_other = decomp[j][0]
                else:
                    int_other = int_other.intersect(decomp[j][0])
            if int_other is not None and ideal_contains(decomp[i][0], int_other):
                return False
                
        # 3. Radicals are distinct
        Ps = [P for Q, P in decomp]
        for i in range(len(Ps)):
            for j in range(i+1, len(Ps)):
                if ideal_contains(Ps[i], Ps[j]) and ideal_contains(Ps[j], Ps[i]):
                    return False
                    
        # 4. Check radicals
        for Q, P in decomp:
            if not check_radical(Q, P):
                return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    """
    witness is expected to be a dictionary with:
    {
        'R': PolyRing or QuotientRing,
        'I': Ideal,
        'P_i': Ideal,
        'decomp1': [(Q1, P1), (Q2, P2), ...],
        'decomp2': [(Q1_prime, P1_prime), (Q2_prime, P2_prime), ...]
    }
    """
    try:
        R = witness['R']
        # H1: R is a commutative Noetherian ring
        h1 = isinstance(R, (sympy.polys.rings.PolyRing, sympy.polys.rings.QuotientRing))
    except Exception:
        h1 = False
        
    try:
        R = witness['R']
        I = witness['I']
        # H2: I is a proper ideal of R
        R_1 = R.ideal(1)
        h2 = not ideal_contains(I, R_1)
    except Exception:
        h2 = False
        
    try:
        P_i = witness['P_i']
        decomp1 = witness['decomp1']
        
        # H3: P_i is an isolated (minimal) prime ideal associated to I
        found = False
        for Q, P in decomp1:
            if ideal_contains(P_i, P) and ideal_contains(P, P_i):
                if check_radical(Q, P):
                    found = True
                break
                
        is_minimal = True
        for Q, P in decomp1:
            if ideal_contains(P_i, P) and ideal_contains(P, P_i):
                continue
            if ideal_contains(P_i, P): # P is strictly contained in P_i
                is_minimal = False
                break
                
        h3 = found and is_minimal
    except Exception:
        h3 = False
        
    try:
        I = witness['I']
        P_i = witness['P_i']
        decomp1 = witness['decomp1']
        decomp2 = witness['decomp2']
        
        # neg_Q: The primary component Q_i is NOT uniquely determined
        if not is_minimal_primary_decomposition(I, decomp1):
            neg_q = False
        elif not is_minimal_primary_decomposition(I, decomp2):
            neg_q = False
        else:
            Q_i_1 = None
            for Q, P in decomp1:
                if ideal_contains(P_i, P) and ideal_contains(P, P_i):
                    Q_i_1 = Q
                    break
                    
            Q_i_2 = None
            for Q, P in decomp2:
                if ideal_contains(P_i, P) and ideal_contains(P, P_i):
                    Q_i_2 = Q
                    break
                    
            if Q_i_1 is None or Q_i_2 is None:
                neg_q = False
            else:
                # Check if Q_i_1 and Q_i_2 are different
                if ideal_contains(Q_i_1, Q_i_2) and ideal_contains(Q_i_2, Q_i_1):
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: I is a proper ideal of R",
    "H_3: P_i is an isolated (minimal) prime ideal associated to I, where P_i is the radical of Q_i",
    "¬Q: The primary component Q_i is NOT uniquely determined by I and P_i"
]

N_HYP = 3
NEG_Q_INDEX = 3