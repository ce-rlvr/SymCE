import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion at the given witness.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok]
    """
    try:
        N, H, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: The orders |N| and |H| are coprime
    try:
        order_N = N.order()
        order_H = H.order()
        h1_ok = math.gcd(order_N, order_H) == 1
    except Exception:
        h1_ok = False

    # H_2: \phi: H \to \text{Aut}(N) is a group homomorphism
    try:
        h2_ok = True
        for h1 in H.elements:
            for h2 in H.elements:
                phi_h1 = phi(h1)
                phi_h2 = phi(h2)
                phi_h1h2 = phi(h1 * h2)
                for n in N.elements:
                    if phi_h1h2(n) != phi_h1(phi_h2(n)):
                        h2_ok = False
                        break
                if not h2_ok:
                    break
            if not h2_ok:
                break
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion FAILS at the witness
    # Conclusion: N \rtimes_\phi H is nilpotent <=> N and H are nilpotent and \phi is trivial
    try:
        n_nilpotent = N.is_nilpotent
        h_nilpotent = H.is_nilpotent
        
        phi_trivial = True
        for h in H.elements:
            for n in N.elements:
                if phi(h)(n) != n:
                    phi_trivial = False
                    break
            if not phi_trivial:
                break
                
        rhs = n_nilpotent and h_nilpotent and phi_trivial
        
        elements = [(n, h) for n in N.elements for h in H.elements]
        
        def multiply(x, y):
            n1, h1 = x
            n2, h2 = y
            return (n1 * phi(h1)(n2), h1 * h2)
            
        # A finite group is nilpotent iff for all x, y with coprime orders, x and y commute.
        def get_order(x):
            curr = x
            ord = 1
            id_elem = (N.identity, H.identity)
            while curr != id_elem:
                curr = multiply(curr, x)
                ord += 1
            return ord

        lhs = True
        orders = {}
        for x in elements:
            orders[x] = get_order(x)
            
        for x in elements:
            for y in elements:
                if math.gcd(orders[x], orders[y]) == 1:
                    if multiply(x, y) != multiply(y, x):
                        lhs = False
                        break
            if not lhs:
                break
                
        neg_q_ok = (lhs != rhs)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The orders |N| and |H| are coprime",
    "H_2: \\phi: H \\to \\text{Aut}(N) is a group homomorphism",
    "¬Q: The semidirect product is nilpotent iff N, H are nilpotent and phi is trivial is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2