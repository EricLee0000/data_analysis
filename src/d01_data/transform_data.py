import numpy as np
import pandas as pd
import sys


def parse_dates(df):
    for col in df.columns:
        if "date" in col or "_at" in col:
            df[col] = pd.to_datetime(df[col])
    return df


def clean_strings(array):
    """Reformat strings from a Pandas array"""
    idx = array.loc[~array.isna()].index
    array.iloc[idx] = [str(x).strip() for x in array.iloc[idx]]

    return array


class External_Data(object):
    def __init__(self,):
        return

    def rename_cols(self, all_cols, attr_cols):
        """Standardize column labels. Add _sot (source of truth) label 
        to attribute cols."""

        edited_cols = [x.lower() for x in all_cols]
        for i, col in enumerate(edited_cols):
            if "start" in col and "date" in col:
                edited_cols[i] = "start_date"
            elif "gender" in col:
                edited_cols[i] = "gender"
            elif "segment" in col:
                edited_cols[i] = "segment"
            elif "performance" in col:
                edited_cols[i] = "performance"
            elif "level" in col:
                edited_cols[i] = "level"
            elif "department" in col:
                edited_cols[i] = "department"
            elif "location" in col:
                edited_cols[i] = "location"
            elif "age group" in col:
                edited_cols[i] = "age group"


            if edited_cols[i] in attr_cols:
                edited_cols[i] += "_sot"

        return edited_cols

    def drop_empty_cols(self, df):
        """Drop columns if only NULL values exist."""
        for col in df.columns:
            try:
                if df[col].isna().sum() == df.shape[0]:
                    df.drop(col, axis=1, inplace=True)
                    print(
                        "{} column dropped because only NULL values exist.".format(col)
                    )
            except KeyError:
                pass
        return df

    def clean_data(self, FILEDIR, attr_cols, primary_key="email"):
        """Clean and standardize the external data file provided by the customer."""
        try:
            df = pd.read_csv(FILEDIR)

            # Rename cols for merge
            df.columns = self.rename_cols(df.columns, attr_cols)
            # update attr_cols to reflect added string '_sot'
            attr_cols = [x + "_sot" for x in attr_cols]
            print(df.head())

            # Find missing columns
            missing_cols = []
            for col in attr_cols:
                if col not in df.columns:
                    missing_cols.append(col)
                    df[col] = np.nan

            # Ensure that the file is not missing any columns
            if len(missing_cols) > 0:
                print(
                    """WARNING! External data file is missing the following columns: {}.
                    These columns were created and filled with NaN.""".format(
                        missing_cols
                    )
                )

            # Remove cols not in attributes or primary key
            drop_cols = list(set(df.columns) - set(attr_cols))
            drop_cols.remove(primary_key)
            df.drop(drop_cols, axis=1, inplace=True)

            # Clean up strings
            existing_attr_cols = set(df.columns).intersection(set(attr_cols))
            for col in existing_attr_cols:
                df[col] = clean_strings(df[col])
            df[primary_key] = [x.strip().lower() for x in df[primary_key]]

            return df

        except FileNotFoundError:
            print("ERROR! File not found.")