#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        guardchecker.py                           ##
##            █ █        █ █        GuardChecker                              ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2015, 2016                  ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
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
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

## Imports ##
import getopt;
import os.path;
import os;
import re;
import sys;


################################################################################
## Don't let the standard import error to users - Instead show a              ##
## 'nice' error screen describing the error and how to fix it.                ##
################################################################################
def __import_error_message_print(pkg_name, pkg_url):
    print "Sorry, "
    print "frame-merger depends on {} package.".format(pkg_name);
    print "Visit {} to get it.".format(pkg_url);
    print "Or checkout the README.md to learn other ways to install {}.".format(pkg_name);
    exit(1);


## cowtermcolor ##
try:
    import cowtermcolor;
    from cowtermcolor import *;
except ImportError, e:
    __import_error_message_print(
        "cowtermcolor",
        "http//opensource.amazingcow.com/cowtermcolor.html");



################################################################################
## Globals                                                                    ##
################################################################################
class Globals:
    file_exts  = [];

    backup_path   = None;
    exclude_paths = [];

    project_root = None;
    project_name = None;

    opt_interactive = False;
    opt_force       = False;
    opt_dry_run     = False;


################################################################################
## Constants                                                                  ##
################################################################################
class Constants:
    FLAG_HELP          = "h", "help";
    FLAG_VERSION       = "v", "version";
    FLAG_INTERACTIVE   = "i", "interactive";
    FLAG_FORCE         = "f", "force";
    FLAG_PROJECT_NAME  = "n", "project-name";
    FLAG_EXT           = "E", "ext";
    FLAG_BACKUP_PATH   = "b", "backup-path";
    FLAG_EXCLUDE_PATHS = "e", "exclude-path"
    FLAG_DRY_RUN       = "D", "dry-run";

    ALL_FLAGS_SHORT = "".join([
            FLAG_HELP          [0],
            FLAG_VERSION       [0],
            FLAG_INTERACTIVE   [0],
            FLAG_FORCE         [0],
            FLAG_PROJECT_NAME  [0] + ":",
            FLAG_EXT           [0] + ":",
            FLAG_BACKUP_PATH   [0] + ":",
            FLAG_EXCLUDE_PATHS [0] + ":",
            FLAG_DRY_RUN       [0],
      ]);

    ALL_FLAGS_LONG = [
            FLAG_HELP          [1],
            FLAG_VERSION       [1],
            FLAG_INTERACTIVE   [1],
            FLAG_FORCE         [1],
            FLAG_PROJECT_NAME  [1] + "=",
            FLAG_EXT           [1] + "=",
            FLAG_BACKUP_PATH   [1] + "=",
            FLAG_EXCLUDE_PATHS [1] + "=",
            FLAG_DRY_RUN       [1],
      ];

    DEFAULT_BACKUP_PATH   = "/tmp/guardchecker";
    DEFAULT_EXT_HEADER    = [".h"];
    DEFAULT_PROJECT_ROOT  = "./";

    #App
    APP_NAME      = "guardchecker";
    APP_VERSION   = "0.3.0";
    APP_AUTHOR    = "N2OMatt <n2omatt@amazingcow.com>"
    APP_COPYRIGHT = "\n".join(("Copyright (c) 2015, 2016 - Amazing Cow",
                               "This is a free software (GPLv3) - Share/Hack it",
                               "Check opensource.amazingcow.com for more :)"));


################################################################################
## Colors                                                                     ##
################################################################################
ColorError   = Color(RED);
ColorWarning = Color(YELLOW);
ColorOK      = Color(GREEN);
ColorPath    = Color(MAGENTA);
ColorInfoMsg = Color(BLUE);


################################################################################
## Helper Functions                                                           ##
################################################################################
def print_help():
    help = """Usage:
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
  """;
    print help;
    exit(0);


def print_version():
    print "{} - {} - {}".format(Constants.APP_NAME,
                                Constants.APP_VERSION,
                                Constants.APP_AUTHOR);
    print Constants.APP_COPYRIGHT;
    print;
    exit(0);


def print_run_warning():
    msg = """{color}WARNING:
  THIS IS A VERY, VERY DANGEROUS PROGRAM. IT WILL MESS WITH YOUR SOURCES.
  THE PROGRAM WILL MAKE A BACKUP AT ({path}{color}) BUT IS STRONGLY ADVISED
  THAT YOU CREATE A HANDMADE BACKUP BEFORE AND PASS ANOTHER CUSTOM BACKUP PATH.
  CURRENTLY IT IS VERY DUMB TO SEEK THE INCLUDE GUARDS, SO IS VERY WISE
  TO RUN IT IN A INTERACTIVE MODE ({flag}{color}) TO CHECK THE CHANGES
  BEFORE THEM HAPPEN.
  RUN THIS AT YOUR OWN RISK, WORKS PRETTY WELL IF USED WITH CARE.
  ENJOY...{reset}"""

    warning = msg.format(color=ColorWarning(auto_reset=False),
                         path =ColorPath(Constants.DEFAULT_BACKUP_PATH),
                         flag =ColorInfoMsg("-i | --interactive"),
                         reset=ColorWarning(auto_reset=True));
    print warning;


def print_run_info():
    print "Run Options";
    print "  Interactive   :", Globals.opt_interactive;
    print "  Dry Run       :", Globals.opt_dry_run;
    print "  Backup path   :", Globals.backup_path;
    print "  File exts     :",  " ".join(Globals.file_exts);
    print "  Project root  :", Globals.project_root;
    print "  Project name  :", Globals.project_name;
    print "  Exclude Paths :", Globals.exclude_paths;


