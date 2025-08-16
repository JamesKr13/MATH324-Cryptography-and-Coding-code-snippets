def repeated_squares_mod_verbose(base, exponent_limit, mod):
    powers = {1: base % mod}
    print(f"{base}^1 ≡ {powers[1]} mod {mod}")
    current_power = 1
    for _ in range(1, exponent_limit):
        prev_power = current_power
        current_power *= 2
        result = (powers[prev_power] ** 2) % mod
        powers[current_power] = result
        print(f"{base}^{current_power} = ({base}^{prev_power})^2 ≡ {result} mod {mod}")
