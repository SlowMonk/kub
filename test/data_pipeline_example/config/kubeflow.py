import kfp

from config.istio_auth import get_istio_auth_session
from config.settings import settings


def connect_to_kube():

    auth_session = get_istio_auth_session(
        url=settings.KUBEFLOW_ENDPOINT,
        username=settings.KUBEFLOW_USERNAME,
        password=settings.KUBEFLOW_PASSWORD
    )

    client = kfp.Client(host=f"{settings.KUBEFLOW_ENDPOINT}/pipeline",
                        cookies=auth_session["session_cookie"],
                        namespace=f"{settings.KUBERFLOW_NAMESPACE}",
                        )
    return client
