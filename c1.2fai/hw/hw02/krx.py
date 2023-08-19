from typing import Any, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import itertools
from copy import deepcopy

from pathlib import Path
from tqdm import tqdm

# custom library
from config import PathConfig, ScraperConfig
from utils import DateUtil

class WebSource:
    def __init__(self) -> None:
        pass

class DataFetcher:
    def __init__(self) -> None:
        ## Init config
        self.scraper_config = ScraperConfig()

        ## Init session
        self.session = requests.session()

        assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
        self.session.hooks["response"] = [assert_status_hook]

        retry_strategy = Retry(**self.scraper_config.retry_strategy)
        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        ## POST data
        self.request_url = self.scraper_config.request_url
        self.request_headers = self.scraper_config.request_headers
        self.POST_data = self.scraper_config.data_without_trdDd

    def get_response(self, trdDd: Union[str, int], mktId: str="ALL"):
        if not isinstance(mktId, str) or mktId.upper() not in ["ALL", "STK", "KSQ", "KNX"]:
            raise Exception("Wrong mktId. Select from ['ALL', 'STK', 'KSQ', 'KNX']")
        
        trdDd = DateUtil.validate_date2str(trdDd)

        POST_data = deepcopy(self.POST_data)
        POST_data["trdDd"] = trdDd
        POST_data["mktId"] = mktId
        res = self.session.post(self.request_url, data=POST_data, headers=self.request_headers)

        return res, trdDd
        
    def parse_response(self, res, trdDd: str):
        data = res.json()["OutBlock_1"]
        df = pd.DataFrame(data)
        df.loc[:, "trdDd"] = int(trdDd)

        return df
