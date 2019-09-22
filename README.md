# quantumhacking2019

## Team Quantumacy: Finding arbitrage opportunities

* [Yvo Keuter](https://github.com/ykeuter), [Davit Khachatryan](https://github.com/DavitKhach), and [Olli Ahonen](https://github.com/olliahonen)
* The challenge:
   > Arbitrage is the practice of taking advantage of a price difference between two or more markets. One example is cross-currency arbitrage. The problem of arbitrage detection is commonly solved by defining a directed graph in which the nodes are the assets and the edge weights are equal to minus the logarithm of the conversion rate and searching searching for negative cycles. In contrast, the problem of finding the most profitable arbitrage opportunity of arbitrary length is NP-hard, and hence the time complexity of an algorithm solving it to optimality is expected to be exponential.
The challenge is to create a QAOA which can be mapped onto an arbitrage cycle and gives the most profitable solution.

* Our solution: https://github.com/ykeuter/arbitrage-qaoa/blob/master/arbitrage-qaoa.ipynb
