## Obtaining data

Please consult top-level README.md.


## Directory layout

|-- data | Experiment datasets.
|   |-- avstats-pdf.shelve | VirusTotal reports of PDF files as Python shelve file.
|   |-- avstats-swf.shelve | VirusTotal reports of SWF files as Python shelve file.
|   |
|   |-- pdf | Extracted numeric features (with SPC) from PDF files in LibSVM format.
|   |   |-- w05-test.libsvm | Evaluation samples (arrived in week 5).
|   |   |-- w05-train.libsvm | Training samples (collected before week 5).
|   |   |-- ...
|   |   |-- w14-test.libsvm | Evaluation samples arrived in last week.
|   |   `-- w14-train.libsvm | Training samples (collected from weeks 10 to 13).
|   |
|   |-- pdf-bin | Extracted binary features (with SPC) from PDF files in LibSVM format.
|   |   |-- w05.nppf | A list of features extracted from first training set.
|   |   |-- w05-test.libsvm | Evaluation samples (arrived in week 5).
|   |   |-- w05-train.libsvm | Training samples (collected before week 5).
|   |   |-- ...
|   |   |-- w14.nppf | A list of features extracted from last training set.
|   |   |-- w14-test.libsvm | Evaluation samples arrived in last week.
|   |   `-- w14-train.libsvm | Training samples (collected from weeks 10 to 13).
|   |
|   |-- SL2013 | Extracted binary features (without SPC) from PDF files in LibSVM format, used in Srndic and Laskov (2013).
|   |   |-- w01.nppf | A list of features extracted from first training set.
|   |   |-- w01-test.libsvm | Evaluation samples (arrived in week 5).
|   |   |-- w01-train.libsvm | Training samples (collected before week 5).
|   |   |-- ...
|   |   |-- w10.nppf | A list of features extracted from last training set.
|   |   |-- w10-test.libsvm | Evaluation samples arrived in last week.
|   |   `-- w10-train.libsvm | Training samples (collected from weeks 10 to 13).
|   |
|   |-- swf | SWF-Normal - extracted numerical features (with SPC) from SWF files in LibSVM format.
|   |   |-- p05-test.libsvm | Evaluation samples (arrived in week 5).
|   |   |-- p05-train.libsvm | Training samples (collected before week 5).
|   |   |-- ...
|   |   |-- p14-test.libsvm | Evaluation samples arrived in last week.
|   |   `-- p14-train.libsvm | Training samples (collected from weeks 10 to 13).
|   |
|   `-- swf-keepmal | SWF-KeepMal - as previous, but retaining malicious training samples indefinitely.
|       |-- p05-test.libsvm | Evaluation samples (arrived in week 5).
|       |-- p05-train.libsvm | Training samples (collected before week 5).
|       |-- ...
|       |-- p14-test.libsvm | Evaluation samples arrived in last week.
|       `-- p14-train.libsvm | Training samples (benign collected from weeks 10 to 13, malicious from 1 to 13).


