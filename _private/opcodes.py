#     ____            ________              
#    / __ )____ _____/ / ____/___ _________
#   / __  / __ `/ __  / /   / __ `/ ___/ _ \
#  / /_/ / /_/ / /_/ / /___/ /_/ (__  )  __/
# /_____/\__,_/\__,_/\____/\__,_/____/\___/
#

import re

from enum import Enum as enum

class ReferenceType(enum):
    def __init__(self, idx, ref_extractor):
        self.idx = idx
        self.extractor = ref_extractor

    @staticmethod
    def _string_extractor(smali, dxcode):
        if dxcode.ref_type != ReferenceType.STRING:
            raise ValueError("invalid smali passed to ReferenceType._string_extractor: %s" % smali)

        return smali[smali.find('"') + 1 : smali.rfind('"')]

    @staticmethod
    def _type_extractor(smali, dxcode):
        if dxcode.ref_type != ReferenceType.TYPE:
            raise ValueError("invalid smali passed to ReferenceType._type_extractor: %s" % smali)

        match = re.match("^(?!.*->).*(L.*;)$", smali)

        return match[1]


    @staticmethod
    def _field_extractor(smali, dxcode):
        if dxcode.ref_type != ReferenceType.FIELD:
            raise ValueError("invalid smali passed to ReferenceType._FIELD_extractor: %s" % smali)
        
        return re.match("L.*;?$", smali)[0]

    @staticmethod
    def _method_extractor(smali, dxcode):
        if dxcode.ref_type != ReferenceType.METHOD:
            raise ValueError("invalid smali passed to ReferenceType._method_extractor: %s" % smali)
        
        return re.match("L.*;?$", smali)[0]

    @staticmethod
    def _none_extractor(smali, dxcode):
        pass # there is nothing to extract here.

    STRING = (0, _string_extractor)
    TYPE = (1, _type_extractor)
    FIELD = (2, _field_extractor)
    METHOD = (3, _method_extractor)
    NONE = (4, _none_extractor)

