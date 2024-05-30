#### INSTRUCTIONS FOR MiRP v1.0 PROCESSING OF MTS #### Leah gheber/Alina Levitin 2024 #

Please follow the instructions in the Tutorial.pdf file.

------------------------------------------------------------------------------------------------------------------------

DEPENDENCIES AND COMMENTS

------------------------------------------------------------------------------------------------------------------------
- python=3.10
- RELION 4.0

The columns in the .STAR files are processed with starfile python library (current v0.5.8) and are referenced by name, so column numering shouldn't be a problem.
.MRC files are handled with mrcfile python library (current v1.5.0).
Some steps require RELION installed therefore needs to be run on a computer with RELION.
RELION is unable to read .STAR files that were created on windows (only linux is compatible).

		
------------------------------------------------------------------------------------------------------------------------

DATA OPTIMISATION

------------------------------------------------------------------------------------------------------------------------

The following can be used to try and improve your data once you have your rough alignment parameters and you have moved to 1xbinned data, either before or between iterations of the high-resolution refinement step.
The use of these steps depends hugely on your sample/data.

1. You can try running an additional supervised 3D classification of 2 references: one with decorating protein and one without (just tubulin). 
In my hands this gives you a class with good decoration and one with poor decoration. Do a further refinement on the class with good decoration. This will probably give you a better decorated map and perhaps a better seam but perhaps at the cost of resolution if you don't have many particles.

2. Try iterative rounds of Bayesian Polishing,CTF Refinement and local refinement- can improve reconstruction resolution.

3. Try running a 3D classification with no alignment with 2 classes with your output reconstruction as a reference you will get poorly aligned particles coming out in one of the 2 classes (class will look poor)- then you can keep the good particles.

4. You can manually check particles by plotting ROT angles against particle numbers and checking you have straight lines within particle from each microtubule. This is a good way to check the protocol has worked well for your dataset. To make the plots, you could either use a standard data analysis program like Excel or Prism, or use the mirpy.py script (python mirpy.py -p *_data.star).

The following should be used at earlier stages of the process;

5. You may want to remove short microtubules from your dataset if you are unconvinced by the angular and translational assignments, as a) shorter microtubules give less statistical certainty for pf number/seam allocations and b) particles towards the ends of MTs include less averaged particles in their segment averages and thus have lower signal to noise. The mirpy.py script can be used for this (e.g for minimum length 10 particles; python mirpy.py -s *_data.star -lw 10)

6. You can pick individual MTs based on how internally consistent (particles within a single MT) their protofilament number sorting or seam check class allocations were. This will probably give you a better seam but sometimes at the cost of resolution if you are low on particles. You can use the mirpy.py script can be used for this, to show confidence plots and/or provide a cutoff (e.g to make a confidence plot; python mirpy.py -c run_it001_data.star, to cutoff MTs below 50% confidence of a class assignment; python mirpy.py -c run_it001_data.star -lw 50).
