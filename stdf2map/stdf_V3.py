"""
    The main object should be used from this module is:
        Rec_Dict3
    which is a dictionary with (typ,sub) tuple as its keys
    and a record instance as its value. For each record instance,
    there's is a field: fieldMap to define the record binary structure.
"""
from stdf_V4 import RecordMeta

class Far:
    __metaclass__ = RecordMeta
    typ = 0
    sub = 10
    fieldMap = ( ('CPU_TYPE', 'U1'),
                 ('STDF_VER', 'U1') )

class Mir:
    __metaclass__ = RecordMeta
    typ = 1
    sub = 10
    fieldMap = ( ('CPU_TYPE', 'U1'),
                 ('STDF_VER', 'U1'),
                 ('MODE_COD', 'C1'),
                 ('STAT_NUM', 'U1'),
                 ('TEST_COD', 'C3'),
                 ('RTST_COD', 'C1'),
                 ('PROT_COD', 'C1'),
                 ('CMOD_COD', 'C1'),
                 ('SETUP_T', 'U4'),
                 ('START_T', 'U4'),
                 ('LOT_ID', 'Cn'),
                 ('PART_TYP', 'Cn'),
                 ('JOB_NAM', 'Cn'),
                 ('OPER_NAM', 'Cn'),
                 ('NODE_NAM', 'Cn'),
                 ('TSTR_TYP', 'Cn'),
                 ('EXEC_TYP', 'Cn'),
                 ('SUPR_NAM', 'Cn'),
                 ('HAND_ID', 'Cn'),
                 ('SBLOT_ID', 'Cn'),
                 ('JOB_REV', 'Cn'),
                 ('PROC_ID', 'Cn'),
                 ('PRB_CARD', 'Cn') )

class Mrr:
    __metaclass__ = RecordMeta
    typ = 1
    sub = 20
    fieldMap = ( ('FINISH_T', 'U4'),
                 ('PART_CNT', 'U4'),
                 ('RTST_CNT', 'I4'),
                 ('ABRT_CNT', 'I4'),
                 ('GOOD_CNT', 'I4'),
                 ('FUNC_CNT', 'I4'),
                 ('DISP_COD', 'C1'),
                 ('USR_DESC', 'Cn'),
                 ('EXC_DESC', 'Cn') )

class Wir:
    __metaclass__ = RecordMeta
    typ = 2
    sub = 10
    fieldMap = ( ('HEAD_NUM', 'U1'),
                 ('PAD_BYTE', 'B1'),
                 ('START_T', 'U4'),
                 ('WAFER_ID', 'Cn') )

class Wrr:
    __metaclass__ = RecordMeta
    typ = 2
    sub = 20
    fieldMap = ( ('FINISH_T', 'U4'),
                 ('HEAD_NUM', 'U1'),
                 ('PAD_BYTE', 'B1'),
                 ('PART_CNT', 'U4'),
                 ('RTST_CNT', 'I4'),
                 ('ABRT_CNT', 'I4'),
                 ('GOOD_CNT', 'I4'),
                 ('FUNC_CNT', 'I4'),
                 ('WAFER_ID', 'Cn'),
                 ('HAND_ID', 'Cn'),
                 ('PRB_CARD', 'Cn'),
                 ('USR_DESC', 'Cn'),
                 ('EXC_DESC', 'Cn') )

class Hbr:
    __metaclass__ = RecordMeta
    typ = 1
    sub = 40
    fieldMap = ( ('HBIN_NUM', 'U2'),
                 ('HBIN_CNT', 'U4'),
                 ('HBIN_NAM', 'Cn') )

class Sbr:
    __metaclass__ = RecordMeta
    typ = 1
    sub = 50
    fieldMap = ( ('SBIN_NUM', 'U2'),
                 ('SBIN_CNT', 'U4'),
                 ('SBIN_NAM', 'Cn') )

class Tsr:
    __metaclass__ = RecordMeta
    typ = 10
    sub = 30
    fieldMap = ( ('TEST_NUM', 'U4'),
                 ('EXEC_CNT', 'I4'),
                 ('FAIL_CNT', 'I4'),
                 ('ALRM_CNT', 'I4'),
                 ('OPT_FLAG', 'B1'),
                 ('PAD_BYTE', 'B1'),
                 ('TEST_MIN', 'R4'),
                 ('TEST_MAX', 'R4'),
                 ('TST_MEAN', 'R4'),
                 ('TST_SDEV', 'R4'),
                 ('TST_SUMS', 'R4'),
                 ('TST_SQRS', 'R4'),
                 ('TEST_NAM', 'Cn'),
                 ('SEQ_NAME', 'Cn') )

class Pir:
    __metaclass__ = RecordMeta
    typ = 5
    sub = 10
    fieldMap = ( ('HEAD_NUM', 'U1'),
                 ('SITE_NUM', 'U1'),
                 ('X_COORD', 'I2'),
                 ('Y_COORD', 'I2'),
                 ('PART_ID', 'Cn') )

