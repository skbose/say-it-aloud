# Say it Aloud

## Overview

Say it Aloud is a web application that allows users to convert Bengali speech to text. It provides a simple and intuitive interface for users to record their speech and convert it to text.

## Features

- Record and convert Bengali speech to text
- Real-time transcription
- User-friendly interface

# Prerequisites

Host the model on Hugging Face Inference API.<br/>
Model ID: `https://huggingface.co/bangla-speech-processing/BanglaASR`

Rename `.env.default` to `.env` and update the `HF_MODEL_URL` and `HF_TOKEN` in the `.env` file.

## Installation

```
conda create -n say-it-aloud python=3.10
conda activate say-it-aloud
```

```
git clone https://github.com/yourusername/say-it-aloud.git
cd say-it-aloud
```

```
pip install -r requirements.txt
```

```
poetry install
```


## Run the application

```
python -m engine.main
```

## TODO

- [ ] Add auto-correct using Indic LLMs
- [ ] Add voice-based navigation
- [ ] Add option to fine-tune the model on custom voice-samples
