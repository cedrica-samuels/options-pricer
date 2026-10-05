import numpy as np
from scipy.stats import norm


def get_d1(S, K, r, sigma, T):
    top = np.log(S / K) + (r + 0.5 * sigma ** 2) * T
    bottom = sigma * np.sqrt(T)
    return top / bottom


def get_d2(S, K, r, sigma, T):
    return get_d1(S, K, r, sigma, T) - sigma * np.sqrt(T)


def black_scholes(S, K, r, sigma, T, option_type):
    d1 = get_d1(S, K, r, sigma, T)
    d2 = get_d2(S, K, r, sigma, T)
    discount = np.exp(-r * T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * discount * norm.cdf(d2)
    if option_type == "put":
        return K * discount * norm.cdf(-d2) - S * norm.cdf(-d1)
    raise ValueError("option_type must be 'call' or 'put'")


def payoff(ST, K, option_type):
    if option_type == "call":
        return np.maximum(ST - K, 0)
    if option_type == "put":
        return np.maximum(K - ST, 0)
    raise ValueError("option_type must be 'call' or 'put'")


def simulate_terminal_prices(S, r, sigma, T, n_paths, seed):
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal(n_paths)
    drift = (r - 0.5 * sigma ** 2) * T
    shock = sigma * np.sqrt(T) * Z
    return S * np.exp(drift + shock)


def mc_price(S, K, r, sigma, T, n_paths, option_type, seed):
    ST = simulate_terminal_prices(S, r, sigma, T, n_paths, seed)
    discounted = np.exp(-r * T) * payoff(ST, K, option_type)
    price = np.mean(discounted)
    std_error = np.std(discounted, ddof=1) / np.sqrt(n_paths)
    return price, std_error


def delta_closed_form(S, K, r, sigma, T, option_type):
    d1 = get_d1(S, K, r, sigma, T)
    if option_type == "call":
        return norm.cdf(d1)
    return norm.cdf(d1) - 1


def delta_bump(S, K, r, sigma, T, n_paths, option_type, seed, bump=0.01):
    price_up, _ = mc_price(S + bump, K, r, sigma, T, n_paths, option_type, seed)
    price_down, _ = mc_price(S - bump, K, r, sigma, T, n_paths, option_type, seed)
    return (price_up - price_down) / (2 * bump)


def parity_check(S, K, r, T, call_price, put_price):
    left_side = call_price - put_price
    right_side = S - K * np.exp(-r * T)
    return left_side, right_side


def implied_vol(market_price, S, K, r, T, option_type):
    discount = np.exp(-r * T)
    if option_type == "call":
        lowest_price = max(S - K * discount, 0)
        highest_price = S
    else:
        lowest_price = max(K * discount - S, 0)
        highest_price = K * discount

    if market_price < lowest_price:
        raise ValueError("Price is below intrinsic value, no volatility can match it")
    if market_price > highest_price:
        raise ValueError("Price is above the maximum possible option price")

    low = 0.0001
    high = 5.0
    for i in range(100):
        mid = (low + high) / 2
        mid_price = black_scholes(S, K, r, mid, T, option_type)
        if mid_price > market_price:
            high = mid
        else:
            low = mid
        if high - low < 0.0000001:
            break
    return (low + high) / 2
