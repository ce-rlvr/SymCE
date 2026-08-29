import sympy
from sympy import S, Interval, FiniteSet, Union, Set

# Top-level setup
R = S.Reals
N = S.Naturals
Z = S.Integers
Q = S.Rationals
Empty = S.EmptySet

def conditions(witness) -> list[bool]:
    # H_1: C(X) is the ring of real-valued continuous functions on X
    # We interpret this as X being a valid topological space (represented as a SymPy Set).
    try:
        h1 = isinstance(witness, Set)
    except Exception:
        h1 = False

    # neg_Q: There exists a maximal ideal of C(X) not of the form {f | f(x) = 0}
    # For completely regular Hausdorff spaces (like subsets of R), 
    # every maximal ideal is fixed iff the space is compact.
    # So the conclusion fails (neg_Q is True) iff the space is NOT compact.
    try:
        def is_compact(space):
            if space == S.EmptySet:
                return True
            if isinstance(space, FiniteSet):
                return True
            if space in (S.Reals, S.Integers, S.Naturals, S.Naturals0, S.Rationals):
                return False
            if isinstance(space, Interval):
                bounded = (space.inf != S.NegativeInfinity) and (space.sup != S.Infinity)
                closed = (not space.left_open) and (not space.right_open)
                return bounded and closed
            if isinstance(space, Union):
                return all(is_compact(arg) for arg in space.args)
            
            try:
                if space.inf == S.NegativeInfinity or space.sup == S.Infinity:
                    return False
            except Exception:
                pass
            
            # Default to False for unknown sets to be safe
            return False

        neg_q = not is_compact(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: C(X) is the ring of real-valued continuous functions on X",
    "¬Q: There exists a maximal ideal M of C(X) without a unique point x such that M = {f in C(X) | f(x) = 0}"
]

N_HYP = 1
NEG_Q_INDEX = 1