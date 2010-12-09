# Copyright 2010 Herve BREDIN (bredin@limsi.fr)
# Contact: http://pyafe.niderb.fr/

# This file is part of PyAFE.
# 
#     PyAFE is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     PyAFE is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with PyAFE.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import getopt
import eval

def getListOfFingerprints( path2fingerprint ):
    f = open(path2fingerprint, 'r')
    fingerprint = {}
    for line in f:
        fingerprint[ line.rstrip()] = 1
    return fingerprint

def getListOfRelativePathToFile( mydir, filename ):
    fileList = []
    rootdir = os.path.normpath(mydir)
    for root, subFolders, files in os.walk(rootdir):
        for file in files:
            if file == filename:
                fileList.append(os.path.dirname(os.path.relpath(os.path.join(root,file), rootdir)))
    return fileList


def full_eval_zik(path2groundtruth, path2submission, subname, partial, skipTwoDaysEvents, fingerprints, verbosity):
    # Get list of annotation files
    gtname = "Music.xml"
    annFiles = getListOfRelativePathToFile( path2groundtruth, gtname )
    # Evaluate one file after the other and put results into evalList
    evalList = []
    for annFile in annFiles:
        # Get full path to groundtruth xml file
        path2xml_gt = os.path.join(path2groundtruth, annFile, gtname)
        # Get full path to expected submission xml file
        path2xml_sub = os.path.join(path2submission, annFile, subname)

        # Make sure it exists
        if os.path.exists(path2xml_sub) == False:
            if partial == False:
                print "%s > ERROR - missing submission file" % (os.path.join(annFile, gtname))
                e = eval.eval_zik(path2xml_gt, None, skipTwoDaysEvents, fingerprints, verbosity)
                evalList.append(e)                
        else:
            if verbosity > 1:
                print ""
                print "#### %s ERROR LIST ####" % (os.path.join(annFile, gtname))
            e = eval.eval_zik(path2xml_gt, path2xml_sub, skipTwoDaysEvents, fingerprints, verbosity)
            if verbosity > 0:
                print "%s > %s " % (os.path.join(annFile, gtname), e.description())
            evalList.append(e)

    return evalList


def full_eval_ads(path2groundtruth, path2submission, subname, partial, skipTwoDaysEvents, fingerprints, verbosity):
    # Get list of annotation files
    gtname = "Advertising.xml"
    annFiles = getListOfRelativePathToFile( path2groundtruth, gtname )
    # Evaluate one file after the other and put results into evalList
    evalList = []
    for annFile in annFiles:
        # Get full path to groundtruth xml file
        path2xml_gt = os.path.join(path2groundtruth, annFile, gtname)
        # Get full path to expected submission xml file
        path2xml_sub = os.path.join(path2submission, annFile, subname)

        # Make sure it exists
        if os.path.exists(path2xml_sub) == False:
            if partial == False:
                print "%s > ERROR - missing submission file" % (os.path.join(annFile, gtname))
                e = eval.eval_ads(path2xml_gt, None, skipTwoDaysEvents, fingerprints, verbosity)
                evalList.append(e) 
        else:
            if verbosity > 1:
                print ""
                print "#### %s ERROR LIST ####" % (os.path.join(annFile, gtname))
            e = eval.eval_ads(path2xml_gt, path2xml_sub, skipTwoDaysEvents, fingerprints, verbosity)
            if verbosity > 0:
                print "%s > %s " % (os.path.join(annFile, gtname), e.description())
            evalList.append(e) 

    return evalList

