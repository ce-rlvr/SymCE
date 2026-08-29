import sympy as sp

Z = sp.ZZ
Q = sp.QQ

CONDITION_LABELS = ['H_1: R is a commutative ring', 'neg_Q: The factor rings are not isomorphic']
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, m, n = witness
            elif len(witness) == 2:
                m, n = witness
                R = sp.ZZ
            else:
                return [False, False]
        else:
            return [False, False]
            
        # H_1: R is a commutative ring
        # We assume R provided in the witness is a valid commutative ring
        h1 = True
        
        m = int(m)
        n = int(n)
        
        if m < 0 or n < 0:
            return [False, False]
            
        x = sp.Symbol('x')
        p1 = x**m - 1
        p2 = x**n - 1
        g_val = sp.gcd(m, n)
        g = x**g_val - 1
        
        if m == 0 and n == 0:
            is_equal = True
        else:
            # Check if the ideal <x^m-1, x^n-1> is equal to <x^gcd(m,n)-1>
            # p1 and p2 are in <g> if they are divisible by g
            rem1 = sp.rem(p1, g)
            rem2 = sp.rem(p2, g)
            ideal_in_g = (rem1 == 0 and rem2 == 0)
            
            # g is in <p1, p2> if the gcd of p1 and p2 is g
            gcd_poly = sp.gcd(p1, p2)
            g_in_ideal = (sp.expand(gcd_poly) == sp.expand(g))
            
            is_equal = ideal_in_g and g_in_ideal
            
        # neg_Q is True if the conclusion FAILS (i.e., the ideals are NOT equal, 
        # meaning the factor rings are not isomorphic via the natural identity map).
        neg_q = not is_equal
        
        return [h1, neg_q]
    except Exception:
        return [False, False]