import sympy

# Top-level setup
# No specific named bindings needed for this number theory problem; use integers directly.

def conditions(witness) -> list[bool]:
    # H_1: Let \tau be the number of divisors function.
    # This is a definition, so it holds trivially for any witness.
    h1 = True
    
    # H_2: Let \mathbf{1} be the constant function defined by \mathbf{1}(n) = 1 for all positive integers n.
    # This is a definition, so it holds trivially for any witness.
    h2 = True
    
    # H_3: Let * denote the Dirichlet convolution of arithmetic functions.
    # This is a definition, so it holds trivially for any witness.
    h3 = True
    
    # ¬Q: \mu * \tau != \mathbf{1}
    # The conclusion is that for the witness n, (\mu * \tau)(n) == \mathbf{1}(n).
    # We evaluate this equality. If it fails or is undefined, neg_q is True.
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            q_ok = False
        else:
            n = int(witness)
            if n <= 0:
                # Dirichlet convolution and \mathbf{1}(n) are defined for positive integers.
                # If n <= 0, the equality does not hold in the standard sense.
                q_ok = False
            else:
                divs = sympy.divisors(n)
                # Compute (\mu * \tau)(n) = \sum_{d|n} \mu(d) \tau(n/d)
                conv = sum(sympy.mobius(d) * sympy.divisor_count(n // d) for d in divs)
                # \mathbf{1}(n) is 1 for all positive integers n
                q_ok = (conv == 1)
    except Exception:
        q_ok = False
        
    neg_q = not q_ok
    
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Let tau be the number of divisors function",
    "H_2: Let 1 be the constant function defined by 1(n) = 1 for all positive integers n",
    "H_3: Let * denote the Dirichlet convolution of arithmetic functions",
    "¬Q: mu * tau != 1 at the witness"
]

N_HYP = 3
NEG_Q_INDEX = 3