def usage():
    print "HELP full_eval.py :"
    print "  -g, --groundtruth  Path to annotation directory"
    print "  -s, --submission   Path to submission directory"
    print "  -n  --filename     Name of submission files. Default is submission.xml"
    print "  -m  --music        Only perform music evaluation"
    print "  -a  --ads          Only perform ads evaluation"
    print "  -p  --partial      Only evaluate available submission files"
    print "  -d  --skip2days    Skip events that starts the day before or ends the day after"
    print "  -f  --fingerprint  Path to list of available fingerprint"
    print "  -v  --verbosity    Set level of verbosity (default=-1)"
    print "                    -1 = only print global results"
    print "                     0 = same as -1 + print command arguments"
    print "                     1 = same as 0 + print per-file results"
    print "                     2 = same as 1 + print list of errors"
    print "  -h, --help         Print this help"
    print ""
    print "OUTPUT FORMAT"
    print "Music|Ads: $ParticipantID$ $RunID$ | P2 = $P2$ | P3 = $P3$ | P2.5 = $P2.5$ | Hit = $Hit$/$Total$ | Miss = $Miss$ | False Alarm = [$FA1$+$fa1$ / $FA2$+$fa2$ / $FA3$+$fa3$]"
    print "  $ParticipantID$: participant ID (from XML submission files)" 
    print "  $RunID$: run ID (from XML submission files)"
    print "  $P2$: performance metric 2 ($Hit$ - $FA2$ - $fa2$) / $Total$" 
    print "  $P3$: performance metric 3 ($Hit$ - $FA3$ - $fa3$) / $Total$"
    print "  $P2.5$: hybrid performance metric ($Hit$ - $FA2$ - $fa3$) / $Total$" 
    print "  $Hit$: number of hits (correct detection)"
    print "  $Total$: number of events to be detected"
    print "  $Miss$: number of misses"
    print "  $FA3$: number of false alarms (+1 for every bad detection -- does not include 'holes')"
    print "         e.g.: If Detected = B C B and Groundtruth = A, then $FA3$ = 3"
    print "  $fa3$: same as $FA3$ but dedicated to 'holes' (time intervals with no events to be detected)"
    print "  $FA2$: same as $FA2$ but multiple errors for the same couple (groundtruth event/detected event) do not add up."
    print "         e.g.: If Detected = B C B and Groundtruth = A, then $FA2$ = 2 (one for B, and one for C)"
    print "  $fa2$: same as $FA2$ but dedicated to 'holes' (time intervals with no events to be detected)"
    print "  $FA1$: same as $FA3$ but multiple errors for the same groundtruth event do not add up."
    print "         e.g.: If Detected = B C B and Groundtruth = A, then $FA1$ = 1"
    print "  $fa1$: same as $FA1$ but dedicated to 'holes' (time intervals with no events to be detected)"

if __name__ == '__main__':
    try:
    	opts, args = getopt.getopt(sys.argv[1:], "hampg:s:n:v:df:", ["help", "music", "ads", "partial", "groundtruth=", "submission=", "filename=", "verbosity=", "skip2days", "fingerprint="])
    except getopt.GetoptError, err:
    	# print help information and exit:
    	print str(err) # will print something like "option -a not recognized"
    	usage()
    	sys.exit(2)
    		
    path2groundtruth = "";
    path2submission = "";
    subName = "submission.xml";
    adsOnly = False
    zikOnly = False
    partial = False
    verbosity = -1
    skipTwoDaysEvents = False
    path2fingerprint = "";
    # print opts
    # print args
    for opt, arg in opts:
    	if opt in ("-h", "--help"):
    		usage()
    		sys.exit()
    	elif opt in ("-a", "--ads"):
    	    adsOnly = True
    	elif opt in ("-m", "--music"):
    	    zikOnly = True
    	elif opt in ("-g", "--groundtruth"):
    		path2groundtruth = arg
    	elif opt in ("-s", "--submission"):
    		path2submission = arg
    	elif opt in ("-n", "--filename"):
    	    subName = arg
    	elif opt in ("-p", "--partial"):
    	    partial = True
    	elif opt in ("-d", "--skip2days"):
    	    skipTwoDaysEvents = True
    	elif opt in ("-f", "--fingerprint"):
    	    path2fingerprint = arg
    	elif opt in ("-v", "--verbosity"):
    	    verbosity = int(arg)
    	else:
    		assert False, "unhandled option"

    if (verbosity > -1):
        print "$ " + ' '.join(sys.argv[0:])

    if len(path2submission) == 0:
    	print "Error : missing submission directory."
    	sys.exit(2)
    if len(path2groundtruth) == 0:
        print "Error : missing groundtruth directory."
        sys.exit(2)
    if adsOnly and zikOnly:
        print "Error : cannot use both --ads and --music options"    
        sys.exit(2)

    fingerprints = {}
    if len(path2fingerprint) != 0:
        # load list of available fingerprints as dictionary 
        fingerprints = getListOfFingerprints( path2fingerprint )

    if adsOnly == False:
        results_zik = full_eval_zik(path2groundtruth, path2submission, subName, partial, skipTwoDaysEvents, fingerprints, verbosity)
        global_zik = eval.eval_result()
        for r in results_zik:
            global_zik.add(r)
        if verbosity > 0:
            print "----------------------------------------------"
        print "Music: ",
        global_zik.show()
        
    if zikOnly == False:
        results_ads = full_eval_ads(path2groundtruth, path2submission, subName, partial, skipTwoDaysEvents, fingerprints, verbosity)
        global_ads = eval.eval_result()
        for r in results_ads:
            global_ads.add(r)
        if verbosity > 0:
            print "----------------------------------------------"
        print "Ads:   ",
        global_ads.show()
    