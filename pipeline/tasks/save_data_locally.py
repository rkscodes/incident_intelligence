from prefect import task
from pathlib import Path


@task()
def save_data_locally(api_data_augmented):
    # Create directory structure if it doesn't exist
    for year in api_data_augmented["incident_year"].unique():
        year_dir = Path("../../data") / year
        year_dir.mkdir(parents=True, exist_ok=True)
        for month in api_data_augmented[api_data_augmented["incident_year"] == year][
            "incident_month"
        ].unique():
            month_dir = year_dir / month
            month_dir.mkdir(parents=True, exist_ok=True)

    # Save the DataFrame into year/month/day CSV files
    for _, row in api_data_augmented.iterrows():
        file_path = (
            Path("../../data")
            / row["incident_year"]
            / row["incident_month"]
            / f"{row['incident_day']}.csv"
        )
        row.to_frame().T.to_csv(
            file_path, mode="a", header=not file_path.exists(), index=False
        )
