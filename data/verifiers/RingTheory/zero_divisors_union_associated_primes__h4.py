import sympy
from sympy import symbols, lcm, factorint

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def is_primary(n):
    try:
        n = int(abs(n))
        if n == 0:
            return True
        if n == 1:
            return False
        factors = factorint(n)
        return len(factors) == 1
    except Exception:
        return False

def radical(n):
    try:
        n = int(abs(n))
        if n == 0:
            return 0
        factors = factorint(n)
        res = 1
        for p in factors:
            res *= p
        return res
    except Exception:
        return -1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    We evaluate the witness as ideals in the ring of integers Z, 
    represented by their non-negative integer generators.
    """
    try:
        if isinstance(witness, dict):
            I_val = witness.get('I')
            q_vals = witness.get('q', [])
            P_vals = witness.get('P', [])
        else:
            I_val = getattr(witness, 'I')
            q_vals = getattr(witness, 'q')
            P_vals = getattr(witness, 'P')
            
        I = int(abs(I_val))
        q_list = [int(abs(q)) for q in q_vals]
        P_list = [int(abs(P)) for P in P_vals]
    except Exception:
        return [False, False, False, False, False]

    # H1: R is a commutative ring with identity
    # Z is a commutative ring with identity
    h1 = True
    
    # H2: R is a Noetherian ring
    # Z is a Noetherian ring (it is a PID)
    h2 = True
    
    # H3: I is a proper ideal of R
    try:
        h3 = (I != 1)
    except Exception:
        h3 = False
        
    # H4: P_i = \sqrt{q_i} for i = 1, ..., n are the associated primes of I
    # In Z, this means I is the intersection of the primary ideals q_i,
    # and P_i are their respective radicals.
    try:
        h4 = True
        if len(q_list) != len(P_list) or len(q_list) == 0:
            h4 = False
        else:
            has_zero = False
            l = 1
            for q in q_list:
                if q == 0:
                    has_zero = True
                elif not has_zero:
                    l = lcm(l, q)
            intersect = 0 if has_zero else int(l)
            
            if I != intersect:
                h4 = False
            
            for q, P in zip(q_list, P_list):
                if not is_primary(q):
                    h4 = False
                if P != radical(q):
                    h4 = False
    except Exception:
        h4 = False
        
    # neg_Q: Conclusion fails
    # Conclusion: An element x in R is a zero divisor on R/I if and only if 
    # x belongs to the union of the associated primes P_1 \cup ... \cup P_n.
    # In Z, Z(Z/I) is the set of multiples of prime factors of I (or {0} if I=0).
    # The union of P_i is the set of multiples of the primes in P_list.
    # They are equal iff the set of prime factors of I equals the set of non-zero P_i.
    try:
        if I == 0:
            # Z(Z/(0)) = Z(Z) = {0}
            # Union of P_i is {0} iff all P_i are 0.
            conclusion_holds = all(P == 0 for P in P_list)
        else:
            factors_I = set(int(k) for k in factorint(I).keys())
            primes_P = set(P_list)
            conclusion_holds = (factors_I == primes_P)
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "H_3: I is a proper ideal of R",
    "H_4: P_i = \\sqrt{q_i} for i = 1, ..., n are the associated primes of I",
    "¬Q: The set of zero divisors on R/I is not equal to the union of the associated primes P_1 \\cup ... \\cup P_n"
]

N_HYP = 4
NEG_Q_INDEX = 4