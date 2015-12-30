# -*- coding: utf-8 -*-
from ctypes import *

# 统一命名风格
BYTE = c_ubyte
WORD = c_ushort
DWORD = c_ulong
LPBYTE = POINTER(c_ubyte)
LPSTR = c_char_p
LPWSTR = c_wchar_p
HANDLE = c_void_p
PVOID = c_void_p
UINT_PTR = c_ulong

DEBUG_PROCESS = 0x00000001 # 与父进程共用一个控制台(以子进程的方式运行)
CREATE_NEW_CONSOLE = 0x00000010 # 独占一个新控制台(以单独的进程运行)
PROCESS_ALL_ACCESS    = 0x001F0FFF
INFINITE = 0xFFFFFFFF
DBG_CONTINUE = 0x00010002

TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPTHREAD = 0x00000004
TH32CS_SNAPMODULE = 0x00000008
TH32CS_INHERIT = 0x80000000
TH32CS_SNAPALL = (TH32CS_SNAPHEAPLIST | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD | TH32CS_SNAPMODULE)
THREAD_ALL_ACCESS = 0x001F03FF

CONTEXT_FULL = 0x00010007
CONTEXT_DEBUG_REGISTERS = 0x00010010

# 定义 CreateProcessA() 所需的结构体
class STARTUPINFOA(Structure):
    _fields_ = [
        ('cb', DWORD),
        ('lpReserved', LPSTR),
        ('lpDesktop', LPSTR),
        ('lpTitle', LPSTR),
        ('dwX', DWORD),
        ('dwY', DWORD),
        ('dwXSize', DWORD),
        ('dwYSize', DWORD),
        ('dwXCountChars', DWORD),
        ('dwYCountChars', DWORD),
        ('dwFillAttribute', DWORD),
        ('dwFlags', DWORD),
        ('wShowWindow', WORD),
        ('cbReserved2', WORD),
        ('lpReserved2', LPBYTE),
        ('hStdInput', HANDLE),
        ('hStdOutput', HANDLE),
        ('hStdError', HANDLE),
    ]

class PROCESS_INFORMATIONA(Structure):
    _fields_ = [
        ('hProcess', HANDLE),
        ('hThread', HANDLE),
        ('dwProcessId', DWORD),
        ('dwThreadId', DWORD),
    ]

########################################################################

class EXCEPTION_RECORD(Structure):
    pass
EXCEPTION_RECORD._fields_ = [ # 这里之所以要这么设计, 是因为 ExceptionRecord 调用了 EXCEPTION_RECORD, 所以要提前声明
        ('ExceptionCode', DWORD),
        ('ExceptionFlags', DWORD),
        ('ExceptionRecord', POINTER(EXCEPTION_RECORD)),
        ('ExceptionAddress', PVOID),
        ('NumberParameters', DWORD),
        ('ExceptionInformation', UINT_PTR * 15),
    ]

class EXCEPTION_DEBUG_INFO(Structure):
    _fields_ = [
        ('ExceptionRecord', EXCEPTION_RECORD),
        ('dwFirstChance', DWORD),
    ]

class U_DEBUG_EVENT(Union):
    _fields_ = [
        ('Exception',         EXCEPTION_DEBUG_INFO),
#        ('CreateThread',      CREATE_THREAD_DEBUG_INFO),
#        ('CreateProcessInfo', CREATE_PROCESS_DEBUG_INFO),
#        ('ExitThread',        EXIT_THREAD_DEBUG_INFO),
#        ('ExitProcess',       EXIT_PROCESS_DEBUG_INFO),
#        ('LoadDll',           LOAD_DLL_DEBUG_INFO),
#        ('UnloadDll',         UNLOAD_DLL_DEBUG_INFO),
#        ('DebugString',       OUTPUT_DEBUG_STRING_INFO),
#        ('RipInfo',           RIP_INFO),
    ]


class DEBUG_EVENT(Structure):
    _fields_ = [
        ('dwDebugEventCode', DWORD),
        ('dwProcessId', DWORD),
        ('dwThreadId', DWORD),
        ('u', U_DEBUG_EVENT),
    ]

##################################################################

class FLOATING_SAVE_AREA(Structure):
   _fields_ = [
        ('ControlWord', DWORD),
        ('StatusWord', DWORD),
        ('TagWord', DWORD),
        ('ErrorOffset', DWORD),
        ('ErrorSelector', DWORD),
        ('DataOffset', DWORD),
        ('DataSelector', DWORD),
        ('RegisterArea', BYTE * 80),
        ('Cr0NpxState', DWORD),
]

class CONTEXT(Structure):
    _fields_ = [
        ('ContextFlags', DWORD),
        ('Dr0', DWORD),
        ('Dr1', DWORD),
        ('Dr2', DWORD),
        ('Dr3', DWORD),
        ('Dr6', DWORD),
        ('Dr7', DWORD),
        ('FloatSave', FLOATING_SAVE_AREA),
        ('SegGs', DWORD),
        ('SegFs', DWORD),
        ('SegEs', DWORD),
        ('SegDs', DWORD),
        ('Edi', DWORD),
        ('Esi', DWORD),
        ('Ebx', DWORD),
        ('Edx', DWORD),
        ('Ecx', DWORD),
        ('Eax', DWORD),
        ('Ebp', DWORD),
        ('Eip', DWORD),
        ('SegCs', DWORD),
        ('EFlags', DWORD),
        ('Esp', DWORD),
        ('SegSs', DWORD),
        ('ExtendedRegisters', BYTE * 512),
]

class THREADENTRY32(Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('cntUsage', DWORD),
        ('th32ThreadID', DWORD),
        ('th32OwnerProcessID', DWORD),
        ('tpBasePri', DWORD),
        ('tpDeltaPri', DWORD),
        ('dwFlags', DWORD),
    ]

class LUID_AND_ATTRIBUTES(Structure):
    _fields_ = [
        ('Luid', DWORD),
        ('Attributes', DWORD),
    ]

class TOKEN_PRIVILEGES(Structure):
    _fields_ = [
        ('PrivilegeCount', DWORD),
        ('Privileges', LUID_AND_ATTRIBUTES * 512),
    ]
