#!/usr/bin/python
import os;
import os.path;
import re;
import termcolor;

start_path = "MonsterFramework"

class Globals:
    fileexts = [".h"];
    backup_dir = "./backup";

def issue_color(msg):
    return termcolor.colored(msg, "red");
def correct_color(msg):
    return termcolor.colored(msg, "green");
def filename_color(msg):
    return termcolor.colored(msg, "blue");

def build_correct_guard(fullpath):
    return "__" + "_".join(fullpath.split("/")).replace(".","_") + "__";

def get_input(msg, options, default):
    index = options.index(default);
    options[index] = options[index].upper();

    msg += "[{}]".format("/".join(options)) + ":";
    inp = raw_input(msg);

    return len(inp) > 0 and inp[0].lower() == "y";

def fix_guard(fullpath, incorrect, correct):
    folderpath, filepath = os.path.splitext(fullpath);
    backuppath = os.path.join(Globals.backup_dir,folderpath);
    
    #Make the backup dir.    
    cmd_mkdir = "mkdir -p {}".format(backuppath);
    os.system(cmd_mkdir);

    #Copy the original file to backup folder.
    cmd_cp = "cp {} {}".format(fullpath, backuppath);
    os.system(cmd_cp);

    #Run sed.
    tempfilepath = fullpath + ".temp";
    cmd_sed = "sed s/{}/{}/g {} > {}".format(incorrect, 
                                             correct,
                                             fullpath,
                                             tempfilepath);
    os.system(cmd_sed);

    #Move the temp file over the original file.
    cmd_mv = "mv {} {}".format(tempfilepath, fullpath);
    os.system(cmd_mv);

def check(root, filename):
    fullpath       = os.path.join(root, filename);
    correct_guard  = build_correct_guard(fullpath);
    
    lines = open(fullpath).readlines();    

    for line in lines:
        search_str = "^{}.*".format("#ifndef");

        #Check if we have a include guard.
        if(re.search(search_str, line) is not None):

            line = line.replace("\n", "");
            line = line.replace("#ifndef", "").lstrip(" ");

            if(line != correct_guard):            
                print "File:    {}".format(filename_color(fullpath));
                print "Found:   {}".format(issue_color(line));
                print "Correct: {}".format(correct_color(correct_guard));
                
                # if(get_input("Correct? ", ["y", "n"], "n")):
                fix_guard(fullpath, line, correct_guard);

## Scan the directories.
for root, dirs, files in os.walk(start_path, topdown=True):
    for file in files:
        filename, fileext = os.path.splitext(file);
        if(fileext in Globals.fileexts):
            check(root, file);

