Mercurial hook for jira
==================================

The Mercurial hook checks that jira key exist in commit message.

The expected JIRA project is based on the name of the repository, and is configured in `~/.config/jirakeycheck.yaml`
See example_jirakeycheck.yaml for an example

Installation
------------
1. Copy `jirakeycheck.py` to ~/.hg (or any dir you like)
2. Add the following lines to $HOME/.hgrc
<div>
<pre>
[hooks]
   #check all outgoing commits
   pretxncommit.jirakeycheck = python:~/.hg/jirakeycheck.py:checkCommitMessage

   #Check all incoming commits when you pull. Good for pull requests control
   pretxnchangegroup.jirakeycheckall = python:~/.hg/jirakeycheck.py:checkAllCommitMessage
</pre>
</div>
3. Copy example_jirakeycheck.yaml to ~/.config/jirakeycheck.yaml
4. Set your JIRA projects and repo names in ~/.config/jirakeycheck.yaml
