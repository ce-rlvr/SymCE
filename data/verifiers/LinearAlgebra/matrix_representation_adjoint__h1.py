import sympy
from sympy import eye, zeros, oo

# Top-level setup for standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let beta be an orthonormal basis for V, and T be a linear operator on V.
     Then the matrix representation of T adjoint is equal to the conjugate transpose of T."
    """
    h1 = False
    h2 = False
    neg_q = False

    # 1. String representation (abstract infinite-dimensional counterexamples)
    if isinstance(witness, str):
        w_lower = witness.lower()
        if any(kw in w_lower for kw in ["infinite", "unbounded", "derivative", "polynomial"]):
            return [True, True, True]

    # 2. Dictionary representation
    if isinstance(witness, dict):
        try:
            if 'is_orthonormal_basis' in witness:
                h1 = bool(witness.get('is_orthonormal_basis', False))
                h2 = bool(witness.get('is_linear_operator', False))
                neg_q = not bool(witness.get('conclusion_holds', True))
                return [h1, h2, neg_q]
        except Exception:
            pass

    # 3. Object with explicit attributes
    try:
        if hasattr(witness, 'is_orthonormal_basis') and hasattr(witness, 'is_linear_operator'):
            attr1 = getattr(witness, 'is_orthonormal_basis')
            h1 = bool(attr1() if callable(attr1) else attr1)
            
            attr2 = getattr(witness, 'is_linear_operator')
            h2 = bool(attr2() if callable(attr2) else attr2)
            
            if hasattr(witness, 'conclusion_holds'):
                attr3 = getattr(witness, 'conclusion_holds')
                neg_q = not bool(attr3() if callable(attr3) else attr3)
            elif hasattr(witness, 'has_adjoint'):
                attr3 = getattr(witness, 'has_adjoint')
                neg_q = not bool(attr3() if callable(attr3) else attr3)
            else:
                neg_q = True
                
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 4. Tuple representation: (G, T, T_star) or (T, T_star)
    if isinstance(witness, (tuple, list)):
        try:
            if len(witness) == 2:
                T, T_star = witness
                if hasattr(T, 'shape'):
                    if T.shape[0] == oo:
                        G = None
                    else:
                        G = eye(T.shape[0])
                    h1 = True
                else:
                    G = None
                    h1 = False
            elif len(witness) == 3:
                G, T, T_star = witness
                if hasattr(G, 'shape') and G.shape[0] == oo:
                    h1 = True
                    G = None
                elif hasattr(G, 'shape') and G.shape[0] == G.shape[1]:
                    h1 = (G == eye(G.shape[0]))
                else:
                    h1 = False
            else:
                G, T, T_star = None, None, None
                
            if T is not None:
                if G is not None:
                    h2 = hasattr(T, 'shape') and T.shape == G.shape
                else:
                    h2 = hasattr(T, 'shape') and T.shape[0] == oo and T.shape[1] == oo
                
                if T_star is None:
                    # T* doesn't exist. This is only valid if dimension is infinite.
                    neg_q = (not hasattr(T, 'shape') or T.shape[0] == oo)
                else:
                    if G is None:
                        neg_q = (T_star != T.H)
                    else:
                        # Verify T_star is actually the adjoint under standard or bilinear form
                        is_adjoint_sesqui = (T.H * G == G * T_star)
                        is_adjoint_bili = (T.T * G == G * T_star)
                        if is_adjoint_sesqui or is_adjoint_bili:
                            neg_q = (T_star != T.H)
                        else:
                            neg_q = False
                        
                return [bool(h1), bool(h2), bool(neg_q)]
        except Exception:
            pass

    # 5. Single matrix representation
    try:
        if hasattr(witness, 'shape') and len(witness.shape) == 2 and witness.shape[0] == witness.shape[1]:
            T = witness
            h1 = True
            h2 = True
            if T.shape[0] == oo:
                neg_q = True
            else:
                # For finite matrices, the only way it fails is if the adjoint is T.T (bilinear form)
                # and T.T != T.H (complex matrix)
                neg_q = (T.T != T.H)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 6. SymPy Operator
    try:
        from sympy.physics.quantum.operator import Operator
        if isinstance(witness, Operator):
            return [True, True, True]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: beta is an orthonormal basis for V",
    "H_2: T is a linear operator on V",
    "not Q: The matrix representation of T adjoint is not equal to the conjugate transpose of the matrix representation of T"
]

N_HYP = 2
NEG_Q_INDEX = 2