class DexOpcodes(enum):
    NOP = (0x00, "nop", ReferenceType.NONE)
    MOVE = (0x01, "move", ReferenceType.NONE)
    MOVE_FROM16 = (0x02, "move/from16", ReferenceType.NONE)
    MOVE_16 = (0x03, "move/16", ReferenceType.NONE)
    MOVE_WIDE = (0x04, "move-wide", ReferenceType.NONE)
    MOVE_WIDE_FROM16 = (0x05, "move-wide/from16", ReferenceType.NONE)
    MOVE_WIDE_16 = (0x06, "move-wide/16", ReferenceType.NONE)
    MOVE_OBJECT = (0x07, "move-object", ReferenceType.NONE)
    MOVE_OBJECT_FROM16 = (0x08, "move-object/from16", ReferenceType.NONE)
    MOVE_OBJECT_16 = (0x09, "move-object/16", ReferenceType.NONE)
    MOVE_RESULT = (0x0a, "move-result", ReferenceType.NONE)
    MOVE_RESULT_WIDE = (0x0b, "move-result-wide", ReferenceType.NONE)
    MOVE_RESULT_OBJECT = (0x0c, "move-result-object", ReferenceType.NONE)
    MOVE_EXCEPTION = (0x0d, "move-exception", ReferenceType.NONE)
    RETURN_VOID = (0x0e, "return-void", ReferenceType.NONE)
    RETURN = (0x0f, "return", ReferenceType.NONE)
    RETURN_WIDE = (0x10, "return-wide", ReferenceType.NONE)
    RETURN_OBJECT = (0x11, "return-object", ReferenceType.NONE)
    CONST_4 = (0x12, "const/4", ReferenceType.NONE)
    CONST_16 = (0x13, "const/16", ReferenceType.NONE)
    CONST = (0x14, "const", ReferenceType.NONE)
    CONST_HIGH16 = (0x15, "const/high16", ReferenceType.NONE)
    CONST_WIDE_16 = (0x16, "const-wide/16", ReferenceType.NONE)
    CONST_WIDE_32 = (0x17, "const-wide/32", ReferenceType.NONE)
    CONST_WIDE = (0x18, "const-wide", ReferenceType.NONE)
    CONST_WIDE_HIGH16 = (0x19, "const-wide/high16", ReferenceType.NONE)
    CONST_STRING = (0x1a, "const-string", ReferenceType.STRING)
    CONST_STRING_JUMBO = (0x1b, "const-string/jumbo", ReferenceType.STRING)
    CONST_CLASS = (0x1c, "const-class", ReferenceType.TYPE)
    MONITOR_ENTER = (0x1d, "monitor-enter", ReferenceType.NONE)
    MONITOR_EXIT = (0x1e, "monitor-exit", ReferenceType.NONE)
    CHECK_CAST = (0x1f, "check-cast", ReferenceType.TYPE)
    INSTANCE_OF = (0x20, "instance-of", ReferenceType.TYPE)
    ARRAY_LENGTH = (0x21, "array-length", ReferenceType.NONE)
    NEW_INSTANCE = (0x22, "new-instance", ReferenceType.TYPE)
    NEW_ARRAY = (0x23, "new-array", ReferenceType.TYPE)
    FILLED_NEW_ARRAY = (0x24, "filled-new-array", ReferenceType.TYPE)
    FILLED_NEW_ARRAY_RANGE = (0x25, "filled-new-array/range", ReferenceType.TYPE)
    FILL_ARRAY_DATA = (0x26, "fill-array-data", ReferenceType.NONE)
    THROW = (0x27, "throw", ReferenceType.NONE)
    GOTO = (0x28, "goto", ReferenceType.NONE)
    GOTO_16 = (0x29, "goto/16", ReferenceType.NONE)
    GOTO_32 = (0x2a, "goto/32", ReferenceType.NONE)
    PACKED_SWITCH = (0x2b, "packed-switch", ReferenceType.NONE)
    SPARSE_SWITCH = (0x2c, "sparse-switch", ReferenceType.NONE)
    CMPL_FLOAT = (0x2d, "cmpl-float", ReferenceType.NONE)
    CMPG_FLOAT = (0x2e, "cmpg-float", ReferenceType.NONE)
    CMPL_DOUBLE = (0x2f, "cmpl-double", ReferenceType.NONE)
    CMPG_DOUBLE = (0x30, "cmpg-double", ReferenceType.NONE)
    CMP_LONG = (0x31, "cmp-long", ReferenceType.NONE)
    IF_EQ = (0x32, "if-eq", ReferenceType.NONE)
    IF_NE = (0x33, "if-ne", ReferenceType.NONE)
    IF_LT = (0x34, "if-lt", ReferenceType.NONE)
    IF_GE = (0x35, "if-ge", ReferenceType.NONE)
    IF_GT = (0x36, "if-gt", ReferenceType.NONE)
    IF_LE = (0x37, "if-le", ReferenceType.NONE)
    IF_EQZ = (0x38, "if-eqz", ReferenceType.NONE)
    IF_NEZ = (0x39, "if-nez", ReferenceType.NONE)
    IF_LTZ = (0x3a, "if-ltz", ReferenceType.NONE)
    IF_GEZ = (0x3b, "if-gez", ReferenceType.NONE)
    IF_GTZ = (0x3c, "if-gtz", ReferenceType.NONE)
    IF_LEZ = (0x3d, "if-lez", ReferenceType.NONE)
    AGET = (0x44, "aget", ReferenceType.NONE)
    AGET_WIDE = (0x45, "aget-wide", ReferenceType.NONE)
    AGET_OBJECT = (0x46, "aget-object", ReferenceType.NONE)
    AGET_BOOLEAN = (0x47, "aget-boolean", ReferenceType.NONE)
    AGET_BYTE = (0x48, "aget-byte", ReferenceType.NONE)
    AGET_CHAR = (0x49, "aget-char", ReferenceType.NONE)
    AGET_SHORT = (0x4a, "aget-short", ReferenceType.NONE)
    APUT = (0x4b, "aput", ReferenceType.NONE)
    APUT_WIDE = (0x4c, "aput-wide", ReferenceType.NONE)
    APUT_OBJECT = (0x4d, "aput-object", ReferenceType.NONE)
    APUT_BOOLEAN = (0x4e, "aput-boolean", ReferenceType.NONE)
    APUT_BYTE = (0x4f, "aput-byte", ReferenceType.NONE)
    APUT_CHAR = (0x50, "aput-char", ReferenceType.NONE)
    APUT_SHORT = (0x51, "aput-short", ReferenceType.NONE)
    IGET = (0x52, "iget", ReferenceType.FIELD)
    IGET_WIDE = (0x53, "iget-wide", ReferenceType.FIELD)
    IGET_OBJECT = (0x54, "iget-object", ReferenceType.FIELD)
    IGET_BOOLEAN = (0x55, "iget-boolean", ReferenceType.FIELD)
    IGET_BYTE = (0x56, "iget-byte", ReferenceType.FIELD)
    IGET_CHAR = (0x57, "iget-char", ReferenceType.FIELD)
    IGET_SHORT = (0x58, "iget-short", ReferenceType.FIELD)
    IPUT = (0x59, "iput", ReferenceType.FIELD)
    IPUT_WIDE = (0x5a, "iput-wide", ReferenceType.FIELD)
    IPUT_OBJECT = (0x5b, "iput-object", ReferenceType.FIELD)
    IPUT_BOOLEAN = (0x5c, "iput-boolean", ReferenceType.FIELD)
    IPUT_BYTE = (0x5d, "iput-byte", ReferenceType.FIELD)
    IPUT_CHAR = (0x5e, "iput-char", ReferenceType.FIELD)
    IPUT_SHORT = (0x5f, "iput-short", ReferenceType.FIELD)
    SGET = (0x60, "sget", ReferenceType.FIELD)
    SGET_WIDE = (0x61, "sget-wide", ReferenceType.FIELD)
    SGET_OBJECT = (0x62, "sget-object", ReferenceType.FIELD)
    SGET_BOOLEAN = (0x63, "sget-boolean", ReferenceType.FIELD)
    SGET_BYTE = (0x64, "sget-byte", ReferenceType.FIELD)
    SGET_CHAR = (0x65, "sget-char", ReferenceType.FIELD)
    SGET_SHORT = (0x66, "sget-short", ReferenceType.FIELD)
    SPUT = (0x67, "sput", ReferenceType.FIELD)
    SPUT_WIDE = (0x68, "sput-wide", ReferenceType.FIELD)
    SPUT_OBJECT = (0x69, "sput-object", ReferenceType.FIELD)
    SPUT_BOOLEAN = (0x6a, "sput-boolean", ReferenceType.FIELD)
    SPUT_BYTE = (0x6b, "sput-byte", ReferenceType.FIELD)
    SPUT_CHAR = (0x6c, "sput-char", ReferenceType.FIELD)
    SPUT_SHORT = (0x6d, "sput-short", ReferenceType.FIELD)
    INVOKE_VIRTUAL = (0x6e, "invoke-virtual", ReferenceType.METHOD)
    INVOKE_SUPER = (0x6f, "invoke-super", ReferenceType.METHOD)
    INVOKE_DIRECT = (0x70, "invoke-direct", ReferenceType.METHOD)
    INVOKE_STATIC = (0x71, "invoke-static", ReferenceType.METHOD)
    INVOKE_INTERFACE = (0x72, "invoke-interface", ReferenceType.METHOD)
    INVOKE_VIRTUAL_RANGE = (0x74, "invoke-virtual/range", ReferenceType.METHOD)
    INVOKE_SUPER_RANGE = (0x75, "invoke-super/range", ReferenceType.METHOD)
    INVOKE_DIRECT_RANGE = (0x76, "invoke-direct/range", ReferenceType.METHOD)
    INVOKE_STATIC_RANGE = (0x77, "invoke-static/range", ReferenceType.METHOD)
    INVOKE_INTERFACE_RANGE = (0x78, "invoke-interface/range", ReferenceType.METHOD)
    NEG_INT = (0x7b, "neg-int", ReferenceType.NONE)
    NOT_INT = (0x7c, "not-int", ReferenceType.NONE)
    NEG_LONG = (0x7d, "neg-long", ReferenceType.NONE)
    NOT_LONG = (0x7e, "not-long", ReferenceType.NONE)
    NEG_FLOAT = (0x7f, "neg-float", ReferenceType.NONE)
    NEG_DOUBLE = (0x80, "neg-double", ReferenceType.NONE)
    INT_TO_LONG = (0x81, "int-to-long", ReferenceType.NONE)
    INT_TO_FLOAT = (0x82, "int-to-float", ReferenceType.NONE)
    INT_TO_DOUBLE = (0x83, "int-to-double", ReferenceType.NONE)
    LONG_TO_INT = (0x84, "long-to-int", ReferenceType.NONE)
    LONG_TO_FLOAT = (0x85, "long-to-float", ReferenceType.NONE)
    LONG_TO_DOUBLE = (0x86, "long-to-double", ReferenceType.NONE)
    FLOAT_TO_INT = (0x87, "float-to-int", ReferenceType.NONE)
    FLOAT_TO_LONG = (0x88, "float-to-long", ReferenceType.NONE)
    FLOAT_TO_DOUBLE = (0x89, "float-to-double", ReferenceType.NONE)
    DOUBLE_TO_INT = (0x8a, "double-to-int", ReferenceType.NONE)
    DOUBLE_TO_LONG = (0x8b, "double-to-long", ReferenceType.NONE)
    DOUBLE_TO_FLOAT = (0x8c, "double-to-float", ReferenceType.NONE)
    INT_TO_BYTE = (0x8d, "int-to-byte", ReferenceType.NONE)
    INT_TO_CHAR = (0x8e, "int-to-char", ReferenceType.NONE)
    INT_TO_SHORT = (0x8f, "int-to-short", ReferenceType.NONE)
    ADD_INT = (0x90, "add-int", ReferenceType.NONE)
    SUB_INT = (0x91, "sub-int", ReferenceType.NONE)
    MUL_INT = (0x92, "mul-int", ReferenceType.NONE)
    DIV_INT = (0x93, "div-int", ReferenceType.NONE)
    REM_INT = (0x94, "rem-int", ReferenceType.NONE)
    AND_INT = (0x95, "and-int", ReferenceType.NONE)
    OR_INT = (0x96, "or-int", ReferenceType.NONE)
    XOR_INT = (0x97, "xor-int", ReferenceType.NONE)
    SHL_INT = (0x98, "shl-int", ReferenceType.NONE)
    SHR_INT = (0x99, "shr-int", ReferenceType.NONE)
    USHR_INT = (0x9a, "ushr-int", ReferenceType.NONE)
    ADD_LONG = (0x9b, "add-long", ReferenceType.NONE)
    SUB_LONG = (0x9c, "sub-long", ReferenceType.NONE)
    MUL_LONG = (0x9d, "mul-long", ReferenceType.NONE)
    DIV_LONG = (0x9e, "div-long", ReferenceType.NONE)
    REM_LONG = (0x9f, "rem-long", ReferenceType.NONE)
    AND_LONG = (0xa0, "and-long", ReferenceType.NONE)
    OR_LONG = (0xa1, "or-long", ReferenceType.NONE)
    XOR_LONG = (0xa2, "xor-long", ReferenceType.NONE)
    SHL_LONG = (0xa3, "shl-long", ReferenceType.NONE)
    SHR_LONG = (0xa4, "shr-long", ReferenceType.NONE)
    USHR_LONG = (0xa5, "ushr-long", ReferenceType.NONE)
    ADD_FLOAT = (0xa6, "add-float", ReferenceType.NONE)
    SUB_FLOAT = (0xa7, "sub-float", ReferenceType.NONE)
    MUL_FLOAT = (0xa8, "mul-float", ReferenceType.NONE)
    DIV_FLOAT = (0xa9, "div-float", ReferenceType.NONE)
    REM_FLOAT = (0xaa, "rem-float", ReferenceType.NONE)
    ADD_DOUBLE = (0xab, "add-double", ReferenceType.NONE)
    SUB_DOUBLE = (0xac, "sub-double", ReferenceType.NONE)
    MUL_DOUBLE = (0xad, "mul-double", ReferenceType.NONE)
    DIV_DOUBLE = (0xae, "div-double", ReferenceType.NONE)
    REM_DOUBLE = (0xaf, "rem-double", ReferenceType.NONE)
    ADD_INT_2ADDR = (0xb0, "add-int/2addr", ReferenceType.NONE)
    SUB_INT_2ADDR = (0xb1, "sub-int/2addr", ReferenceType.NONE)
    MUL_INT_2ADDR = (0xb2, "mul-int/2addr", ReferenceType.NONE)
    DIV_INT_2ADDR = (0xb3, "div-int/2addr", ReferenceType.NONE)
    REM_INT_2ADDR = (0xb4, "rem-int/2addr", ReferenceType.NONE)
    AND_INT_2ADDR = (0xb5, "and-int/2addr", ReferenceType.NONE)
    OR_INT_2ADDR = (0xb6, "or-int/2addr", ReferenceType.NONE)
    XOR_INT_2ADDR = (0xb7, "xor-int/2addr", ReferenceType.NONE)
    SHL_INT_2ADDR = (0xb8, "shl-int/2addr", ReferenceType.NONE)
    SHR_INT_2ADDR = (0xb9, "shr-int/2addr", ReferenceType.NONE)
    USHR_INT_2ADDR = (0xba, "ushr-int/2addr", ReferenceType.NONE)
    ADD_LONG_2ADDR = (0xbb, "add-long/2addr", ReferenceType.NONE)
    SUB_LONG_2ADDR = (0xbc, "sub-long/2addr", ReferenceType.NONE)
    MUL_LONG_2ADDR = (0xbd, "mul-long/2addr", ReferenceType.NONE)
    DIV_LONG_2ADDR = (0xbe, "div-long/2addr", ReferenceType.NONE)
    REM_LONG_2ADDR = (0xbf, "rem-long/2addr", ReferenceType.NONE)
    AND_LONG_2ADDR = (0xc0, "and-long/2addr", ReferenceType.NONE)
    OR_LONG_2ADDR = (0xc1, "or-long/2addr", ReferenceType.NONE)
    XOR_LONG_2ADDR = (0xc2, "xor-long/2addr", ReferenceType.NONE)
    SHL_LONG_2ADDR = (0xc3, "shl-long/2addr", ReferenceType.NONE)
    SHR_LONG_2ADDR = (0xc4, "shr-long/2addr", ReferenceType.NONE)
    USHR_LONG_2ADDR = (0xc5, "ushr-long/2addr", ReferenceType.NONE)
    ADD_FLOAT_2ADDR = (0xc6, "add-float/2addr", ReferenceType.NONE)
    SUB_FLOAT_2ADDR = (0xc7, "sub-float/2addr", ReferenceType.NONE)
    MUL_FLOAT_2ADDR = (0xc8, "mul-float/2addr", ReferenceType.NONE)
    DIV_FLOAT_2ADDR = (0xc9, "div-float/2addr", ReferenceType.NONE)
    REM_FLOAT_2ADDR = (0xca, "rem-float/2addr", ReferenceType.NONE)
    ADD_DOUBLE_2ADDR = (0xcb, "add-double/2addr", ReferenceType.NONE)
    SUB_DOUBLE_2ADDR = (0xcc, "sub-double/2addr", ReferenceType.NONE)
    MUL_DOUBLE_2ADDR = (0xcd, "mul-double/2addr", ReferenceType.NONE)
    DIV_DOUBLE_2ADDR = (0xce, "div-double/2addr", ReferenceType.NONE)
    REM_DOUBLE_2ADDR = (0xcf, "rem-double/2addr", ReferenceType.NONE)
    ADD_INT_LIT16 = (0xd0, "add-int/lit16", ReferenceType.NONE)
    RSUB_INT = (0xd1, "rsub-int", ReferenceType.NONE)
    MUL_INT_LIT16 = (0xd2, "mul-int/lit16", ReferenceType.NONE)
    DIV_INT_LIT16 = (0xd3, "div-int/lit16", ReferenceType.NONE)
    REM_INT_LIT16 = (0xd4, "rem-int/lit16", ReferenceType.NONE)
    AND_INT_LIT16 = (0xd5, "and-int/lit16", ReferenceType.NONE)
    OR_INT_LIT16 = (0xd6, "or-int/lit16", ReferenceType.NONE)
    XOR_INT_LIT16 = (0xd7, "xor-int/lit16", ReferenceType.NONE)
    ADD_INT_LIT8 = (0xd8, "add-int/lit8", ReferenceType.NONE)
    RSUB_INT_LIT8 = (0xd9, "rsub-int/lit8", ReferenceType.NONE)
    MUL_INT_LIT8 = (0xda, "mul-int/lit8", ReferenceType.NONE)
    DIV_INT_LIT8 = (0xdb, "div-int/lit8", ReferenceType.NONE)
    REM_INT_LIT8 = (0xdc, "rem-int/lit8", ReferenceType.NONE)
    AND_INT_LIT8 = (0xdd, "and-int/lit8", ReferenceType.NONE)
    OR_INT_LIT8 = (0xde, "or-int/lit8", ReferenceType.NONE)
    XOR_INT_LIT8 = (0xdf, "xor-int/lit8", ReferenceType.NONE)
    SHL_INT_LIT8 = (0xe0, "shl-int/lit8", ReferenceType.NONE)
    SHR_INT_LIT8 = (0xe1, "shr-int/lit8", ReferenceType.NONE)
    USHR_INT_LIT8 = (0xe2, "ushr-int/lit8", ReferenceType.NONE)

    def __init__(self, opcode, instruction, ref):
        self.opcode = opcode,
        self.instruction = instruction
        self.ref_type = ref

    @staticmethod
    def of_reftype(ref):
        def generator():
            for dxcode in DexOpcodes:
                if dxcode.ref_type == ref:
                    yield dxcode

        return list(generator())

    @staticmethod
    def get_opcode(instruction):
        for dxcode in DexOpcodes:
            if dxcode.instruction == instruction:
                return dxcode.opcode

        return -1

    @staticmethod
    def get_instruction(opcode):
        for dxcode in DexOpcodes:
            if dxcode.opcode == opcode:
                return dxcode.instruction

        return None

    @staticmethod
    def dxcode_from_inst(instruction):
        for dxcode in DexOpcodes:
            if dxcode.instruction == instruction:
                return dxcode

        return None

    @staticmethod
    def dxcode_from_op(opcode):
        for dxcode in DexOpcodes:
            if dxcode.opcode == opcode:
                return dxcode

        return None