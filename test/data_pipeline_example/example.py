import kfp
import kfp
import kfp.components as comp
from kfp import dsl
from connect_to_kube import connect_to_kube

client = connect_to_kube()
TEST_COMPONENT_PATH = "Table"

import kfp
from kfp import dsl
def flip_coin_op():
    return dsl.ContainerOp(
        name='Flip coin',
        image='python:alpine3.6',
        command=['sh', '-c'],
        arguments=['python -c "import random; result = \'heads\' if random.randint(0,1) == 0 '
                  'else \'tails\'; print(result)" | tee /tmp/output'],
        file_outputs={'output': '/tmp/output'}
    )
def print_op(msg):
    """Print a message."""
    return dsl.ContainerOp(
        name='Print',
        image='alpine:3.6',
        command=['echo', msg],
    )
    
@dsl.pipeline(
    name='test_pipeline_C',
    description='A pipeline with two sequential steps.'
)
def sequential_pipeline():
    """A pipeline with two sequential steps."""
    flip = flip_coin_op()
    print_op(flip.output)

'''
create_run_from_pipeline_func
'''
# def coin_pipeline():
#     client.create_run_from_pipeline_func(
#         pipeline_func=sequential_pipeline,
#         arguments={},
#         run_name="surro_ml_engine_jk_sequential_test",
#         experiment_name="surro_ml_engine_jk",
#         namespace="kubeflow-user-example-com"
#     )
'''
run_pipeline
'''
def coin_pipeline():
    
    kfp.compiler.Compiler().compile(sequential_pipeline, 'example.zip')
    my_experiment = client.create_experiment(name='surro_ml_engine_jkt')
    my_run = client.run_pipeline(my_experiment.id, 'surro_ml_engine_jk_sequential_test', 'example.zip')

if __name__ == "__main__":
    coin_pipeline()