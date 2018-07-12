""" 
    The STDF parser.
    class parser.
"""
import os
import sys
import struct
import math
import gzip
import bz2
import logging

from stdf_V4 import Rec_Dict4
from stdf_V3 import Rec_Dict3
from stdf_V4 import Far

class parser:
    """     self.log : logger
            self.endian : endian type used to parse STDF file
            self.stdf_ver : STDF file version
            self.Rec_Dict : a dictionary with (typ, sub) as keys and the
                corresponding record instance as its value.
            self.RecName_Dict : a dict with the string representation of a
                record as its keys and the corresponding record instance as
                its value.
            self.Rec_Set : The record types going to be parsed, e.g. ['Ptr', 'Ftr']
            self.Rec_NSet : The record types going to be ignored. Used only when
                self.Rec_Set is [] (empty set).
            self.Cur_Rec : The current record instance being processing.
            self.Return : Default to empty string. Set to none-empty (in function take)
                string to abort the processing of the current file.
            self.Ignore_File : if set True (in file_setup),
                the to be processed file (and only that one file) will be ignored.
            self.File_Name : the file name currently being processing.

            self.data : all data items got from current record.


        Fucntions that should be overwrite by its child:
        setup():
        cleanup():
        file_setup():
        file_cleanup():
        take():

       NOTE: You should never overwritten the following functions:
        unp, process, parse, get_parse_func;
        _set_endian, _get_def, _set_stdfver, _check_struct_size, _get_header, _get_far,
            _check_Rec_Set, _get_Nn, _get_Un, _get_In, _get_Rn, _get_Cn, _get_Bn, _get_Bn,
            _get_Dn, _get_Kx, _get_Vn.
    """
    def __init__(self):
        """
            The parser class doesn't take any argument to initialize.
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self.The_End = False
        self.endian = '@'
        self.stdf_ver = 0
        self._check_struct_size()
        self.Rec_Dict = {(0, 10): Far()}
        self.RecName_Dict = {}
        self.Rec_Set = []
        self.Rec_Nset = [] # list of records to ignore, higher priority over Rec_Set
        self.Cur_Rec = None
        self.Rec_Cnt = 0 # the first FAR record is not incremented, so set default to count the FAR record.
        self.Return = ''
        self.Ignore_File = False
        self.File_Name = '' # set near the start of parse()

    def _set_endian(self, cpu_type):
        if cpu_type == 1:
            self.log.info('Set to Big Endian Mode')
            self.endian = '>'
        elif cpu_type == 2:
            self.log.info('Set to Small Endian Mode')
            self.endian = '<'
        elif cpu_type == 0:
            self.log.critical('DEC PDP-11 or VAX processors, not supported!')
            sys.exit(0)

    def _get_def(self, stdf_ver):
        if stdf_ver == 3:
            return Rec_Dict3
        elif stdf_ver == 4:
            return Rec_Dict4
        else:
            self.log.critical('Python bug.')
            sys.exit(-1)

    def _set_stdfver(self, stdf_ver):
        assert stdf_ver in [3, 4], 'unknown stdf version %s' % str(stdf_ver) # only version 3 or 4 is accepted
        self.stdf_ver = stdf_ver
        self.Rec_Dict = self._get_def(stdf_ver)
#        self.log.debug('Generating RecName_Dict ...')
        # only after the stdf version is known can the self.Rec_Dict be used.
        for i in self.Rec_Dict.keys():
            self.RecName_Dict[str(self.Rec_Dict[i])] = self.Rec_Dict[i]
#        self.log.debug('%s' % str(self.RecName_Dict))
        self.log.info('STDF version: %s ' % str(stdf_ver))

    def _check_struct_size(self):
        assert struct.calcsize('H') == 2
        assert struct.calcsize('B') == 1
        assert struct.calcsize('I') == 4
 #       assert struct.calcsize('L') == 4  #!daf - disabled, never used, assertion fail in Ubuntu 16.04
        assert struct.calcsize('Q') == 8
        assert struct.calcsize('f') == 4
        assert struct.calcsize('d') == 8

    def _get_header(self, fd):
        # STDF header is 4 bytes long
        buf = fd.read(4)
        if len(buf) == 0:
#            self.log.info('EOF reached.')
            return 'EOF'
        elif len(buf) != 4:
            self.log.critical('_get_header: Incomplete STDF file.')
            sys.exit(-1)
        else:
            slen = self.unp('H', buf[0:2])
            typ = self.unp('B', buf[2])
            sub = self.unp('B', buf[3])
            self.Cur_Rec = self.Rec_Dict[(typ,sub)]
            self.Cur_Rec_Name = str(self.Cur_Rec)
            return (slen, (typ, sub))

    def unp(self, format, buf):
        r, = struct.unpack(self.endian+format, buf)
        return r

    def _get_far(self, fd):
        buf = fd.read(6)
        # the fifth byte is CPU type.
        cpu_type = self.unp('B', buf[4])
        self._set_endian(cpu_type)
        stdf_ver = self.unp('B', buf[5])
        self._set_stdfver(stdf_ver)
        # the above two byte is endian type independent.
        # the unp for more than one byte data type can only
        # be called after _set_endian.
        slen = self.unp('H', buf[0:2])
        assert slen == 2, "FAR record length is not 2! slen: %d" % slen
        typ = self.unp('B', buf[2])
        sub = self.unp('B', buf[3])
        assert (typ, sub) == (0, 10), "Wrong FAR header: typ-%d, sub-%d" % (typ, sub)

    def setup(self): pass

    def cleanup(self): pass

    def file_setup(self): pass

    def file_cleanup(self): pass

    def take(self, typsub):
        self.log.info('===========  Star of Record %s =======' % str(self.Rec_Dict[typsub]))
        for i,j in self.Rec_Dict[typsub].fieldMap:
            self.log.info('< %s >  :   %s ---> %s' % (str(self.Rec_Dict[typsub]), str(i), str(self.data[i])))
          
    def process(self, buf, typsub):
        """
          get_parse_func get the parser functions according to i[1] (the data type)
          and it returns the unpacked value and the remaining buf
          which excluded the data that have already unpacked
          the buf will be checked in the returned parsing function to
          see if it contains less data than expected, in which case a
          warning will be raised.
        """
        self.data = {}
        for i in self.Cur_Rec.fieldMap:
            tmp = i[1]
            self.data[i[0]], buf = self.get_parse_func(tmp)(tmp, buf)

    def _check_Rec_Set(self):
        for i in self.Rec_Set:
            assert i in self.RecName_Dict.keys(), 'Unknown record: %s in Rec_Set' % i

    def parse(self, file_list):
        """
            function parse receives a list of files to be parsed.
            If the files are not in the current working directory,
            the full path to the file should be provided instead of
            simply the file name.
        """
        self.setup()
        for f in file_list:
            self.File_Name = os.path.basename(f)
            
            if f.endswith('gz'): # OK, gzip file, gzip file must ends with 'gz'
                fd = gzip.open(f, 'rb')
            elif f.endswith('bz2'): # OK, bzip2 file, bzip2 file must ends with 'bz2'
                fd = bz2.BZ2File(f, 'rb')
            else: # treated as normal file without compression
                fd = open(f, 'rb')
            self._get_far(fd) # the _get_header function can only be called after
                              # _get_far() been called, from when on the endian type
                              # is set properly.
            self.file_setup() # this function could have set up self.Ignore_File
            if self.Ignore_File == True:
                self.log.info('File %s ignored.' % self.File_Name)
                self.Ignore_File = False
                continue # continue to process next file
            if self.The_End == True:
                self.log.info('Parsing aborted by application.')
                break
            while True:
                # set up break condition
                if self.Return != '':
                    self.log.info("Job aborted: %s" % self.Return)
                    self.Return = '' # reset the self.Return value to empty string.
                    break
                r = self._get_header(fd)
                self.Rec_Cnt += 1
                if r == 'EOF': # No data in file anymore, break
                    break
                else:
                    slen, (typ, sub) = r # buf length and type,sub is returned
                # break condition setup done!
                flag = self.Cur_Rec_Name not in self.Rec_Nset
                # setting Rec_Set made Rec_Nset useless
                if self.Rec_Set == [] and flag:
                    # process all records except those in self.Rec_Nset ...
                    buf = fd.read(slen)
                    assert len(buf) == slen, 'Not enough data read from %s for record %s' % (f, str(self.Rec_Dict[(typ, sub)]))
                    self.process(buf, (typ, sub))
                    # data is a dictionay with field name as its key
                    self.take((typ, sub))
                    # the take method is overwritten by its child to implement specific function
                elif self.Cur_Rec_Name in self.Rec_Set and flag:
                    # only process the records in Rec_Set
                    buf = fd.read(slen)
                    assert len(buf) == slen, 'Not enough data read from %s for record %s' % (f, str(self.Rec_Dict[(typ, sub)]))
                    self.process(buf, (typ, sub))
                    self.take((typ, sub))
                else:
                # simply skip the records by fd.seek(slen, os.SEEK_CUR),
                # which takes less time than fd.read(slen)
                    fd.seek(slen, os.SEEK_CUR)
            fd.close()
            self.file_cleanup()
        self.cleanup()

    def get_parse_func(self, format):
#        if format not in ['U4', 'U1', 'U2', 'C1', 'Cn', 'I1', 'I2', 'I4',
#                          'R4', 'R8', 'B1', 'Bn', 'N1', 'Dn', 'Vn']\
#                          and not format.startswith('K')\
#                          and not (format.startswith('C') and (format[1:].isdigit())):
#            self.log.critical('get_parse_func: unknow format: %s' % format)
#       d = {'U': self._get_Un, 'I': self._get_In,
#            'R': self._get_Rn, 'C': self._get_Cn,
#            'B': self._get_Bn, 'K': self._get_Kx,
#            'N': self._get_Nn, 'D': self._get_Dn,
#            'V': self._get_Vn }
#       tmp = format[0]
#       if d.has_key(tmp):
#           return d[tmp]
#       else:
#           assert False, 'Unkown Format: %s' % format
#           sys.exit(-1)
        if format in ['U4', 'U1', 'U2']:
            return self._get_Un
        elif format in ['I1', 'I2', 'I4']:
            return self._get_In
        elif format in ['R4', 'R8']:
            return self._get_Rn
        elif format == 'Cn' \
        or (format.startswith('C') and (format[1:].isdigit())):
            return self._get_Cn
        elif format in ['B1', 'Bn']:
            return self._get_Bn
        elif format.startswith('K'):
            return self._get_Kx
        elif format == 'N1':
            return self._get_Nn
        elif format == 'Dn':
            return self._get_Dn
        elif format in ['B0', 'Vn']:
            return self._get_Vn
        else:
            assert False, 'Unkown Format: %s' % format
            sys.exit(-1)
    
    def _get_Nn(self, format, buf):
        """ Note: this function process two N1 type every time instead of one
        """
#        self.log.debug('In Get_Nn(): %s' % format)
        r = []
        if format == 'N1':
            if len(buf) < 1:
                return (None, '')
            else:
                tmp = self.unp('B', buf[0])
                r.append(tmp & 0x0F)
                r.append(tmp >> 4)
                return (r, buf[1])
        else:
            self.log.critical('_get_Nn: Error format: %s' % format)
            sys.exit(-1)

    def _get_Un(self, format, buf):
#        self.log.debug('In Get_Un(): %s' % format) 
        if format == 'U4':
            if len(buf) < 4:
                return (None, '')
            else:
                r = self.unp('I', buf[0:4])
                return (r, buf[4:])
        elif format == 'U2':
            if len(buf) < 2:
                return (None, '')
            else:
                r = self.unp('H', buf[0:2])
                return (r, buf[2:])
        elif format == 'U1':
            if len(buf) < 2:
                return (None, '')
            else:
                r = self.unp('B', buf[0:1])
                return (r, buf[1:])
        else:
            self.log.critical('Error format: %s' % format)
            sys.exit(-1)

    def _get_In(self, format, buf):
#        self.log.debug('In Get_In(): %s' % format) 
        if format == 'I4':
            if len(buf) < 4:
                return (None, '')
            else:
                r = self.unp('i', buf[0:4])
                return (r, buf[4:])
        elif format == 'I2':
            if len(buf) < 2:
                return (None, '')
            else:
                r = self.unp('h', buf[0:2])
                return (r, buf[2:])
        elif format == 'I1':
            if len(buf) < 2:
                return (None, '')
            else:
                r = self.unp('b', buf[0:1])
                return (r, buf[1:])
        else:
            self.log.critical('Error format: %s' % format)
            sys.exit(-1)

    def _get_Rn(self, format, buf):
#        self.log.debug('In Get_Rn() %s' % format) 
        if format == 'R4':
            if len(buf) < 4:
                return (None, '')
            else:
                r = self.unp('f', buf[0:4])
                return (r, buf[4:])
        elif format == 'R8':
            if len(buf) < 8:
                return (None, '')
            else:
                r = self.unp('d', buf[0:8])
                return (r, buf[8:])
        else:
            self.log.critical('Error format: %s' % format)
            sys.exit(-1)

    def _get_Cn(self, format, buf):
#        self.log.debug('In Get_Cn(): %s' % format) 
        if format == 'C1':
            if len(buf) < 1:
                return (None, '')
            else:
                r = buf[0]
#                self.log.debug('len(buf): %s' % str(len(buf)))
                return (r, buf[1:])
        elif format == 'Cn':
            if len(buf) < 1:
                return (None, '')
            else:
                char_cnt = self.unp('B', buf[0])
#                self.log.debug('length of buf: %s' % str(len(buf)))
#                self.log.debug('length of byt: %s' % str(char_cnt))
                if len(buf) < (1 + char_cnt):
                    self.log.critical('Cn: Not enough data in buffer: needed: %s, actual: %s' % (str(1+char_cnt), str(len(buf))))
                    #print str(self.Cur_Rec)+' : '+str(self.Rec_Cnt)
                    #for i,j in self.Cur_Rec.fieldMap:
                    #    if self.data.has_key(i):
                    #        print "%s : %s" % (str(i), str(self.data[i]))
                    #return (buf[1:], '')
                    # this return condition is only for Cn, and actually only stdf v3 Etsr(V3) encounters this problem.
                    # the recommended way is to for now, ignore these two records in self.Rec_Nset.
                    # sys.exit(-1)
                    return (buf[1:],buf[len(buf):])
                r = buf[1:(1+char_cnt)]
                return (r, buf[(1+char_cnt):])
        elif (format.startswith('C') and format[1:].isdigit()):
            if len(buf) < 1:
                return (None, '')
            else:
                cnt = int(format[1:])
                r = buf[0:cnt]
                return (r, buf[cnt:])
        else:
            self.log.critical('Error format: %s' % format)
            sys.exit(-1)

    def _get_Bn(self, format, buf):
#        self.log.debug('In Get_Bn(): %s' % format) 
        hexstring = '0123456789ABCDEF'
        if format == 'B1':
            if len(buf) < 1:
                return (None, '')
            else:
                r = self.unp('B', buf[0])
                r = '0x'+hexstring[r>>4]+hexstring[r & 0x0F]
#                self.log.debug('B1: len(buf): %s' % str(len(buf)))
                if len(buf) == 1:
                    return (r, '')
                else:
                    return (r, buf[1:])
        if format == 'Bn':
            if len(buf) < 1:
                return (None, '')
            else:
                char_cnt = self.unp('B', buf[0])
#                self.log.debug('length of buf: %s' % str(len(buf)))
#                self.log.debug('length of byt: %s' % str(char_cnt))
                if len(buf) < (1 + char_cnt):
                    self.log.critical('Bn: Not enough data in buffer: needed: %s, actual: %s' % (str(1+char_cnt), str(len(buf))))
                    sys.exit(-1)
                r = buf[1:(1+char_cnt)]
                tmp = '0x'
                for i in r:
                    v = self.unp('B', i)
                    tmp = tmp+hexstring[v >> 4]+hexstring[v & 0x0F]
                r = tmp
                return (r, buf[(1+char_cnt):])
        else:
            self.log.critical('Error format: %s' % format)
            sys.exit(-1)

    def _get_Dn(self, format, buf):
#        self.log.debug('In Get_Dn(): %s' % format)
        if format == 'Dn':
            if len(buf) < 1:
                return (None, '')
            else:
                dlen = self.unp('H', buf[0:2])
                buf = buf[2:]
                r = []
                dbyt = int(math.ceil(dlen/8.0))
                assert len(buf) >= dbyt
                for i in range(dbyt):
                    tmp = self.unp('B',buf[i])
                    for j in range(8):
                        r.append((tmp>>j) & 0x01)
                return (r, buf[dbyt:])

    def _get_Kx(self, format, buf):
        # first, parse the format to find out in which field of the record defined the length of the array
        assert format.startswith('K'), 'In Get_Kx(): format error: %s' % format
        assert len(format) == 4 or len(format) == 5
        # assume format = 'K3U4' or 'K13U4', then item_format = 'U4'
        item_format = format[-2:]
        # then index_cnt = 3 or 13
        index_cnt = format[1:-2]
        cnt = self.data[self.Cur_Rec.fieldMap[int(index_cnt)][0]]
        r = []
        func = self.get_parse_func(item_format)
        if item_format == 'N1':
            cnt = int(math.ceil(cnt/2.0))
            for i in range(cnt):
                item, buf = func(item_format, buf)
                r.append(item[0])
                r.append(item[1])
            return (r, buf)
        else:
            for i in range(cnt):
                item, buf = func(item_format, buf)
                r.append(item)
            return (r, buf)

    def _get_Vn(self, format, buf):
#        self.log.debug('In Get_Vn(): %s' % format)
        data_type = ['B0', 'U1', 'U2', 'U4', 'I1', 'I2', 'I4',
                     'R4', 'R8', 'Cn', 'Bn', 'Dn', 'N1']
        if len(buf) < 1:
            return (None, '')
        else:
            typ = self.unp('B', buf[0])
            buf = buf[1:]
            func = self.get_parse_func(data_type[typ])
            r, buf = func(data_type[typ], buf)
            return (r, buf)
