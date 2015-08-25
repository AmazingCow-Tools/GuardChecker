#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        main.py                                   ##
##             ████████████         cpp-guard-checker                         ##
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
    file_exts    = [];
    backup_path  = "";
    project_root = "";
    project_name = "";

    opt_interactive = False;

################################################################################
## Constants                                                                  ##
################################################################################
class Constants:
    FLAG_HELP        = "h", "help";
    FLAG_VERSION     = "v", "version";
    FLAG_EXT         =      "ext";
    FLAG_BACKUP_PATH =      "backup-path";
    FLAG_INTERACTIVE = "i", "interactive";

    ALL_FLAGS_SHORT = "hvi";
    ALL_FLAGS_LONG  = ["help", "version", "ext=",
                       "backup-path=", "interactive"];

    DEFAULT_BACKUP_PATH   = "/tmp/cppguardchecker";
    DEFAULT_EXT_HEADER    = [".h"];
    DEFAULT_PROJECT_ROOT  = "./";

    #App
    APP_NAME      = "cpp-guard-checker";
    APP_VERSION   = "0.1";
    APP_AUTHOR    = "N2OMatt <n2omatt@amazingcow.com>"
    APP_COPYRIGHT = "\n".join(("Copyright (c) 2015 - Amazing Cow",
                               "This is a free software (GPLv3) - Share/Hack it",
                               "Check opensource.amazingcow.com for more :)"));

################################################################################
## Color Functions                                                            ##
################################################################################
def red_color(msg):
    return termcolor.colored(msg, "red");
def green_color(msg):
    return termcolor.colored(msg, "green");
def blue_color(msg):
    return termcolor.colored(msg, "blue");
def magenta_color(msg):
    return termcolor.colored(msg, "magenta");
def yellow_color(msg):
    return termcolor.colored(msg, "yellow");

################################################################################
## Helper Functions                                                           ##
################################################################################
def print_help():
    help = """Usage:
  cpp-guard-checker [-hv] [-i] [--ext <ext>] [--backup-dir <path>] <project root>

  -h --help           : Show this screen.
  -v --version        : Show app version and copyright.
  --ext <ext>         : Add the file extension to search. (Must include the dot)
  --backup-dir <path> : Where the original files will be backup.
"""
    print help;

def print_version():
    print "{} - {} - {}".format(Constants.APP_NAME,
                                    Constants.APP_VERSION,
                                    Constants.APP_AUTHOR);
    print Constants.APP_COPYRIGHT;
    print;

def print_run_warning():
    msg = """WARNING:
    THIS IS A VERY, VERY DANGEROUS PROGRAM. IT WILL MESS WITH YOUR SOURCES.
    THE PROGRAM WILL MAKE A BACKUP AT ({}) BUT IS STRONGLY ADVISED
    THAT YOU CREATE A HANDMADE BACKUP BEFORE AND PASS ANOTHER CUSTOM BACKUP PATH.
    CURRENTLY IT IS VERY DUMB TO SEEK THE INCLUDE GUARDS, SO IS VERY WISE
    TO RUN IT IN A INTERACTIVE MODE ({}) TO CHECK THE CHANGES
    BEFORE THEM HAPPEN.
    RUN THIS AT YOUR OWN RISK, WORKS PRETTY WELL IF USED WITH CARE.
    ENJOY..."""
    warning = msg.format((Constants.DEFAULT_BACKUP_PATH),
                         ("-i | --interactive"));
    print red_color(warning);

def print_run_info():
    print "Run Options";
    print "Interactive  :", Globals.opt_interactive;
    print "Backup path  :", Globals.backup_path;
    print "File exts    :",  " ".join(Globals.file_exts);
    print "Project root :", Globals.project_root;
    print "Project name :", Globals.project_name;

def should_correct_guard_prompt():
    r = raw_input("Correct the guard? [Y/n]:");
    if(len(r) != 0 and r.lower() == "n"):
        return False;
    return True;
def should_continue_run_prompt():
    r = raw_input("Run the program? [y/N]:");
    if(len(r) != 0 and r.lower() == "y"):
        return True;
    return False;

def system_cmd(cmd):
    ret = os.system(cmd);
    if(ret != 0):
        print red_color("[ERROR]"), "cmd:", cmd;
        exit(1);

def expand_path(path):
    return os.path.abspath(os.path.expanduser(path));
def normalize_path(path):
    return os.path.normpath(expand_path(path));

