# Solar Wind Multimodal AI Agent (Azure)

Predict near-term solar wind speed (km/s) using EUV images (SDO/AIA via Helioviewer API) and OMNI solar-wind time series.
This repo includes:
- **Azure ML** training and real-time inference (PyTorch).
- **Azure Functions** tool endpoints used by the "agent" to fetch EUV/OMNI data and call the AML endpoint.
- End-to-end scripts to deploy the model to an **Azure ML Managed Online Endpoint**.

> Notes
> - This project provides deployable scaffolding. You must set environment variables and provision Azure resources (AML, Storage, Key Vault, Functions) in your subscription.
> - Helioviewer API and OMNI data are public services. Respect rate limits and usage policies.

## Quick Start

1. Create an AML workspace and GPU compute (e.g., `Standard_NC6s_v3`).
2. Upload this project to a dev machine or Azure Cloud Shell.
3. Create the AML environment and run training:
   ```bash
   az extension add -n ml -y
   az ml job create -f azureml/job-train.yaml -g <rg> -w <workspace>
   ```
4. Register and deploy the trained model as an online endpoint:
   ```bash
   az ml job create -f azureml/job-register-deploy.yaml -g <rg> -w <workspace>
   ```
5. Deploy Azure Functions (HTTP triggers) from `functions/` to use as tools for your agent or external automations.

## Project Structure

- `src/` : Data ingestion, dataset, model, training, and serving code.
- `azureml/` : AML job specs for training and deployment.
- `functions/` : Azure Functions for `fetch_euv`, `fetch_omni`, `predict_now`, `notify_teams`.
- `scripts/` : Convenience deployment scripts.

## Inputs & Outputs

- **Inputs**: A sequence of EUV frames (AIA 193Å JP2 images) and an OMNI timeseries window of plasma/magnetic parameters.
- **Output**: Predicted solar wind speed (km/s) for the next hour (extendable to multi-horizon).

## Citations

- OMNIWeb (NASA/GSFC), Helioviewer API, SDO/AIA.
- Multimodal approach adapted from peer-reviewed work on combining EUV imagery with solar wind time series.
