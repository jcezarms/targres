"""A varied scale of Kialo-specific data filtering functions.
"""
from tree_mapping import METADATA, children

vote_types = ['false', 'improbable', 'plausible', 'probable', 'true']


def is_thesis(ID) -> bool:
    """The broadest and simplest method for identifying thesis `ID`s.
    """
    return ID and ID.endswith('.1')


def is_zeroth_node(obj) -> bool:
    """Identifies Kialo root nodes. Such nodes were of no use in the scope of this study.
    """
    return obj.get('id') and obj['id'].endswith('.0')


def find_claim(ID, discussion) -> dict:
    """Finds the first (if any) claim object linked to `ID` and within `discussion`.
    """
    return next(claim for claim in discussion['arguments']['claims'] if claim['id'] == ID)


def votes_for(obj, votes) -> dict:
    """Generates per-category vote count dict for `obj`. 
    """
    votes_by_id = votes.get(obj['id']) or [0] * len(vote_types)
    return dict(zip(vote_types, votes_by_id))

def is_useless_claim(claim):
    return any([
        is_zeroth_node(claim),
        claim.get('isDeleted') and claim['isDeleted'],
        claim.get('flag') is not None
    ])

def useful_claims_from(claims):
    useless = []
    for claim in claims:
        if is_useless_claim(claim):
            useless.append(claim)
            useless_children = METADATA[children].get(claim['id']) or []
            useless += useless_children
            
            parent_id = claim.get('parentId')
            if parent_id:
                METADATA[children][parent_id].remove(claim)
            
    return [claim for claim in claims if claim not in useless]

def is_useful_discussion(discussion):
    return all([
        [c for c in discussion['arguments']['claims'] if is_thesis(c['id'])],
        discussion['statistics']['voteCount'] > 0
    ])

def useful_discussions_from(discussions):
    return [d for d in discussions if is_useful_discussion(d)]