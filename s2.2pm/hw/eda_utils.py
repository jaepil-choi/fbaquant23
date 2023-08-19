import numpy as np
import pandas as pd

class Stats:
    @staticmethod
    def agg_pct(pct):
        def percentile_(x):
            return x.quantile(pct)
    
        percentile_.__name__ = f'pct_{pct*100:02.0f}'
    
        return percentile_
    
    @staticmethod
    def pd_statistics(pd_data, statistics:list, excluded_cols=[]):
        pd_type = type(pd_data)
    
        if pd_type is pd.Series:
            s_stats = pd_data.agg(statistics)
        
            return s_stats
        elif pd_type is pd.DataFrame:
            excluded_cols = excluded_cols
            cols = [col for col in pd_data.columns if col not in excluded_cols]
            df_stats = pd_data.agg({
                col: statistics for col in cols
            })
        
            return df_stats
        else:
            print('Wrong data type. Only takes pd.DataFrame or pd.Series')
    
    @staticmethod
    def compare_series_stats(s_list, statistics:list, series_names=None):
        s_list = [pd.Series(s) for s in s_list]
        s_stats = [Stats.pd_statistics(s, statistics) for s in s_list]
    
        stats_df = pd.DataFrame(s_stats).T
    
        if series_names:
            stats_df.columns = series_names
        else:
            stats_df.columns = np.arange(len(s_list))
    
        return stats_df
    

BASIC_STATS = [
    'count',
    'mean',
    'median',
    'max',
    'min',
    'std',
    'var',
    'skew',
    'kurt',
]

PCT_RANKS = [
    Stats.agg_pct(0.05),
    Stats.agg_pct(0.1),
    Stats.agg_pct(0.2),
    Stats.agg_pct(0.3),
    Stats.agg_pct(0.01),
    Stats.agg_pct(0.4),
    Stats.agg_pct(0.5),
    Stats.agg_pct(0.6),
    Stats.agg_pct(0.7),
    Stats.agg_pct(0.8),
    Stats.agg_pct(0.9),
    Stats.agg_pct(0.95),
    Stats.agg_pct(0.99),
]

STATISTICS = BASIC_STATS + PCT_RANKS