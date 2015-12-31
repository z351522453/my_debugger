# -*- coding: utf-8 -*-
from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32
advapi32 = windll.advapi32

class debugger():
    def __init__(self):
        self.h_process = None
        self.pid = None
        self.debugger_active = False # 用来控制循环的开关

    def load(self, path_to_exe):
        creation_flags = DEBUG_PROCESS

        startupinfo = STARTUPINFOA()
        process_information = PROCESS_INFORMATIONA()

        startupinfo.cb = sizeof(startupinfo)
        # 下面的设置让新进程在一个单独窗体中被显示
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0

        if kernel32.CreateProcessA(path_to_exe,
                                    None,
                                    None,
                                    None,
                                    None,
                                    creation_flags,
                                    None,
                                    None,
                                    byref(startupinfo),
                                    byref(process_information)):
            print 'We have successfully launched the process!'
            print 'PID: %d' % process_information.dwProcessId

            # 成功, 保存句柄
            self.h_process = self.open_process(process_information.dwProcessId)
        else:
            print 'Error: 0x%08x' % kernel32.GetLastError()

    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process

    def attach(self, pid):
        self.h_process = self.open_process(pid)
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
            #self.run()
        else:
            print 'Unable to attach to the process.'

    def run(self):
        while self.debugger_active == True:
            self.get_debug_event()

    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            raw_input('press a key to continue ...')
            self.debugger_active = False
            kernel32.ContinueDebugEvent(debug_event.dwProcessId,
                                        debug_event.dwThreadId,
                                        continue_status)

    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print 'Finished debugging. Exiting ...'
            return True
        else:
            print 'There was an error'
            return False

    def open_thread(self, tid):
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, tid)
        if h_thread is not None:
            return h_thread
        else:
            print 'Could not obtain a valid thread handle.'
            return False

    def enumerate_threads(self):
        thread_entry = THREADENTRY32()
        thread_list = []
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)

        if snapshot is not None:
            thread_entry.dwSize = sizeof(thread_entry)
            success = kernel32.Thread32First(snapshot, byref(thread_entry))

            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))

            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            return False

    def get_thread_context(self, thread_id = None, h_thread = None):
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

        h_thread = self.open_thread(thread_id)
        if kernel32.GetThreadContext(h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        else:
            return False

    def privilege(self):
        # token_handle = win32security.OpenProcessToken(kernel32.GetCurrentProcess(), win32con.TOKEN_ALL_ACCESS) != 0
        # if token_handle == 0:
        #     print '提取令牌失败'
        # else:
        #     Luid = win32security.LookupPrivilegeValue(None, win32security.SE_DEBUG_NAME)
        #     if Luid == 0:
        #         print 'Luid获取失败'
        #     else:
        #         new_token_pricileges = (Luid, win32security.SE_PRIVILEGE_ENABLED)
        #         i = win32security.AdjustTokenPrivileges(token_handle, 0, new_token_pricileges)
        #         if i == 0:
        #             print '提权失败'
        # win32api.CloseHandle(token_handle)

        h_token = HANDLE()
        TOKEN_ALL_ACCESS = 0x000F01FF
        SE_PRIVILEGE_ENABLED = 0x00000002

        if kernel32.OpenProcessToken(kernel32.GetCurrentProcess(), TOKEN_ALL_ACCESS, byref(h_token)) != True:
            print '提权失败 -- OpenProcessToken'
            return False

        tp = TOKEN_PRIVILEGES()
        luid = DWORD()

        if advapi32.LookupPrivilegeValueA(None, 'SeDebugPrivilege', byref(luid)) != True:
            print '提权失败 -- LookupPrivilegeValueA'
            return False

        tp.PrivilegeCount = 1
        tp.Privileges[0].Luid = luid
        tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED

        if advapi32.AdjustTokenPrivileges(h_token, False, byref(tp), sizeof(tp), None, None) != True:
            print '提权失败 -- AdjustTokenPrivileges'
            return False

        kernel32.CloseHandle(h_token)

        print '提权成功'
        return True
