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
  - `SQLAlchemy==1.1.2`


```
pip install -r requirements.txt
```

### Usage

Generate database models:
```
python models.py
```

Then, insert tuples into database with:
```
python insert_data.py
```