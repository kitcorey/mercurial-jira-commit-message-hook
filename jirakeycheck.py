#coding: utf-8
import os
import re
import json

#If the hook returns True - hook fails
BAD_COMMIT = True
OK = False
CONFIG_FILE = "~/.config/jirakeycheck.json"

def readConfiguration(ui):
    """Read configuration from the CONFIG_FILE directory"""
    #List of the available JIRA projects
    try:
        with open(os.path.expanduser(CONFIG_FILE), 'r') as cfgfile:
            cfg = json.load(cfgfile)
    except IOError:
        ui.warn("Could not read {}".format(CONFIG_FILE))
        cfg = {}
    except ValueError as e:
        ui.warn("Could not parse {} as valid json: {}".format(CONFIG_FILE, e))
        cfg = {}

    return cfg


def getJIRAProjectFromDirectoryName(directoryName, ui):
    """Given the basename for a directory, return the first
    JIRA project that has a matching regex.
    
    If there are no matches, return an empty string
    """
    cfg = readConfiguration(ui)
    jiraProjects = cfg.get('projects', None)
    if jiraProjects is None:
        return ""

    for projectName, directoryRegexes in jiraProjects.iteritems():
        for directoryRegex in directoryRegexes:
            if re.search(directoryRegex, directoryName):
                return projectName

    return ""


def checkCommitMessage(ui, repo, **kwargs):
    """Checks commit message for matching commit rule:
    Every commit message must include JIRA issue key
    Example:

    PRJ-42: added meaning of life

    Include this hook in .hg/hgrc

    [hooks]
    pretxncommit.jirakeycheck = python:/path/jirakeycheck.py:checkCommitMessage
    """

    jiraProject = getJIRAProjectFromDirectoryName(os.path.basename(repo.root), ui)
    if not jiraProject:
        return OK

    hg_commit_message = repo['tip'].description()
    if checkMessage(hg_commit_message, jiraProject) is False:
        printUsage(ui, jiraProject)
        #reject commit transaction
        return BAD_COMMIT
    else:
        return OK


def checkAllCommitMessage(ui, repo, node, **kwargs):
    """
    For pull: checks commit messages for all incoming commits
    It is good for master repo, when you pull a banch of commits

    [hooks]
    pretxnchangegroup.jirakeycheckall =
        python:/path/jirakeycheck.py:checkAllCommitMessage
    """
    print(hook)
    print(node)
    for rev in xrange(repo[node].rev(), len(repo)):
        message = repo[rev].description()
        if checkMessage(message) is False:
            ui.warn(
                "Revision "
                + str(rev)
                + " commit message:["
                + message
                + "] | JIRA issue key is not set\n"
            )
            printUsage(ui)
            #reject
            return BAD_COMMIT
    return OK


def checkMessage(msg, jiraProject):
    """
    Checks message for matching regex

    Correct message example:
    PRJ-123: your commit message here

    #"PRJ-123: " is necessary prefix here
    """

    is_correct = False
    re_names = '%s-\d+' % jiraProject
    p = re.compile('(^({0}): )|(^Merge {0})|(^Merging {0})'.format(re_names))
    res = p.search(msg)
    if res:
        is_correct = True
    return is_correct


def printUsage(ui, board):
    ui.warn('=====\n')
    ui.warn('Commit message must have {} issue key\n'.format(board))
    ui.warn('Examples:\n')
    ui.warn('{}-42: the answer to life, universe and everything \n'.format(board))
    ui.warn('Merge {}-42 into upstream\n'.format(board))
    ui.warn('=====\n')
