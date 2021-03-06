import sys
import unittest


def main():
	if len(sys.argv) > 2:
		from config import init_config
		init_config(sys.argv[1])
		from config import init_config
		from config import CONFIG
		from logger import CustomLogger
		cust_logger = CustomLogger(CONFIG.web_server.logger_name)
		cust_logger.add_file("log/"+CONFIG.web_server.logger_name, False)
		import app
		if bool(int(sys.argv[2])) == True:
			app.main()
		#else:
		#	from test_webserver import *
		#	unittest.main()


if __name__ == '__main__':
	main()