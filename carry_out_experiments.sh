#! /bin/bash
SEED=1879465786

echo Processing raw data
python -m src.data.poland_dem
python -m src.data.generate

echo Processing finished

echo Subsampling data
python -m src.data.subsample -d data/processed/generated/waves.asc -t data/processed/generated/waves_sub005.asc -r 0.05 -s $SEED
python -m src.data.subsample -d data/processed/generated/waves.asc -t data/processed/generated/waves_sub002.asc -r 0.02 -s $SEED
python -m src.data.subsample -d data/processed/generated/waves.asc -t data/processed/generated/waves_sub001.asc -r 0.01 -s $SEED

python -m src.data.subsample -d data/processed/poland_DEM/area_elevation_1.asc -t data/processed/poland_DEM/area_elevation_1_sub005.asc -r 0.05 -s $SEED
python -m src.data.subsample -d data/processed/poland_DEM/area_elevation_1.asc -t data/processed/poland_DEM/area_elevation_1_sub002.asc -r 0.02 -s $SEED
python -m src.data.subsample -d data/processed/poland_DEM/area_elevation_1.asc -t data/processed/poland_DEM/area_elevation_1_sub001.asc -r 0.01 -s $SEED

echo Subsampling finished

echo Training models
# Linear regression
python -m src.models.linear_regression train -d data/processed/generated/waves_sub005.asc -t models/linear_regression_waves_sub005
python -m src.models.linear_regression train -d data/processed/generated/waves_sub002.asc -t models/linear_regression_waves_sub002
python -m src.models.linear_regression train -d data/processed/generated/waves_sub001.asc -t models/linear_regression_waves_sub001

python -m src.models.linear_regression train -d data/processed/poland_DEM/area_elevation_1_sub005.asc -t models/linear_regression_area_elevation_1_sub005
python -m src.models.linear_regression train -d data/processed/poland_DEM/area_elevation_1_sub002.asc -t models/linear_regression_area_elevation_1_sub002
python -m src.models.linear_regression train -d data/processed/poland_DEM/area_elevation_1_sub001.asc -t models/linear_regression_area_elevation_1_sub001

echo Training finished

echo Predicting missing values
# Linear regression
python -m src.models.linear_regression predict -m models/linear_regression_waves_sub005 -q data/processed/generated/waves_sub005.asc -t data/processed/generated/waves_sub005_predicted_linear.asc
python -m src.models.linear_regression predict -m models/linear_regression_waves_sub002 -q data/processed/generated/waves_sub002.asc -t data/processed/generated/waves_sub002_predicted_linear.asc
python -m src.models.linear_regression predict -m models/linear_regression_waves_sub001 -q data/processed/generated/waves_sub001.asc -t data/processed/generated/waves_sub001_predicted_linear.asc

python -m src.models.linear_regression predict -m models/linear_regression_area_elevation_1_sub005 -q data/processed/poland_DEM/area_elevation_1_sub005.asc -t data/processed/poland_DEM/area_elevation_1_sub005_predicted_linear.asc
python -m src.models.linear_regression predict -m models/linear_regression_area_elevation_1_sub002 -q data/processed/poland_DEM/area_elevation_1_sub002.asc -t data/processed/poland_DEM/area_elevation_1_sub002_predicted_linear.asc
python -m src.models.linear_regression predict -m models/linear_regression_area_elevation_1_sub001 -q data/processed/poland_DEM/area_elevation_1_sub001.asc -t data/processed/poland_DEM/area_elevation_1_sub001_predicted_linear.asc

# IDW
python -m src.models.idw -q data/processed/generated/waves_sub001.asc -p 0.5 -n 3 -t data/processed/generated/waves_sub001_05_3_predicted_idw.asc
python -m src.models.idw -q data/processed/generated/waves_sub001.asc -p 0.5 -n 7 -t data/processed/generated/waves_sub001_05_7_predicted_idw.asc
python -m src.models.idw -q data/processed/generated/waves_sub001.asc -p 0.5 -n 15 -t data/processed/generated/waves_sub001_05_15_predicted_idw.asc

python -m src.models.idw -q data/processed/generated/waves_sub001.asc -p 1 -n 3 -t data/processed/generated/waves_sub001_1_3_predicted_idw.asc
python -m src.models.idw -q data/processed/generated/waves_sub001.asc -p 1 -n 7 -t data/processed/generated/waves_sub001_1_7_predicted_idw.asc
python -m src.models.idw -q data/processed/generated/waves_sub001.asc -p 1 -n 15 -t data/processed/generated/waves_sub001_1_15_predicted_idw.asc

python -m src.models.idw -q data/processed/generated/waves_sub001.asc -p 2 -n 3 -t data/processed/generated/waves_sub001_2_3_predicted_idw.asc
python -m src.models.idw -q data/processed/generated/waves_sub001.asc -p 2 -n 7 -t data/processed/generated/waves_sub001_2_7_predicted_idw.asc
python -m src.models.idw -q data/processed/generated/waves_sub001.asc -p 2 -n 15 -t data/processed/generated/waves_sub001_2_15_predicted_idw.asc

python -m src.models.idw -q data/processed/poland_DEM/area_elevation_1_sub001.asc -p 0.5 -n 3 -t data/processed/poland_DEM/area_elevation_1_sub001_05_3_predicted_idw.asc
python -m src.models.idw -q data/processed/poland_DEM/area_elevation_1_sub001.asc -p 0.5 -n 7 -t data/processed/poland_DEM/area_elevation_1_sub001_05_7_predicted_idw.asc
python -m src.models.idw -q data/processed/poland_DEM/area_elevation_1_sub001.asc -p 0.5 -n 15 -t data/processed/poland_DEM/area_elevation_1_sub001_05_15_predicted_idw.asc