class Prr:
    __metaclass__ = RecordMeta
    typ = 5
    sub = 20
    fieldMap = ( ('HEAD_NUM', 'U1'),
                 ('SITE_NUM', 'U1'),
                 ('NUM_TEST', 'U2'),
                 ('HARD_BIN', 'U2'),
                 ('SOFT_BIN', 'U2'),
                 ('PART_FLG', 'B1'),
                 ('PAD_BYTE', 'B1'),
                 ('X_COORD', 'I2'),
                 ('Y_COORD', 'I2'),
                 ('PART_ID', 'Cn'),
                 ('PART_TXT', 'Cn'),
                 ('PART_FIX', 'Bn') )

class Fdr:
    __metaclass__ = RecordMeta
    typ = 10
    sub = 20
    fieldMap = ( ('TEST_NUM', 'U4'),
                 ('DESC_FLG', 'B1'),
                 ('TEST_NAM', 'Cn'),
                 ('SEQ_NAME', 'Cn') )

class Ftr:
    __metaclass__ = RecordMeta
    typ = 15
    sub = 20
    fieldMap = ( ('TEST_NUM', 'U4'),
                 ('HEAD_NUM', 'U1'),
                 ('SITE_NUM', 'U1'),
                 ('TEST_FLG', 'B1'),
                 ('DESC_FLG', 'B1'),
                 ('OPT_FLAG', 'B1'),
                 ('TIME_SET', 'U1'),
                 ('VECT_ADR', 'U4'),
                 ('CYCL_CNT', 'U4'),
                 ('REPT_CNT', 'U2'),
                 ('PCP_ADR', 'U2'),
                 ('NUM_FAIL', 'U4'),
                 ('FAIL_PIN', 'Bn'),
                 ('VECT_DAT', 'Bn'),
                 ('DEV_DAT', 'Bn'),
                 ('RPIN_MAP', 'Bn'),
                 ('TEST_NAM', 'Cn'),
                 ('SEQ_NAME', 'Cn'),
                 ('TEST_TXT', 'Cn') )

class Pdr:
    __metaclass__ = RecordMeta
    typ = 10
    sub = 10
    fieldMap = ( ('TEST_NUM', 'U4'),
                 ('DESC_FLG', 'B1'),
                 ('OPT_FLAG', 'B1'),
                 ('RES_SCAL', 'I1'),
                 ('UNITS', 'C7'),
                 ('RES_LDIG', 'U1'),
                 ('RES_RDIG', 'U1'),
                 ('LLM_SCAL', 'I1'),
                 ('HLM_SCAL', 'I1'),
                 ('LLM_LDIG', 'U1'),
                 ('LLM_RDIG', 'U1'),
                 ('HLM_LDIG', 'U1'),
                 ('HLM_RDIG', 'U1'),
                 ('LO_LIMIT', 'R4'),
                 ('HI_LIMIT', 'R4'),
                 ('TEST_NAM', 'Cn'),
                 ('SEQ_NAME', 'Cn') )

class Ptr:
    __metaclass__ = RecordMeta
    typ = 15
    sub = 10
    fieldMap = ( ('TEST_NUM', 'U4'),
                 ('HEAD_NUM', 'U1'),
                 ('SITE_NUM', 'U1'),
                 ('TEST_FLG', 'B1'),
                 ('PARM_FLG', 'B1'),
                 ('RESULT', 'R4'),
                 ('OPT_FLAG', 'B1'),
                 ('RES_SCAL', 'I1'),
                 ('RES_LDIG', 'U1'),
                 ('RES_RDIG', 'U1'),
                 ('DESC_FLG', 'B1'),
                 ('UNITS', 'C7'),
                 ('LLM_SCAL', 'I1'),
                 ('HLM_SCAL', 'I1'),
                 ('LLM_LDIG', 'U1'),
                 ('LLM_RDIG', 'U1'),
                 ('HLM_LDIG', 'U1'),
                 ('HLM_RDIG', 'U1'),
                 ('LO_LIMIT', 'R4'),
                 ('HI_LIMIT', 'R4'),
                 ('TEST_NAM', 'Cn'),
                 ('SEQ_NAME', 'Cn'),
                 ('TEST_TXT', 'Cn') )

# The following records are STDF+ specific and 
# additional defined to the STDF (standard Teradyne format)
class Brr:
    __metaclass__ = RecordMeta
    typ = 220
    sub = 201
    fieldMap = ( ('RTST_COD', 'C1'),
                 ('BIN_CNT', 'U2'),
                 ('BIN_NUM', 'U2') )

class Wtr:
    __metaclass__ = RecordMeta
    typ = 220
    sub = 202
    fieldMap = ( ('TEST_TYPE', 'C1') )

