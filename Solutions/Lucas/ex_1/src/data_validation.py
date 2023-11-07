import json
import logging

def validate_pooling_data(data):
    """ Function to check if incoming data 
        is valid for processing. 
    """

    try:
        # Loading json as an object
        object = json.loads(data)
        # Setting required params
        required_params = [
            'id',   'title', 'author', 
            'year', 'genre', 'summary', 
        ]
        # Checking if the message has required params
        for param in required_params:
            value = str(object[param]).strip()
            if len(value) < 1:
                # Logging error before returning false
                logging.warning('Invalid Key: <{}> can not be empty'.format(param))
                return False
        
        if str(object['genre']).lower() not in ['romance', 'scifi']:
            #Logging invalid genre message before returning false 
            logging.warning('Message with id <{}> contains invalid genre'.format(object['id']))
            return False
        elif len(str(object['title'])) > 230:
            #Logging invalid title message before returning false
            logging.warning('Message with id <{}> contains invalid title: title > 230 chr'.format(object['id']))
            return False
        return object
    except json.JSONDecodeError as e:
        # Logging error before returning false
        logging.warning('Invalid Format: Body is not valid JSON')
        return False
    except KeyError as e:
        # Logging error before returning false
        logging.warning('Missing Key: at least one required key is missing')
        return False
    