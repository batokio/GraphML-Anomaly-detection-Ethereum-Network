#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 17:04:47 2022

@author: Bryan
"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import concatenate, square, array, trace, amax
from math import sqrt
from tqdm.notebook import tqdm
from datetime import datetime
from datetime import timedelta
from scipy.sparse import identity, diags
import pickle