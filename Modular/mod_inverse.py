def modinv_latex(a, m):
    """
    Computes the modular inverse of a modulo m using the Extended Euclidean Algorithm
    and returns the inverse along with LaTeX steps showing the working.
    """
    # Ensure positive values
    original_a, original_m = a, m
    steps = []

    # Extended Euclidean Algorithm
    r0, r1 = a, m
    s0, s1 = 1, 0
    t0, t1 = 0, 1

    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
        steps.append((r0, r1, q, s0, s1, t0, t1))

    gcd = r0
    if gcd != 1:
        raise ValueError(f"{a} and {m} are not coprime, inverse does not exist.")

    # Modular inverse
    inv = s0 % m

    # Generate LaTeX for the table of steps
    latex_code = "\\begin{align*}\n"
    latex_code += f"&\\text{{Compute using Extended Euclidean Algorithm:}} \\\\\n"
    for r0, r1, q, s0, s1, t0, t1 in steps:
        latex_code += f"&r = {r0}, s = {s0}, t = {t0} \\\\\n"
    latex_code += f"&\\text{{Modular inverse: }} {original_a}^{{-1}} \\equiv {inv} \\pmod{{{original_m}}} \\\\\n"
    latex_code += "\\end{align*}"

    return inv, latex_code