python -m src.models.idw -q data/processed/poland_DEM/area_elevation_1_sub001.asc -p 1 -n 3 -t data/processed/poland_DEM/area_elevation_1_sub001_1_3_predicted_idw.asc
python -m src.models.idw -q data/processed/poland_DEM/area_elevation_1_sub001.asc -p 1 -n 7 -t data/processed/poland_DEM/area_elevation_1_sub001_1_7_predicted_idw.asc
python -m src.models.idw -q data/processed/poland_DEM/area_elevation_1_sub001.asc -p 1 -n 15 -t data/processed/poland_DEM/area_elevation_1_sub001_1_15_predicted_idw.asc

python -m src.models.idw -q data/processed/poland_DEM/area_elevation_1_sub001.asc -p 2 -n 3 -t data/processed/poland_DEM/area_elevation_1_sub001_2_3_predicted_idw.asc
python -m src.models.idw -q data/processed/poland_DEM/area_elevation_1_sub001.asc -p 2 -n 7 -t data/processed/poland_DEM/area_elevation_1_sub001_2_7_predicted_idw.asc
python -m src.models.idw -q data/processed/poland_DEM/area_elevation_1_sub001.asc -p 2 -n 15 -t data/processed/poland_DEM/area_elevation_1_sub001_2_15_predicted_idw.asc

echo Predicting finished

echo Generating visualizations
# Linear regression
python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub005.asc -p data/processed/generated/waves_sub005_predicted_linear.asc -t reports/figures/waves_sub005_linear_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub002.asc -p data/processed/generated/waves_sub002_predicted_linear.asc -t reports/figures/waves_sub002_linear_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub001.asc -p data/processed/generated/waves_sub001_predicted_linear.asc -t reports/figures/waves_sub001_linear_predictions_visualization

python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub005.asc -p data/processed/poland_DEM/area_elevation_1_sub005_predicted_linear.asc -t reports/figures/area_elevation_1_sub005_linear_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub002.asc -p data/processed/poland_DEM/area_elevation_1_sub002_predicted_linear.asc -t reports/figures/area_elevation_1_sub002_linear_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub001.asc -p data/processed/poland_DEM/area_elevation_1_sub001_predicted_linear.asc -t reports/figures/area_elevation_1_sub001_linear_predictions_visualization

# IDW
python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub001.asc -p data/processed/generated/waves_sub001_05_3_predicted_idw.asc -t reports/figures/waves_sub001_05_3_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub001.asc -p data/processed/generated/waves_sub001_05_7_predicted_idw.asc -t reports/figures/waves_sub001_05_7_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub001.asc -p data/processed/generated/waves_sub001_05_15_predicted_idw.asc -t reports/figures/waves_sub001_05_15_idw_predictions_visualization

python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub001.asc -p data/processed/generated/waves_sub001_1_3_predicted_idw.asc -t reports/figures/waves_sub001_1_3_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub001.asc -p data/processed/generated/waves_sub001_1_7_predicted_idw.asc -t reports/figures/waves_sub001_1_7_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub001.asc -p data/processed/generated/waves_sub001_1_15_predicted_idw.asc -t reports/figures/waves_sub001_1_15_idw_predictions_visualization

python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub001.asc -p data/processed/generated/waves_sub001_2_3_predicted_idw.asc -t reports/figures/waves_sub001_2_3_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub001.asc -p data/processed/generated/waves_sub001_2_7_predicted_idw.asc -t reports/figures/waves_sub001_2_7_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/generated/waves.asc -s data/processed/generated/waves_sub001.asc -p data/processed/generated/waves_sub001_2_15_predicted_idw.asc -t reports/figures/waves_sub001_2_15_idw_predictions_visualization

python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub001.asc -p data/processed/poland_DEM/area_elevation_1_sub001_05_3_predicted_idw.asc -t reports/figures/area_elevation_1_levation_1_sub001_05_3_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub001.asc -p data/processed/poland_DEM/area_elevation_1_sub001_05_7_predicted_idw.asc -t reports/figures/area_elevation_1_levation_1_sub001_05_7_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub001.asc -p data/processed/poland_DEM/area_elevation_1_sub001_05_15_predicted_idw.asc -t reports/figures/area_elevation_1_levation_1_sub001_05_15_idw_predictions_visualization

python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub001.asc -p data/processed/poland_DEM/area_elevation_1_sub001_1_3_predicted_idw.asc -t reports/figures/area_elevation_1_levation_1_sub001_1_3_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub001.asc -p data/processed/poland_DEM/area_elevation_1_sub001_1_7_predicted_idw.asc -t reports/figures/area_elevation_1_levation_1_sub001_1_7_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub001.asc -p data/processed/poland_DEM/area_elevation_1_sub001_1_15_predicted_idw.asc -t reports/figures/area_elevation_1_levation_1_sub001_1_15_idw_predictions_visualization

python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub001.asc -p data/processed/poland_DEM/area_elevation_1_sub001_2_3_predicted_idw.asc -t reports/figures/area_elevation_1_levation_1_sub001_2_3_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub001.asc -p data/processed/poland_DEM/area_elevation_1_sub001_2_7_predicted_idw.asc -t reports/figures/area_elevation_1_levation_1_sub001_2_7_idw_predictions_visualization
python -m src.visualization.heatmaps_comparison -r data/processed/poland_DEM/area_elevation_1.asc -s data/processed/poland_DEM/area_elevation_1_sub001.asc -p data/processed/poland_DEM/area_elevation_1_sub001_2_15_predicted_idw.asc -t reports/figures/area_elevation_1_levation_1_sub001_2_15_idw_predictions_visualization
echo Generating visualizations finished