################################################################################
## Guard Related Functions                                                    ##
################################################################################
def fix_guard(fullpath, incorrect, correct):
    #Create the temp directory.
    base_path           = os.path.dirname(fullpath);
    current_backup_path = os.path.join(Globals.backup_path, base_path);
    current_backup_path = normalize_path(current_backup_path);

    mkdir_cmd = "mkdir -p {}".format(current_backup_path);
    system_cmd(mkdir_cmd);

    #Replace the incorrect guard with correct one.
    #This operation will create a "temporary" file that
    #will become the "new correct" file after we copy the original
    #file to backup folder.
    temp_file_path = fullpath + "_TEMP";
    sed_cmd  = "sed s/\"{incorrect_guard}\"/\"{correct_guard}\"/g "
    sed_cmd += "\"{original_file}\" > \"{temporary_file}\"";
    sed_cmd = sed_cmd.format(incorrect_guard=incorrect,
                             correct_guard=correct,
                             original_file=fullpath,
                             temporary_file=temp_file_path);

    system_cmd(sed_cmd);

    # #Now move the "original" file to backup folder
    # #and rename the temporary file as the "original".
    mv_original_cmd = "mv {} {}".format(fullpath, current_backup_path);
    mv_temp_cmd     = "mv {} {}".format(temp_file_path, fullpath);

    system_cmd(mv_original_cmd);
    system_cmd(mv_temp_cmd);

    backup_fullpath = os.path.join(current_backup_path,
                                   os.path.basename(fullpath));
    return backup_fullpath;

def build_correct_guard(fullpath):
    path = os.path.normpath(os.path.join(Globals.project_name, fullpath));
    return "__{}__".format(path.replace("/", "_").replace(".", "_"));

def check_file(root, filename):
    #Make the fullpath for file and open and read all lines.
    fullpath   = os.path.join(root, filename);
    file_lines = open(fullpath).readlines();

    #Search entire file for a line with guard.
    for file_line in file_lines:
        #COWTODO: Find a better way to check if we're dealing with an guard.
        #COWTODO: Find a better way to check if we're dealing with an guard.
        #COWTODO: Find a better way to check if we're dealing with an guard.
        search_str = "^{}.*".format("#ifndef");
        #Check if we have a include guard.
        if(re.search(search_str, file_line) is None):
            continue;

        #Clean the line to let us compare.
        current_guard = file_line.replace("\n", "").lstrip("#ifndef ");
        correct_guard = build_correct_guard(fullpath);

        #Check if guards matches.
        if(correct_guard == current_guard):
            print green_color("[OK]"), fullpath;
            break;

        #Guards doesn't matches...
        print yellow_color("[NOT MATCH]"), fullpath;
        print "  Expected :", green_color(correct_guard);
        print "  Found    :", red_color(current_guard);

        #If running in non interactive mode, or user asks to correct the guard.
        if(not Globals.opt_interactive or should_correct_guard_prompt()):
            back_path = fix_guard(fullpath, current_guard, correct_guard);
            print "  Backup   :", magenta_color(back_path);

def scan():
    #Change the current working directory to the directory
    #of project root. We do this bacause ease **all** other operations.
    os.chdir(Globals.project_root);

    ## Scan the directories.
    for root, dirs, files in os.walk(".", topdown=True):
        for file in files:
            filename, fileext = os.path.splitext(file);
            if(fileext in Globals.file_exts):
                check_file(root, file);

################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    #Get the command line options.
    try:
        options = getopt.gnu_getopt(sys.argv[1:],
                                    Constants.ALL_FLAGS_SHORT,
                                    Constants.ALL_FLAGS_LONG);
    except Exception, e:
        print red_color("[ERROR]"), e;
        exit(1);

    #Optiongs switches.
    help_resquested   = False;
    version_requested = False;

    #Parse the options.
    for option in options[0]:
        key, value = option;
        key = key.lstrip("-");

        #Check if flags are present.
        #Help.
        if(key in Constants.FLAG_HELP):
            help_resquested = True;
        #Version.
        elif(key in Constants.FLAG_VERSION):
            version_requested = True;
        #Interactive.
        elif(key in Constants.FLAG_INTERACTIVE):
            Globals.opt_interactive = True;
        #Backup Path.
        elif(key in Constants.FLAG_BACKUP_PATH):
            Globals.backup_path = value;
        #File Extensions.
        elif(key in Constants.FLAG_EXT):
            Globals.file_exts.append(value);

    #Check if the exclusive operations are requested.
    if(help_resquested):
        print_help();
        exit(0);
    if(version_requested):
        print_version();
        exit(0);

    #Check if user passed the project root.
    if(len(options[1]) != 0):
        Globals.project_root = options[1][0];

    #Check if user passed custom info, if not set the defaults.
    if(len(Globals.backup_path) == 0):
        Globals.backup_path = Constants.DEFAULT_BACKUP_PATH;
    if(len(Globals.file_exts) == 0):
        Globals.file_exts = Constants.DEFAULT_EXT_HEADER;
    if(len(Globals.project_root) == 0):
        Globals.project_root = Constants.DEFAULT_PROJECT_ROOT;

    #Set the project name.
    Globals.project_name = os.path.basename(expand_path(Globals.project_root));
    #Set the backup path
    Globals.backup_path = os.path.join(Globals.backup_path,
                                       Globals.project_name + "_BACKUP");

    #Print the program start up info.
    print_run_warning();
    print_run_info();
    if(not should_continue_run_prompt()):
        print yellow_color("Aborting...");
        exit(0);

    # Start...
    scan();

if(__name__ == "__main__"):
    main();

