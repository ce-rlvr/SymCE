import sympy

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            S_witness, n = witness
        else:
            n = witness
            S_witness = None
            
        # H1: S is the set of all primitive n-th roots of unity in C
        if isinstance(n, (int, sympy.Integer)):
            if n == 0:
                S_true = set()
            elif n > 0:
                S_true = {sympy.exp(2 * sympy.I * sympy.pi * k / n) for k in range(n) if sympy.gcd(k, n) == 1}
            else:
                S_true = {sympy.exp(2 * sympy.I * sympy.pi * k / abs(n)) for k in range(abs(n)) if sympy.gcd(k, abs(n)) == 1}
        else:
            # For non-integer n (e.g., rational), compute the principal n-th root
            val = sympy.exp(2 * sympy.I * sympy.pi / n)
            S_true = {val}
            
        if S_witness is not None:
            # Compare sets, handling potential sympy expression differences
            h1 = (set(S_witness) == S_true)
        else:
            h1 = True
            S_witness = S_true
            
    except Exception:
        return [False, False]

    if not h1:
        return [False, False]

    try:
        # Check if S forms a Q-basis for Q(zeta_n)
        # For positive integers, the primitive roots form a normal basis iff n is square-free.
        # For negative integers, the same holds for |n|.
        if isinstance(n, (int, sympy.Integer)):
            if n == 0:
                forms_basis = False
            else:
                forms_basis = sympy.is_square_free(abs(n))
        else:
            # For non-integers like n = 1/2, S = {1}, which forms a basis for Q(1) = Q
            if S_witness == {1}:
                forms_basis = True
            else:
                forms_basis = False
                
        # Check if n is a square-free integer
        if isinstance(n, (int, sympy.Integer)):
            is_sqf = sympy.is_square_free(n)
        else:
            is_sqf = False
            
        # The conclusion is the biconditional: forms_basis <-> is_sqf
        conclusion = (forms_basis == is_sqf)
        neg_q = not conclusion
        
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is the set of all primitive n-th roots of unity in C",
    "¬Q: The set S forms a Q-basis for Q(zeta_n) iff n is a square-free integer fails"
]

N_HYP = 1
NEG_Q_INDEX = 1