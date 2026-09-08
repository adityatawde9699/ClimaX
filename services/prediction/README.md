# Prediction Domain Service (`services/prediction`)

Responsible for Vertex AI forecasting pipelines and atmospheric plume dispersion modeling.

## Responsibilities:
- **Spatio-Temporal Sequence Forecasting**: 6-hour, 24-hour, and 72-hour rolling forecasts for PM2.5, PM10, and AQI across spatial grids.
- **Plume Transport Modeling**: Simulates Gaussian plume dispersion driven by real-time meteorological conditions (wind speed, atmospheric boundary layer height, temperature inversion).
- **Model Evaluation & Drift Monitoring**: Continuously compares historical predictions against realized sensor ground truth to track RMSE, MAE, and model drift.

## Planned Implementation Phase:
- Phase 6 (Pollution Prediction).
