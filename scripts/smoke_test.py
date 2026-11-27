"""로컬 서버를 시작한 뒤 uv run --env-file .env python scripts/smoke_test.py 로 실행합니다."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit

import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient
from prefect import flow, task
from prefect.cache_policies import NO_CACHE
from prefect.client.orchestration import get_client
from prefect.runtime import flow_run


@task(cache_policy=NO_CACHE)
def record_sample() -> str:
    sample = pd.DataFrame({"station_id": [1, 2, 3], "bike_count": [5, 10, 15]})
    with TemporaryDirectory() as directory:
        path = Path(directory) / "smoke.parquet"
        sample.to_parquet(path, index=False)
        mlflow.set_experiment("environment-check")
        with mlflow.start_run(tags={"prefect.flow_run_id": str(flow_run.id)}) as run:
            run_id = run.info.run_id
            mlflow.log_metric("row_count", len(sample))
            mlflow.log_artifact(str(path))

        client = MlflowClient()
        recorded = client.get_run(run_id)
        if recorded.info.status != "FINISHED" or recorded.data.metrics.get(
            "row_count"
        ) != len(sample):
            raise RuntimeError(
                f"MLflow 실행 상태 또는 row_count를 확인하세요. run_id={run_id}"
            )

        destination = Path(directory) / "download"
        destination.mkdir()
        downloaded = client.download_artifacts(run_id, path.name, str(destination))
        pd.testing.assert_frame_equal(pd.read_parquet(downloaded), sample)
    return run_id


@flow(name="environment-check")
def environment_check() -> str:
    return record_sample()


if __name__ == "__main__":
    for key in ("PREFECT_API_URL", "MLFLOW_TRACKING_URI"):
        url = urlsplit(os.environ.get(key, ""))
        if url.scheme not in ("http", "https") or not url.hostname:
            raise SystemExit(
                f"{key}에 서버 URL을 설정하고 --env-file .env 옵션으로 실행하세요."
            )

    state = environment_check(return_state=True)
    run_id = state.result()
    flow_id = state.state_details.flow_run_id
    with get_client(sync_client=True) as client:
        if not client.read_flow_run(flow_id).state.is_completed():
            raise RuntimeError(
                f"Prefect 서버에서 완료 상태를 확인할 수 없습니다. flow_run_id={flow_id}"
            )
    print(
        f"Prefect Completed ({flow_id}), MLflow FINISHED ({run_id}), row_count=3, Parquet OK"
    )
