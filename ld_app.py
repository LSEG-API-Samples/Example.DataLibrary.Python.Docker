import os
import sys
import warnings
import lseg.data as ld 
from lseg.data import session

# Only ignore deprecation warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

def get_historical_interday_data(universe, fields):
    """
    This method sends a request message to RDP Historical Pricing service to get Interday data with the Data Library Access Layer.

    Args:
        universe (str): RIC Code

    Returns: 
        interday data (Pandas Dataframe): Interday data in DataFrame object
    """
    # Time Variables
    interval = 'weekly' #weekly
    start_day = '2025-01-01'
    end_day = '2025-02-10'

    # Send request message
    df = ld.get_history(universe=universe,
                        interval=interval, 
                        fields=fields,
                        count=15,
                        start=start_day,
                        end= end_day)
    print('This is a Historical Pricing Inter-Day data result from Data Library - Access Layer - get_history method')
    print(df)

def get_news_headlines(universe):
    """
    This method sends a request message to RDP News service to get news headlines data with the Data Library Access Layer.

    Args:
        universe (str): RIC Code

    Returns: 
        news headlines (Pandas Dataframe): News Headlines data in DataFrame object
    """
    start_day = '2025-11-01'
    end_day = '2025-11-06'

    query = f'R:{universe} AND Language:LEN AND Source:RTRS'

    # Send request message
    df = ld.news.get_headlines(query, start=start_day, end=end_day, count=5)

    print('This is a News headlines from Data Library - Access Layer - get_headlines')
    print(df)
    return df

def get_news_story(story_id):
    """
    This method sends a request message to RDP News service to get news story data with the Data Library Access Layer.

    Args:
        story_id (str): Story ID code from news headlines.

    Returns: 
        None.
    """
    # Send request message
    story = ld.news.get_story(story_id, format=ld.news.Format.TEXT)
    print(f'This is a News story from Data Library - Access Layer - get_story for {story_id}')
    print(story)

if __name__ == '__main__':
    universe = 'NVDA.O'  # NVIDIA RIC Code
    fields=['BID','ASK','OPEN_PRC','HIGH_1','LOW_1','TRDPRC_1','NUM_MOVES','TRNOVR_UNS']
    try:
        # Open the data session
        ld.open_session()
        #ld.open_session(config_name='./lseg-data-derel.config.json')
        session = ld.session.Definition().get_session()
        session.open()
        if str(session.open_state) == 'OpenState.Opened':
            get_historical_interday_data(universe, fields)
            #headlines = get_news_headlines(universe)
            #story_id = headlines.iloc[-1]['storyId']
            #print()
            #get_news_story(story_id)

        print('Close Session')
        ld.close_session()
    except Exception as ex:
        print(f'Error in open_session: {str(ex)}')
        sys.exit(1)

    
   
