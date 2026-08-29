import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2) # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard matrix bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of groups (N, G, F).
    """
    try:
        if isinstance(witness, tuple) and len(witness) >= 3:
            N = witness[0]
            G = witness[1]
            F = witness[2]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def is_group(grp):
        if hasattr(grp, 'is_group') and grp.is_group:
            return True
        try:
            from sympy.combinatorics.free_groups import FreeGroup
            if isinstance(grp, FreeGroup):
                return True
        except ImportError:
            pass
        return False

    # H_1: N, G, and F are groups
    try:
        h1 = is_group(N) and is_group(G) and is_group(F)
    except Exception:
        h1 = False

    # H_2: F is a free group
    try:
        h2 = False
        try:
            from sympy.combinatorics.free_groups import FreeGroup
            if isinstance(F, FreeGroup):
                h2 = True
        except ImportError:
            pass
        # The trivial group is the free group on 0 generators
        if not h2 and hasattr(F, 'order') and F.order() == 1:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: G is NOT isomorphic to a semidirect product of N and F
    try:
        neg_q = False
        is_F_free_inf = False
        try:
            from sympy.combinatorics.free_groups import FreeGroup
            if isinstance(F, FreeGroup):
                is_F_free_inf = True
        except ImportError:
            pass
        
        if is_F_free_inf:
            try:
                g_order = G.order()
                # If G is finite and F is infinite, G cannot be isomorphic to N ⋊ F
                if isinstance(g_order, (int, sympy.Integer)):
                    neg_q = True
            except Exception:
                pass
        else:
            # For finite groups, the order of N ⋊ F is |N| * |F|
            if G.order() != N.order() * F.order():
                neg_q = True
            elif F.order() == 1:
                # If F is trivial, the only semidirect product is N itself
                neg_q = not G.is_isomorphic(N)
            else:
                # Basic abelian mismatch checks if orders happen to match
                if G.is_abelian and not N.is_abelian:
                    neg_q = True
                elif G.is_abelian and not F.is_abelian:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N, G, and F are groups",
    "H_2: F is a free group",
    "¬Q: G is not isomorphic to a semidirect product of N and F"
]

N_HYP = 2
NEG_Q_INDEX = 2