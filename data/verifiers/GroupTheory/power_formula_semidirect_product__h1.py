import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 4
NEG_Q_INDEX = 4

CONDITION_LABELS = [
    "H_1: phi: H -> Aut(N) is a group homomorphism",
    "H_2: G = N \\rtimes_\\phi H is the external semidirect product of N and H",
    "H_3: (n, h) is an element of G",
    "H_4: m is a positive integer",
    "¬Q: The m-th power (n, h)^m in G is NOT equal to (n \\phi_h(n) \\phi_{h^2}(n) \\cdots \\phi_{h^{m-1}}(n), h^m)"
]

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion for the given witness.
    
    The witness is expected to be a tuple: (mul_G, mul_N, mul_H, phi, n, h, m)
    where:
      - mul_G(g1, g2) is the multiplication function for G.
      - mul_N(n1, n2) is the multiplication function for N.
      - mul_H(h1, h2) is the multiplication function for H.
      - phi(h, n) applies the automorphism phi_h to n.
      - n is an element of N.
      - h is an element of H.
      - m is an integer.
    """
    try:
        mul_G, mul_N, mul_H, phi, n, h, m = witness
    except Exception:
        return [False, False, False, False, False]

    # Generate small sets of elements to test properties
    try:
        h_powers = [h]
        curr_h = h
        for _ in range(m + 2):
            curr_h = mul_H(curr_h, h)
            if curr_h not in h_powers:
                h_powers.append(curr_h)
                
        n_powers = [n]
        curr_n = n
        for _ in range(m + 2):
            curr_n = mul_N(curr_n, n)
            if curr_n not in n_powers:
                n_powers.append(curr_n)
    except Exception:
        return [False, False, False, False, False]

    # H_1: phi: H -> Aut(N) is a group homomorphism.
    h1_ok = True
    try:
        for h1 in h_powers:
            for h2 in h_powers:
                for x in n_powers:
                    if phi(mul_H(h1, h2), x) != phi(h1, phi(h2, x)):
                        h1_ok = False
        for h1 in h_powers:
            for x in n_powers:
                for y in n_powers:
                    if phi(h1, mul_N(x, y)) != mul_N(phi(h1, x), phi(h1, y)):
                        h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: G = N \rtimes_\phi H is the external semidirect product of N and H.
    h2_ok = True
    try:
        for h1 in h_powers:
            for h2 in h_powers:
                for n1 in n_powers:
                    for n2 in n_powers:
                        g1 = (n1, h1)
                        g2 = (n2, h2)
                        expected_g = (mul_N(n1, phi(h1, n2)), mul_H(h1, h2))
                        if mul_G(g1, g2) != expected_g:
                            h2_ok = False
    except Exception:
        h2_ok = False

    # H_3: (n, h) is an element of G.
    try:
        h3_ok = (n is not None) and (h is not None)
    except Exception:
        h3_ok = False

    # H_4: m is a positive integer.
    try:
        h4_ok = isinstance(m, int) and m > 0
    except Exception:
        h4_ok = False

    # neg_Q: The m-th power (n, h)^m in G is NOT equal to the formula.
    try:
        # Compute actual power using G's multiplication
        actual_power = (n, h)
        for _ in range(m - 1):
            actual_power = mul_G(actual_power, (n, h))
            
        # Compute formula power
        form_n = n
        curr_h = h
        for _ in range(m - 1):
            form_n = mul_N(form_n, phi(curr_h, n))
            curr_h = mul_H(curr_h, h)
        form_h = curr_h
        
        expected_power = (form_n, form_h)
        
        neg_q_ok = (actual_power != expected_power)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]