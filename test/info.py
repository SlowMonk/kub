import json
import kfp
import kfp.dsl as dsl
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


@dsl.pipeline(
    name="resourceop-basic",
    description="A Basic Example on ResourceOp Usage."
)
def resourceop_basic():

    # Start a container. Print out env vars.
    op = dsl.ResourceOp(
        name='test-step',
        k8s_resource=json.loads(_CONTAINER_MANIFEST),
        action='create'
    )


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(resourceop_basic, __file__ + '.yaml')
    my_experiment = client.create_experiment(name='JK_ml_engine_ml_pipeline_test')
    my_run = client.run_pipeline(my_experiment.id, 'JK_ml_engine_ml_pipeline_test', 'example.zip')
    print('Pipeline End...')