import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    # Setup witness
    if isinstance(witness, tuple) and len(witness) == 2:
        G, G_prime = witness
    else:
        G = witness
        try:
            G_prime = G.derived_subgroup()
        except Exception:
            G_prime = None

    # H_1: G' is the commutator subgroup of G
    try:
        actual_G_prime = G.derived_subgroup()
        h1 = (G_prime == actual_G_prime)
    except Exception:
        h1 = False
        actual_G_prime = None

    # neg_Q: The conclusion FAILS
    try:
        # Evaluate RHS: x^2 \in G' for all x \in G
        rhs = True
        if h1:
            # Optimization: if G/G' is abelian, we only need to check generators
            for g in G.generators:
                if (g**2) not in G_prime:
                    rhs = False
                    break
        else:
            # Fallback for invalid witnesses
            if G.order() > 5000:
                rhs = False 
            else:
                for x in G.elements:
                    if (x**2) not in G_prime:
                        rhs = False
                        break
        
        # Evaluate LHS: G/G' is an elementary abelian 2-group
        # An elementary abelian 2-group is a non-trivial abelian group where every element has order 1 or 2.
        order_quotient = G.order() // G_prime.order()
        if order_quotient == 1:
            # The trivial group is not considered an elementary abelian 2-group in this context
            lhs = False
        else:
            if h1:
                # If G_prime is the commutator subgroup, G/G' is abelian.
                # Thus, it is an elementary abelian 2-group iff every element has order 1 or 2 (which is exactly RHS).
                lhs = rhs
            else:
                # Fallback check if G_prime is not the commutator subgroup
                is_normal = True
                for h in G_prime.generators:
                    for g in G.generators:
                        if (g**-1 * h * g) not in G_prime:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                
                if not is_normal:
                    lhs = False
                else:
                    is_abelian = True
                    if actual_G_prime is not None:
                        for h in actual_G_prime.generators:
                            if h not in G_prime:
                                is_abelian = False
                                break
                    else:
                        is_abelian = False
                        
                    if is_abelian:
                        lhs = rhs
                    else:
                        lhs = False
                        
        conclusion = (lhs == rhs)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G' is the commutator subgroup of G",
    "¬Q: The quotient group G/G' is an elementary abelian 2-group if and only if x^2 \\in G' for all x \\in G is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1