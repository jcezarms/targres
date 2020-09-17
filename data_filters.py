"""A varied scale of Kialo-specific data filtering functions.
"""
from tree_mapping import METADATA, children

vote_types = ['false', 'improbable', 'plausible', 'probable', 'true']


def is_thesis(ID) -> bool:
    """The broadest and simplest method for identifying Kialo thesis `ID`s.
    """
    return ID and ID.endswith('.1')


def is_zeroth_node(obj) -> bool:
    """Identifies Kialo root nodes.
    
    These root nodes were of no use in the scope of this study,
    since they theoretically contain only the most generic information
    about a (supposedly) newly created discussion.
    """
    return obj.get('id') and obj['id'].endswith('.0')


def find_claim(ID, discussion) -> dict:
    """Finds the first (if any) claim object linked to `ID` and within `discussion`.
    """
    return next(claim for claim in discussion['arguments']['claims'] if claim['id'] == ID)

def is_useless_claim(claim) -> bool:
    """Defines conditions for the uselessness of `claim`.

    Any claim that either a) has an ID that indicates it's the 0th ID node;
    b) is currently under deletion, or c) contains any flag indicating inconsistencies,
    will be declared as "useless" from the point of view of this study, for which case a
    `True` is returned.
    """
    return any([
        is_zeroth_node(claim),
        claim.get('isDeleted') and claim['isDeleted'],
        claim.get('flag') is not None
    ])

def useful_claims_from(claims: list):
    """Based on `is_useless_claim`, filters `claims` entries.

    If a condition of uselessness is met, both the tagged claim
    and all of its children are filtered out of `claims`.
    The filtered claims are also removed from their parents' children map.
    """
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
    """If `discussion` contains a thesis node and a total vote count above 0, returns `True`.
    """
    return all([
        [c for c in discussion['arguments']['claims'] if is_thesis(c['id'])],
        discussion['statistics']['voteCount'] > 0
    ])

def useful_discussions_from(discussions):
    """Filters `discussions` based on `is_useful_discussion`.

    Discussions that don't attend these conditions cannot possibly
    be processed by the study's pipeline.
    """
    return [d for d in discussions if is_useful_discussion(d)]