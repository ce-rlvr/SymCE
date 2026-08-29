import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
x = sp.Symbol('x', real=True)
y = sp.Symbol('y', real=True)

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (a function, sympy expression, or dictionary representing a transformation T),
    checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        # Extract the transformation if a tuple (V, W, T) was provided
        if isinstance(witness, (tuple, list)) and len(witness) > 0:
            witness = witness[-1]

        # Handle dictionary-based finite function witnesses
        if isinstance(witness, dict):
            # 0 must be in the domain for ker(T) to be evaluated
            if 0 not in witness and sp.S.Zero not in witness:
                return [False, False]
            
            h1 = True  # We assume the domain and codomain form valid vector spaces
            
            ker = [k for k, v in witness.items() if v == 0]
            ker_zero = (set(ker) == {0} or set(ker) == {sp.S.Zero})
            
            values = list(witness.values())
            injective = (len(values) == len(set(values)))
            
            neg_q = bool(injective != ker_zero)
            return [h1, neg_q]

        # Handle callable or sympy expression witnesses
        if callable(witness):
            expr = witness(x)
        elif isinstance(witness, sp.Expr):
            free_symbols = list(witness.free_symbols)
            if len(free_symbols) == 1:
                expr = witness.subs(free_symbols[0], x)
            elif len(free_symbols) == 0:
                expr = witness
            else:
                return [False, False]
        else:
            return [False, False]

        if not isinstance(expr, sp.Expr):
            return [False, False]

        # H1: V and W are vector spaces over a field F
        # Since the witness is a well-defined real function, V=R and W=R are vector spaces.
        h1 = True

        # Check if ker(T) == {0}
        ker_sols = sp.solveset(expr, x, domain=sp.S.Reals)
        ker_zero = (ker_sols == sp.FiniteSet(0))

        # Check if T is injective (T(x) == T(y) implies x == y)
        inj_sols = sp.solveset(expr.subs(x, y) - expr, y, domain=sp.S.Reals)
        injective = (inj_sols == sp.FiniteSet(x))

        # ¬Q: The conclusion "T is injective iff ker(T) = {0}" FAILS
        neg_q = bool(injective != ker_zero)

        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "¬Q: T is injective is not equivalent to ker(T) = {0}"
]

N_HYP = 1
NEG_Q_INDEX = 1