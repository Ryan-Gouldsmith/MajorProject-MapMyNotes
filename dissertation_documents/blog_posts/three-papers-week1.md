As the project is new and has only just started I have conducted some reading around the subject to help to understand specific information about the topic. Below are the 3 papers which I read, which I felt were relevant, and the paper which I found was better suited to my project


1. Recognition of Handwritten Roman Script Using Tesseract Open source OCR Engine
by: Sandip Rakshit, Subhadip Basu [Link to PDF](http://arxiv.org/abs/1003.5891)

2.
Optical Character Recognition by Open source OCR Tool Tesseract: A Case Study by: C. Patel, A. Patel, D. Patel [Link to PDF](http://research.ijcaonline.org/volume55/number10/pxc3882784.pdf)

3.  Hough technique for bar charts detection and recognition in document images
by: Yan P. Zhou, Chew L. Tan [Link to PDF](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=899506)


###### Recognition of Handwritten Roman Script Using Tesseract Open source OCR Engine

This paper was chosen as it leads on from the "*Optical Character Recognition by Open source OCR Tool Tesseract: A Case Study*" paper and instead of identifying against digital text this paper conducts their experiments against Roman handwriting which is more appropriate to my dissertation, as I will be looking at human handwritten notes.

This was a good paper as they showed that tesseract needed to be trained for human handwritten input data, which I didn't consider. Once the system was trained with over 1800 characters it is tested on 1133 characters and yielded an 83.5% accuracy. This shows, to me, that the tesseract OCR engine, when trained, will be able to identify human handwriting very well.

One disadvantage of this paper is that it runs the experiments on tesseract 2.01 and the latest version is 3.04 - so some features may have been improved or not, it is hard to say.

The paper clearly gives detail on how it trains the data and presents itself in such a way that I could go and train my own data following similar principles. Additionally the authors go into detail about the different files needed for training and how you need to rename the files for the specific language.

The authors then go on to conclude the paper with the experiment results and identifies that a lot of the error is segmentation errors. They give explanation about this by stating tesseract's default application was to identify characters with uniformity and again splitting of the letter i is a problem. They report that i reports around 53% of the overall misclassified examples - this is something I found interesting and was to be made aware of.


###### Optical Character Recognition by Open source OCR Tool Tesseract: A Case Study

As the title of the paper suggests, this is a paper which used the OCR tool Tesseract (which was suggested to me by both Hannah and Harry). This paper was interesting because it gave a comparison to the open source [Tesseract](https://github.com/tesseract-ocr/tesseract) and the commercially available OCR tool, [Transym](http://www.transym.com/). This paper was chosen to see the comparison of different OCR tools and how well tesseract actually worked compared to commercially available OCR systems and provided consideration of what I needed to choose.

It explores the issues with extracting text from images due differing style, size, orientation etc, which is something I would have to consider if I was to use an OCR tool. As well as these, when using the OCR tool the paper explores some of the issues such as misclassification of letters (e.g i) where it tries to classify it as two different letters due to the dot.

The paper was interesting as it explores how tesseract actually parses the image and eventually comes out with the classification, this is obviously important as it is key to understand how the system would work before you can use it.




###### Hough technique for bar charts detection and recognition in document images

From previous Computer Vision experience I knew that the Hough transform would be a technique available to detect lines, so when I found an article on the Hough Transform and extracting bar charts (which was discussed [here](http://ryangouldsmith.uk/2016/01/28/taxonomy-of-notes/) and mentioning Hough [here](http://ryangouldsmith.uk/2016/01/27/kicking-off-the-major-project/)) I thought that this paper would be a great reference material.

This paper suggests that although there has been work to identify and extract pictures/diagrams from images there has been little to no research in extracting charts from images, instead the focus has been on engineering drawings etc.

The authors say that the technique has 3 different stages: preprocessing, detection and recognition to make this technique work. They use a modified probabilistic hough transform to extract the diagrams, which apparently it will "save on computation time by diminishing the number of voting points". Another bonus and interesting fact is that the authors are claiming that their technique is orientation invariant as well as hand drawn charts.

The premise is that they group bar chart candidates together and then use the modified probabilistic hough transform algorithm to detect parallel line clusters and then perform filtering to remove the lines which are similar.

The authors claim that the reconstruction rate is 92.3% which is an impressive achievement, given how complex bar charts are.  

#### Best paper I read, and why?
All 3 papers were relevant to my dissertation, hence why I gave them all a bit of a lengthy description (instead of choosing one to write a lengthy description in this section) but one which I will consider the most important would have to be the "*Recognition of Handwritten Roman Script Using Tesseract Open source OCR Engine
by: Sandip Rakshit, Subhadip Basu*" paper.

This paper was the most relevant as I would have to train the handwriting data, like they did with the Roman scriptures. The handwriting recognition will be an integral part of the application and finding a paper which has done it using the tool I have considered was important. It now gives me something I can look into and see how they trained their data and how that can be used in my application.

The paper also showed that it will give a very high accuracy rate if it is given the right training data. This has made me think how I can try to follow similar processes to achieve a success similar to that for my application. As well as this, I have gained an overview of how tesseract actually works from this paper such as the word and line fitter.

Overall, all the papers were equally relevant but I feel that the Roman script detection paper added more useful insight with the fact I will have to train the tesseract tool. 
