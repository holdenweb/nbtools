### Project Outline

SCAM, Steve's Content and Authoring Manager, is a simple system to deploy the IPython notebook in creating versatile training materials and presentations. It is driven by an indented table of contents in a text file, a format most users can handle, and maintains content in editable IPython notebooks.

Its initial goal is to assist with the production of a specific set of commercial video lectures on Intermediate Python (in development in an open source repository).

The scope of the SCAM software will, until the initial application is complete, be limited as strictly as possible to developments required to complete that initial project.

__What Can I Do?__  
The coding work is a way to get involved in a reasonably simple  project manipulating JSON data structures. There are a number of other ways to help, depending on your skill set and interests. Feel free to mail me (steve at holdenweb dot com) with questions. But remember I'm busy!

Those in the Portland area can sign up for in-person review sessions that focus on topics needing content and filling in gaps in participant's knowledge through interactive us of the IPython notebook. These notebooks will be shared with the participants after each session. [URL to follow]

NOTE: Please be aware there is no guarantee this software will be released under an open source license, though the matter of licensing will be kept under review.  

#### Project Structure


Each project should be maintained as a directory containing the following items:

  * `outline.txt`, the indented and annotated table of contents
  * A `data` directory containing all required static resources
    * A `templates` directory containing notebook templates to be merged
      with the content
    * An `images` subdirectory containing graphical images used in notebooks
  * An `nbsource` directory in which the `mktopic` utility creates the
    notebook working copies
  * A `tools` directory containing the utility sources

Any other directories you find in there are not yet a permanent part of the project structure.

#### Available Utilities


__`topics.py`__  
This program reports on the state of the outline. The optional list of words will limit the output to topics containing all those words. You can also get a list of _orphaned_ files, which do not correspond to any title not included in the outline. 

  * `tools/topics.py [word ...]` lists all topics in the outline
    for which there is a source notebook.

  * `tools/topics.py -a [word ...]` lists all topics.
  
  * `tools/topics.py -u [word ...]` lists topics for which
    there is currently no source notebook.
  
  * `tools/topics.py -o` lists orphaned notebooks, _i.e._ files
     for which there is currently no corresponding topic in the outline.

__`mktopic.py`__  
Takes a sequence of arguments, concatenates them into a title,
creates the appropriate initial working notebook in the `nbsource` directory from the current base template for the user to edit. _E.g._

`(py3)airhead:project sholden$ mktopic Writing to Files`

This will create the notebook `nbsource/writing-to-files.ipynb`. The initial content is taken from the `data/templates/base.ipynb` notebook, which can be edited before notebook creation occurs. Certain substitutions are made for sequences enclosed by `{{` ... `}}`, but these are not currently documented.

__Note:__ there is currently no way to inject changes in the base notebook into already-created topic files.

__nbstats.py__  
Reports on the cells, lines and character count of both code and markdown cells in the `nbsource` directory, _e.g._

<img src="files/images/nbstats_out.png" />

You can optionally follow the command with a list of filenames to report on.

### Running IPython Notebooks in the Cloud

First you need to have a Google account (which is also your Notebook Cloud Server account - it's an Appspot app) and an Amazon AWS account. None of this costs anything, and even if you aren't helping with the project this is a really easy way to access Python.

___Signing Up for Notebook Cloud Services___  
All the computing you need to evaluate these notebooks (and a whole bunch more!) can be accomplished with virtuals that qualify for Amazon's free-tier pricing. Free-tier remains free for the first twelve months, and it's unlikely anything you do will exceed the very generous limits. To sign up for an AWS account:

  * Visit the [Amazon AWS home page](http://aws.amazon.com) 
  * Click the “Sign Up” link
  * Enter an email address, select “I am a new user” and click “Sign in ..”

Once you have opened your account (there's the usual "please confirm" email with a link) you need to sign up with Notebook Cloud, a Google AppSpot application that uses AWS services on your behalf to create virtual machines running the IPython Notebook server on demand.

  * Visit the [notebook cloud](http://notebookcloud.appspot.com) home page
  * Take a quick look at the simple documentation
  * Click "Log in with Google Account"
  * Once logged in, click the "Account Details" button,
    enter your AWS credentials (instructions how to get them are shown)
    and click "Save"

NOTE: you can password-protect all your notebooks by entering a password on this form. There is no mechanism to rerieve this password - you have been warned!

___Using the Notebook Cloud Service___  
You are now looking at the IPython Notebook Cloud server control window. For this purpose you only need to start the very smallest instance.

  * Click the "Micro" button to create a new Notebook Server

It will take a minute or two to create a new virtual machine. The Cloud server monitors the status of the virtual machine. Wait until it says "Serving" on the status line under the machine description, you are looking for something like

  __Instance id: i-706d2551    Type: t1.micro    Started: 01:04:36 ~ 2014-03-11__  
    __State__: Serving

Click on the word "serving" and a new window will open up with a notebook server showing an empty list of files. You can then drag Notebook (`.ipynb`) files into the (initially empty) files list, and an upload button appears. After uploading a notebook you can start it. Each notebook appears in its own browser window or tab.

After updating a notebook you can download a copy with the Notebook Server's "File | Download As ..." menu item. This allows you to download either a Python file (in which all the markdown text appears as comments) or a Notebook file that you can upload to another server if you want.

Your notebooks persist on the server between sessions. You can choose, though it's not necessary, to shut them down before closing or shutting down the Notebook Server.
When you are done, you might want to shut your Notebook Server down. There's no point leaving the clock ticking when it's not being used, but at the same time it costs hardly anything. I just don't like waste, you could be computing with those cycles. :)

In the Cloud Server window click the "Stop" button next to your chosen virtual. It takes a while (maybe up to a minute: what do you care, it's free, right?) to shut down a running virtual. The next time you visit your Notebook Cloud account (or even immediately!) you can restart it by clicking on its "Start" button.

The "Terminate" button removes the VM instance completely, dstroying its file store (so better make sure that before you terminate an instance you have downloaded copies of all Notebooks you may want to keep).

___Reviewing the Course Content___  
The simplest way to achieve this is to 

