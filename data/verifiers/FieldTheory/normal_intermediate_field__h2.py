import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

# Top-level setup for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1) * Permutation(2, 3), Permutation(0, 2) * Permutation(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            K, F, E = witness
        elif len(witness) == 2:
            K, E = witness
            F = None
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # Try group theory interpretation first (Galois correspondence)
    # K corresponds to subgroup N, F to group G, E to subgroup H
    try:
        if F is not None and hasattr(K, 'generators') and hasattr(F, 'generators') and hasattr(E, 'generators'):
            def is_sub(A, B):
                return all(g in B for g in A.generators)
                
            def is_norm(A, B):
                if not is_sub(A, B):
                    return False
                for b in B.generators:
                    b_inv = ~b
                    for a in A.generators:
                        if (b * a * b_inv) not in A:
                            return False
                return True

            h1 = is_norm(K, F)
            # K is an extension of E iff K is a subgroup of E
            # K/E is normal iff K is a normal subgroup of E
            q = is_sub(K, E) and is_norm(K, E)
            return [bool(h1), not bool(q)]
    except Exception:
        pass

    # Try field theory interpretation (Expr or Poly)
    try:
        from sympy import minpoly, factor, RootOf
        from sympy.abc import x
        
        def splits_completely(poly, ext):
            factored = factor(poly, extension=ext)
            if factored.is_Mul:
                factors = factored.args
            else:
                factors = [factored]
            for f in factors:
                if f.has(x):
                    if f.is_Pow:
                        base = f.args[0]
                        p = base.as_poly(x)
                    else:
                        p = f.as_poly(x)
                    if p is None or p.degree() != 1:
                        return False
            return True

        if hasattr(K, 'is_Poly') or (hasattr(K, 'has') and K.has(x)):
            K_poly = K.as_poly(x) if not hasattr(K, 'is_Poly') else K
            E_poly = E.as_poly(x) if not hasattr(E, 'is_Poly') else E
            K_gen = RootOf(K_poly, 0)
            pK = K_poly
            pE = E_poly
        else:
            K_gen = K
            E_gen = E
            pK = minpoly(K_gen, x)
            pE = minpoly(E_gen, x)
            
        # If K/Q is normal, it is normal over any subfield F.
        h1 = splits_completely(pK, K_gen)
        # E is a subfield of K iff pE splits completely in K (since K/Q is normal).
        # If E is a subfield, K/E is always normal. If not, K/E is not an extension.
        q = splits_completely(pE, K_gen)
        return [bool(h1), not bool(q)]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: K/F is a normal extension",
    "¬Q: K/E is not a normal extension"
]

N_HYP = 1
NEG_Q_INDEX = 1