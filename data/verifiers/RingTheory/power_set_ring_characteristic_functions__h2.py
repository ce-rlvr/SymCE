import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness references
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Parse the witness. It could be a set X, an integer n (representing set {0..n-1}),
        # or a tuple (X, add_op, mul_op) if the witness explicitly provides operations for P(X).
        if isinstance(witness, int):
            X = set(range(witness))
            add_op, mul_op = None, None
        elif hasattr(witness, 'X') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
            X = set(witness.X)
            add_op = witness.add
            mul_op = witness.mul
        elif isinstance(witness, tuple) and len(witness) == 3:
            X, add_op, mul_op = witness
            X = set(X)
        else:
            X = set(witness)
            add_op, mul_op = None, None
            
        H1 = len(X) > 0
    except Exception:
        H1 = False
        X = set()
        add_op, mul_op = None, None

    # H2: F(X, Z_2) is the Boolean ring of functions from X to Z_2 under pointwise operations.
    # This is a definitional hypothesis that holds for any valid set X.
    H2 = H1

    # H3: phi maps P(X) to F(X, Z_2) via characteristic functions.
    # This is also definitional and holds for any valid set X.
    H3 = H1

    # neg_Q: The map phi is a ring isomorphism.
    # The conjecture is false because the hypothesis specifying the ring operations on P(X) 
    # (symmetric difference and intersection) was dropped. Without operations, P(X) is just a set, 
    # not a ring, so phi cannot be a ring isomorphism.
    # If the witness provides custom operations, we check if phi is a homomorphism under them.
    neg_Q = False
    if H1:
        if add_op is None or mul_op is None:
            # No operations provided, P(X) is not a ring.
            neg_Q = True
        else:
            try:
                X_list = list(X)
                # Generate the power set P(X)
                P_X = list(itertools.chain.from_iterable(
                    itertools.combinations(X_list, r) for r in range(len(X_list) + 1)
                ))
                P_X = [frozenset(s) for s in P_X]
                
                def phi(A):
                    return tuple(1 if x in A else 0 for x in X_list)
                
                is_homo = True
                for A in P_X:
                    for B in P_X:
                        try:
                            sum_AB = frozenset(add_op(A, B))
                            prod_AB = frozenset(mul_op(A, B))
                            
                            phi_A = phi(A)
                            phi_B = phi(B)
                            phi_sum = phi(sum_AB)
                            phi_prod = phi(prod_AB)
                            
                            # Pointwise addition and multiplication in Z_2
                            pw_add = tuple((a + b) % 2 for a, b in zip(phi_A, phi_B))
                            pw_mul = tuple((a * b) % 2 for a, b in zip(phi_A, phi_B))
                            
                            if phi_sum != pw_add or phi_prod != pw_mul:
                                is_homo = False
                                break
                        except Exception:
                            is_homo = False
                            break
                    if not is_homo:
                        break
                
                neg_Q = not is_homo
            except Exception:
                neg_Q = True

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: X is a non-empty set",
    "H_2: F(X, Z_2) is the Boolean ring of functions from X to Z_2",
    "H_3: phi maps P(X) to F(X, Z_2) via characteristic functions",
    "¬Q: phi is not a ring isomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3