class Etsr:
    __metaclass__ = RecordMeta
    typ = 220
    sub = 203
    fieldMap = ( ('TEST_NUM', 'U4'),
                 ('EXEC_CNT', 'I4'),
                 ('FAIL_CNT', 'I4'),
                 ('ALRM_CNT', 'I4'),
                 ('TEST_10', 'R4'),
                 ('TEST_90', 'R4'),
                 ('OPT_FLAG', 'B1'),
                 ('PAD_BYTE', 'B1'),
                 ('TEST_MIN', 'R4'),
                 ('TEST_MAX', 'R4'),
                 ('TST_MEAN', 'R4'),
                 ('TST_SDEV', 'R4'),
                 ('TST_SUMS', 'R4'),
                 ('TST_SQRS', 'R4'),
                 ('TEST_NAM', 'Cn'),
                 ('SEQ_NAME', 'Cn') )

class EtsrV3:
    __metaclass__ = RecordMeta
    typ = 220
    sub = 203
    fieldMap = ( ('TEST_NUM', 'U4'),
                 ('EXEC_CNT', 'I4'),
                 ('FAIL_CNT', 'I4'),
                 ('ALRM_CNT', 'I4'),
                 ('OPT_FLAG_QU', 'B1'),
                 ('TEST_05', 'R4'),
                 ('TEST_10', 'R4'),
                 ('TEST_50', 'R4'),
                 ('TEST_90', 'R4'),
                 ('TEST_95', 'R4'),
                 ('OPT_FLAG', 'B1'),
#                ('PAD_BYTE', 'B1'),
                 ('TEST_MIN', 'R4'),
                 ('TEST_MAX', 'R4'),
                 ('TST_MEAN', 'R4'),
                 ('TST_SDEV', 'R4'),
                 ('TST_SUMS', 'R4'),
                 ('TST_SQRS', 'R4'),
                 ('TEST_NAM', 'Cn'),
                 ('SEQ_NAME', 'Cn') )
 
class Gtr:
    __metaclass__ = RecordMeta
    typ = 220
    sub = 204
    fieldMap = ( ('TEXT_NAME', 'C16'),
                 ('TEXT_VAL', 'Cn') )

class Adr:
    __metaclass__ = RecordMeta
    typ = 220
    sub = 205
    fieldMap = ( ('CPU_TYPE', 'U1'),
                 ('STDF_VER', 'Cn'),
                 ('DB_ID', 'U1'),
                 ('PARA_CNT', 'U2'),
                 ('LOT_FLG', 'U1'),
                 ('RTST_CNT', 'U2'),
                 ('LOT_TYPE', 'C1'),
                 ('RTST_WAF', 'K5Cn'),
                 ('RTST_BIN', 'K5U4') )

class Epdr:
    __metaclass__ = RecordMeta
    typ = 220
    sub = 206
    fieldMap = ( ('TEST_NUM', 'U4'),
                 ('OPT_FLAG', 'B1'),
                 ('CAT', 'C2'),
                 ('TARGET', 'R4'),
                 ('SPC_FLAG', 'C2'),
                 ('LVL', 'R4'),
                 ('HVL', 'R4'),
                 ('TEST_NAM', 'Cn') )

class Gdr:
    __metaclass__ = RecordMeta
    typ = 50
    sub = 10
    fieldMap = ( ('FLD_CNT', 'U2'),
                 ('GEN_DATA', 'K0Vn') )

class Shb:
    """SiteSpecificHardwareBinRecord (STDF_V3+ only)
    """
    __metaclass__ = RecordMeta
    typ = 25
    sub = 10
    fieldMap = ()

class Ssb:
    """ SiteSpecificSoftwareBinRecord (STDF_V3+ only)
    """
    __metaclass__ = RecordMeta
    typ = 25
    sub = 20
    fieldMap = ()

class Sts:
    """ SiteSpecificTestSynopsisRecord (STDF_V3+ only)
    """
    __metaclass__ = RecordMeta
    typ = 25
    sub = 30
    fieldMap = ()

class Scr:
    """ SiteSpecificPartCountRecord (STDF_V3+ only)
    """
    __metaclass__ = RecordMeta
    typ = 25
    sub = 40
    fieldMap = ()

class Bps:
  __metaclass__ = RecordMeta
  typ = 20
  sub = 10
  fieldMap = (
    ('SEQ_NAME','Cn'),
  )

class Eps:
  __metaclass__ = RecordMeta
  typ = 20
  sub = 20
  fieldMap = ()

class Dtr:
  __metaclass__ = RecordMeta
  typ = 50
  sub = 30
  fieldMap = (
    ('TEXT_DAT', 'Cn'),
  )

Records = [Far(), Mir(), Mrr(), Wir(), Wrr(), Hbr(), Sbr(),
           Tsr(), Pir(), Prr(), Fdr(), Ftr(), Pdr(), Ptr(),
           Brr(), Wtr(), EtsrV3(), Gtr(), Adr(), Epdr(),
           Gdr(), Shb(), Ssb(), Sts(), Scr(), Bps(), Eps(),
           Dtr()]

Rec_Dict3 = {}
for r in Records:
    Rec_Dict3[(r.typ, r.sub)] = r