def should_correct_guard_prompt():
    try:
        r = raw_input("Correct the guard? [Y/n]:");
        if(len(r) != 0 and r.lower() == "n"):
            return False;
        return True;
    except KeyboardInterrupt, e:
        print ColorWarning("\nCanceling");
        exit(0);


def should_continue_run_prompt():
    try:
        r = raw_input("Run the program? [y/N]:");
        if(len(r) != 0 and r.lower() == "y"):
            return True;
        return False;
    except KeyboardInterrupt, e:
        print ColorWarning("\nCanceling");
        exit(0);


def system_cmd(cmd):
    ret = os.system(cmd);
    if(ret != 0):
        print_fatal("cmd: {}".format(cmd));


def expand_path(path):
    return os.path.abspath(os.path.expanduser(path));


def normalize_path(path):
    return os.path.normpath(expand_path(path));


def print_fatal(msg):
    print ColorError("[FATAL]"), msg;
    exit(1);


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

    #Now move the "original" file to backup folder
    #and rename the temporary file as the "original".
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
        #COWHACK: Find a better way to check if we're dealing with an guard.
        #COWNOTE: Find a better way to check if we're dealing with an guard.
        search_str = "^{}.*".format("#ifndef");
        #Check if we have a include guard.
        if(re.search(search_str, file_line) is None):
            continue;

        #Clean the line to let us compare.
        current_guard = file_line.replace("\n", "").lstrip("#ifndef ");
        correct_guard = build_correct_guard(fullpath);

        #Check if guards matches.
        if(correct_guard == current_guard):
            print ColorOK("[OK]"), fullpath;
            break;

        #Guards doesn't matches...
        print ColorWarning("[NOT MATCH]"), fullpath;
        print "  Expected :", ColorOK(correct_guard);
        print "  Found    :", ColorError(current_guard);

        if(Globals.opt_dry_run):
            print ColorInfoMsg("[DRY RUN]");
            return;

        #If running in non interactive mode, or user asks to correct the guard.
        if(not Globals.opt_interactive or should_correct_guard_prompt()):
            back_path = fix_guard(fullpath, current_guard, correct_guard);
            print "  Backup   :", ColorPath(back_path);


def scan():
    #Change the current working directory to the directory
    #of project root. We do this because ease **all** other operations.
    os.chdir(Globals.project_root);

    ## Scan the directories.
    for root, dirs, files in os.walk(".", topdown=True):
        if(expand_path(root) in Globals.exclude_paths):
            print ColorInfoMsg("[SKIPPING]:"), ColorPath(root);
            dirs [:] = [];
            files[:] = [];
            continue;

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
        print_fatal(str(e));

    #Options switches.
    help_resquested   = False;
    version_requested = False;

    #Parse the options.
    for option in options[0]:
        key, value = option;
        key = key.lstrip("-");

        #Check if flags are present.
        if  (key in Constants.FLAG_HELP         ): help_resquested         = True;
        elif(key in Constants.FLAG_VERSION      ): version_requested       = True;
        elif(key in Constants.FLAG_INTERACTIVE  ): Globals.opt_interactive = True;
        elif(key in Constants.FLAG_FORCE        ): Globals.opt_force       = True;
        elif(key in Constants.FLAG_DRY_RUN      ): Globals.opt_dry_run     = True;
        elif(key in Constants.FLAG_BACKUP_PATH  ): Globals.backup_path     = value;
        elif(key in Constants.FLAG_PROJECT_NAME ): Globals.project_name    = value;
        elif(key in Constants.FLAG_EXT          ): Globals.file_exts.append(value);
        elif(key in Constants.FLAG_EXCLUDE_PATHS): Globals.exclude_paths.append(value);


    #Check if the exclusive operations are requested.
    if(help_resquested  ): print_help();
    if(version_requested): print_version();

    #Check if user passed the project root.
    if(len(options[1]) != 0):
        Globals.project_root = options[1][0];

    #Check if user passed custom info, if not set the defaults.
    #Backup path.
    if(Globals.backup_path is None or len(Globals.backup_path) == 0):
        Globals.backup_path = Constants.DEFAULT_BACKUP_PATH;
    #File extensions.
    if(len(Globals.file_exts) == 0):
        Globals.file_exts = Constants.DEFAULT_EXT_HEADER;
    #Project Root.
    if(Globals.project_root is None or len(Globals.project_root) == 0):
        Globals.project_root = Constants.DEFAULT_PROJECT_ROOT;
    #Project Name.
    if(Globals.project_name is None or len(Globals.project_name) == 0):
        Globals.project_name = os.path.basename(expand_path(Globals.project_root));

    #Set the backup path
    Globals.backup_path = os.path.join(Globals.backup_path,
                                       Globals.project_name + "_BACKUP");

    #Interactive flag ALWAYS override the force flag.
    if(Globals.opt_interactive == True):
        Globals.opt_force = False;

    #Print the program start up info.
    if(Globals.opt_force == False):
        print_run_warning();
        print_run_info();
        if(not should_continue_run_prompt()):
            print ColorWarning("Aborting...");
            exit(0);

    #Expand all excluded paths.
    Globals.exclude_paths = map(expand_path, Globals.exclude_paths);

    # Start...
    scan();

if(__name__ == "__main__"):
    main();

