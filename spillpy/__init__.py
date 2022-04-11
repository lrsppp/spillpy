""" spillpy: Spillover measures """

import numpy as np
import pandas as pd
from statsmodels.tsa.vector_ar.var_model import VARResultsWrapper


class Spillover(VARResultsWrapper):
    """
    Implementation of spillover measures based on forecast error variance
    decomposition in vector autoregressive models (Diebold and Yilmaz (2012)).
    @article{diebold2012better,
        title={Better to give than to receive: Predictive directional
        measurement of volatility spillovers},
        author={Diebold, Francis X and Yilmaz, Kamil},
        journal={International Journal of forecasting},
        volume={28},
        number={1},
        pages={57--66},
        year={2012},
        publisher={Elsevier}
    }
    https://doi.org/10.1016/j.ijforecast.2011.02.006
    """
    def __init__(self, res):
        VARResultsWrapper.__init__(self, res)
        self.fitted = False
        self.fevd_norm = None
        self.dir_from = None
        self.dir_to = None

    def fit(self, nfore = 4):
        """
        Parameters
        ----------
        nfore : int
            number h of step-ahead forecast used in FEVD
        """
        # estimate fevd
        sigma_u = np.asarray(self.sigma_u)
        sd_u = np.sqrt(np.diag(sigma_u)) # used in var_decomp
        fevd_n = self.fevd(nfore, sigma_u / sd_u)

        # select fevd at t+h
        fevd_last = fevd_n.decomp[:,-1]

        # normalize
        fevd_norm = (fevd_last / fevd_last.sum(1)[:,None] * 100)

        # directional spillover
        tril = np.tril(fevd_norm, k = -1)
        triu = np.triu(fevd_norm, k = 1)
        dir_from = (tril + triu).sum(axis = 1)
        dir_to = (tril + triu).sum(axis = 0)

        self.fevd_norm = fevd_norm
        self.dir_from = dir_from
        self.dir_to = dir_to

        self.fitted = True

    def spillover_index(self):
        """
        (Total) spillover index.

        Returns
        -------
        spill_index : float

        """
        spill_index = self.dir_from.sum() / self.fevd_norm.sum(axis = 1).sum() * 100
        return spill_index
    
    def spillover_table(self, to_pandas = False):
        """
        Creates spillover table based on directional spillover measures.

        Parameters
        ----------
        to_pandas : bool

        Returns
        -------
        table : array_like or pandas DataFrame

        """
        if not self.fitted:
            raise NotImplementedError
            
        col_right = np.hstack([self.dir_from, self.spillover_index()])
        table = np.r_[self.fevd_norm, [self.dir_to]]
        table = np.c_[table, col_right]

        if to_pandas:
            index = self.names + ['dir_from']
            columns = self.names + ['dir_to']
            table = pd.DataFrame(table, index = index, columns = columns)

        return table
