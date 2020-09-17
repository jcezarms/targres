# TARGRES

TARGRES, or **T**ree-based **Arg**umetation **Res**olution, is a method for determining the robustness of a collaboratively discussed thesis, where arguments and counter-arguments can be represented as a tree. Based on the imbalance between pro-thesis and anti-thesis robustness, TARGRES ultimately confirms or debunks the thesis - all, of course, limited by public opinion reflected in the data.

# Introduction

Debate resolution helps shape social and scientific progress since the dawn
of time. In today's era this is not only factual offline - it's
also one of the backbones of the internet:

- StackOverflow and [over a hundred siblings](https://stackexchange.com/sites)
- [a](http://www.reddit.com/r/explainlikeimfive+doesanybodyelse+tipofmytongue+answers+explainlikeIAmA+relationship_advice+whatisthisthing+techsupport+explainlikeimcalvin+whatsthisbug+tipofmypenis+whatstheword+homeworkhelp+relationshipadvice+species+NoStupidQuestions) [vast](http://www.reddit.com/r/AskReddit+AskScience+AskHistorians+AskWomen+AskMen+AskCulinary+TrueAskReddit+AskSocialScience+AskEngineers+AskPhilosophy+AskScienceFiction+Ask_Politics+AskAcademia+AskTransgender+AskComputerScience+AskDrugs+AskFeminists+AskGames+AskPhotography+AskUk+AskStatistics+AskSciTech+AskSciTech+askGSM+AskModerators) [portion](http://www.reddit.com/r/help+findareddit+modhelp+csshelp+bugs+RESissues+askmoderators+aboutreddit) of Reddit
- Quora

... and the many forums in between. The whole ever-present world of
Q\&A was built to thrive on the resolution of various rarely one-sided
debates. The goal of
TARGRES is to help lead to intelligence that can receive a **debate as
input**, and **output the answer** that's most robust - and likely
right.  

This implementation makes use of BERT's embedding features, `LGBMRegressor` and a custom scraped dataset of a thousand discussions from the [Kialo](https://kialo.com). Through these, this study aims to understand and rank the robustness of argumentations in a discussion, with a combination of
textual context, localized social impact (feedback from ratings) and
ramifications (pros \& cons stemming from a given argumentation). 

# Conceptualization and Implementation

This is the Capstone Project of a Machine Learning Engineering specialization, so there are two main blocks of depth to be understood:
- [The study paper](./TARGRES_Project_Paper.pdf), containing all mathematical constructs in support of TARGRES.
- [The project Notebook](./TARGRES.ipynb), with the full implementation of the algorithm, along with documented sequential use of local modules.