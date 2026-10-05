# Options Pricer

A small Python project that prices European call and put options three ways: the Black-Scholes formula, Monte Carlo simulation, and an implied volatility solver. Built as a learning project. It was built with AI assistance, and I studied the code so I can explain it.

## How to run

```
pip install -r requirements.txt
python run_demo.py
python test_pricer.py
```

`run_demo.py` prints the tables and saves `convergence.png`.

## What it does

- Black-Scholes price for calls and puts
- Monte Carlo price with standard error
- Convergence table and log-log plot (100 to 1,000,000 paths)
- Delta: closed form vs bump-and-reprice using the same random numbers
- Put-call parity check using Monte Carlo prices
- Implied volatility by bisection, with a round-trip test

## Real results

Inputs: S=100, K=100, r=0.05, sigma=0.2, T=1, seed=42.

- Black-Scholes call = 10.4506, put = 5.5735
- Monte Carlo call at 1,000,000 paths = 10.4532, standard error 0.0147 (error 0.0026)
- Monte Carlo call at 100 paths = 7.8258, standard error 1.0120
- Call delta: closed form 0.6368, bump-and-reprice 0.6368
- Put-call parity: MC call - MC put = 4.8809, S - K*exp(-rT) = 4.8771 (difference 0.0038)
- Implied vol recovered the true sigma to 6 decimals for strikes 80 to 120
- 7 of 7 tests pass

## Limits

- European options only (no early exercise)
- Constant volatility (no smile or skew)
- No dividends
- Monte Carlo uses one random draw per path, with no variance reduction
- Call and put MC prices use the same seed, so they share random numbers
- Not meant for real trading
