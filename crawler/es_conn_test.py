import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('DeepSearch'))))
from connector import es_connector

es = es_connector.ES()


print(es.allIndex())