import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: G is a solvable group
    try:
        if callable(witness.is_solvable):
            h1 = bool(witness.is_solvable())
        else:
            h1 = bool(witness.is_solvable)
    except Exception:
        h1 = False

    # H_2: G acts transitively and faithfully on a finite set X
    try:
        if callable(witness.is_transitive):
            h2 = bool(witness.is_transitive())
        else:
            h2 = bool(witness.is_transitive)
    except Exception:
        h2 = False

    # ¬Q: Conclusion fails
    # Conclusion: G contains a unique regular normal subgroup of order p, 
    # and G is isomorphic to a subgroup of the affine general linear group AGL(1, p).
    try:
        p = witness.degree
        if callable(p):
            p = p()
        
        # A regular subgroup must have order equal to the degree of the permutation group.
        # Thus, if it has order p, the degree of G must be p.
        if not isprime(p):
            q_ok = False
        else:
            # Check for a unique regular normal subgroup of order p.
            # Since p is prime, such a subgroup must be the unique Sylow p-subgroup.
            H = witness.sylow_subgroup(p)
            H_order = H.order() if callable(H.order) else H.order
            
            if H_order != p:
                q_ok = False
            else:
                # Check if H is normal in G
                is_normal = True
                for g in witness.generators:
                    for h in H.generators:
                        conj = g * h * (~g)
                        if conj not in H:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                
                if not is_normal:
                    q_ok = False
                else:
                    # Check if H is regular (transitive of order p on p points implies regular)
                    H_is_transitive = H.is_transitive() if callable(H.is_transitive) else H.is_transitive
                    if not H_is_transitive:
                        q_ok = False
                    else:
                        # Check if G is isomorphic to a subgroup of AGL(1, p).
                        # Since H is normal of order p, G/H acts faithfully on H.
                        # Thus G/H embeds into Aut(H) = Z_{p-1}, so G/H must be abelian.
                        # This is equivalent to the derived subgroup of G being contained in H.
                        D = witness.derived_subgroup()
                        is_subgroup = True
                        for d in D.generators:
                            if d not in H:
                                is_subgroup = False
                                break
                        q_ok = is_subgroup
                        
        neg_q = not q_ok
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "H_2: G acts transitively and faithfully on a finite set X",
    "¬Q: G does not contain a unique regular normal subgroup of order p, or G is not isomorphic to a subgroup of AGL(1, p)"
]

N_HYP = 2
NEG_Q_INDEX = 2