# src/evaluator.py
# Description: Evaluates synthetic data using custom metrics (Wasserstein, KL)
# and generates Plotly figures for visualization (Adapted for Streamlit).

import pandas as pd
import numpy as np
from scipy.stats import wasserstein_distance, entropy
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging


logger = logging.getLogger(__name__)



class EvaluateSynthetic:

    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame, metadata_path: str | None = None):
        """
        Initializes the evaluator with real and synthetic data.

        Parameters:
            real_data (pd.DataFrame): The original dataset (potentially preprocessed/hashed).
            synthetic_data (pd.DataFrame): The generated synthetic dataset.
            metadata_path (str, optional): Path to metadata JSON (needed for SDV evals). Not used for custom metrics/plots here.
        """
        logger.info("Initializing EvaluateSynthetic instance.")
        logger.debug(f"Real data shape: {real_data.shape}, Synthetic data shape: {synthetic_data.shape}, Metadata path: {metadata_path}")

        if real_data is None or real_data.empty or synthetic_data is None or synthetic_data.empty:
             raise ValueError("Real and synthetic data must be valid DataFrames.")

        # Ensure consistent column types where possible, especially for comparison
        self.real_data = real_data.copy()
        self.synthetic_data = synthetic_data.copy()
        potential_numeric_cols = self.real_data.select_dtypes(include=np.number).columns.tolist()
        common_numeric_cols = list(set(potential_numeric_cols) & set(self.synthetic_data.columns))

        for col in common_numeric_cols:
            try:
                # Attempt conversion to numeric, coercing errors to NaN
                self.real_data[col] = pd.to_numeric(self.real_data[col], errors='coerce')
                self.synthetic_data[col] = pd.to_numeric(self.synthetic_data[col], errors='coerce')
            except Exception as e:
                logger.warning(
                    f"Could not coerce column '{col}' to numeric during init. Error: {e}. It might be excluded from numeric analysis.")


        for col in self.real_data.columns:
             if col in self.synthetic_data.columns:
                 # Attempt to align types, favoring object if conversion fails
                 try:
                     # Convert synth data to real data's type if possible
                     # Handle cases where synth might be float and real int, etc.
                     target_dtype = self.real_data[col].dtype
                     self.synthetic_data[col] = self.synthetic_data[col].astype(target_dtype)
                 except Exception as e:
                     # If direct conversion fails (e.g., hashed string to int/float),
                     # check if real data was NOT object initially. If so, warn and convert both to string.
                     if not pd.api.types.is_object_dtype(self.real_data[col].dtype):
                         logging.warning(f"Could not align dtype for column '{col}' to {self.real_data[col].dtype} (Error: {e}). Treating as string/category for evaluation.")
                         try:
                            # Convert both to string for consistent categorical comparison
                            self.real_data[col] = self.real_data[col].astype(str)
                            self.synthetic_data[col] = self.synthetic_data[col].astype(str)
                         except Exception as e_str:
                             logging.error(f"Failed converting column '{col}' to string during fallback: {e_str}")

        # Identify column types AFTER potential type alignment to object
        self.common_columns = list(set(self.real_data.columns) & set(self.synthetic_data.columns))
        if not self.common_columns:
             raise ValueError("No common columns found between real and synthetic data for evaluation.")

        # Use the potentially modified dtypes for classification
        self.numeric_columns = self.real_data[self.common_columns].select_dtypes(include=np.number).columns.tolist()
        self.categorical_columns = self.real_data[self.common_columns].select_dtypes(include=['object', 'category', 'string']).columns.tolist() # Include string
        self.scaler = MinMaxScaler()
        logging.info(f"Evaluator initialized. Common columns: {len(self.common_columns)}, Numeric: {len(self.numeric_columns)}, Categorical: {len(self.categorical_columns)}")



    # --- Custom Metrics (Wasserstein, KL) ---

    def _calculate_wasserstein_distance(self, column: str) -> float | None:
        """Calculates Wasserstein distance for a single common column."""
        if column not in self.common_columns: return None
        try:
            real_vals_col = self.real_data[column].dropna()
            synth_vals_col = self.synthetic_data[column].dropna()

            if real_vals_col.empty or synth_vals_col.empty:
                logging.warning(f"Skipping Wasserstein for '{column}': one or both columns have no non-NA data.")
                return None

            # Check if column is numeric based on initial classification
            is_numeric = column in self.numeric_columns

            if is_numeric:
                try:
                    # Attempt numeric conversion and calculation
                    real_numeric = pd.to_numeric(real_vals_col)
                    synth_numeric = pd.to_numeric(synth_vals_col)

                    # Reshape for scaler
                    real_vals = real_numeric.values.reshape(-1, 1)
                    synth_vals = synth_numeric.values.reshape(-1, 1)

                    # Fit scaler only on real data, transform both
                    real_norm = self.scaler.fit_transform(real_vals).ravel()
                    # Handle case where synth data might be outside the range of real data
                    synth_norm = np.clip(self.scaler.transform(synth_vals).ravel(), 0, 1)

                    return wasserstein_distance(real_norm, synth_norm)

                except (ValueError, TypeError) as num_err:
                    # FALLBACK: If numeric fails due to hashing, treat as categorical
                    logging.warning(f"Numeric Wasserstein failed for '{column}' (Error: {num_err}). Falling back to categorical calculation.")
                    is_numeric = False # Force categorical path

            # Categorical Calculation
            if not is_numeric:
                # Ensure values are strings for consistent categorical handling
                real_vals_col = real_vals_col.astype(str)
                synth_vals_col = synth_vals_col.astype(str)

                real_freq = real_vals_col.value_counts(normalize=True)
                synth_freq = synth_vals_col.value_counts(normalize=True)
                # Combine categories from both, ensuring alignment
                all_cats = sorted(list(set(real_freq.index) | set(synth_freq.index)))

                real_aligned = pd.Series([real_freq.get(cat, 0) for cat in all_cats], index=all_cats)
                synth_aligned = pd.Series([synth_freq.get(cat, 0) for cat in all_cats], index=all_cats)


                # Add small epsilon for safety if sum is slightly off due to floating point
                epsilon = 1e-9
                if not np.isclose(real_aligned.sum(), 1): real_aligned = (real_aligned + epsilon) / (real_aligned.sum() + epsilon * len(real_aligned))
                if not np.isclose(synth_aligned.sum(), 1): synth_aligned = (synth_aligned + epsilon) / (synth_aligned.sum() + epsilon * len(synth_aligned))

                # Ensure no zeros before distance calculation if needed by specific implementations
                return wasserstein_distance(real_aligned.values, synth_aligned.values)
            else:
                 # This case should ideally not be reached due to the logic above
                 logging.warning(f"Column '{column}' type unrecognized for Wasserstein distance after checks.")
                 return None

        except Exception as e:
            logging.error(f"Error calculating Wasserstein for column '{column}': {e}", exc_info=True)
            return None

    def _calculate_kl_divergence(self, column: str) -> float | None:
        """Calculates KL divergence (KL(Real || Synthetic)) for a single common column."""
        if column not in self.common_columns: return None
        epsilon = 1e-10 # Small constant to avoid log(0) or division by zero
        try:
            real_vals_col = self.real_data[column].dropna()
            synth_vals_col = self.synthetic_data[column].dropna()

            if real_vals_col.empty or synth_vals_col.empty:
                 logging.warning(f"Skipping KL Divergence for '{column}': one or both columns have no non-NA data.")
                 return None

            # Check if column is numeric based on initial classification
            is_numeric = column in self.numeric_columns

            # Add explicit check if data *can* be treated as numeric
            if is_numeric:
                try:
                    # Attempt numeric conversion and calculation
                    real_numeric = pd.to_numeric(real_vals_col)
                    synth_numeric = pd.to_numeric(synth_vals_col)

                    # Determine shared bins based on combined range
                    # Use try-except for min/max in case of unexpected types remaining
                    try:
                        min_val = min(real_numeric.min(), synth_numeric.min())
                        max_val = max(real_numeric.max(), synth_numeric.max())
                    except TypeError as type_err:
                         logging.warning(f"Could not determine min/max numerically for KL on '{column}' (Error: {type_err}). Falling back.")
                         raise ValueError("Cannot treat as numeric") # Trigger fallback

                    if min_val == max_val: # Handle case where all values are the same
                        bins = np.array([min_val - epsilon, min_val + epsilon])
                    else:
                        # Calculate reasonable number of bins, avoid too many if few unique values
                        num_unique_real = real_numeric.nunique()
                        num_bins = min(50, num_unique_real + 1) if num_unique_real > 1 else 2
                        bins = np.linspace(min_val, max_val, num=num_bins)

                    real_hist, _ = np.histogram(real_numeric, bins=bins, density=True)
                    synth_hist, _ = np.histogram(synth_numeric, bins=bins, density=True)

                    # Add epsilon and re-normalize to ensure valid probability distributions
                    P = real_hist + epsilon
                    Q = synth_hist + epsilon
                    P /= P.sum()
                    Q /= Q.sum()

                    return entropy(P, Q) # Calculates KL(P || Q)
                except (ValueError, TypeError) as num_err:
                     # FALLBACK: If numeric fails due to hashing, treat as categorical
                    logging.warning(f"Numeric KL failed for '{column}' (Error: {num_err}). Falling back to categorical calculation.")
                    is_numeric = False # Force categorical path


            # Categorical Calculation
            if not is_numeric:
                # Ensure values are strings for consistent categorical handling
                real_vals_col = real_vals_col.astype(str)
                synth_vals_col = synth_vals_col.astype(str)

                real_freq = real_vals_col.value_counts(normalize=True)
                synth_freq = synth_vals_col.value_counts(normalize=True)
                all_cats = sorted(list(set(real_freq.index) | set(synth_freq.index)))

                # Align frequencies, add epsilon, and re-normalize
                P = pd.Series([real_freq.get(cat, 0) + epsilon for cat in all_cats], index=all_cats)
                Q = pd.Series([synth_freq.get(cat, 0) + epsilon for cat in all_cats], index=all_cats)
                P /= P.sum()
                Q /= Q.sum()

                return entropy(P.values, Q.values) # KL(P || Q)
            else:
                # This case should ideally not be reached
                logging.warning(f"Column '{column}' type not recognized for KL divergence after checks.")
                return None
        except Exception as e:
            logging.error(f"Error calculating KL divergence for column '{column}': {e}", exc_info=True)
            return None

    def evaluate_all_columns_custom(self) -> dict:
        """Calculates Wasserstein and KL divergence for all common columns."""
        results = {}
        logging.info(f"Calculating custom metrics for {len(self.common_columns)} common columns.")
        for column in self.common_columns:
            # Calculate metrics using the potentially fixed methods
            wasserstein = self._calculate_wasserstein_distance(column)
            kl_div = self._calculate_kl_divergence(column)

            # Store metrics even if None, so UI knows calculation was attempted
            results[column] = {
                 'wasserstein': wasserstein,
                 'kl_divergence': kl_div
            }
        logging.info("Finished calculating custom metrics.")
        return results

    def get_custom_metrics_summary(self, column_metrics: dict | None = None) -> dict:
        """Provides summary statistics for the custom evaluation metrics."""
        if column_metrics is None:
             # Calculate if not provided
             column_metrics = self.evaluate_all_columns_custom()

        if not column_metrics:
            return {'wasserstein': {}, 'kl_divergence': {}} # Return empty structure

        # Extract valid, non-infinite numeric values for summary stats
        wasserstein_vals = [m['wasserstein'] for m in column_metrics.values() if m.get('wasserstein') is not None and np.isfinite(m['wasserstein'])]
        kl_vals = [m['kl_divergence'] for m in column_metrics.values() if m.get('kl_divergence') is not None and np.isfinite(m['kl_divergence'])]

        # Define function to calculate stats safely
        def calculate_stats(values):
            if not values: return {'mean': None, 'median': None, 'min': None, 'max': None, 'std': None, 'count': 0}
            return {
                'mean': float(np.mean(values)),
                'median': float(np.median(values)),
                'min': float(np.min(values)),
                'max': float(np.max(values)),
                'std': float(np.std(values)),
                'count': len(values)
            }

        summary = {
            'wasserstein': calculate_stats(wasserstein_vals),
            'kl_divergence': calculate_stats(kl_vals)
        }
        logging.info(f"Generated metrics summary. Wasserstein count: {summary['wasserstein']['count']}, KL count: {summary['kl_divergence']['count']}")
        return summary


    # --- Plotting Function  ---
    def create_distribution_plot(self, column_name: str, max_cats_to_show: int = 50) -> go.Figure | None:
        """
        Generates ONE interactive Plotly plot (histogram or bar chart)
        to compare real and synthetic data distributions for a specific column.
        Handles potential type mismatches (e.g., due to hashing).
        """

        logger.info(f"Creating distribution plot for column: '{column_name}'")

        if column_name not in self.common_columns:
             logging.warning(f"Cannot plot '{column_name}': not found in common columns.")
             return None

        fig = go.Figure()
        try:
            real_data_col = self.real_data[column_name].dropna()
            synth_data_col = self.synthetic_data[column_name].dropna()

            if real_data_col.empty and synth_data_col.empty:
                logging.warning(f"Skipping plot for '{column_name}': No non-NA data in either real or synthetic.")
                fig.add_annotation(text=f"No data available for {column_name}", showarrow=False)
                fig.update_layout(title=f'Distribution Comparison: {column_name} (No Data)', xaxis={'visible': False}, yaxis={'visible': False})
                return fig # Return the empty figure with annotation

            # Determine plot type based on attempting numeric conversion AND original type
            plot_as_numeric = False
            if column_name in self.numeric_columns: # Check original classification first
                try:
                    # Try converting both to numeric. If it works, plot as histogram.
                    pd.to_numeric(real_data_col)
                    pd.to_numeric(synth_data_col)
                    plot_as_numeric = True
                except (ValueError, TypeError):
                    # If conversion fails for originally numeric column, treat as categorical for plot
                    logging.warning(f"Numeric plot failed for '{column_name}'. Falling back to categorical plot.")
                    plot_as_numeric = False

            # Numerical Data Plotting (Histogram)
            if plot_as_numeric:
                 # Convert again just to be safe, using the numeric versions
                real_numeric = pd.to_numeric(real_data_col)
                synth_numeric = pd.to_numeric(synth_data_col)
                fig.add_trace(go.Histogram(
                    x=real_numeric, name="Original Data", opacity=0.7, nbinsx=30, marker_color='#1f77b4'
                ))
                fig.add_trace(go.Histogram(
                    x=synth_numeric, name="Generated Data", opacity=0.7, nbinsx=30, marker_color='#ff7f0e'
                ))
                fig.update_layout(barmode='overlay', title=f'Numeric Distribution: {column_name}',
                                  xaxis_title=column_name, yaxis_title='Frequency')

            # Categorical/Object Data Plotting (Bar Chart)
            else:
                 # Ensure strings for categorical plotting
                real_data_cat = real_data_col.astype(str)
                synth_data_cat = synth_data_col.astype(str)

                real_counts = real_data_cat.value_counts(normalize=True)
                synth_counts = synth_data_cat.value_counts(normalize=True)

                # Combine categories and fill missing ones with 0
                comparison_df = pd.DataFrame({'Original': real_counts, 'Generated': synth_counts}).fillna(0)

                # Limit categories shown if needed
                if len(comparison_df) > max_cats_to_show:
                     logging.info(f"'{column_name}' has >{max_cats_to_show} categories. Showing top {max_cats_to_show} by original frequency.")
                     # Get top categories based on original data frequency
                     top_cats_index = real_counts.nlargest(max_cats_to_show).index
                     # Filter the comparison dataframe using these indices
                     comparison_df = comparison_df.loc[comparison_df.index.isin(top_cats_index.astype(str))]


                # Sort by index (category name) for consistent plotting order
                comparison_df = comparison_df.sort_index()

                fig.add_trace(go.Bar(
                    x=comparison_df.index, y=comparison_df['Original'], name="Original Data", marker_color='#1f77b4' # Blue
                ))
                fig.add_trace(go.Bar(
                    x=comparison_df.index, y=comparison_df['Generated'], name="Generated Data", marker_color='#ff7f0e' # Orange
                ))
                fig.update_layout(barmode='group', title=f'Categorical Distribution: {column_name}',
                                xaxis_title=column_name, yaxis_title='Proportion', xaxis={'type': 'category'})

            # Apply common layout updates
            fig.update_layout(
                hovermode='x unified',
                legend_title_text='Dataset',
            )
            return fig



        except Exception as plot_err:
             logging.error(f"Could not generate plot for '{column_name}': {plot_err}", exc_info=True)
             fig = go.Figure()
             fig.add_annotation(text=f"Error plotting {column_name}:\n{plot_err}", showarrow=False)
             fig.update_layout(title=f'Plotting Error: {column_name}', xaxis={'visible': False}, yaxis={'visible': False})
             return fig

    def create_correlation_heatmap(self, method: str = 'pearson', min_numeric_cols: int = 2) -> go.Figure | None:
        """
        Generates interactive Plotly heatmaps comparing the correlation matrices
        of numeric columns in the real and synthetic datasets.

        Args:
            method (str): Method of correlation ('pearson', 'kendall', 'spearman').
            min_numeric_cols (int): Minimum number of numeric columns required to generate heatmaps.

        Returns:
            go.Figure | None: A Plotly figure containing the heatmaps, or None if not enough numeric columns.
        """
        logger.info(f"Creating correlation heatmaps using method: '{method}'")

        if len(self.numeric_columns) < min_numeric_cols:
            logger.warning(
                f"Skipping correlation heatmap: Need at least {min_numeric_cols} numeric columns, found {len(self.numeric_columns)}.")
            return None

        try:
            # Select only common numeric columns guaranteed to exist in both datasets
            real_numeric_df = self.real_data[self.numeric_columns].copy()
            synth_numeric_df = self.synthetic_data[self.numeric_columns].copy()

            # Drop columns that are entirely NaN after potential coercion in __init__
            real_numeric_df.dropna(axis=1, how='all', inplace=True)
            synth_numeric_df.dropna(axis=1, how='all', inplace=True)

            # Recalculate common numeric columns after dropping all-NaN ones
            valid_numeric_cols = list(set(real_numeric_df.columns) & set(synth_numeric_df.columns))
            if len(valid_numeric_cols) < min_numeric_cols:
                logger.warning(
                    f"Skipping correlation heatmap: After dropping all-NaN columns, need at least {min_numeric_cols} numeric columns, found {len(valid_numeric_cols)}.")
                return None

            real_corr = real_numeric_df[valid_numeric_cols].corr(method=method)
            synth_corr = synth_numeric_df[valid_numeric_cols].corr(method=method)

            # Create Plotly figure with subplots
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=(
                    f"Original Data Correlation ({method.capitalize()})",
                    f"Synthetic Data Correlation ({method.capitalize()})"
                ),
                horizontal_spacing=0.1  # Adjust spacing
            )

            # Create Plotly heatmap traces
            heatmap_real = go.Heatmap(
                z=real_corr.values,
                x=real_corr.columns,
                y=real_corr.columns,
                colorscale='RdBu',  # Red-Blue diverging scale
                zmid=0,  # Center color scale at 0
                zmin=-1, zmax=1,  # Set scale range from -1 to 1
                colorbar_x=0.45  # Position colorbar for first plot
            )
            heatmap_synth = go.Heatmap(
                z=synth_corr.values,
                x=synth_corr.columns,
                y=synth_corr.columns,
                colorscale='RdBu',
                zmid=0,
                zmin=-1, zmax=1,
                colorbar_x=1.0  # Position colorbar for second plot
            )

            fig.add_trace(heatmap_real, row=1, col=1)
            fig.add_trace(heatmap_synth, row=1, col=2)

            fig.update_layout(
                title_text=f"Comparison of Numeric Column Correlations ({method.capitalize()})",
                title_x=0.5,  # Center title
                xaxis_tickangle=-45,
                xaxis2_tickangle=-45
            )
            logger.info("Successfully generated correlation heatmaps.")
            return fig

        except Exception as plot_err:
            logger.error(f"Could not generate correlation heatmap: {plot_err}", exc_info=True)

            # Optionally return a figure with an error message
            fig = go.Figure()
            fig.add_annotation(text=f"Error generating correlation heatmap:\n{plot_err}", showarrow=False)
            fig.update_layout(
                title='Correlation Heatmap Error',
                xaxis={'visible': False},
                yaxis={'visible': False}
            )
            return fig  # Return figure with error message

