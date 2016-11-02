## :bike: OpenBikes Challenge

### Setup Virtual environment

If your're using Anaconda:
```
conda create -n wheeling python=3
```

Then, activate it:
```
source activate wheeling
```

### Install dependencies

Requirements:
  - `click==6.6`
  - `numpy==1.11.2`
  - `pandas==0.19.0`
  - `sklearn==0.0`


```
pip install -r requirements.txt
```

### Usage

Data wrangling:
```
python get_data.py
```

Training step:
```
python train.py
```