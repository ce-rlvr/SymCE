import sympy
import sympy.abc

# Expected witness format: a tuple of 3 SymPy expressions (F_expr, E_expr, L_expr)
# representing the primitive elements of the fields F, E, L over QQ.
# For example: (sympy.S(0), sympy.cbrt(2), sympy.cbrt(2))
# This represents F = QQ, E = QQ(cbrt(2)), L = QQ(cbrt(2)).

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        F_expr, E_expr, L_expr = witness
    except Exception:
        return [False, False, False]
    
    x = sympy.abc.x

    # H1: F is a field
    try:
        F_sym = sympy.sympify(F_expr)
        # If F_sym is a valid algebraic number, QQ(F_sym) is a field.
        pF = sympy.minpoly(F_sym, x)
        h1 = True
    except Exception:
        h1 = False

    # H2: E is a finite separable field extension of F
    try:
        E_sym = sympy.sympify(E_expr)
        # In characteristic 0 (QQ), any algebraic extension is finite and separable.
        pE_QQ = sympy.minpoly(E_sym, x)
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails.
    # The conclusion states there exists a unique K such that E ⊆ K ⊆ L, K/F is Galois, and K is minimal.
    # This minimal Galois extension K is exactly the normal closure of E over F.
    # Thus, the conclusion holds iff the normal closure of E over F is contained in L.
    # The normal closure is contained in L iff the minimal polynomial of E over F splits completely in L.
    # We check if it does NOT split completely (meaning K does not exist in L).
    try:
        F_sym = sympy.sympify(F_expr)
        E_sym = sympy.sympify(E_expr)
        L_sym = sympy.sympify(L_expr)
        
        # To simplify relative extension math, we evaluate the counterexample assuming F = QQ.
        if F_sym.is_Rational:
            pE = sympy.minpoly(E_sym, x)
            if L_sym.is_Rational:
                facs = sympy.factor_list(pE)
            else:
                facs = sympy.factor_list(pE, extension=L_sym)
            
            # Check if all irreducible factors over L are linear
            all_linear = all(sympy.Poly(f, x).degree() == 1 for f, _ in facs[1])
            neg_q = not all_linear
        else:
            # If F is not QQ, we conservatively return False to avoid complex relative extension math,
            # since a valid counterexample can easily be found with F = QQ.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is a finite separable field extension of F",
    "¬Q: There does not exist a unique field K such that E ⊆ K ⊆ L, K/F is a finite Galois extension, and K is minimal"
]

N_HYP = 2
NEG_Q_INDEX = 2