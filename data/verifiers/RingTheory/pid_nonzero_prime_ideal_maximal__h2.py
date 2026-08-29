import sympy

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In a principal ideal domain, every ideal is a maximal ideal."
    (The dropped hypothesis was that the ideal is a non-zero prime ideal).
    """
    
    # Extract generator if witness is a tuple like (Ring, Ideal) or (Ring, Generator)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            witness = witness[1]
    except Exception:
        pass

    # Extract generator if witness is a SymPy Ideal
    try:
        if hasattr(witness, 'gens'):
            gens = witness.gens
            if callable(gens):
                gens = gens()
            if len(gens) == 1:
                witness = gens[0]
    except Exception:
        pass

    h1 = False
    try:
        # H_1: R is a principal ideal domain
        # We assume the witness represents a generator of an ideal in Z or QQ[x], both of which are PIDs.
        if isinstance(witness, (int, sympy.Integer)):
            h1 = True
        elif isinstance(witness, sympy.Expr):
            if len(witness.free_symbols) <= 1:
                h1 = True
    except Exception:
        pass

    neg_q = False
    try:
        # ¬Q: P is not a maximal ideal in R
        if isinstance(witness, (int, sympy.Integer)):
            # In Z, an ideal nZ is maximal iff |n| is prime.
            val = abs(int(witness))
            is_max = sympy.isprime(val)
            neg_q = not is_max
        elif isinstance(witness, sympy.Expr):
            if len(witness.free_symbols) == 0:
                if witness.is_Integer:
                    val = abs(int(witness))
                    is_max = sympy.isprime(val)
                    neg_q = not is_max
                else:
                    neg_q = True
            elif len(witness.free_symbols) == 1:
                # In QQ[x], an ideal is maximal iff its generator is irreducible and non-constant.
                var = list(witness.free_symbols)[0]
                poly = sympy.Poly(witness, var, domain='QQ')
                is_max = poly.is_irreducible and poly.degree() > 0
                neg_q = not is_max
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: P is not a maximal ideal in R"
]

N_HYP = 1
NEG_Q_INDEX = 1