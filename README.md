# Bagel Jam
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ServiceInnovationLab/bagel-jam/master)

This is a repository to interpret submission data and serve it up as tasty tasty ~~jam~~ JSON for visualisation and further analysis.

It has a few parts, and some more READMEs:

- A subset of submissions from the Zero Carbon Bill and a Te Reo Māori corpus - more details in the READMEs for those folders
- Amazon Comprehend's topic modelling, key phrase detection, and sentiment analysis of these
- Jupyter notebooks to play with the data - these are interactive at [Binder](https://mybinder.org/v2/gh/ServiceInnovationLab/bagel-jam/master)
- The JSON files in `docs` are served with GitHub Pages

To run notebooks locally:

```
# Install correct python version (you'll need pyenv)
pyenv < .python-version
# install dependencies
pip install -r requirements.txt
# spin up the notebook
jupyter notebook
```
