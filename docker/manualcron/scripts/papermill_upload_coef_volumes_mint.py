import datetime as dt

import papermill as pm

TODAY = dt.date.today()
S3_BUCKET = "s3://noos-prod-neptune-services/Staging/Extracts/PAPERMILL/"

if __name__ == "__main__":
    pm.execute_notebook(
        input_path="/papermill/upload_coef_volumes_mint.ipynb",
        output_path=f"{S3_BUCKET}profile_mint_{TODAY.isoformat()}.ipynb",
        # parameters={"CREATED_AT": TODAY},
    )
