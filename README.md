# Hidost Eurasip result reproduction

Copyright 2015 Nedim Srndic, University of Tuebingen
nedim.srndic@uni-tuebingen.de

Source code for the reproduction of experiments and figures 
published in the paper "Hidost: a static machine-learning-based 
malicious software detector for multiple file formats". 


## Environment and prerequisits

This code has been tested under Ubuntu 14.04 with the following packages 
installed:

* python-matplotlib 
* python-scipy 
* python-scikits-learn 
* texlive-full (for the plot style)


## Directory layout

```
root
|-- README.md | This file.
|-- Makefile | Makefile for experiment and plot reproduction.
|
|-- data | Put experiment datasets here.
|
|-- exper | After running the Makefile, experiment results will be saved here as Python pickle files. 
|   |-- pdf | Hidost results on PDF data.
|   |   |-- result-bin.pickle | Binary features.
|   |   `-- result.pickle | Numerical features.
|   |
|   |-- SL2013 | Results of the SL2013 method on PDF data.
|   |   |-- result.pickle | Using SVM.
|   |   `-- result-rf.pickle | Using Random Forest.
|   |
|   |-- swf | Results on SWF-Normal.
|   |   |-- result-bin.pickle | Binary features.
|   |   `-- result.pickle | Numerical features.
|   |
|   `-- swf-keepmal
|       |-- result-bin.pickle | Binary features.
|       `-- result.pickle | Numerical features.
|
|-- plots | After running the Makefile, plots will be saved here in both PDF and EPS format.
|   |-- feat-drift.eps | Figure 12.
|   |-- feat-drift.pdf | Figure 12.
|   |-- pdf-avstats.eps | Figure 18, left.
|   |-- pdf-avstats.pdf | Figure 18, left.
|   |-- pdf-comparison.eps | Figure 16.
|   |-- pdf-comparison.pdf | Figure 16.
|   |-- pdf-data.eps | Figure 13.
|   |-- pdf-data.pdf | Figure 13.
|   |-- swf-avstats.eps | Figure 18, right.
|   |-- swf-avstats.pdf | Figure 18, right.
|   |-- swf-comparison.eps | Figure 17.
|   |-- swf-comparison.pdf | Figure 17.
|   |-- swf-data.eps | Figure 14.
|   |-- swf-data.pdf | Figure 14.
|   |-- swf-data-keepmal.eps | Figure 15.
|   `-- swf-data-keepmal.pdf | Figure 15.
|
`-- src | Python source code for experiment reproduction and plotting.
    |-- avstats.py | Antivirus comparison plot. 
    |-- dataset_partitioning.py | Dataset plot.
    |-- datasets.py | Python module for dataset handling.
    |-- experiment.py | Experiment reproduction.
    |-- feat_drift.py | Feature drift plot.
    |-- method_comparison.py | Classification performance comparison of different methods.
    |-- plots.py | Python module for plotting.
```

## Obtaining data

You can download the entire dataset required to reproduce all results and 
plots from [here](https://drive.google.com/file/d/0ByiDcbjWwz4tcDVaMFNCaThDSXM/). 
Extract the contents of the archived file into the `data/` directory. 

## Reproducing results

To reproduce all results, run `make all` in the root directory 
of the uncompressed archive. 

Experiments on NDSS 2013 dataset and features using Random Forest as 
classifier may lead to a memory consumption of over 20 GB. 
To combat this effect, training dataset subsampling has been implemented 
and set to 20%. 
It is controlled by the `SUBSAMPLE_PERC` makefile variable. 

Reproduction of all results takes around 24 hours on a virtualized test 
system with 3 CPU cores (with HT) and 12 GB of RAM. 
The resulting plots are saved in the `plots/` directory. 

## Licensing

Hidost is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Hidost is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Hidost.  If not, see <http://www.gnu.org/licenses/>.

