import json

class ThrottlingRules:
    def __init__(self, rules_endpoint):
        self.rules = self.load_rules(rules_endpoint)
    
    def load_rules(self, rules_endpoint):
        with open(rules_endpoint) as f:
            rules = json.load(f)
            return rules