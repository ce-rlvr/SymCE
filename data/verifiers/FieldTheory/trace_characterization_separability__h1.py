import sympy as sp

# Standard algebra objects relevant to the domain
x, y, z, t, u = sp.symbols('x y z t u')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the conjecture:
    "The extension E/F is separable if and only if the field trace map Tr_{E/F} : E → F is not identically zero."
    
    The witness is expected to be a polynomial P(x) defining the extension E = F[x]/(P(x)).
    If the dropped hypothesis "E is a field" is violated (i.e., P is not irreducible, so E is an algebra),
    the equivalence can fail.
    """
    try:
        # Parse the witness into a SymPy Poly object
        if isinstance(witness, tuple):
            expr, char = witness
            if char > 0:
                P = sp.Poly(expr, domain=sp.GF(char))
            else:
                P = sp.Poly(expr)
        else:
            P = sp.Poly(witness)
            char = getattr(P.domain, 'char', 0)

        gen = P.gen
        
        # Check if the extension is separable
        # An algebra F[x]/(P) is separable iff P is square-free (gcd(P, P') == 1)
        P_prime = P.diff(gen)
        gcd_poly = P.gcd(P_prime)
        is_separable = (gcd_poly.degree() == 0)
        
        n = P.degree()
        if n < 1:
            return [False]
            
        # Make the polynomial monic to easily extract coefficients for Newton's sums
        LC = P.LC()
        P_monic = P.exquo(sp.Poly(LC, gen))
        c = P_monic.all_coeffs()  # c[0]=1, c[1]=coeff of x^{n-1}, ..., c[n]=coeff of x^0
        
        # Check if the trace map is identically zero
        # The trace map is identically zero iff Tr(x^k) = 0 for all k = 0, ..., n-1.
        # We compute Tr(x^k) using Newton's sums s_k.
        s = [0] * n
        s[0] = n
        if char > 0:
            s[0] = s[0] % char
            
        trace_not_zero = (sp.simplify(s[0]) != 0)
        
        if not trace_not_zero:
            for k in range(1, n):
                # Newton's sum formula: s_k = - sum_{i=1}^{k-1} c_i s_{k-i} - k c_k
                term_sum = sum(c[i] * s[k - i] for i in range(1, k))
                s_k = -term_sum - k * c[k]
                if char > 0:
                    s_k = s_k % char
                s_k = sp.simplify(s_k)
                s[k] = s_k
                if s_k != 0:
                    trace_not_zero = True
                    break
                    
        # The conclusion states that the extension is separable iff the trace is not identically zero
        conclusion = (is_separable == trace_not_zero)
        
        # We want the conclusion to FAIL at the witness
        neg_Q = not conclusion
        
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence (E/F is separable iff Tr_{E/F} is not identically zero) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0