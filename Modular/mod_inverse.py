def modinv_euclidean_algo(a, m):
    """
    Compute the modular inverse of a modulo m using the Extended Euclidean Algorithm
    and produce LaTeX with full back-substitution steps.
    """
    # Step 1: Euclidean algorithm, storing each step
    r0, r1 = m, a
    steps = []
    while r1 != 0:
        q = r0 // r1
        r2 = r0 - q * r1
        steps.append((r0, r1, q, r2))
        r0, r1 = r1, r2

    if r0 != 1:
        raise ValueError(f"{a} and {m} are not coprime; inverse does not exist.")

    # Step 2: Back-substitution
    # Start with last nonzero remainder = 1
    # Build list of expressions: r = previous - quotient * current
    exprs = []
    for r_prev, r_curr, q, r_next in reversed(steps):
        exprs.append(f"{r_next} = {r_prev} - {q} \\times {r_curr}")

    # Step 3: Extended Euclidean algorithm to find modular inverse
    r_prev, r_curr = m, a
    s_prev, s_curr = 1, 0
    t_prev, t_curr = 0, 1
    for r_prev_step, r_curr_step, q, _ in steps:
        s_prev, s_curr = s_curr, s_prev - q * s_curr
        t_prev, t_curr = t_curr, t_prev - q * t_curr
    inv = t_prev % m

    # Step 4: Generate LaTeX output
    latex_code = "\\begin{align*}\n"
    latex_code += "&\\text{Euclidean algorithm:} \\\\\n"
    for r_prev, r_curr, q, r_next in steps:
        latex_code += f"&{r_prev} = {r_curr} \\times {q} + {r_next} \\\\\n"

    latex_code += "&\\text{Back-substitution to express 1 as combination of } a \\text{ and } m: \\\\\n"
    
    # Step 5: Full back-substitution
    # We reconstruct the substitution chain step by step
    last = 1
    for r_prev, r_curr, q, r_next in steps[::-1]:
        latex_code += f"&{last} = {r_prev} - {q} \\times {r_curr} \\\\\n"
        last = f"{r_prev} - {q} \\times {r_curr}"

    latex_code += f"&\\text{{Modular inverse: }} {a}^{{-1}} \\equiv {inv} \\pmod{{{m}}} \\\\\n"
    latex_code += "\\end{align*}"

    return inv, latex_code
