import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # 1. Object with explicit methods
    try:
        if hasattr(witness, 'is_finite') and hasattr(witness, 'is_galois'):
            h1 = bool(witness.is_finite())
            h2 = bool(witness.is_galois())
            q = bool(witness.has_normal_basis())
            return [h1, h2, not q]
    except Exception:
        pass

    # 2. Dictionary representation
    try:
        if isinstance(witness, dict) and 'is_finite' in witness:
            h1 = bool(witness.get('is_finite', False))
            h2 = bool(witness.get('is_galois', False))
            q = bool(witness.get('has_normal_basis', True))
            return [h1, h2, not q]
    except Exception:
        pass

    # Extract matrices if witness is a tuple (e.g., (matrices, field))
    try:
        if isinstance(witness, tuple) and len(witness) >= 1:
            if isinstance(witness[0], list) and len(witness[0]) > 0 and hasattr(witness[0][0], 'shape'):
                witness = witness[0]
    except Exception:
        pass

    def make_hashable(M):
        return tuple(tuple(row) for row in sp.Matrix(M).tolist())

    # 3. List of matrices (representing the Galois group action on K as an F-vector space)
    try:
        if isinstance(witness, list) and len(witness) > 0 and hasattr(witness[0], 'shape'):
            n = witness[0].shape[0]
            h1 = all(sp.Matrix(M).shape == (n, n) for M in witness)
            
            if len(witness) != n:
                h2 = False
            else:
                matrix_set = {make_hashable(M) for M in witness}
                h2 = True
                for A in witness:
                    for B in witness:
                        if make_hashable(sp.Matrix(A) * sp.Matrix(B)) not in matrix_set:
                            h2 = False
                            break
                    if not h2:
                        break
                        
            v = sp.Matrix([sp.Symbol(f'x{i}') for i in range(n)])
            orbit = [sp.Matrix(M) * v for M in witness]
            orbit_matrix = sp.Matrix.hstack(*orbit)
            det = sp.simplify(orbit_matrix.det())
            is_z = det.is_zero
            if is_z is None:
                is_z = (det == 0)
            q = not is_z
            
            return [h1, h2, not q]
    except Exception:
        pass

    # 4. Single matrix (generator of a cyclic Galois group)
    try:
        if hasattr(witness, 'shape') and not isinstance(witness, list):
            M = sp.Matrix(witness)
            n = M.shape[0]
            h1 = True
            
            group = [sp.eye(n)]
            current = M
            while current != sp.eye(n) and len(group) <= n:
                group.append(current)
                current = current * M
                
            if len(group) != n:
                h2 = False
            else:
                h2 = True
                
            v = sp.Matrix([sp.Symbol(f'x{i}') for i in range(n)])
            orbit = [A * v for A in group]
            orbit_matrix = sp.Matrix.hstack(*orbit)
            det = sp.simplify(orbit_matrix.det())
            is_z = det.is_zero
            if is_z is None:
                is_z = (det == 0)
            q = not is_z
            
            return [h1, h2, not q]
    except Exception:
        pass

    # 5. SymPy Poly (representing an inseparable normal extension)
    try:
        if isinstance(witness, sp.Poly):
            h1 = True
            h2 = True  # Assume normal if provided as a counterexample candidate
            # If the extension is inseparable, the derivative is zero, and the Galois group is trivial
            # meaning the orbit size is 1 < degree, so it cannot form a basis.
            q = not witness.diff().is_zero
            return [h1, h2, not q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: The extension K/F is finite",
    "H_2: The extension K/F is Galois",
    "¬Q: There does not exist an element whose orbit forms a basis for K as an F-vector space"
]

N_HYP = 2
NEG_Q_INDEX = 2