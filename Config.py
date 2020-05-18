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

evt_root = os.environ.get('ISO_EV_DIR',None)
if evt_root is None:
    EVT_ROOT='../ISOGlyP-EV_Tables/20200516'
else:
    EVT_ROOT = evt_root

CURRENT_EV = '20200516'
