import logging

logging.basicConfig(filename='app.log', filemode='a', encoding='utf-8')

logger = logging.getLogger('app module logger')

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s : %(name)s : %(levelname) : %(message)s'))

logger.addHandler(handler)



