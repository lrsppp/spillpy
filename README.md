# spillpy

Implementation of total and directional spillover metrics (see e.g. Diebold and Yilmaz (2012)). This small package is built around `VARResultsWrapper` and [`statsmodels.tsa.vector_ar.VAR`](https://www.statsmodels.org/dev/vector_ar.html).

See `examples` for usage. 

## Installation

Installation using `setup.py`, for e.g.:

    cd spillpy && pip install .

## References

    @article{diebold2012better,
      title={Better to give than to receive: Predictive directional measurement of volatility spillovers},
      author={Diebold, Francis X and Yilmaz, Kamil},
      journal={International Journal of forecasting},
      volume={28},
      number={1},
      pages={57--66},
      year={2012},
      publisher={Elsevier}
    }
