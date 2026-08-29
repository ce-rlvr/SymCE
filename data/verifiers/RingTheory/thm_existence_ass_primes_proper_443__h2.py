import sympy

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a list of generators for an ideal I in the polynomial ring R = QQ[vars].
    """
    try:
        # Normalize witness to a list of expressions
        if not isinstance(witness, (list, tuple, set)):
            if isinstance(witness, (sympy.Expr, int, float, str)):
                witness = [witness]
            else:
                return [False, False]
        
        exprs = []
        for w in witness:
            exprs.append(sympy.sympify(w))
            
        # Extract all variables to define the polynomial ring QQ[vars]
        vars_set = set()
        for expr in exprs:
            vars_set.update(expr.free_symbols)
        vars_list = sorted(list(vars_set), key=lambda s: s.name)
        if not vars_list:
            vars_list = [x]
            
        # H_1: R is a Noetherian ring
        # The ring R = QQ[vars_list] is a polynomial ring over a field, 
        # which is always Noetherian by Hilbert's Basis Theorem.
        h1 = True
        
        # neg_Q: Ass(R/I) is empty
        # For a Noetherian ring R, Ass(R/I) is empty if and only if R/I is the zero module,
        # which means I = R.
        # I = R iff the reduced Groebner basis of I is [1] (or any non-zero constant).
        gb = sympy.groebner(exprs, *vars_list, domain='QQ')
        gb_list = list(gb)
        
        neg_q = False
        if len(gb_list) == 1:
            p = gb_list[0]
            if p.is_number and p != 0:
                neg_q = True
                
    except Exception:
        return [False, False]
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "¬Q: Ass(R/I) is empty"
]

N_HYP = 1
NEG_Q_INDEX = 1