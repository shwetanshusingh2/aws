Project Title :

The aim of this project was to automate the process of deployment of aws services using jenkins and python. we also used Jenkinsfile and trigger based system in jenkins to build everytime when the github repository is changed. We used Pycharm as our coding IDE.

Getting Started : Install Python 3.7 into your system. Also download and install pyCharm.download jenkins and configure it using git plugin.

Installing :

1)Pycharm : Download Pycharm and install it. 
2)Python : Download Python and install it. 
3)AWS CloudFormation : In PyCharm , Install AWS CloudFormation package to use AWS CloudFormation in it. 
4)AWS ToolKit : In PyCharm , Install AWS ToolKit package to use AWS ToolKit in it.
5)Jenkins : install jenkins on the system and configure it for using github integration.

Deployment :

step 1: go to new item , give name for the project and select create using pipeline in it
step 2: in trigger select poll scm and give timer for one minute 
step 3: in pipeline select pipeline script from scm 
                          select git
                          give the git repository name and then click save.
step 4: select build now in the project or change the repoitory to see the jenkins working. 
