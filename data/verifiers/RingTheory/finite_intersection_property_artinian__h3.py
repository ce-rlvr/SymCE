import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M is an Artinian R-module",
    "¬Q: F does not have the finite intersection property"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # H_1: R is a ring
    try:
        # We accept sympy.S.Integers (or sympy.ZZ) as the ring Z
        H1 = (witness.R in (sympy.S.Integers, sympy.ZZ))
    except Exception:
        H1 = False

    # H_2: M is an Artinian R-module
    try:
        # A finite Z-module (finite abelian group) is Artinian.
        if hasattr(witness, 'M_order'):
            H2 = isinstance(witness.M_order, int) and witness.M_order > 0
        elif hasattr(witness, 'M'):
            if isinstance(witness.M, PermutationGroup):
                H2 = witness.M.is_finite and witness.M.is_abelian
            else:
                H2 = False
        else:
            H2 = False
    except Exception:
        H2 = False

    # ¬Q: F does not have the finite intersection property
    # If F is a strictly descending chain of non-zero ideals in Z, its infinite intersection is (0).
    # However, any finite subset of F has a non-zero intersection (the smallest ideal in the subset).
    # Thus, no finite subset has an intersection equal to the intersection of all submodules in F.
    try:
        neg_Q = False
        if hasattr(witness, 'F_expr'):
            n = witness.n
            F_expr = witness.F_expr
            F_inf = witness.F_inf
            
            # Check if F_expr forms a strictly descending chain of ideals in Z
            # Ideal (a) contains (b) iff a divides b.
            next_F = F_expr.subs(n, n + 1)
            ratio = sympy.simplify(next_F / F_expr)
            
            if ratio.is_constant():
                is_descending = abs(int(ratio)) > 1
            else:
                is_descending = all(abs(int(ratio.subs(n, i))) > 1 for i in range(1, 10))
                
            neg_Q = is_descending and (F_inf == 0)
            
        elif hasattr(witness, 'F_chain'):
            is_descending = True
            for i in range(1, 20):
                a = witness.F_chain(i)
                b = witness.F_chain(i+1)
                if a == 0 or b % a != 0 or abs(a) == abs(b):
                    is_descending = False
                    break
            neg_Q = is_descending and (witness.F_inf == 0)
            
        elif hasattr(witness, 'F_gen') or hasattr(witness, 'F_iter'):
            obj = getattr(witness, 'F_gen', getattr(witness, 'F_iter', None))
            gen = iter(obj() if callable(obj) else obj)
            is_descending = True
            try:
                a = next(gen)
                for _ in range(19):
                    b = next(gen)
                    if a == 0 or b % a != 0 or abs(a) == abs(b):
                        is_descending = False
                        break
                    a = b
            except StopIteration:
                is_descending = False
            neg_Q = is_descending and (witness.F_inf == 0)
            
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]