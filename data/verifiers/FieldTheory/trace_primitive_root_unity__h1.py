import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (expected to be an integer n representing the index of the root of unity),
    returns a list of booleans:
      [H_1_ok, neg_Q_ok]
    where:
      H_1_ok is True if n is a valid index for a primitive n-th root of unity (n >= 1).
      neg_Q_ok is True if the conclusion FAILS at the witness.
    """
    try:
        n = int(witness)
    except Exception:
        return [False, False]

    # H_1: \zeta_n is a primitive n-th root of unity in \mathbb{C}
    # This just requires n to be a valid positive integer index for roots of unity.
    try:
        h1_ok = (n >= 1)
    except Exception:
        h1_ok = False

    # Conclusion: The field trace Tr_{\mathbb{Q}(\zeta_n)/\mathbb{Q}}(\zeta_n) is equal to \mu(n).
    # The trace of \zeta_n in \mathbb{Q}(\zeta_n)/\mathbb{Q} is the sum of its Galois conjugates,
    # which are the roots of the n-th cyclotomic polynomial.
    # Thus, the trace is the negative of the coefficient of x^{\phi(n)-1} in \Phi_n(x).
    try:
        if n >= 1:
            x = sympy.abc.x
            poly = sympy.polys.cyclotomic_poly(n, x)
            deg = poly.degree()
            trace = -poly.coeff(x, deg - 1)
            expected_mu = sympy.ntheory.mobius(n)
            q_ok = (trace == expected_mu)
        else:
            q_ok = True  # Vacuously true if out of domain, so neg_Q will be False
        neg_q_ok = not q_ok
    except Exception:
        # If evaluation fails (e.g., mobius of negative number), we consider the conclusion to fail
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: \\zeta_n is a primitive n-th root of unity in \\mathbb{C}",
    "¬Q: The field trace Tr_{\\mathbb{Q}(\\zeta_n)/\\mathbb{Q}}(\\zeta_n) is NOT equal to \\mu(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1