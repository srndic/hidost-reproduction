############################ CONFIGURATION ###################################
SHELL:=/bin/bash

### Important directories
PLOT_DIR:=plots
SRC_DIR:=src
EXPER_DIR:=exper
DATA_DIR:=data

### Python scripts
DATASET_PARTITIONING:=$(SRC_DIR)/dataset_partitioning.py
METHOD_COMPARISON:=$(SRC_DIR)/method_comparison.py
FEAT_DRIFT:=$(SRC_DIR)/feat_drift.py
EXPERIMENT:=$(SRC_DIR)/experiment.py
AVSTATS:=$(SRC_DIR)/avstats.py

### Data files
AVSTATS_PDF:=$(DATA_DIR)/avstats-pdf.shelve
AVSTATS_SWF:=$(DATA_DIR)/avstats-swf.shelve

### Feature lists
SL2013_FEATS:=$(shell echo $(DATA_DIR)/SL2013/w{01..10}.nppf)
PDF_SPC_FEATS:=$(shell echo $(DATA_DIR)/pdf-bin/w{05..14}.nppf)

### Training/test files
# SL2013
SL2013_TR:=$(shell echo $(DATA_DIR)/SL2013/w{01..10}-train.libsvm)
SL2013_TE:=$(shell echo $(DATA_DIR)/SL2013/w{01..10}-test.libsvm)
# PDF with SPC
PDF_BIN_TR:=$(shell echo $(DATA_DIR)/pdf-bin/w{05..14}-train.libsvm)
PDF_BIN_TE:=$(shell echo $(DATA_DIR)/pdf-bin/w{05..14}-test.libsvm)
# PDF with SPC and numerical values
PDF_TR:=$(shell echo $(DATA_DIR)/pdf/w{05..14}-train.libsvm)
PDF_TE:=$(shell echo $(DATA_DIR)/pdf/w{05..14}-test.libsvm)
# SWF with SPC and numerical values
SWF_TR:=$(shell echo $(DATA_DIR)/swf/p{05..14}-train.libsvm)
SWF_TE:=$(shell echo $(DATA_DIR)/swf/p{05..14}-test.libsvm)
# SWF with SPC and numerical values and KeepMal
SWF_KEEPMAL_TR:=$(shell echo $(DATA_DIR)/swf-keepmal/p{05..14}-train.libsvm)
SWF_KEEPMAL_TE:=$(shell echo $(DATA_DIR)/swf-keepmal/p{05..14}-test.libsvm)

### Experiment result files
# SWF
SWF_RES:=$(EXPER_DIR)/swf.pickle
SWF_BIN_RES:=$(EXPER_DIR)/swf-bin.pickle
SWF_KEEPMAL_RES:=$(EXPER_DIR)/swf-keepmal.pickle
SWF_KEEPMAL_BIN_RES:=$(EXPER_DIR)/swf-keepmal-bin.pickle
# PDF
SL2013_RES:=$(EXPER_DIR)/SL2013.pickle
SL2013_RF_RES:=$(EXPER_DIR)/SL2013-rf.pickle
PDF_RES:=$(EXPER_DIR)/pdf.pickle
PDF_BIN_RES:=$(EXPER_DIR)/pdf-bin.pickle

### Experiment settings
REPETITIONS:=10
SUBSAMPLE_PERC:=0.2


####################################################################
####################### EXPERIMENTS ################################
####################################################################

RESs:=$(SWF_RES) $(SWF_BIN_RES) $(SWF_KEEPMAL_RES) $(SWF_KEEPMAL_BIN_RES) \
      $(SL2013_RES) $(SL2013_RF_RES) $(PDF_BIN_RES) $(PDF_RES)


########################### SWF ####################################

$(SWF_RES): $(SWF_TR) $(SWF_TE)
	python $(EXPERIMENT) \
		--train $(SWF_TR) \
		--test $(SWF_TE) \
		--count $(REPETITIONS) \
		--avstats $(AVSTATS_SWF) \
		--res-out $@


######################### SWF BIN ##################################

$(SWF_BIN_RES): $(SWF_TR) $(SWF_TE)
	python $(EXPERIMENT) \
		--train $(SWF_TR) \
		--test $(SWF_TE) \
		--count $(REPETITIONS) \
		--avstats $(AVSTATS_SWF) \
		--binarize \
		--res-out $@


####################### SWF KEEPMAL ################################

$(SWF_KEEPMAL_RES): $(SWF_KEEPMAL_TR) $(SWF_KEEPMAL_TE)
	python $(EXPERIMENT) \
		--train $(SWF_KEEPMAL_TR) \
		--test $(SWF_KEEPMAL_TE) \
		--count $(REPETITIONS) \
		--avstats $(AVSTATS_SWF) \
		--res-out $@


####################### SWF KEEPMAL BIN ############################

$(SWF_KEEPMAL_BIN_RES): $(SWF_KEEPMAL_TR) $(SWF_KEEPMAL_TE)
	python $(EXPERIMENT) \
		--train $(SWF_KEEPMAL_TR) \
		--test $(SWF_KEEPMAL_TE) \
		--count $(REPETITIONS) \
		--avstats $(AVSTATS_SWF) \
		--binarize \
		--res-out $@


########################### PDF ####################################

$(PDF_RES): $(PDF_TR) $(PDF_TE)
	python $(EXPERIMENT) \
		--train $(PDF_TR) \
		--test $(PDF_TE) \
		--count $(REPETITIONS) \
		--avstats $(AVSTATS_PDF) \
		--res-out $@


########################### PDF BIN ################################

