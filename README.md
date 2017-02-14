# GoMoKu
GoMoKu implementation with Monte Carlo Search Tree and value network

# Installation
```cmd
$git clone https://github.com/s8w1e2ep/GoMoKu.git
```

# Dependency
```python
import GUI;
import Tkinter;
import os;
import time;
import ast;
import random;
import math;
import numpy;
```

# Method
## Monte Carlo Tree Search
> Use UCB1 selection

<p>Initial setting</p>
* MAX_TIME = 3 (seconds)
* MAX_MOVE = 100
* C = 1.4

## Value network
Detect GoMoKu shape and calculate value
* Five in a row - 99999
* Live four - 10000
* Die four and other - 3000
* Die four - 2500
* Live three - 1500
* Live two and other - 650
* Die three - 500
* Die two - 150

# Execution
```python
python main.py
```

# License
MIT
