# Guard Checker

**Made with <3 by [Amazing Cow](http://www.amazingcow.com).**


## Guard Checker is DEPRECATED:
We won't develop it furthermore since we're now using ```#pragma once``` instead
of the hand written include guards.  

The project continues to be free and available, but please notice that we 
**WILL NOT** work on it anymore, so no bug fixes, no new features ;D

<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Description:

```guardchecker``` - Verify and enforce the consistency of C/C++ include guards.

```guardchecker``` tries to correct includes guards that doesn't matches the 
following convention:    

* ```__PROJECTNAME_FOLDER1_FOLDER2_FOLDERN_FILENAME_FILEEXT__```  

Where:

* ```PROJECTNAME``` is the desired project name.
* ```FOLDER1...FOLDERN``` is the subfolders of the file in the project tree.
* ```FILENAME``` is the filename of the current file.
* ```FILEEXT``` is the extension of the current file.


So a header file in the following path:
  
* ```AwesomeProject/include/scenes/menu/somefile.h```  

Should have the following include guard:

```cpp
    #ifndef __AwesomeProject_include_scenes_menu_somefile_h__
    #define __AwesomeProject_include_scenes_menu_somefile_h__

    #endif 
```

### DISCLAIMER 

```guardchecker``` **could be a very dangerous program if not used with care.**   
**It WILL MESS with your sources.**    
**While it will make backups is strongly advised that you create a handmade**    
**backup before and pass another custom backup path.**    

**Use it with care and everything should be fine**    

**Again... use the** ```--interactive``` **flag to see the changes before them**    
**happen and/or use the** ```--dry-run``` **to check out if the** ```guardchecker```    
**is doing what you want without doing anything for real.** 

<br>

As usual, you are **very welcomed** to **share** and **hack** it.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Usage:

``` 
  guardchecker [-h | -v]

  guardchecker [-i | -f] [-D]
               [-n <project-name>]
               [-E <ext>]
               [-e <path>]
               [-b <path>]
               <project-root>

Options:
 *-h --help    : Show this screen.
 *-v --version : Show app version and copyright.

  -i --interactive : Runs in interactive mode (Asks before make a change).
  -f --force       : Don't prompt anything... (Overridden by -i).

  -n --project-name : Set the Project Name (First part of include guard).

  -E --ext <ext> : Add the file extension to search  (Must include the dot).

  -b --backup-dir   <path>  : Where the original files will be backup-ed.
  -e --exclude-path <path>  : The path (and all its children) is skipped.

  -D --dry-run : No modifications will actually be made.

Notes:
  If <project-root> is blank the current dir is assumed.

  If --project-name is not set the Project Name is assumed
  as the last part of <project-root>.

  Multiple --ext <ext> can be used.
  Multiple --exclude-path <path> can be used.

  Options marked with * are exclusive, i.e. the guardchecker will run that
  and exit successfully after the operation.
```


<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Install:

Use the Makefile.

``` bash
    make install
```

Or to uninstall

``` bash
    make uninstall
```



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Dependencies:

This project uses / depends on:

* Amazing Cow's 
[cowtermcolor](http://www.github.com/AmazingCow-Libs/cowtermcolor_py)
package to coloring the terminal.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Environment and Files: 

```guardchecker``` do not create / need any other files or environment vars.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## License:

This software is released under GPLv3.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## TODO:

Check the TODO file for general things.

This projects uses the COWTODO tags.   
So install [cowtodo](http://www.github.com/AmazingCow-Tools/COWTODO) and run:

``` bash
$ cd path/for/the/project
$ cowtodo 
```

That's gonna give you all things to do :D.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## BUGS:

We strive to make all our code the most bug-free as possible - But we know 
that few of them can pass without we notice ;).

Please if you find any bug report to [bugs_opensource@amazingcow.com]() 
with the name of this project and/or create an issue here in Github.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Source Files:

* AUTHORS.txt
* CHANGELOG.txt
* COPYING.txt
* guardchecker.py
* Makefile
* OLDREADME.md
* README.md
* TODO.txt



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Others:
Check our repos and take a look at our [open source site](http://opensource.amazingcow.com).
