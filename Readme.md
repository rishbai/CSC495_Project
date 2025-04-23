# Defect Predictor using RepoMiner

This project provides an implementation of a Defect Predictor by leveraging RepoMiner and PyDriller to analyze commit history and predict the risk associated with files in a given revision. It extends the RepoMiner example and includes risk calculation based on commit history.

## Features
- Traverse Git repositories to identify modified Python files.
- Classify fixing commits using a `FixingCommitClassifier`.
- Calculate risk scores for Python files based on bug revisions and modification frequency.

# Setup Instructions


## Installation
Follow the steps below to set up and run the project:

### 1. Clone the repository

```bash
git clone https://github.com/rishbai/CSC495_Project.git
```

### 2. Build the docker file
Create a docker image (see Dockerfile) for the project: 
```bash
docker build -t defect-predictor .
```

### 3. Run the project
Run the docker container from the image. See instruction RUN at the end of Dockerfile. It will execute the harness function within a docker container, print the results, and exit.
```bash
docker run --rm -it defect-predictor
```
  #### Expected output:
  ```plaintext
  Risky Python files: {'local_fno_block.py', 'data_pipeline.py', 'training_state.py', 'gino.py', 'coda_layer.py', 'trainer.py', 'spherical_convolution.py', 'conf.py', 'plot_UNO_darcy.py', 'plot_darcy_flow_spectrum.py', 'data_losses.py', 'padding.py', '__init__.py', 'train_darcy.py', 'losses.py', 'darcy.py', 'spectral_convolution.py', 'utils.py', 'einsum_utils.py', 'uno.py', 'discrete_continuous_convolution.py', 'zarr_dataset.py', 'data_processors.py', 'pt_dataset.py', 'adamw.py', 'skip_connections.py', 'integral_transform.py', 'transforms.py', 'plot_count_flops.py', 'mesh_datamodule.py', 'mlp.py', 'fnogno.py', 'gno_block.py', 'base_model.py', 'train_cfd.py', 'tfno.py', 'embeddings.py', 'car_cfd_dataset.py', 'complex.py', 'plot_SFNO_swe.py', 'codano.py', 'burgers.py', 'plot_DISCO_convolutions.py', 'navier_stokes.py', 'attention_kernel_integral.py', 'incremental.py', 'base_spectral_conv.py', 'plot_FNO_darcy.py', 'comm.py', 'model_dispatcher.py', 'train_gino_carcfd.py', 'hdf5_dataset.py', 'tensor_dataset.py', 'checkpoint_FNO_darcy.py', 'segment_csr.py', 'train_navier_stokes.py', 'setup.py', 'fno.py', 'differential_conv.py', 'plot_darcy_flow.py', 'tune_darcy.py', 'callbacks.py', 'patching.py', 'meta_losses.py', 'train_burgers.py', 'data_transforms.py', 'fno_block.py', 'resample.py', 'output_encoder.py'}

Calculating risk scores...

Risk Scores (File Name -> Risk Value):
resample.py -> 147.9327
torch_setup.py -> 133.9377
__init__.py -> 202.93380000000002
cfd_dataset.py -> 138.9344
pt_dataset.py -> 988.5351
plot_neighbor_search.py -> 65.9695
differential_conv.py -> 245.8853
local_no_block.py -> 900.576
model_dispatcher.py -> 185.9165
data_pipeline.py -> 479.7756
fno.py -> 2873.6638
tensor_galore_projector.py -> 104.9505
meta_losses.py -> 108.9495
embeddings.py -> 698.6727
tensor_dataset.py -> 173.921
positional_embeddings.py -> 273.8703
plot_embeddings.py -> 116.9449
normalization_layers.py -> 48.9784
local_no.py -> 488.7686
integral_transform.py -> 983.5407
plot_FNO_darcy.py -> 315.8575
gino.py -> 1175.4471
attention_kernel_integral.py -> 621.7111
burgers.py -> 773.639
padding.py -> 531.7589
trainer.py -> 2993.6011
train_cfd.py -> 356.8325
train_burgers.py -> 330.8489
patching.py -> 600.7167
mappings.py -> 114.9458
darcy.py -> 1257.4095
uno.py -> 1001.5395
codano.py -> 616.7078
fourier_continuation.py -> 74.9656
coda_layer.py -> 549.74
login_wandb.py -> 1.9995
fnogno.py -> 1554.2729
transforms.py -> 339.8424
patching_transforms.py -> 113.9463
gno_block.py -> 308.8545
adamw.py -> 227.8926
web_utils.py -> 160.9244
train_gino_carcfd.py -> 200.9059
fno_block.py -> 2912.6416
train_navier_stokes.py -> 616.7183
training_state.py -> 222.8972
plot_count_flops.py -> 70.9685
plot_DISCO_convolutions.py -> 219.8973
complex.py -> 78.9634
spherical_swe.py -> 285.8669
segment_csr.py -> 203.9072
plot_UNO_darcy.py -> 216.9041
tune_darcy.py -> 387.8165
skip_connections.py -> 204.9053
equation_losses.py -> 85.96
data_processors.py -> 511.76
navier_stokes.py -> 1390.3466
discrete_continuous_convolution.py -> 1143.4588
positional_encoding.py -> 47.9785
plot_SFNO_swe.py -> 246.89
spectral_convolution.py -> 2399.8792
spherical_convolution.py -> 1352.3682
plot_darcy_flow.py -> 102.9546
fetch_cfd_data.py -> 43.9795
neighbor_search.py -> 200.9067
finite_diff.py -> 123.9416
channel_mlp.py -> 256.8831
output_encoder.py -> 1266.4094
train_fnogno_carcfd.py -> 234.893
plot_darcy_flow_spectrum.py -> 155.929
mesh_datamodule.py -> 1235.416
utils.py -> 540.7509
comm.py -> 310.8531
data_transforms.py -> 967.5465
callbacks.py -> 1737.1913
helpers.py -> 145.9311
incremental.py -> 206.9039
base_model.py -> 278.8723
train_uqno_darcy.py -> 584.7225
train_darcy.py -> 579.7354
zarr_dataset.py -> 391.8168
simple_neighbor_search.py -> 29.9862
dict_dataset.py -> 128.9406
base_transforms.py -> 135.9359
einsum_utils.py -> 128.9404
plot_burgers.py -> 0.0008
normalizers.py -> 248.8822
hdf5_dataset.py -> 109.9495
car_cfd_dataset.py -> 97.9549
conf.py -> 145.9336
legacy_spectral_convolution.py -> 753.6426
uqno.py -> 65.9695
checkpoint_FNO_darcy.py -> 335.8467
plot_incremental_FNO_darcy.py -> 250.8844
data_losses.py -> 1734.181
base_spectral_conv.py -> 30.9865
setup.py -> 78.965
sfno.py -> 14.9938

Top 3 Risky Files:
  - trainer.py -> 2993.6011
  - fno_block.py -> 2912.6416
  - fno.py -> 2873.6638

Comparing Top 3 Risky Files with Ground Truth...

False Positives (Files predicted but not in ground truth):
fno_block.py
fno.py

False Negatives (Files in ground truth but not predicted):
spectral_convolution.py
local_no_block.py

Accuracy: 0.20
  ```

  ### Explanation of outputs:
  - **Modified Files**: Lists all Python files that were modified during the specified period, based on the defect predictor analysis.
  - **Comparison with Ground Truth**: 
    The comparison is based on a ground truth file, which contains a list of files modified between a start and end date. This ground truth data is compared with the predictions made by the sample defect predictor model to assess its accuracy.
    - **False Positives**: Files that were predicted by the model but are not in the ground truth.
    - **False Negatives**: Files that are in the ground truth but were not predicted by the model.
    - **Precision, Recall, and F1 Score**: Metrics that summarize the prediction accuracy of the model.
  - **Risk Scores**: Displays the calculated risk scores for each modified file.
  
  
### 4. Login and run 
Create a docker container and run a bash shell in it. From there, you can modify the file config.json as you wish.
```bash
 docker run -it --rm defect-predictor bash
```

## Overview of files

  ### SampleDefectPredictor.py:
  - This is the core logic for defect prediction. It performs the following:
    - **Repository Analysis**: Uses PyDriller to scan Git commit history for Python files modified in the configured date range.
    - **Fix Detection**: Tags commits as fixing commits using a rule-based keyword search (e.g., "fix", "bug", "issue").
    - **Risk Calculation**: Assigns a risk score to each file based on:
      - Number of distinct contributors who modified it.
      - Frequency of modifications across commits.
      - Whether it was involved in fixing commits.
    - **Output**: Returns a set of predicted risky files along with their associated risk scores.
  ### harness.py
  - This script runs the defect predictor (SampleDefectPredictor.py) logic to generate a list of modified files, calculate their risk scores, and compare the results with a ground truth file. Please note that this file should not be modified, as your implementation is expected to function using it as is.
 ### run_all_configs.py:
  - Automates the execution of the defect predictor using multiple configuration files.
    - Iterates over all .json files in a specified directory.
    - Loads each config file and runs the prediction process.
    - Prints precision, recall, and F1 score for each configuration.
  - Useful for benchmarking the model across various repositories, branches, or time intervals.
  - File is used primarily for running multiple tests simultaneously. Not neccesary for system deployment
  ### requirements.txt
  - Lists all the dependencies and libraries required to run the project seamlessly.
  ### ground_truth.csv
  - Provides a reference dataset containing start and end dates along with the modified files. It is used to compare expected results with actual outputs. You can test various scenarios by customizing this file.
  ### config.json
  - Allows you to specify the repository to be tested, the local path where it should be cloned, the branch to analyze, and the start and end dates for conducting tests within a specified time frame.
  ### Docker 
  - Sets up the necessary environment with Python, Git, dependencies, and your project files to run the defect predictor seamlessly inside a container.
