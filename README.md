cpp-guard-checker
====
Made with <3 by [Amazing Cow](http://www.amazingcow.com).

## Intro:
**Check and correct the include guards in our C++ files. **
 
Basically our includes guards are formated in the way of:
    
```__PROJECTNAME_FOLDER1_FOLDER2_FOLDERN_FILENAME_FILEEXT__```   

Where FOLDER1...FOLDERN are the dir structure that the file is placed.   
So for example one include guard of the file:  
```AwesomeProject/include/scenes/menu/somefile.h```  

Should have the following include guard:

```cpp
#ifndef __AwesomeProject_include_scenes_menu_somefile_h__
#define __AwesomeProject_include_scenes_menu_somefile_h__
...
#endif 
```

This program fix the guards that doesn't follow this convention.

Since we made this to fit our needs, it's probably doesn't fits
what you expects/needs, but you're **very welcomed** to **hack it** 
to better fit your needs :)

## Install:

```$ sudo cp -f path/to/cpp-guard-checker.py /usr/local/bin/cpp-guard-checker```

or use the makefile

```$ make install ```

## Usage:

```
cpp-guard-checker [-hv] [-i] [-n <project_name>] [--dry-run]
                    [--ext <ext>] [--backup-dir <path>] <project_root>

Options:
 *-h --help              : Show this screen.
 *-v --version           : Show app version and copyright.
  -i --interactive       : Runs in interactive mode (Asks before make a change).
  -n --project-name      : Set the Project Name (First part of include guard).
     --ext        <ext>  : Add the file extension to search. (Must include the dot)
     --backup-dir <path> : Where the original files will be backup-ed.
     --dry-run           : No modifications will actually be made.
```

##### Notes:
If ```<project_root>``` is blank the current dir is assumed.  
If ```--project-name``` is not set the Project Name is assumed as last part of ```<project_root>```   
Multiple ```--ext <ext>``` can be used.

Options marked with * are exclusive, i.e. ```the cpp-guard-checker``` will run that
and exit successfully after the operation.

## Warning
***THIS IS A VERY, VERY DANGEROUS PROGRAM. IT WILL MESS WITH YOUR SOURCES.  
    THE PROGRAM WILL MAKE A BACKUP AT (```/tmp/cppguardchecker```) BUT IS STRONGLY ADVISED  
    THAT YOU CREATE A HANDMADE BACKUP BEFORE AND PASS ANOTHER CUSTOM BACKUP PATH.  
    CURRENTLY IT IS VERY DUMB TO SEEK THE INCLUDE GUARDS, SO IS VERY WISE  
    TO RUN IT IN A INTERACTIVE MODE (```-i | --interactive```) TO CHECK THE CHANGES  
    BEFORE THEM HAPPEN.  
    RUN THIS AT YOUR OWN RISK, WORKS PRETTY WELL IF USED WITH CARE.  
    ENJOY...***

## License:
This software is released under GPLv3.

## TODO:
Check the TODO file.

## Others:
Check our repos and take a look at our [open source site](http://opensource.amazingcow.com).
