Week 2 of the project has finished and it has left me in a place to continue development and really begin to make a mark on the project.

Majority of the week was preparing and releasing the project outline specification. This was just a small document to outline some of the core requirements and features. Whilst doing this I identified an issue with my expectations - like many people probably found out, their scope was a bit too large.

I've scaled back the scope for an MVP, but I am ready for the challenge of the other bits later. Instead of doing full OCR it will now just do very basic OCR at the top of the notes and suggested automatic tagging. Additional OCR extraction and OpenCV integration will be added in the future. It was also confirmed that this was going to be a web app.

Other things I have done this week:

* **Server Configuration** - With it being  web application I'd like to host it, not only for the mid-project demo, but I do feel as though this application has a real purpose. So I've set up a basic area for the server where the application can reside whilst I develop.  

* **Decided on a methodology** - I have firmly decided what to do for my methodology - Extreme Programming and Scrum combined. I am used to this in a team, as it was what we used during my intern at Sky, however I need to adapt this to a single person project. I have been conducting daily standups with a set of peers and so far seems to be working out well. I have set up a task tracking tool Tiaga, and will be tracking my sprints and story points there.

* **Written up user stories** - I have also written up some user stories for the project. They are very simple, an example is: <code>As a user I want to be able to tag my notes so that all my notes are under the correct module</code>. This is something I can go off and show my supervisor in the next meeting to decide what's most important for the next sprint.

* **Investigation into web frameworks** - Although frameworks can often be too bloated, if used correctly they can aid a developer and provide good structure. As I will be looking to use OpenCV in the future, and although I will be following a YAGNI approach, getting the core was still important. Therefore, I began to look into Python based frameworks and came across a minimalist micro-framework [Flask](http://flask.pocoo.org/).
Obviously there was many thoughts going around my head: PHP vs Python vs Ruby for the server side, should I be using React or Ember? Should I make a one page app and a REST API? I then remembered the YAGNI and KISS principles and decided I will just create a simple web application with multiple URLs and pages and create it in its most basic form, and then go from there.


*  **Created a spike solution using flask and OpenCV** - Leading on from choosing a micro-framework, my supervisor suggested I look into it to make sure it was the right idea for future use.  I was requested to make a simple app which could upload an image, display an image and interact with the OpenCV libraries to turn it greyscale. [Here's a short video of the web app turning an image grey](https://youtu.be/frXrjANY69s). Although this was spike work and no tests were written I got a good idea of what the structure of applications were like, and found a few interesting quirks compared to previous frameworks I have used.

* **Investigated Travis CI** - I will be looking to use some form of CI. I have previous experience of Jenkins, but I looked into Travis as it is in the cloud and my supervisor can see when tests are passing or failing easier than a Jenkins build screen. I have a few concerns with this though: time being the main one, as it would have to install Tesseract and OpenCV for every build, meaning builds could become quite lengthy. I think more Spike work into looking into it would be needed - sooner rather than later as I want to have a good solid foundation to build upon.

* **Started to train my own handwriting data** - Some more investigation work into looking into Tesseract and handwriting text was conducted. I have began to train and label boxes (this is how Tesseract bounds the letters) with the correct character classification. I have been battling homebrews default install, where it did not install program commands such as <code>mftraining</code> which I will need in the latter half of the training. After a lot of sighing and looking on their GitHub issues I didn't find anything useful. Then I found [this fantastic blog post](https://ryanfb.github.io/etc/2014/11/19/installing\_tesseract\_training\_tools\_on\_mac\_os\_x.html) which explained that the author submitted  pull request to add training tools as a flag: <code>brew install --with-training-tools tesseract</code> which I means I can continue with the training process. Below is an example of the bounding boxes and how it tries to identify each character.
![alt](/content/images/2016/02/-sign.png)

So I feel I completed or started to investigate quite a lot this week. I have decided my sprints are going to be Thursday -> Thursday - as that's when I have my personal 1:1 meeting and it's more convenient. So as I am half way through "Sprint 0" what are my tasks for the latter half of the Sprint:





* Look more into Travis, I am still not convinced with it, maybe I will switch to Jenkins.
* Continue with training my handwriting data - this won't take up a lot of my time, just to get a basic language file set up would be great.
* Begin the TDD process and produce a skeleton project with simple routing and views, with more investigation with the Flask framework. 
