"""
CTGAN Model Training and Serialization.

This module provides a class to train, save, and load a CTGAN model using SDV's CTGANSynthesizer.
It includes automatic metadata detection and column consistency checks.
"""

import pickle
import os
import pandas as pd
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer
from itertools import product
import numpy as np
from evaluator import Evaluator


class CTGANModel:
    """
    CTGAN Model Training and Management.

    This class trains a CTGAN model using a given preprocessed dataset. It handles metadata 
    detection, model training, and serialization for later reuse.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initializes the CTGAN model with metadata detection.

        Args:
            df (pd.DataFrame): Preprocessed dataset to train the model on.

        Raises:
            ValueError: If the input DataFrame is empty.
        """
        if df.empty:
            raise ValueError("Input DataFrame is empty. Provide valid data for training.")

        # Create a copy of the DataFrame to prevent unintended modifications
        self.df = df.copy()
        self.synthesizer = None  # Will be initialized during training

        # Detect metadata
        print("Detecting metadata for the dataset...")
        self.metadata = SingleTableMetadata()
        self.metadata.detect_from_dataframe(self.df)

        print("Metadata detection complete.")
        print(self.metadata.to_dict())  # Debugging: Print metadata structure

    def meta_metric(synthesizer, real_df):
        """
        Computes a combined meta-metric from mean KL divergence and Wasserstein distance.

        Args:
            synthesizer (CTGANSynthesizer): Trained synthesizer.
            real_df (pd.DataFrame): Original data.

        Returns:
            float: Negative of combined divergence (higher is better).
        """
        synthetic_data = synthesizer.sample(len(real_df))
        evaluator = Evaluator(real_data=real_df, synthetic_data=synthetic_data)
        summary = evaluator.get_summary_statistics()

        mean_kl = summary['kl_divergence']['mean']
        mean_wass = summary['wasserstein']['mean']

        combined_score = -(mean_kl + mean_wass)

        return combined_score


    def train_model(self, epochs = 300, batch_size = 500, generator_lr = 2e-4, discriminator_lr = 2e-4, embedding_dim = 128, discriminator_steps = 1):
        """
        Trains the CTGAN model on the provided dataset.

        Args:
            epochs (int, optional): Number of training epochs. Defaults to 300.
            batch_size (int, optional): Batch size for training. Defaults to 500.
            generator_lr (float, optional): Generator learning rate. Defaults to 2e-4.
            discriminator_lr (float, optional): Discriminator learning rate. Defaults to 2e-4.
            embedding_dim (int, optional): Embedding dimension. Defaults to 128.
            discriminator_steps (int, optional): Discriminator steps per generator step. Defaults to 1.

        Raises:
            RuntimeError: If metadata detection fails.
        """
        print("Initializing CTGAN training...")

        if not self.metadata:
            raise RuntimeError("Metadata is missing. Ensure metadata detection was successful.")

        # Initialize and train the synthesizer
        self.synthesizer = CTGANSynthesizer(
        metadata=self.metadata,
        epochs=epochs,
        batch_size=batch_size,
        generator_lr=generator_lr,
        discriminator_lr=discriminator_lr,
        embedding_dim=embedding_dim,
        discriminator_steps=discriminator_steps
    )
        # Debugging: Verify column consistency
        print("Validating column consistency between metadata and dataframe...")
        print("Metadata Columns:", self.metadata.to_dict())
        print("Dataframe Columns:", list(self.df.columns))

        try:
            self.synthesizer.fit(self.df)
            print("CTGAN model training complete.")
        except Exception as e:
            print(f"Training failed due to: {str(e)}")
            raise  # Re-raise exception for further debugging

    def save_model(self, model_path: str = "trained_ctgan.pkl"):
        """
        Saves the trained CTGAN model to a file.

        Args:
            model_path (str, optional): File path to save the model. Defaults to 'trained_ctgan.pkl'.

        Raises:
            ValueError: If no trained model is found.
        """
        if self.synthesizer is None:
            raise ValueError("No trained model found. Train the model before saving.")

        model_path = os.path.join(os.getcwd(), model_path)

        try:
            with open(model_path, "wb") as model_file:
                pickle.dump(self.synthesizer, model_file)
            print(f"Model successfully saved at: {model_path}")
        except Exception as e:
            print(f"Error saving the model: {str(e)}")
            raise  # Re-raise for debugging

    def tune_hyperparameters(self, param_grid):
        """
        Tunes CTGAN hyperparameters using grid search and a specified evaluation metric.

        Args:
            param_grid (dict): Dictionary specifying parameter ranges.
            eval_metric (function, optional): Evaluation metric function. If None, uses meta_metric.
        """
        best_score = float('-inf')
        best_params = None
        keys, values = zip(*param_grid.items())
        
        for param_values in product(*values):
            params = dict(zip(keys, param_values))
            print(f"Training with hyperparameters: {params}")
            self.train_model(
                epochs=params['epochs'],
                batch_size=params['batch_size'],
                generator_lr=params['generator_lr'],
                discriminator_lr=params['discriminator_lr'],
                embedding_dim=params['embedding_dim'],
                discriminator_steps=params['discriminator_steps']
            )

            score = self.meta_metric(self.synthesizer, self.df)
            print(f"Score: {score}")

            if score > best_score:
                best_score = score
                best_params = params

        print(f"Best hyperparameters found: {best_params}")

        self.train_model(
            epochs=best_params['epochs'],
            batch_size=best_params['batch_size'],
            generator_lr=best_params['generator_lr'],
            discriminator_lr=best_params['discriminator_lr'],
            embedding_dim=best_params['embedding_dim'],
            discriminator_steps=best_params['discriminator_steps']
        )