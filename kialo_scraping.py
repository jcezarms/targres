"""Provides data scraping utilities used for the retrieval of data through Kialo's APIs.
"""
import requests
from tqdm import tqdm

domain = 'https://www.kialo.com/api/v1'


def get_discussions() -> list:
    """Retrieves generic discussion objects from Kialo.
    """
    disc_params = {
        'filter': 'promoted',
        'limit': 1000,
        'skip': 0,
        'sort': 'view_count'
    }
    return requests.get(f'{domain}/discussions', params=disc_params).json()['discussions']


def get_stats(discussion) -> dict:
    """Retrieves real-time statistics for a `discussion` from Kialo.
    """
    path = f'https://www.kialo.com/api/v1/discussions/{discussion["id"]}/statistics'
    return requests.get(path).json()


def get_args(discussion) -> dict:
    """Retrieves argumentations within `discussion` from Kialo.
    """
    path = f'{domain}/arguments?discussionId={discussion["id"]}'
    return requests.get(path).json()


def get_votes(discussion) -> dict:
    """Retrieves votes on both argumentations and the thesis itself.
    """
    path = f'{domain}/discussions/{discussion["id"]}/perspectives/1/votes?filter=all'
    return requests.get(path).json()['votes']


def scrape_into(discussions, with_tqdm=True):
    """Loops the retrieval of statistics, votes and argumentations for all `discussions`.

    Accepts the response of `get_discussions()`, but was made separate from it 
    to organically prevent loss of progress in case of mid-loop exceptions.

    Args:
        discussions (list): A list of discussions.
        with_tqdm (bool): Determines if a progress bar should be spawned.
    """
    loop_wrap = tqdm if with_tqdm else lambda x: x

    for discussion in loop_wrap(discussions):
        try:
            discussion['votes'] = get_votes(discussion)
            discussion['arguments'] = get_args(discussion)
            discussion['statistics'] = get_stats(discussion)
        except Exception as e:
            are_votes_in = discussion.get('votes') is not None
            are_args_in = discussion.get('arguments') is not None
            are_stats_in = discussion.get('statistics') is not None
            
            prefix = f'[Votes in: {are_votes_in} | Args in: {are_args_in} | Stats in: {are_stats_in}]'
            print(f'{prefix} Interrupting due to:\n{e}')
            
            raise e
