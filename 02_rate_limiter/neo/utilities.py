from typing import Any, Dict

from common import ApiRateLimitDefinition, RateLimitDefinition


class RateLimitRegistry:
    def __init__(self, file_path: str):
        import yaml
        self.reference_file: str = file_path

        with open(file_path, "r") as file:
            rate_limits: Dict[str, Any] = yaml.safe_load(file).get("rate_limits", {})

        self.default_limits: RateLimitDefinition = RateLimitDefinition(5, 1)
        self.registry: Dict[str, ApiRateLimitDefinition] = {}
        for api_name, rate_limit in rate_limits.items():
            if api_name == "default":
                print(f"[DEBUG] Loading default rate limit: {rate_limit}")
                self.default_limits = RateLimitDefinition(rate_limit["burst"], rate_limit["rate"])
                continue
            print(f"[DEBUG] Loading rate limit for {api_name}: {rate_limit}")
            self.registry[api_name] = ApiRateLimitDefinition.load(rate_limit)

    def get_rate_limit(self, api_name: str, actor_id: str) -> RateLimitDefinition:
        if api_name in self.registry:
            return self.registry[api_name].get_rate_limit(actor_id)
        return self.default_limits

    def __repr__(self):
        return f"RateLimitRegistry(default={self.default_limits}, registry={self.registry})"
