import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#logging.disable(logging.CRITICAL)
#uncommenting the above line would disable debugging across the board
#much easier than finding and deleting print statements
#disables that tier of logging and below

logging.debug('Start of program') #works like our debug print statements
logging.info('Info tier') #higher tiers going downard
logging.warning('warning tier')
logging.error('error tier')
logging.critical('critical tier')

#can also write all log messages to a file by using
#logging.basicConfig(filename='myProgramLog.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
