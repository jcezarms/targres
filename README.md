<p align="center">
    <img style="cursor: default;" src="./logo/logo.svg" height="250px" alt="TARGRES Logo" />
</p>

| English | [Português](README-ptBR.md) |
| --- | --- |

---

TARGRES, or **T**ree-based **Arg**umetation **Res**olution, is a method for determining the robustness of a collaboratively discussed thesis, where arguments and counter-arguments can be represented as a tree. Based on the imbalance between pro-thesis and anti-thesis argumentation robustness, TARGRES ultimately confirms or debunks the thesis - all, of course, based on opinions reflected in the data.

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
input**, and **output the most robust answer** - and likely the
right one.  

Through a [custom scraped dataset](./data) of discussions from the [Kialo](https://kialo.com) website, this study aims to understand and rank the robustness of argumentations in a discussion, with a combination of
textual context, localized social impact (feedback from ratings) and
ramifications (pros \& cons) stemming from a given argumentation. 

# Concept
[TARGRES Paper](./TARGRES_Project_Paper.pdf) has the complete research, mathematical constructs in support of TARGRES and model benchmarks.

# How to use
In [TARGRES.ipynb](./TARGRES.ipynb) you'll find the sequential documented guide on using the algorithm.

# Running the code

The only necessary step:  
`pip install -r requirements.txt`

> The notebook assumes a [CUDA-enabled pytorch installation](https://pytorch.org/get-started/locally/#with-cuda-1) to run BERT's embedding process. A GPU with ~2.5k CUDA cores and 12GB RAM (compute 3.7) took ~1h30m to embed a batch of 100k rows.

After a successful installation, the execution of [TARGRES.ipynb](./TARGRES.ipynb) is sequential. Scraping and preprocessing can be entirely skipped, as section "5. Intelligence Architecture" will load the dataset from `data/clean_claims_df.pkl`.

# Next steps

- [ ] An argument-type-identifier should come for individual argument analysis. Which is potentially a full-fledged project, by itself.
    - Real-time impact involves strong single-argument strength analysis.
- [ ] An open interface to interact with TARGRES.
- [ ] Automate releases (e.g. through GitHub Actions).
- [ ] Normalize model fairness, as done in [scikit-fairness](https://github.com/koaning/scikit-fairness).
    - Either team up with Kialo itself, or deduce userbase demographics.
- [ ] Extrapolate TARGRES to external data (StackExchange or Reddit, e.g. [/r/changemyview](https://www.reddit.com/r/changemyview))
    - Labeling, adapting and running against [a well structured base argument](https://www.reddit.com/r/changemyview/comments/o3adet/cmv_antivax_doctors_and_nurses_and_other_licensed/) to start. Eventually a one-fits-_most_ implementation could be thought.