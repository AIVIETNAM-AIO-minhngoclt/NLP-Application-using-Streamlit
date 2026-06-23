# Streamlit NLP Pipeline Demo

A simple NLP web application built with Streamlit, featuring two main functions: text translation and spell checking.

## Features

- **Text Translation**: Automatically detects the input language and translates it to the target language of your choice
- **Spell Checking**: Detects the input language and corrects spelling mistakes

## Installation

```bash
pip install streamlit langdetect pyspellchecker nltk langcodes deep-translator
```

## Usage

```bash
streamlit run app.py
```

## Supported Languages

**Translation**: Vietnamese, English, French, Japanese, Chinese, Korean, Spanish, German

**Spell Checking**: English, Spanish, French, Portuguese, German, Russian, Arabic, Basque, Latvian, Dutch

## Dependencies

| Library | Purpose |
|---|---|
| `streamlit` | Web interface |
| `langdetect` | Language detection |
| `pyspellchecker` | Spell checking |
| `nltk` | Tokenization |
| `langcodes` | Language code to name conversion |
| `deep-translator` | Text translation via Google |
