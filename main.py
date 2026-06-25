import logging
from waitress import serve
from ecommerce.wsgi import application

if __name__ == "__main__":
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    print("Starting Waitress Server on http://127.0.0.1:8000 ")
    
    serve(
        application, 
        host='127.0.0.1', 
        port=8000, 
        threads=30, 
        connection_limit=300
    )