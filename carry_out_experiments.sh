#! /bin/bash

echo echo Processing raw data
python -m src.data.poland_dem
python -m src.data.generate
echo echo Processing finished
echo ''


echo Subsampling data
DATA_FILES=("data/processed/generated/waves" "data/processed/poland_DEM/area_elevation_1")
EXT=.asc
SUBSAMPLE_SUFFIX=_sub
SUBSAMPLING_RATIOS=("0.01" "0.005" "0.001")
SEED=1879465786

max_count=$((${#DATA_FILES[@]}*${#SUBSAMPLING_RATIOS[@]}))
counter=0

for file in "${DATA_FILES[@]}"; do
    for ratio in "${SUBSAMPLING_RATIOS[@]}"; do
        python -m src.data.subsample -d $file$EXT -t $file$SUBSAMPLE_SUFFIX${ratio//.}$EXT -r $ratio -s $SEED
        ((counter++))
        echo Data subsamplings: ${counter} out of ${max_count}
    done
done
echo Subsampling finished
echo ''

echo Training models
# Linear regression
LINEAR_MODEL_PREFIX=models/linear_regression_

max_count=$((${#DATA_FILES[@]}*${#SUBSAMPLING_RATIOS[@]}))
counter=0

for file in "${DATA_FILES[@]}"; do
    for ratio in "${SUBSAMPLING_RATIOS[@]}"; do
        python -m src.models.linear_regression train -d $file$SUBSAMPLE_SUFFIX${ratio//.}$EXT -t $LINEAR_MODEL_PREFIX${file##*/}$SUBSAMPLE_SUFFIX${ratio//.}
        ((counter++))
        echo Trained linear regression models: ${counter} out of ${max_count}
    done
done

# Kriging
KRIGING_MODEL_PREFIX=models/kriging_

max_count=${#DATA_FILES[@]}
counter=0

for file in "${DATA_FILES[@]}"; do
    python -m src.models.kriging train -d $file$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}$EXT -t $KRIGING_MODEL_PREFIX${file##*/}$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}
    ((counter++))
    echo Trained kriging models: ${counter} out of ${max_count}
done
echo Training finished
echo ''

echo Predicting missing values
# Linear regression
LINEAR_PREDICTIONS_SUFFIX=_predicted_linear

max_count=$((${#DATA_FILES[@]}*${#SUBSAMPLING_RATIOS[@]}))
counter=0

for file in "${DATA_FILES[@]}"; do
    for ratio in "${SUBSAMPLING_RATIOS[@]}"; do
        python -m src.models.linear_regression predict -m $LINEAR_MODEL_PREFIX${file##*/}$SUBSAMPLE_SUFFIX${ratio//.} -q $file$SUBSAMPLE_SUFFIX${ratio//.}$EXT -t $file$SUBSAMPLE_SUFFIX${ratio//.}$LINEAR_PREDICTIONS_SUFFIX$EXT
        ((counter++))
        echo Linear regression predictions made: ${counter} out of ${max_count}
    done
done

# IDW
IDW_PREDICTIONS_SUFFIX=_predicted_idw
IDW_POWERS=("0.5" "1" "2")
IDW_N_NEIGHBORS=("3" "7" "15")

max_count=$((${#DATA_FILES[@]}*${#IDW_POWERS[@]}*${#IDW_N_NEIGHBORS[@]}))
counter=0

for file in "${DATA_FILES[@]}"; do
    for power in "${IDW_POWERS[@]}"; do
        for neighbors in "${IDW_N_NEIGHBORS[@]}"; do
            python -m src.models.idw -q $file$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}$EXT -p $power -n $neighbors -t $file$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}_${power//.}_$neighbors$IDW_PREDICTIONS_SUFFIX$EXT
            ((counter++))
            echo IDW predictions made: ${counter} out of ${max_count}
        done
    done
done

# Kriging
KRIGING_PREDICTIONS_SUFFIX=_predicted_kriging

max_count=${#DATA_FILES[@]}
counter=0

for file in "${DATA_FILES[@]}"; do
    python -m src.models.kriging predict -m $KRIGING_MODEL_PREFIX${file##*/}$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.} -q $file$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}$EXT -t $file$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}$KRIGING_PREDICTIONS_SUFFIX$EXT
    ((counter++))
    echo Kriging predictions made: ${counter} out of ${max_count}
done
echo Predicting finished
echo ''


echo Generating visualizations
# Linear regression
FIGURE_PREFIX=reports/figures/
LINEAR_FIGURE_SUFFIX=_linear_predictions_visualization

max_count=$((${#DATA_FILES[@]}*${#SUBSAMPLING_RATIOS[@]}))
counter=0

for file in "${DATA_FILES[@]}"; do
    for ratio in "${SUBSAMPLING_RATIOS[@]}"; do
        python -m src.visualization.heatmaps_comparison -r $file$EXT -s $file$SUBSAMPLE_SUFFIX${ratio//.}$EXT -p $file$SUBSAMPLE_SUFFIX${ratio//.}$LINEAR_PREDICTIONS_SUFFIX$EXT -t $FIGURE_PREFIX${file##*/}$SUBSAMPLE_SUFFIX${ratio//.}$LINEAR_FIGURE_SUFFIX
        ((counter++))
        echo Linear regressions visualizations made: ${counter} out of ${max_count}
    done
done

# IDW
IDW_FIGURE_SUFFIX=_idw_predictions_visualization

max_count=$((${#DATA_FILES[@]}*${#IDW_POWERS[@]}*${#IDW_N_NEIGHBORS[@]}))
counter=0

for file in "${DATA_FILES[@]}"; do
    for power in "${IDW_POWERS[@]}"; do
        for neighbors in "${IDW_N_NEIGHBORS[@]}"; do
            python -m src.visualization.heatmaps_comparison -r $file$EXT -s $file$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}$EXT -p $file$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}_${power//.}_$neighbors$IDW_PREDICTIONS_SUFFIX$EXT -t $FIGURE_PREFIX${file##*/}$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}_${power//.}_$neighbors$IDW_FIGURE_SUFFIX
            ((counter++))
            echo IDW visualizations made: ${counter} out of ${max_count}
        done
    done
done

# Kriging
KRIGING_FIGURE_SUFFIX=_kriging_predictions_visualization

max_count=${#DATA_FILES[@]}
counter=0

for file in "${DATA_FILES[@]}"; do
    python -m src.visualization.heatmaps_comparison -r $file$EXT -s $file$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}$EXT -p $file$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}$KRIGING_PREDICTIONS_SUFFIX$EXT -t $FIGURE_PREFIX${file##*/}$SUBSAMPLE_SUFFIX${SUBSAMPLING_RATIOS[2]//.}$KRIGING_FIGURE_SUFFIX
    ((counter++))
    echo Kriging visualizations made: ${counter} out of ${max_count}
done
echo Generating visualizations finished
echo ''