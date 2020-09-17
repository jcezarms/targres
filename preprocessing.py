"""Preprocessing logic used into Kialo data.
"""
import re
import nltk
import string
import pandas as pd
from collections import Counter

try:
    nltk.data.find('corpus/stopwords')
except LookupError:
    nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = Counter(stopwords.words('english')) # reduces complexity of stopword removal to ~O(1) with Counter

dropcols = {
    'discussions': [
        'argumentCount', 'viewCount', 'participantCount', 'contributionCount',
        'image', 'hasDefaultImage', 'language', 'effectiveRole', 'accessToken',
        'latestActivity.accountId', 'latestActivity.type', 'latestActivity.date',
        'arguments.touchedArguments', 'statistics.participantStatistics',
        'statistics.accountInfos', 'arguments.locations', 'activitiesLastDay',
        'activitiesLastWeek', 'isFresh', 'lastSeen', 'isArchived', 'isPublic',
        'trending', 'popular', 'featured', 'rank', 'voteCount'
    ],
    'claims': [
        'authorId', 'version', 'frontendOnlyLocation',
        'lastModifiedForSitemaps', 'edited', 'votes', 'isOrigin',
        'isDeleted', 'accepterId', 'copierId', 'discussionLinkTo'
    ]
}

def clean_text(text, lower=True, markdown=True, punctuation=True, stopwords=True) -> str:
    """Removes Markdown links and NLP-standard formattings from `text`.
    """
    clean_text = text.replace('\\', '')

    if lower:
        clean_text = clean_text.lower()
    if markdown:
        clean_text = re.sub(r'\[(.*)\]\(http[s]{0,}:.*\)', r'\1', clean_text)
    if punctuation:
        clean_text = clean_text.translate(str.maketrans('', '', string.punctuation))
    if stopwords:
        clean_text = ' '.join([word for word in clean_text.split() if word not in stop_words])
    
    return clean_text.strip()

def camel_to_snake(name: str) -> str:
    """Turns camelCased `name` into snake_case.
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def snakecols(df: pd.DataFrame) -> dict:
    """Makes a mapper dictionary, for renaming all `df.columns` to snake_case using `df.rename`.
    """
    return dict([(col, camel_to_snake(col)) for col in df.columns])

def discussions_to_df(discussions: list) -> pd.DataFrame:
    """Generates a discussion-centered DataFrame from the `discussions` list.

    Args:
        discussions (list): Designed to be the output of the `tree_mapping.map_as_tree` method.

    Returns:
        (pd.DataFrame): a DataFrame based on `discussions`.
    """
    discdf = pd.json_normalize(discussions).fillna(0)
    discdf.drop(columns=dropcols['discussions'], inplace=True)

    statscols = dict([(col, col.split('.')[1]) for col in discdf.columns if '.' in col])
    discdf.rename(mapper=statscols, axis='columns', inplace=True)

    discdf.rename(mapper=snakecols(discdf), axis='columns', inplace=True)
    return discdf

def discussions_to_claim_df(discussions_df: pd.DataFrame) -> pd.DataFrame:
    """Generates a one-claim-per-row processed DataFrame from `discussions_df`.

    Args:
        discussions_df (pd.DataFrame): result of the `discussions_to_df()` method

    Returns:
        (pd.DataFrame): a DataFrame of claims also containing each claim's discussion metadata.
    """
    claim_basedf = discussions_df.explode('claims').reset_index().drop(columns='index')
    claimdf = claim_basedf.claims.apply(pd.Series)
    claimdf.drop(columns=dropcols['claims'], inplace=True)

    claimdf.rename(mapper=snakecols(claimdf), axis='columns', inplace=True)

    claimcols = dict([(col, 'claim_' + col) for col in claimdf.columns])
    claimdf.rename(mapper=claimcols, axis='columns', inplace=True)

    claimdf = claimdf.join(claim_basedf.drop(columns='claims'))
    discussioncols = dict([(col, 'disc_' + col) for col in claim_basedf.columns if col != 'claims'])
    claimdf.rename(mapper=discussioncols, axis='columns', inplace=True)

    return claimdf