$(PDF_BIN_RES): $(PDF_BIN_TR) $(PDF_BIN_TE)
	python $(EXPERIMENT) \
		--train $(PDF_BIN_TR) \
		--test $(PDF_BIN_TE) \
		--count $(REPETITIONS) \
		--avstats $(AVSTATS_PDF) \
		--res-out $@


########################### SL 2013 ################################

$(SL2013_RES): $(SL2013_TR) $(SL2013_TE)
	python $(EXPERIMENT) \
		--train $(SL2013_TR) \
		--test $(SL2013_TE) \
		--count 1 \
		--avstats $(AVSTATS_PDF) \
		--classifier SVM \
		--subsample $(SUBSAMPLE_PERC) \
		--res-out $@


########################### SL 2013 RF #############################

$(SL2013_RF_RES): $(SL2013_TR) $(SL2013_TE)
	python $(EXPERIMENT) \
		--train $(SL2013_TR) \
		--test $(SL2013_TE) \
		--count 2 \
		--avstats $(AVSTATS_PDF) \
		--subsample $(SUBSAMPLE_PERC) \
		--res-out $@


####################################################################
######################### PLOTS ####################################
####################################################################

PDFs:=swf-data.pdf swf-data-keepmal.pdf pdf-data.pdf \
	  swf-comparison.pdf pdf-comparison.pdf \
	  feat-drift.pdf \
	  swf-avstats.pdf pdf-avstats.pdf
PDFs:=$(PDFs:%=$(PLOT_DIR)/%)

EPSs:=$(PDFs:.pdf=.eps)


############ DATASET PARTITIONING ##################################

$(PLOT_DIR)/swf-data.pdf $(PLOT_DIR)/swf-data.eps: $(SWF_TR) $(SWF_TE)
	python $(DATASET_PARTITIONING) \
		--train $(SWF_TR) \
		--test $(SWF_TE) \
		--data-plot $(PLOT_DIR)/swf-data.{pdf,eps}

$(PLOT_DIR)/swf-data-keepmal.pdf $(PLOT_DIR)/swf-data-keepmal.eps: \
        $(SWF_KEEPMAL_TR) $(SWF_KEEPMAL_TE)
	python $(DATASET_PARTITIONING) \
		--train $(SWF_KEEPMAL_TR) \
		--test $(SWF_KEEPMAL_TE) \
		--legend none \
		--data-plot $(PLOT_DIR)/swf-data-keepmal.{pdf,eps}

$(PLOT_DIR)/pdf-data.pdf $(PLOT_DIR)/pdf-data.eps: $(PDF_TR) $(PDF_TE)
	python $(DATASET_PARTITIONING) \
		--train $(PDF_TR) \
		--test $(PDF_TE) \
		--legend none \
		--data-plot $(PLOT_DIR)/pdf-data.{pdf,eps}


#################### METHOD COMPARISON #############################

$(PLOT_DIR)/swf-comparison.pdf $(PLOT_DIR)/swf-comparison.eps: \
        $(SWF_BIN_RES) $(SWF_RES) $(SWF_KEEPMAL_BIN_RES) $(SWF_KEEPMAL_RES)
	python $(METHOD_COMPARISON) \
		--res $(SWF_BIN_RES) $(SWF_RES) $(SWF_KEEPMAL_BIN_RES) \
			$(SWF_KEEPMAL_RES) \
		--methods 'SWF-Normal binary' 'SWF-Normal numerical' \
			'SWF-KeepMal binary' 'SWF-KeepMal numerical' \
		--metrics AUC acc TPR FPR \
		--plot $(PLOT_DIR)/swf-comparison.{pdf,eps} \
		--legend 'lower right/1'

$(PLOT_DIR)/pdf-comparison.pdf $(PLOT_DIR)/pdf-comparison.eps: \
       $(SL2013_RES) $(SL2013_RF_RES) $(PDF_BIN_RES) $(PDF_RES)
	python $(METHOD_COMPARISON) \
		--res $(SL2013_RES) $(SL2013_RF_RES) $(PDF_BIN_RES) $(PDF_RES) \
		--methods "SL2013 reproduction" "SL2013 + Random Forest" \
			'Hidost binary' 'Hidost numerical' \
		--metrics AUC acc TPR FPR \
		--legend best/1 \
		--plot $(PLOT_DIR)/pdf-comparison.{pdf,eps}


######################### FEAT DRIFT ###############################

$(PLOT_DIR)/feat-drift.pdf $(PLOT_DIR)/feat-drift.eps: \
        $(SL2013_FEATS) $(PDF_SPC_FEATS)
	python $(FEAT_DRIFT) \
		--first $(SL2013_FEATS) \
		--second $(PDF_SPC_FEATS) \
		--methods 'Without SPC' 'With SPC' \
		--metrics Add Del Same \
		--legend best/0 \
		--plot $(PLOT_DIR)/feat-drift.{pdf,eps}


########################## AVSTATS #################################

$(PLOT_DIR)/swf-avstats.pdf $(PLOT_DIR)/swf-avstats.eps: $(SWF_KEEPMAL_RES)
	python $(AVSTATS) $(SWF_KEEPMAL_RES) \
		--plot $(PLOT_DIR)/swf-avstats.{pdf,eps}

$(PLOT_DIR)/pdf-avstats.pdf $(PLOT_DIR)/pdf-avstats.eps: $(PDF_RES)
	python $(AVSTATS) $(PDF_RES) \
		--plot $(PLOT_DIR)/pdf-avstats.{pdf,eps}


############################ ALL ###################################

all: $(PDFs)

clean: 
	rm -f $(PDFs) $(EPSs) $(RESs)

.PHONY: all clean .NOTPARALLEL

# Running in parallel doesn't make sense because individual 
# experiments are already parallelized
.NOTPARALLEL:

