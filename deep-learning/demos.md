# SageMaker Demo

## Create Notebook

- Select SageMaker from the console home page.
- Click *Create notebook instance*.
- *Notebook instance name*: `demo1`
- *Notebook instance type*: `ml.t2.medium` (smallest)
- *IAM role*: `AmazonSageMaker-Execution-Role-ID` (generated for you)
- Click *Create notebook instance*.
- Will take about 5 minutes to be online.

## Login Without Username Password

Get presigned URL.

```bash
aws sagemaker create-presigned-notebook-instance-url \
  --notebook-instance-name demo1 \
  --query AuthorizedUrl \
  --output text
```

Paste this into a browser.

## Explore Jupyter

- Click on *Open* to open a Jupyter notebook.
- Test out the Jupyter interface.

# SageMaker Gas Price Prediction

## Find Gas Forecasting Notebook

- Go to SageMaker's Jupyter notebook on `demo1`.
- Click on *sample-notebooks*.
- Find this notebook.
    - `sample-notebooks/introduction_to_applying_machine_learning/linear_time_series_forecast`

## Time Series Analysis

- This notebook explores predicting gas prices.
- It builds a model by using recent prices as features. 
- The label or target is price one day after the prices used as features. 
- You can use this approach on any time series data.

# MXNet Computations

Open `mxnet-computations.ipynb`

# San Ramon Prediction Using Linear Model

Open `san-ramon-linear-model.ipynb`

# San Ramon Prediction Using MXNet

Open `san-ramon-mxnet.ipynb`
