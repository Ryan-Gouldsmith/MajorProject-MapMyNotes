So my major project has started. For those who don't know a major project is essentially my dissertation. It should be around 400 hours worth of work encompassing many aspects of my degree.

### What is my project?
My project was originally put forward by Dr Harry Strange, but my supervisor for the duration of the project will be Dr Hannah Dee. Nevertheless, my project is called *MapMyNotes*.

The premise of the project is to take an image and extract specific "information" from the image. Typically a note will contain text, diagrams and graphs. I will be looking to model lecture and University notes, but this will be extensible to any form of notes.

I recently had a meeting with Dr Harry Strange to find out what his original plans were for the project. I have now a better understanding of the projects outcome, from both Hannah and Harry.

The application will upload an image to an application (this will either be a Web application or a desktop application - this needs to be decided) and it will process the image using a variety of Computer Vision algorithm techniques. It will align the photo to be portrait, so if the user takes a photo at an angle then it will automatically make it vertical.

The application would require to use some form of OCR (optical character recognition) tool to extract textual information from the application. Originally, Harry's idea was to upload the image and then use OCR to extract metadata such as the module code, time and location for automatic tagging of the note. However, Hannah and myself had an alternative view that the image is read via the OCR tool and all textual information is extracted and is inserted onto a canvas (a bit like how EverNote works) - which the user can then edit. Therefore Harry suggested that maybe there should be two sides to this application: the fully OCR version and one which does metadata extraction.

#### Partial OCR extraction
The partial OCR application would upload an image and take the metadata about the course title, what lecture it is and the location which will then  automatically tag the note in the application. For example, if the note was for CS31310, then the OCR application would see this and add a tag for "CS31310". Once uploaded, the notes can be annotated in the application and maybe linked to other notes and external tools such as Blackboard etc.

#### Full OCR example
Another option Harry suggested was to have an alternative section where the user's image is converted fully to text which they can edit. This is more like the interaction of an application like Evernote.

#### Other bits and bobs
Other key features are that the notes in the application are archivable, so it will need to integrate into a calendar. Additionally, it will need to store the images, metadata and any associated additional notes in a structured database. This also means that the notes are searchable via some metadata, such as the course title.

Harry suggested for additional flair aspects for the application could include any coloured text which has been written could be carried through to the application. He suggested using the OCR and Computer Vision techniques to mask the original document and extract the colour for each of the words.

#### What about diagrams and images I hear you say?
Well, this will be something I will need to consider for the application. I will have to detect the images and diagrams in the notes and either extract them or label them as an image. For this to work they will have to have a common structure to be able to extract them from the notes, how I deal with them has not been thought about just yet. I am aware that this will involve Computer Vision, and based on some research and previous experience I will be looking into using the Hough Transform to detect boxes around images and diagrams.

#### Set of Features I probably need
As you can see this project has a lot of work and lots of different aspects to it, so I will summarise the points which seem to be most important:

* Create some form of application to transform images with text to a digital note.
* Align an image using Computer Vision techniques
* Use some OCR techniques to extract textual information
* Use Computer Vision techniques to extract images and diagrams
* Store the notes in a structured database
* Allow the ability to annotate the notes
* Integrate with a calendar for archival purposes.
* Make the notes searchable so we can find them again.

#### What's next?
I need to collate a taxonomy of what is in a set of notes, read a few papers about different aspects of this major project and Harry suggested to come up a set of specific constraints for the notes structure.

More to follow over the next few months. 
