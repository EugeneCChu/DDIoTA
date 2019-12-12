---
layout: default
---

# Digital Distributed IoT Assistant

Eugene Chu 405219652  
Nicolas Cheng 905219471

## Abstract
With an Internet of Things (IoT) spatially distributed in our environment, users often feel a need to interact with them more efficiently. We summarize a design space of interaction with different deivce and identify an underexplored area that inspires the design of DDIoTA--- a front end “digital assistant” system that listens to user commands and coordinates distributed applications spanning multiple devices including sensors/actuators. We collected some real world commands that are largely used in daily lives and used multiple models such as Bert[1], Flair[2] and NTLK[3] to process the command. In this report, we first introduce the background, goals and related works of this project, then we provide system design and technical approaches on how the command is processed. At last, we organize the potential future works and conclusion for this project.


## Introduction
### Background & Goals
  A large number of spatially-distributed Internet of Things (IoT) has populated our living and work environments, motivating researchers to explore various interaction techniques. At present, the main interaction method with a majority of IoT assistants such as Amazon Alexa, Google Home and Apple Siri is through voice command. However, these interaction techniques are limited to a single command over a static device rather than a dynamic distribution on multiple devices. This brings plenty of inefficiency to the interaction scenario, as when a user attempts to make commands over a wide range of devices, there is no way for him to simply conduct a one-time command. Instead, he'd have to input those commands one at a time depending on the number of device. 
  
  To solve this inefficient scenario, we present DDIoTA, an IoT assistant that could achieve macroprogramming over a dynamic set of devices. This project is based on some state-of-the-art models and neural networks. There are three major steps of this project:
  
**First**: identify the function that user is attempting to input and generate a list of parameter-less macro-programs. This step mainly aims at reconstructing the capability of Siri, which assumes that the device to be interact with is already known, and the system simply attempt to grasp the action on the device without any parameters or conditions. The following graph helps explaining how the first phase works: in this sentence, only two key elements can be grasped: *open* and *door*. After grasping those two words, the system then simply put the word “open” in the *Action* position and put “door” in the *Device* position.

