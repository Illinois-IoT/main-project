# Surg
Alarm Clock 

Utilizes HAAR CASCADE on face detection to identify if a person can be found in a burst of images.

Steps:

Use a multitude of functions to identify a person is still in their bed

- Identify if motion exists in an image burst
- Identify if a person's face is found
    - front of head
    - side of head
    - back of head
- set user operated parameters that allows motion to be set at specific times
    - internally will need to use a cronjob
    
    
