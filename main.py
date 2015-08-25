#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █                                                  ##
##             ████████████         cowtodo.py - COWTODO                      ##
##           █              █       Copyright (c) 2015 AmazingCow             ##
##          █     █    █     █      www.AmazingCow.com                        ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgmentopensource@AmazingCow.com               ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must notbe misrepresented as being the original software.       ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

## Imports ##
import os;
import os.path;
import re;
import termcolor;
import sys;
import getopt;

################################################################################
## Globals                                                                    ##
################################################################################
class Globals:
    file_exts   = [];
    backup_path = "";
    start_path  = "";

    opt_backup      = False;
    opt_interactive = False;

################################################################################
## Constants                                                                  ##
################################################################################
class Constants:
    FLAG_HELP        = "h", "help";
    FLAG_VERSION     = "v", "version";
    FLAG_EXT         = "e", "ext";
    FLAG_BACKUP      = "b", "backup";
    FLAG_BACKUP_PATH = "o", "backup-path";
    FLAG_INTERACTIVE = "i", "interactive";

    ALL_FLAGS_SHORT = "hve:bo:i";
    ALL_FLAGS_LONG  = ["help", "version", "ext=",
                       "backup", "backup-path", "interactive"];

    BACKUP_PATH_DEFAULT = "./backup";
    BACKUP_PATH_TEMP    = "/tmp/cppguardchecker";

    EXT_HEADER_DEFAULT  = ".h";
    START_PATH_DEFAULT  = "./";

################################################################################
## Color Functions                                                            ##
################################################################################
def issue_color(msg):
    return termcolor.colored(msg, "red");
def correct_color(msg):
    return termcolor.colored(msg, "green");
def filename_color(msg):
    return termcolor.colored(msg, "blue");

################################################################################
## Helper Functions                                                           ##
################################################################################
def print_help():
    print "Help";
def print_version():
    print "version";
def print_run_options():
    print "Run Options";
    print "Backup      :", Globals.opt_backup;
    print "Interactive :", Globals.opt_interactive;
    print "Backup path :", Globals.backup_path;
    print "File exts   :",  " ".join(Globals.file_exts);

def build_correct_guard(fullpath):
    return "__" + "_".join(fullpath.split("/")).replace(".","_") + "__";

def should_correct_guard_prompt():
    r = raw_input("Correct the guard? [Y/n]:");
    if(len(r) != 0 and r.lower() == "n"):
        return False;
    return True;

def system_cmd(cmd):
    ret = os.system(cmd);
    if(ret != 0):
        print issue_color("[ERROR]"), "cmd:", cmd;
        exit(1);

################################################################################
## Guard Related Functions                                                    ##
################################################################################
def fix_guard(fullpath, incorrect, correct):
    #Split the dir path and file path. Next create the "same" fullpath
    #but inside the backup dir. So the path structure is preserved but
    #inside the backup dir.
    folderpath, filepath = os.path.splitext(fullpath);
    backuppath = os.path.join(Globals.backup_dir,folderpath);

    #Make the backup dir.
    cmd_mkdir = "mkdir -p {}".format(backuppath);
    os.system(cmd_mkdir);

    #Copy the original file to backup folder.
    cmd_cp = "cp {} {}".format(fullpath, backuppath);
    system_cmd(cmd_cp);

    #Run sed.
    tempfilepath = fullpath + ".temp";
    cmd_sed = "sed s/{}/{}/g {} > {}".format(incorrect,
                                             correct,
                                             fullpath,
                                             tempfilepath);
    system_cmd(cmd_sed);

    #Move the temp file over the original file.
    cmd_mv = "mv {} {}".format(tempfilepath, fullpath);
    system_cmd(cmd_mv);

def check_file(root, filename):
    #Build the fullpath of the file and the correct guard based on it.
    fullpath       = os.path.join(root, filename);
    correct_guard  = build_correct_guard(fullpath);


    lines = open(fullpath).readlines();
    for line in lines:
        search_str = "^{}.*".format("#ifndef");

        #Check if we have a include guard.
        if(re.search(search_str, line) is not None):
            #Clear the line.
            line = line.replace("\n", "");
            line = line.replace("#ifndef", "").lstrip(" ");

            #Check if we have a correct guard.
            if(line != correct_guard):
                #Show to user that the guard is incorrect.
                print "File:    {}".format(filename_color(fullpath));
                print "Found:   {}".format(issue_color(line));
                print "Correct: {}".format(correct_color(correct_guard));

                #Fix the guard if running in non interactive mode.
                if(Globals.opt_interactive == False):
                  fix_guard(fullpath, line, correct_guard);
                #Ask the user if should correct the guard.
                else:
                    if(should_correct_guard_prompt()):
                        fix_guard(fullpath, line, correct_guard);

def scan():
    ## Scan the directories.
    for root, dirs, files in os.walk(start_path, topdown=True):
        for file in files:
            filename, fileext = os.path.splitext(file);
            if(fileext in Globals.fileexts):
                check(root, file);


################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    #Get the command line options.
    options = getopt.gnu_getopt(sys.argv[1:],
                                Constants.ALL_FLAGS_SHORT,
                                Constants.ALL_FLAGS_LONG);

    #Optiongs switches.
    help_resquested   = False;
    version_requested = False;

    #Parse the options.
    for option in options[0]:
        key, value = option;
        key = key.lstrip("-");

        #Check if flags are present.
        if(key in Constants.FLAG_HELP):
            help_resquested = True;
        elif(key in Constants.FLAG_VERSION):
            version_requested = True;
        elif(key in Constants.FLAG_INTERACTIVE):
            Globals.opt_interactive = True;
        elif(key in Constants.FLAG_BACKUP):
            Globals.opt_backup = True;
        elif(key in Constants.FLAG_BACKUP_PATH):
            Globals.backup_path = value;
        elif(key in Constants.FLAG_EXT):
            Globals.file_exts.append(value);

    #Check if the exclusive operations are requested.
    if(help_resquested):
        print_help();
        exit(0);
    if(version_requested):
        print_version();
        exit(0);


    if(len(Globals.backup_path) == 0):
        if(Globals.opt_backup):
            Globals.backup_path = Constants.BACKUP_PATH_DEFAULT;
        else:
            Globals.backup_path = Constants.BACKUP_PATH_TEMP;
    if(len(Globals.file_exts) == 0):
        Globals.file_exts = [Constants.EXT_HEADER_DEFAULT];

    #Show the run options.
    print_run_options();

if(__name__ == "__main__"):
    main();

