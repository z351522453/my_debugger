# -*- coding: utf-8 -*-
import my_debugger

debugger = my_debugger.debugger()

debugger.up()

pid = raw_input('Enter the pid: ')

debugger.attach(int(pid))

list_threads = debugger.enumerate_threads()

for thread in list_threads:
    thread_context = debugger.get_thread_context(thread)
    print thread
    print 'eax: 0x%08x' %  thread_context.Eax
    print 'ebx: 0x%08x' %  thread_context.Ebx
    print 'ecx: 0x%08x' %  thread_context.Ecx
    print 'edx: 0x%08x' % thread_context.Edx
    print 'esp: 0x%08x' %  thread_context.Esp

debugger.detach()
