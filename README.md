# Sentiment

Sentiment is a brane package for converting strings to a sentiment scores between -1 and 1. The expeceted input is an array of english strings.

## Installation

This package required an operational Brane Framework.
To set up this framework follow the official guide: https://docs.brane-framework.org/getting-started/installation

If on Linux or MacOS first run:

``` chmod +x sentiment.py ```

Otherwise/then:

```console
brane build container.yml --kind ecu
brane push sentiment 1.0.0
```

Or install using the brane import function: 
```
brane import lucasdegeus/braneSentiment --kind ecu
```

## Usage

```brane
import sentiment;
get_sentiment(["This is a very positive sentence!"]);
```

## Notes
Currently only the english language is supported. This package uses multiple python libraries including:
- spacy
- numpy
- nltk
- emosent
