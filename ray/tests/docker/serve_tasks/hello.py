from ray import serve
from starlette.requests import Request


@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 0.2, "num_gpus": 0}, route_prefix="/hello")
class Hello:
    def __call__(self, http_request: Request) -> int:
        print("called")
        return "hello world"


serve.run(Hello.bind(), name="hello", host="0.0.0.0")
