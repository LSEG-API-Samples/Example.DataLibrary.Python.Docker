# |-----------------------------------------------------------------------------
# |            This source code is provided under the Apache 2.0 license      --
# |  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
# |                See the project's LICENSE.md for details.                  --
# |           Copyright LSEG 2025. All rights reserved.                       --
# |-----------------------------------------------------------------------------


#!/usr/bin/env python
import sys
import warnings
import lseg.data as ld 
from lseg.data import session

# Only ignore deprecation warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

def get_historical_interday_data(instruments, fields):
    """
    This method sends a request message to RDP Historical Pricing service.

    Args:
        universe (str): RIC Code

    Returns: 
        interday data (Pandas Dataframe): Interday data in DataFrame object
    """
    print(f'Getting Historical Pricing Interday data for {instruments} fields = {fields}')
    # Time Variables
    interval = 'weekly' #weekly
    start_day = '2025-10-01'
    end_day = '2025-11-10'

    # Send request message
    response = ld.get_history(universe=instruments,
                        interval=interval, 
                        fields=fields,
                        count=15,
                        start=start_day,
                        end= end_day)
    print('This is a Historical Pricing Inter-Day data result from Data Library - Access Layer - get_history method')
    print(response)

def get_price_data(instruments, fields):
    """ This method gets snapshot pricing data from RDP """
    print(f'Getting Snapshot Price data for {instruments} fields = {fields}')
    data = ld.get_data(instruments, fields)
    print(data)

if __name__ == '__main__':
    universes = ['THB=', 'JPY=']  # NVIDIA RIC Code
    fields=['BID','ASK','OPEN_PRC','HIGH_1','LOW_1','TRDPRC_1','NUM_MOVES','TRNOVR_UNS']
    try:
        # Open the data session
        ld.open_session()
        #ld.open_session(config_name='./lseg-data-devrel.config.json')
        session = ld.session.get_default()
        session.open()
        if str(session.open_state) == 'OpenState.Opened':
            print('Session is opened')
            get_price_data(['THB=', 'JPY='],['BID', 'ASK'])
            print()
            get_historical_interday_data(
                instruments=['AMD.O','NVDA.O'],
                fields=['BID','ASK','OPEN_PRC','HIGH_1','LOW_1','TRDPRC_1','NUM_MOVES','TRNOVR_UNS'])
           
        print('Close Session')
        ld.close_session()
    except Exception as ex:
        print(f'Error in open_session: {str(ex)}')
        sys.exit(1)