![openthedoor](https://github.com/EugeneCChu/DDIoTA/blob/master/supportive_imgs/open_door.png)


**Second**: Compared with the first phase, there are two main breakthroughs in the second phase. On one hand, from the input voice command, the system should be able to do a system structure analysis throughout the command and accurately grasp the four command output elements: *Action*, *Device/System*, *Parameter* and *Condition*. This is still within the capability of existing interaction techniques. On the other hand, if there are multiple intended commands within one sentence, the system is supposed to split out each individual command with the four elements (*Action*, *Device/System*, *Parameter* and *Condition*) and output these commands separately. For instance, in the example below, the system can process the input “Put the cup and plate on the shelf and floor.” into four output four-element tuples: (Put, Cup, Shelf, None), (Put, Plate, Shelf, None), (Put, Cup, Floor, None), (Put, Plate, Shelf, None). Note that there are no trigger conditions in this command, so the *Condition* element is left blank.

![command generation](https://github.com/EugeneCChu/DDIoTA/blob/master/supportive_imgs/command_generation.png)

**Third**: The third phase is the one where dynamically assemble macro-programs across dynamic device sets. In this step, the user is no longer required to mention the details of each command. Instead, he would give a “condensed” command, and the system would extract key information from this command to determine which devices or systems to trigger and how the operation should be. For instance, when the user says a command “Catch the thief”, the system would first capture the keywords *catch* and *thief*, after which a series of text commands would be generated such as “initiate the camera at location xx”, “send drones to follow the thief” and “notify the police where the thief is”. After that, each text command would be processed and executed respectively to *dynamically* distributed macro-programs. 

Unfortunately, due to time limitation, we are only able to complete the first two phases and the third phase would need more time before it can be implemented. 

  
  
  
## Technical Background
  
  
  
  
  The application platform for the prototype of this system is DDFlow, an active research project that is being conducted by Joseph Noor. By connecting the DDIoTA and DDFlow, 

## System Design

![flowchart](https://github.com/EugeneCChu/DDIoTA/blob/master/supportive_imgs/flowchart.png)

The flowchart above illustrates the process of our work. As a user makes a voice input, it is first transcribed into text string by *Python SpeechRecognition Model*. Then using Spacy, which syntactically analyzes and parses the string, each word is represented by a token which not only includes what this word is, but also its relationships between other words in the command. The output of SpaCy-processed command is a structured command. Then the command goes through a extraction algorithm which generates a list of four-word tuples, each of which represents a parsed command. After that, stop words are removed from each command to make sure that only the key information is preserved. Lastly, a mapping between the parsed commands and available commands is applied. Mainly consists of *acronym* and *synonym* word replacement, this procedure guarantees that the parsed command can be understood by the executing programs. More details about how each step is implemented s introduced in the following *technical approach* section.



## Technical Approach

### Voice to text

To transfer voice command to text string, we used *Python SpeechRecognition Model* [reference] with the *Google Speech API*. The performance of transcription is generally satisfying, with an accuracy of 92.5%. The accuracy of other APIs are also tested such as (Add api names), and their success rate of transcription varies between 71% to 85%. Below are the API comparison table using *Python SpeechRecognition Model*. 

![table](https://github.com/EugeneCChu/DDIoTA/blob/master/supportive_imgs/table.png)


### Bert

### Flair

### Command Generator

### Synonym & Acronym

Because our system’s purpose is to convert voice to multiple commands in tuple form and feed those tuples to DDFlow, it is crucial that the output is understood-able by the DDFlow system. This brings in the necessity that when the command uses a word that DDFlow cannot comprehend, the command can be converted in a way within DDFlow’s comprehension capability. For instance, the operation *direct the TV channel to 75* may confuse DDFlow because it does not have an action *direct* for the device TV. Instead, the word *switch* is available. In this scenario, introducing word substitution becomes essential. So far, we have come up with two kinds of word substitutions: *synonym* and *acronym*. First, we wrote a python dictionary simulating what devices/systems there are and what their available commands are respectively. If a command’s device element is not recognizable by the system, we would introduce the *synonym & acronym handling* procedure. For acronym, if the device name consists of two or more words (e.g air conditioner), we simply take the first letter abbreviation and see if it matches any available registered device. Then if there’s still no matching, we would check whether the device name’s synonym list has anything in the available device list, and if there is any, we would replace the device element with that available device name. After that, the *action* element goes through the same procedure. We use the python *NTLK Wordnet*[reference] to achieve synonym list organization and word replacement.

One instance of *synonym & acronym handling* is presented below:

![set_ac](https://github.com/EugeneCChu/DDIoTA/blob/master/supportive_imgs/acro_syno.png)


## Result

A 41-command-included file is used for DDIoTA system verification. These commands are all acquired from popular *Siri* and *Alexa* popular command lists. The length of commands ranges from 3 to 12 words and desired output tuple-command number range from 1 to 4. The accuracy versus command length graph is shown below.

![accuracy](https://github.com/EugeneCChu/DDIoTA/blob/master/supportive_imgs/result_accuracy.png)

Out of the 41 commands, 37 are correctly processed by our system, which yields an accuracy of 92.5%. It is worth saying that most of the long commands are not correctly parsed, which suggests that when the command becomes lengthy, our system still suffers a hard time to accurately yield the output completely, although partial of its output is accurate. But for shorter commands, it can already reach a high recognition accuracy.

The latency incurred by processing is shown below. We can observe that the latency does not vary much with the change of command length. This proves the stability of our system as the work to be done does not increase dramatically with the increasing complexity of input command. Generally, the latency stays between 0.05s to 0.25s, which performs like a real-time system. Nevertheless, for some rare cases, there exist latency spikes that could reach 1 to 1.5s. This may become an aspect that future work could pay attention to.

![latency](https://github.com/EugeneCChu/DDIoTA/blob/master/supportive_imgs/result_latency.png)



## Strength and Weakness


## Future Works


## Conclusion


## Reference

