===================================
Welcome to pymixup's documentation!
===================================
*pymixup* is a Python project obfuscator. It takes Python code that looks like this::

   def mk_formatted_array_string(number_array, decimal='.', separator=',',
                                 is_sort_array=False,
                                 is_strip_unused_decimals=False,
                                 joiner='   '):
       """Format an array of numbers into a string of formatted numbers.

       Parameters
       ----------
       decimal : str
       is_sort_array : bool
       is_strip_unused_decimals : bool
       joiner : str
       number_array : np.array
       separator : str
       """
       try:
           if is_sort_array:
               number_array_ = np.sort(number_array)
           else:
               number_array_ = number_array
           formatted_string = joiner.join([
               mk_formatted_number(
                   number, is_strip_unused_decimals=is_strip_unused_decimals)
               for number in number_array_
           ])
       except ValueError:
           raise
       if decimal != '.' or separator != ',':
           formatted_string = formatted_string.replace(',', '~'). \
               replace('.', decimal).replace('~', separator)
       return formatted_string

and turns it into this::

   def raiug(enihb,xskrm='.',oqkio=',',fmzcc=False,jkego=False,aidon='   '):
       try:
           if fmzcc:
               voxaq=np.sort(enihb)
           else:
               voxaq=enihb
           zexay=aidon.join([gkmiw(number,jkego=jkego)for number in voxaq])
       except ValueError:
           raise
       if xskrm!='.'or oqkio!=',':
           zexay=zexay.replace(',','~').replace('.',xskrm).replace('~',oqkio)
   return zexay

Why Obfuscate?
==============
Python is a great interpreted language. Its syntax allows us to write elegant easy-to-read code.

But sometimes you may not want your code to easy to understand. For example, if you are charging for an app that is installed on a mobile phone, then you do not want competitors to copy your code and resell your app at a lower cost. Even if you distribute just the compiled .pyc byte code, it can be decompiled and made readable.

In this case, it's sensible to make the program as hard as possible for someone else to copy and edit. That's the work of obfuscation.

Because of its interpreted nature, there are limits to how much a Python program can be obfuscated, since the program must still be understood by the interpreter. For example, Python keywords like "if" and "class" cannot be changed, or Python won't be able to understand them. However, variables and method names you create can be changed--as long as the changes are duplicated throughout the source files.

That's what *pymixup* does. It obfuscates non-reserved words (e.g., words that are not keywords) into garbled words of random characters to make the program harder to understand and follow.

**CAVEAT**: The obfuscated code can be reverse engineered by deciphering what an obfuscated variable or method does and renaming the garbled term to a meaningful one. That's a potentially labor-intensive process that hopefully discourages those who want to steal your code from attempting it.

What *pymixup* Does
===================
*pymixup* will read **all** the Python files in a project and obfuscate the file contents, the file names, and the folder names based on rules you specify in the setup lists. **All** is emphasized because *pymixup* works with projects--it's not restricted to single source files. So obfuscated packages can use other obfuscated packages, since the obfuscated names will be shared between them.

In addition, for the cross-platform program Kivy, *pymixup* will also obfuscate the corresponding .kv files.

Other files types may be added in the future; for example, Django .html template files. Pull requests are welcome.


Installation
============
See `Installation <docs/install.rst>`_ for instructions to install *pymixup*.

Setup
=====
See `Setup <docs/setup.rst>`_ for instruction on how to set up for an obfuscated project .

Documentation
=============
Visit the `documentation <http://pymixup.readthedocs.org>`_ for more information.