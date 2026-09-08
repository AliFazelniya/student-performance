from pathlib import Path  # Provides path handling for locating project directories
from typing import List, Tuple  # Supplies type hints for collection and tuple outputs

import pandas as pd  # Imports pandas for dataframe operations
from sklearn.compose import ColumnTransformer  # Enables parallel preprocessing pipelines
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # Offers encoding and scaling transformers


PROJECT_ROOT = Path(__file__).resolve().parent.parent  # Calculates the repository root relative to this file
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"  # Points to the folder containing unprocessed datasets
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"  # Targets the directory for saving processed outputs


def load_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:  # Loads raw math and Portuguese datasets from disk
    mat_path = RAW_DATA_DIR / "student-mat.csv"  # Constructs the path to the math dataset
    por_path = RAW_DATA_DIR / "student-por.csv"  # Constructs the path to the Portuguese dataset
    mat_df = pd.read_csv(mat_path, sep=";")  # Reads the math CSV with semicolon delimiters into a DataFrame
    por_df = pd.read_csv(por_path, sep=";")  # Reads the Portuguese CSV with semicolon delimiters into a DataFrame
    return mat_df, por_df  # Returns both datasets for downstream processing


def build_preprocessor(feature_columns: List[str]) -> ColumnTransformer:  # Constructs encoders and scalers for all features
    binary_cols = [  # Defines features expected to take binary values
        "sex",  # Indicates student sex category
        "address",  # Differentiates urban versus rural residence
        "famsize",  # Distinguishes small versus large family
        "Pstatus",  # Encodes parental cohabitation status
        "schoolsup",  # Flags access to school-provided support
        "famsup",  # Flags availability of family support
        "paid",  # Notes whether extra paid classes are taken
        "activities",  # Identifies participation in extracurricular activities
        "nursery",  # Records nursery school attendance history
        "higher",  # Captures aspiration for higher education
        "internet",  # Flags home internet availability
        "romantic",  # Indicates involvement in a romantic relationship
    ]  # Ends the enumeration of binary feature names
    categorical_cols = ["school", "Mjob", "Fjob", "reason", "guardian"]  # Lists nominal categorical features
    numeric_cols = [col for col in feature_columns if col not in binary_cols + categorical_cols]  # Identifies remaining numeric columns by exclusion

    return ColumnTransformer(  # Builds a composite transformer that encodes and scales feature groups
        transformers=[  # Supplies the ordered set of named transformers with their target columns
            ("bin", OneHotEncoder(drop="if_binary"), binary_cols),  # One-hot encodes binary flags while dropping redundant levels
            ("cat", OneHotEncoder(), categorical_cols),  # One-hot encodes categorical features preserving all levels
            ("num", StandardScaler(), numeric_cols),  # Standardizes numeric features to zero mean and unit variance
        ]  # Concludes the ordered transformer definitions
    )  # Finalizes and returns the configured ColumnTransformer instance


def save_processed(df_mat: pd.DataFrame, df_por: pd.DataFrame) -> None:  # Writes processed feature matrices to CSV files
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)  # Ensures the processed data directory exists
    df_mat.to_csv(PROCESSED_DATA_DIR / "processed_mat.csv", index=False)  # Writes the processed math dataset without row indices
    df_por.to_csv(PROCESSED_DATA_DIR / "processed_por.csv", index=False)  # Writes the processed Portuguese dataset without row indices


def main() -> None:  # Coordinates dataset loading, preprocessing, and saving
    mat, por = load_datasets()  # Loads both raw datasets from disk
    preprocessor = build_preprocessor(mat.columns.tolist())  # Creates the preprocessing pipeline based on available columns

    processed_mat = preprocessor.fit_transform(mat)  # Fits the transformers on math data and applies them
    processed_por = preprocessor.transform(por)  # Applies the fitted transformers to Portuguese data for consistency

    bin_enc = preprocessor.named_transformers_["bin"]  # Extracts the binary encoder to inspect generated feature names
    cat_enc = preprocessor.named_transformers_["cat"]  # Extracts the categorical encoder to inspect generated feature names

    bin_feature_names = bin_enc.get_feature_names_out(bin_enc.feature_names_in_)  # Computes output names for binary encodings
    cat_feature_names = cat_enc.get_feature_names_out(cat_enc.feature_names_in_)  # Computes output names for categorical encodings
    num_feature_names = preprocessor.transformers_[2][2]  # Retrieves the original numeric column names used in scaling

    all_feature_names = list(bin_feature_names) + list(cat_feature_names) + list(num_feature_names)  # Concatenates all output feature names in order

    df_mat = pd.DataFrame(processed_mat, columns=all_feature_names)  # Wraps the processed math array into a labeled DataFrame
    df_por = pd.DataFrame(processed_por, columns=all_feature_names)  # Wraps the processed Portuguese array into a labeled DataFrame

    save_processed(df_mat, df_por)  # Persists both processed datasets to disk
    print("DONE! CSV files saved successfully!")  # Logs a completion message after saving


if __name__ == "__main__":  # Executes when the script is invoked directly
    main()  # Runs the preprocessing workflow entry point
