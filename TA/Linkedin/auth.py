%load_ext autoreload
%autoreload 2

from linkedin_v2  import linkedin


import os
import json
import pathlib


def getCreds():
    rootPath = pathlib.Path().resolve()
    pathToCreds = os.path.abspath(os.path.join(rootPath ,"TA", "Creds" , "linkedin.secrets"))
    creds = json.load(open(pathToCreds , "r"))
    return creds


def authenticate():
    creds = getCreds()
    API_KEY = creds["client_id"]
    API_SECRET = creds["client_secret"]
    RETURN_URL = 'http://localhost:8000'
    authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL,["r_liteprofile"])

    print(authentication.authorization_url)  # open this url on your browser

    authentication.authorization_code = "AQTiVEHx5potAMyle43UKPKU8ObWt2z2tUI75E72b1RMgRwvs2ZJ97kC97hEKyX56Eostp7FxhRzbcXhugSfkUK28czXIuunoyIj6mo_hT-aYbWeUocBcCkeVQmEhznbIpgENQl3yj6h2FuIFPcXFqo737bZVEyyiZfgkYPV1IExCgRBo0xHzrtmzljw_A"
    token = authentication.get_access_token()
    token_str = "AQVIe5jsla4VrGMRDNCuEcWkZYZxD5e93TSEwZZXNpKANy74NgGctVaLKUG3UcGrAI1tM_aUBxga91jx301sXCA7ahR3yOgLBB_LvZf9NaEAXAEQfi_0CUVoNf8JUPcyr9jcNZXvFYQZ8Hv-lp0JPlUTwOHcaVFple8g58LUHA5hQpAlQHar97yIk6zLU6D6fr8-czngg0fuOJ2cYBehqJ-DrTJKvE3Q3FmJbTmdlujhYVm-9X0WLFdRL2gAchJhhxubRo-ilNDAvYRPUHfDa2st2eJ_5w5woiS4qjJcTwBlyOewLFoXpaAxLrKbEdO83m_vz9NiaayC3EdxzNflq4HomaKyZg"
    application = linkedin.LinkedInApplication(token=authentication.authorization_code)
    application.
    application.get_profile()
