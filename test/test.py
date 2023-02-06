import kfp
import kfp.compiler
from kfp.components import create_component_from_func, OutputTextFile, InputPath, OutputPath

from kubeflow_connection import connect_to_kube


client = connect_to_kube()


@create_component_from_func
def make_dataset_op(
        dataset_size: int,
        data_path: OutputPath("Table")
):
    import random
    import os

    NUM_GBS = 5
    GB_IN_BYTES = 1e+9
    CURRENT_GB = 1

    header = "a, b, c, d, e,\n"
    col_num = len(header.split(",")) - 1

    f = open(data_path, "w")
    f.writelines(header)
    while os.path.getsize(data_path) < NUM_GBS * GB_IN_BYTES:
        for num in range(dataset_size):
            for i in range(col_num):
                rand_num = random.random()
                f.write(str(rand_num)+", ")
            f.write("\n")
        f.flush()
        if os.path.getsize(data_path) > CURRENT_GB * GB_IN_BYTES:
            print(f"File size {CURRENT_GB} GBS")
            CURRENT_GB += 1
    f.close()


@create_component_from_func
def processing_dataset_op(
        data_path: InputPath("Table"),
        dataset_path: OutputPath("Table")
):

    f = open(data_path, "r")

    ds = open(dataset_path, "w")
    for i, val in enumerate(f.readlines()):
        ds.writelines(f"${i}..$" + val)
        ds.flush()
    ds.close()


@kfp.dsl.pipeline(name="test")
def test_pipeline():
    making_task = make_dataset_op(10)
    _ = processing_dataset_op(making_task.outputs["data"])


def run_pipeline():

    client.create_run_from_pipeline_func(
        pipeline_func=test_pipeline,
        arguments={},
        run_name="test222",
        experiment_name="test_dkshin",
        namespace="kubeflow-user-example-com"
    )


if __name__ == "__main__":

    run_pipeline()
