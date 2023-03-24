import kfp
import kfp.components as comp
from kfp import dsl
from connect_to_kube import connect_to_kube


_CONTAINER_MANIFEST = """
{
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        "generateName": "resourceop-basic-job-"
    },
    "spec": {
        "template": {
            "metadata": {
                "name": "resource-basic"
            },
            "spec": {
                "containers": [{
                    "name": "sample-container",
                    "image": "k8s.gcr.io/busybox",
                    "command": ["/usr/bin/env"]
                }],
                "restartPolicy": "Never"
            }
        },
        "backoffLimit": 4      
    }
}
"""

def logg_env_function():
  import os
  import logging
  logging.basicConfig(level=logging.INFO)
  env_variable = os.getenv('example_env')
  logging.info('The environment variable is: {}'.format(env_variable))


client = connect_to_kube()
TEST_COMPONENT_PATH = "Table"

NAME = 'kf-sw-v17'
TRAIN_VER = 'train_v2'
DESCRIPTION = 'jk_test'

@dsl.pipeline(
    name=NAME,
    description=DESCRIPTION
)


def kf_iris_pipeline():

    add_p = dsl.ContainerOp(

        name="load iris data pipeline",
        image="repo.surromind.ai/sw/example-preprocessing:v10",
        command= ["python",'load_data.py'],
        arguments=[
            '--data_path', './Iris.csv'
        ],
        file_outputs={'result' : '/result.csv'}
    )

    ml = dsl.ContainerOp(
        name="training pipeline",
        image=f"repo.surromind.ai/sw/example-traning:{TRAIN_VER}",
        command= ["python",'training_model.py'],
        arguments=[
            '--data', add_p.outputs['result'],
            '--name',  NAME
        ])

    ml.after(add_p)

if __name__ == "__main__":

    kfp.compiler.Compiler().compile(kf_iris_pipeline, 'example.zip')
    my_experiment = client.create_experiment(name='JK_ml_engine_ml_pipeline_test')
    my_run = client.run_pipeline(my_experiment.id, 'JK_ml_engine_ml_pipeline_test', 'example.zip')
    print('Pipeline End...')
