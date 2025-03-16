from throttling_counter import ThrottlingCounter
import logging
logging.basicConfig(level = logging.INFO)
class RateLimiter:
    def __init__(self):
        self.throttle_counter = ThrottlingCounter()

    def request(self, endpoint, payload):
        logging.info("Incoming request for API Endpoint {}".format(endpoint))
        if self.throttle_counter.needs_throttle(endpoint, payload):
            logging.info("Request for API Endpoint {} for account Id {} has been throttled".format(endpoint, payload.account_id))
            return self.throttled_response()
        logging.info("Request for API Endpoint {} for account Id {} has been forwarded".format(endpoint, payload.account_id))
        return self.normal_response(endpoint, payload)
    
    def throttled_response(self):
        return  """
        {
            'status' : 400,
            'body' : {'message' : 'ThrottlingException: Rate exceeded'}
        }
        """
    def normal_response(self, endpoint, payload):
        # Some Service not here
        self.throttle_counter.decrease_counter(payload.account_id, endpoint)
        return self.forward_request_to_service(endpoint, payload)
    
    def forward_request_to_service(self, endpoint, payload):
        # Make HTTPS call
        return  """
        {
            'status' : 200,
            'body' : {'message' : 'This is response from real service'}
        }
        """