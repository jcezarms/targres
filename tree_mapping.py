"""Core functions for backtracking and reproducing dicussion-tree data structures from the scraped dataset.

Most of this module's functions are inplace operations, purposefuly having a ` -> None` return type.
"""
import numpy as np
from tqdm import tqdm

from data_filters import *

METADATA = {}
votes = 'votes'
parents = 'parents'
children = 'children'

location_keys = ['isOrigin', 'parentId', 'relation', 'isDeleted']
vote_types = ['false', 'improbable', 'plausible', 'probable', 'true']


def merge_location_data(claim: dict, discussion: dict) -> None:
    """Adds metadata (like `parentId` and `isDeleted`) into `claim` from Kialo's `locations` list.
    
    Also updates `claim`'s parent and children links, given the newly added `parentId`.
    """
    if is_zeroth_node(claim):
        return claim
    
    location = [
        loc for loc in discussion['arguments']['locations'] if loc['targetId'] == claim['id']
    ]

    if location and not location[0]['parentId'].endswith('.0'):
        location = location[0]
        parent_id = location['parentId']

        METADATA[parents][claim['id']] = find_claim(parent_id, discussion)
        METADATA[children][parent_id] = (METADATA[children].get(parent_id) or []) + [claim]

        for k in location_keys:
            claim[k] = location[k]
    else:
        # Thesis or 0th node
        METADATA[parents][claim['id']] = None
    
    return claim

def set_tree_metadata(parent: dict, total_votes: int) -> None:
    """Traverses the subtree under `parent`, assigning metadata like level and avg. impact to all nodes.
    """
    if is_thesis(parent['id']):
        parent['level'] = 0
        parent['avg_impact'] = np.mean(list(parent['votes'].values())) / total_votes

    subtree = METADATA[children].get(parent['id']) or []

    if subtree:
        for child in subtree:
            child['level'] = parent['level'] + 1
            child['avg_impact'] = (sum(child['votes'].values()) / 5) / total_votes
            
            set_tree_metadata(child, total_votes)

    parent['pros'] = [child['id'] for child in subtree if child['relation'] == 1]
    parent['cons'] = [child['id'] for child in subtree if child['relation'] == -1]

def traverse_robustness(claim: dict, discussion: dict, assign_values=True) -> float:
    """Recursive robustness of a claim, based on its weight and the weights of its entire subtree.
    
    Args:
        claim (dict): The claim for which to calculate robustness.
        discussion (list): The discussion `claim` belongs to.
        assign_values (bool): If set to `True`, calculated values will be 
            assigned to the claims as their `robustness` attribute.

    Returns:
        (float): The recursive robustness for the current `claim`.
    """
    pro_children = [find_claim(child_id, discussion) for child_id in claim['pros']]
    con_children = [find_claim(child_id, discussion) for child_id in claim['cons']]
    pro_score = sum(
        [traverse_robustness(child, discussion) for child in pro_children]
    ) or 1.0
    con_score = sum(
        [traverse_robustness(child, discussion) for child in con_children]
    ) or 1.0

    if is_thesis(claim['id']):
        R = pro_score / con_score
    else:
        R = claim['weight'] * (pro_score / con_score)
        
    if assign_values:
        claim['robustness'] = R

    return R

def votes_for(obj: dict, votes: dict) -> dict:
    """Generates per-category vote count dict for `obj`.
    
    Each of Kialo's 5 rating types, from "false" to "true",
    will have their own vote count in the resulting dict, starting from 0.
    Defaults all vote values to 0 if an entry of `obj['id']` isn't found in `votes`.

    An example of the returned vote dictionary:
    ```
    {
        'false': 17,
        'improbable': 11,
        'plausible': 5,
        'probable':3,
        'true': 20
    }
    ```
    """
    votes_by_id = votes.get(obj['id']) or [0] * len(vote_types)
    return dict(zip(vote_types, votes_by_id))


def map_as_tree(discussions: list, with_tqdm=True) -> None:
    """Traverses all votes and claims from `discussions` for robustness calculations,
    throwing out unusable data and linking parent nodes to child nodes in the meantime.

    Parent and children links are kept by storing node IDs in the local `METADATA` dictionary.

    Args:
        discussions (list): A list of discussions.
        with_tqdm (bool): Determines if a progress bar should be spawned.
    """
    loop_wrap = tqdm if with_tqdm else lambda x: x
    METADATA[votes] = {}
    METADATA[parents] = {}
    METADATA[children] = {}

    discussions = useful_discussions_from(discussions)

    for discussion in loop_wrap(discussions):
        claims = discussion['arguments']['claims']
        claims[:] = [merge_location_data(claim, discussion) for claim in claims]
        claims[:] = useful_claims_from(claims)
        
        for claim in claims:
            claim['votes'] = votes_for(claim, discussion['votes'])
        
        
        thesis = next(claim for claim in claims if is_thesis(claim['id']))
        total_votes = discussion['statistics']['voteCount']
        set_tree_metadata(thesis, total_votes)
        
        claims[:] = [claim for claim in claims if 'level' in claim]
        max_tree_level = max([claim['level'] for claim in claims])
        for claim in claims:
            if claim['level'] > 0:
                claim['weight'] = claim['avg_impact'] + (max_tree_level / claim['level'])
                
        discussion['thesis_robustness'] = traverse_robustness(thesis, discussion, assign_values=True)
        discussion['avg_veracity'] = sum(thesis['votes'].values()) / 5
        
        METADATA[votes][discussion['id']] = discussion['votes']
        del discussion['votes']
