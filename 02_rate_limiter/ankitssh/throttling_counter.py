import copy
import logging
from rules_service import ThrottlingRules

logging.basicConfig(level = logging.INFO)

class ThrottlingCounter:
    def __init__(self):
        self.throttling_rules = ThrottlingRules("rules.json").rules
        self.accout_id_counter_map = {}
    
    def needs_throttle(self, endpoint, payload):
        if payload.account_id not in self.accout_id_counter_map:
            self.accout_id_counter_map[payload.account_id] = copy.deepcopy(self.throttling_rules)
        
        logging.info("Current counter for account {} is {}".format(payload.account_id, self.accout_id_counter_map[payload.account_id]["ThrottlingRules"]))
        
        if endpoint in self.throttling_rules["ThrottlingRules"] and self.current_counter(payload.account_id, endpoint) <= 0:
            return True
        return False 
    
    def current_counter(self, account_id, endpoint):
        return self.accout_id_counter_map[account_id]["ThrottlingRules"][endpoint]["Rate"]
    
    def decrease_counter(self, account_id, endpoint):
        self.accout_id_counter_map[account_id]["ThrottlingRules"][endpoint]["Rate"] -= 1
    
    def refill_counter(self, account_id, endpoint):
        # Real time refill logic
        raise NotImplementedError