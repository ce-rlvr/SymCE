import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Parse witness
        if isinstance(witness, dict):
            W_raw = witness.get('W', witness)
            F = witness.get('F', None)
        elif isinstance(witness, tuple):
            if len(witness) >= 2:
                W_raw = witness[1]
                F = witness[2] if len(witness) > 2 else None
            else:
                W_raw = witness[0]
                F = None
        else:
            W_raw = witness
            F = None

        # Convert W_raw to a sympy Matrix whose columns span the subspace W
        if not isinstance(W_raw, sp.Matrix):
            if isinstance(W_raw, list) and len(W_raw) > 0 and isinstance(W_raw[0], sp.Matrix):
                W = sp.Matrix.hstack(*W_raw)
            else:
                W = sp.Matrix(W_raw)
        else:
            W = W_raw

        # H1: V is a finite-dimensional vector space over a field F
        h1 = True
        if F is not None:
            if isinstance(F, int):
                h1 = sp.isprime(F)
            elif hasattr(F, 'is_Field'):
                h1 = F.is_Field

        # H2: W is a subspace of V
        # The column space of a matrix is always a valid subspace of the ambient space.
        h2 = True

        # neg_Q: W != \bigcap_{f \in W^0} \ker(f)
        # W^0 is the annihilator, represented by the left nullspace of W.
        W_T = W.T
        W0_basis = W_T.nullspace()

        if not W0_basis:
            # W^0 is trivial, so the intersection of kernels is the entire space V.
            # We check if W is the entire space V (i.e., rank equals ambient dimension).
            neg_q = (W.rank() != W.rows)
        else:
            # W0 is the matrix whose rows are the basis vectors of W^0
            W0 = sp.Matrix.hstack(*W0_basis).T
            
            # The intersection of kernels is the right nullspace of W0
            int_ker_basis = W0.nullspace()

            if not int_ker_basis:
                # The intersection of kernels is {0}. We check if W is {0}.
                neg_q = not all(val == 0 for val in W)
            else:
                int_ker = sp.Matrix.hstack(*int_ker_basis)
                
                # Check if the column space of W equals the column space of int_ker
                rank_W = W.rank()
                rank_int = int_ker.rank()
                rank_aug = sp.Matrix.hstack(W, int_ker).rank()
                
                neg_q = not (rank_W == rank_int == rank_aug)

        return [bool(h1), bool(h2), bool(neg_q)]

    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    r"H_1: V is a finite-dimensional vector space over a field F",
    r"H_2: W is a subspace of V",
    r"¬Q: W != \bigcap_{f \in W^0} \ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2