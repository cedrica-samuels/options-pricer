import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pricer import (black_scholes, mc_price, delta_closed_form,
                    delta_bump, parity_check, implied_vol)

S = 100
K = 100
r = 0.05
sigma = 0.2
T = 1
seed = 42


def run_convergence():
    print("CONVERGENCE (call option)")
    print("n_paths     MC price   BS price   error      std error")
    bs_price = black_scholes(S, K, r, sigma, T, "call")
    sizes = [100, 1000, 10000, 100000, 1000000]
    abs_errors = []
    std_errors = []
    for n in sizes:
        price, std_error = mc_price(S, K, r, sigma, T, n, "call", seed)
        error = price - bs_price
        abs_errors.append(abs(error))
        std_errors.append(std_error)
        print(f"{n:<11d} {price:<10.4f} {bs_price:<10.4f} {error:<10.4f} {std_error:<10.4f}")
    print()

    plt.figure(figsize=(7, 5))
    plt.loglog(sizes, abs_errors, "o-", label="absolute error")
    plt.loglog(sizes, std_errors, "s--", label="standard error")
    plt.xlabel("number of paths")
    plt.ylabel("error")
    plt.title("Monte Carlo error vs number of paths")
    plt.legend()
    plt.grid(True)
    plt.savefig("convergence.png", dpi=120)
    plt.close()
    print("Saved convergence.png")
    print()


def run_delta():
    print("DELTA (n_paths = 1,000,000)")
    for option_type in ["call", "put"]:
        exact = delta_closed_form(S, K, r, sigma, T, option_type)
        bumped = delta_bump(S, K, r, sigma, T, 1000000, option_type, seed)
        print(f"{option_type}: closed form = {exact:.4f}, bump and reprice = {bumped:.4f}, difference = {bumped - exact:.4f}")
    print()


def run_parity():
    print("PUT-CALL PARITY (n_paths = 1,000,000)")
    call_price, call_se = mc_price(S, K, r, sigma, T, 1000000, "call", seed)
    put_price, put_se = mc_price(S, K, r, sigma, T, 1000000, "put", seed)
    left_side, right_side = parity_check(S, K, r, T, call_price, put_price)
    print(f"MC call - MC put = {left_side:.4f}")
    print(f"S - K*exp(-rT)   = {right_side:.4f}")
    print(f"difference       = {left_side - right_side:.4f}")
    print(f"call std error = {call_se:.4f}, put std error = {put_se:.4f}")
    print()


def run_implied_vol():
    print("IMPLIED VOLATILITY ROUND TRIP")
    print("strike  true sigma  price     recovered sigma")
    for strike in [80, 90, 100, 110, 120]:
        for true_sigma in [0.15, 0.3]:
            price = black_scholes(S, strike, r, true_sigma, T, "call")
            recovered = implied_vol(price, S, strike, r, T, "call")
            print(f"{strike:<7d} {true_sigma:<11.2f} {price:<9.4f} {recovered:.6f}")
    print()


print("S=100, K=100, r=0.05, sigma=0.2, T=1")
print(f"Black-Scholes call = {black_scholes(S, K, r, sigma, T, 'call'):.4f}")
print(f"Black-Scholes put  = {black_scholes(S, K, r, sigma, T, 'put'):.4f}")
print()
run_convergence()
run_delta()
run_parity()
run_implied_vol()
