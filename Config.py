# Configuration data for the BBRC Exome analysis pipeline.
# In Python:
#   import bbrcConfig as config
#   print config.DB_ROOT
import os,sys

# Root of the project heirarchy. 
proj_root=os.environ.get('ISOGLYP_HOME',None)
if proj_root is None:
    PROJECT_ROOT='./ISOGlyp/'
else:
    PROJECT_ROOT=proj_root

#ISOGlyP Core Program
sys.path.insert(0,'%s'%PROJECT_ROOT)
import isoglyp_core

# Root of the pipeline code/data tree.
PIPELINE_ROOT=PROJECT_ROOT+'/pipeline'

# Root of the database tree.
db_root = os.environ.get('ISO_DB_DIR',None)
if db_root is None:
    DB_ROOT=PROJECT_ROOT+'/db'
else:
    DB_ROOT = db_root

evt_root = os.environ.get('ISO_EV_DIR',None)
if evt_root is None:
    EVT_ROOT=PROJECT_ROOT+'EV_Tables/20180321'
else:
    EVT_ROOT = evt_root

CURRENT_EV = '20180321'

proj_work = os.environ.get('ISO_WORK_DIR',None)
if proj_work is None:
    PROJ_WORK=PROJECT_ROOT+'/workData/work'
else:
    PROJ_WORK=proj_work

# Directory containing input datasets.
#INPUT_DIR=PROJECT_ROOT+'/input'

# Directory containing output datasets.
#OUTPUT_DIR=PROJECT_ROOT+'/output'



