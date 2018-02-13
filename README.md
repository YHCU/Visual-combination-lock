# Visual Combination Lock Project

Author: Yang He

## Environment

- OS: MacOS High Sierra Version 10.13.1
- Platform: Python 3.6.2
- Libraries:
	- OpenCV 3.4.0
	- Numpy

## Project Description

This project uses the game 'Rock, Scissor, Paper' to define the grammar of hand gestures. A pre-defined gesture sequence of 3 is stored in the system and remains constant. Then the user plays the game, using either gesture pictures taken forehand or live capturing, in three rounds with the system, and the system will accept the user's gesture inputs if the user does not lose any round. (i.e. win or draw are both acceptable). 


## Run it
- Make sure the environment is set up properly as above (critical)
- For gesture sequences taken forehand:
	- Store the sequence under 'imgs/Sequences/[sequence_id]/' folder (sequence_id should be a positive integer)
	- The gestures should be stored in '.jpg' format, with the name indicating the round number (i.e. '1.jpg'). Files does not follow the naming format will be ignored. The system will prompt error if the three pictures are not all found.
	- Under 'src' folder, run the following command in python
		- python main.py <sequence_id>
- For live gesture capturing:
	- Under 'src' folder, run the following command in python
		- python main.py 0
		- Press 'c' on the keyboard to capture the gesture
		- Press 'q' to quit

## Specifications

### Domain Engineering

- Recommended picture taking device is iPhone.
- For optimal results, a background with black or dark color would be suggested.
- A single picture should contain a single hand, fully visible and flat on the background surface, no matter the position in the picture. The palm can either face outwards or inwards.
- The pictures should be stored in the format as mentioned in "Run it" section.

### Data reduction

The system identifies the hand by recognizing the skin parts in the picture, and transform the picture into black and white format for later gesture recognition. A demo of the reduced pictures of acceptable gestures are stored in 'examples/reduced' folder.

For better demonstration, the system will also annotate the inputs in command line in the following way:
- "What"
	- The system will annotate the gesture inputs as "Rock", "Scissor", "Paper" or "unknown". The pictures annotated as "unknown" will be treated as a loss in the game.
- "Where"
	- Since the system uses the fingers as a way to identify gestures, the position of the hand in the frame is not necessarily important, as long as the fingers are visible in the picture. The system will annotate it as "visible" or "not visible"

### Parsing & Performance

A dozen of sample sequences are stored in 'imgs/Sequences/' folder, with the number 1 to 8 indicating sequences that were given proper answer, 9 to 10 indicating false negatives, 11 to 12 indicating false positives. The outputs are stored in 'imgs/Sequences/output' folder. Note that the false negatives & false positives are based on the gesture, not the system final output.

The system makes use of convex hull and convexity defects in the reduced pictures to detect number of fingers, and hence the gesture. Therefore, this would certainly create some limitations:
- The angle between the fingers needs to be not larger than 90 degrees to be recognized. The reason is that due to the natural shape of hands, there will be other convexity defects (e.g. wrists) other than space between fingers. Therefore, this would also require that the fingers to be placed in a natural way, not delibrately forcing the angle between to be larger than 90 degrees.
- A usual camera is a 2D picture taking device, therefore the hand gesture needs to be flat on the surface. A side view of a "Paper" will probably not recognize the fingers and therefore the gesture either. 
- The design of the grammar and method has some limitations as well. A palm gesture with thumb splayed out would probably be recognized as a "Scissor", because there exists a less than 90 degree angle between. Similarly, a "Paper" gesture with the four fingers holded together would probably have the same effect. To demonstrate these false positives/negatives, a collection of reduced pictures of failure examples are stored in 'examples/failures' folder.

### Creative Part

Real time gesture recognition enabled. After running the system, the system will try to detect the gesture, within the green frame in the pop-up UI, each time the 'c' button is pressed on the keyboard. Then the system will prompt in command line and output the gesture annotation. The built-in camera of the device is used.

The real time gesture recognition part right now is somewhat limited. The reduced picture is easily affected by the light reflections on the background, therefore it poses strict limits on the background used - black, unreflective. Based on different camera capturing devices, the lighting conditions, the system would possibly give answers that vary. 
