Mike:

I have saved the two python3 scripts required for the SG measurements and report generation in the following directories:

"SGmeasure.py" is in "/WFdata/Diagnostics/BPM_SGC/SG5_9_2025B"
"SGpdf.py" is in "/WFdata/Diagnostics/BPM_SGC/SG5_9_2025B/Images"

As you recall, we created the "SG5_9_2025B" subdirectory to hold all the data generated from this SG scan.  When a new SG scan is to be done, create a new subdirectory under "/WFdata/Diagnostics/BPM_SGC" of the form "SG<month>_<day>_<year>".  I usually add a "B" if it is a repeat of a previous scan.  The SG data collection should be performed under the following conditions:
1.	Copy the script "SGmeasure.py" into this new directory.
2.	All ID gaps set OPEN and all feedback system turned OFF except for Bunch-by-Bunch feedback.
3.	Storage Ring 1200 bunches filled with 2 or 3 complete passes over all bunches so that no particular bunch is much higher or lower that the others.  This usually requires a fill of between 60 and 70mA. 
4.	The stored beam is then scraped down to 33mA.
5.	BPM Autogain tool is turned OFF but Autogain CSS GUI need to be viewed.
6.	Set all BPMs to 0dB attenuation and check that no BPMs are saturated (ADC count = 255).  If any are saturated then you must scrape some more beam away.  In the Autogain GUI, look for the BPM with the high ADC count.  You want the highest BPM to have an ADC count above 200.  If it is below 200 then you will need to fill (evenly) some more beam and scrap down to a higher current.
7.	if all is well, start the script.  It will take about 20 minutes for the script to finish.

This script will create 4 subdirectories, namely:
•	"Data" which contains all the raw data collected from each BPM
•	"Old_SG_Tables" contains the original SG tables found in each BPM
•	"New_SG_Tables" contains the newly generated SG tables for each BPM
•	"Images" contains plots of all the collected data comparing the effect of the new SG table and the old AG table to the data generated by a unity gain SG table.  These images will be used in the SG report.

You should view every image in the "Images" directory looking for BPMs where there is a relatively large deviation between the data generated by the old SG table (RED trace) and the data generated by the new SG table (GREEN trace).  Note all the BPMs that have large deviations.  These BPMs will have their SG tables updated in the following manner:
1.	Telnet into the BPM through the MOXA port.
2.	Enter the command "sgain"
3.	From the "New_SG_Tables" directory, display the text file containing the new SG table for that BPM and copy and paste it into the telnet session.  You should see a sensible stream of data appear in the telnet session.  If it looks like there were errors then try again.  
4.	If it appears the table transfer went OK, enter the "reboot" command.  If you watch carefully you should see the new SG table scroll by as the BPM boots up.
5.	After the BPM has rebooted, go to the engineering CSS panel for that BPM and toggle the 3 reconnect buttons to reestablish the network connections to that BPM.
6.	Repeat for the other BPMs that require new SG tables installed.

If time allows, repeat this entire procedure to create a new SG scan of all SR BPMs.  This scan will be used to verify the effectiveness of the new SG tables just installed in some of the BPMs.  When this scan has completed compare the images from the previous scan to the images generated by this scan for all the updated BPMs.  You should see improvement in the form of less deviation between the RED and GREEN traces in these images.

Once the data is collected, copy the "SGpdf.py" code into the "Images" directory and run it there.  When the code finishes, a PDF file called "SGreport.pdf" should appear in the "Images" directory.  This PDF file is usually distributed to Danny and Guimei.

We should create a Git directory to archive all the data collected for each scan along with the scripts and report files.  Perhaps we can set that up next week.

Tony C.
