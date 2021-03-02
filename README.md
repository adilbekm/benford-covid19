# Benford's Law Applied to COVID-19 Reports

**A look at COVID-19 case reports around the world to see how well the numbers of daily positive cases fit into Benford's Law. The better the fit, the more likely the data for the location to be accurate and trustworthy.**

### What is Benford's Law?

Numbers that represent real-life events follow a certain regularity. Specifically, the first digit of these numbers follows a strange pattern with the number 1 appearing about 30% of the time, the number 2 about 18% of the time, etc. — a frequency that declines in a logarithmic way. This pattern is known as the Benford's Law, and it can be used to identify fraud and other irregularities with reported numbers. To learn more, see this [wikipedia page](https://en.wikipedia.org/wiki/benford's_law).

### How does it apply to COVID-19 reports?

COVID-19 reports are made of numbers just like financial reports, and that makes it possible to apply Benford's Law. I obtained the daily positive case numbers for the U.S. (from [Covid Tracking Project](https://covidtracking.com/)) and countries around the world (from [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)). For each location, I computed the frequency of numbers 1 to 9 in the first digit of the positive case numbers, and compared it the Benford frequency — the difference is the Benford error. I used this error to rank the locations from best (smallest error) to worst (largest error), and created plots for each location that show the error from Benford visually.

### What are the results?

`usa_rank.csv` — Use this file to see how each U.S. state or territory ranks from best to worst, based on how their COVID-19 case numbers fit into Benford's Law. The last column has the file name with the Benford plot for the location.

`usa_output/` — Folder containing Benford plots for U.S. states and territories.

`world_rank.csv` — Use this file to see how each country and province ranks from best to worst, based on how their COVID-19 case numbers fit into Benford's Law. The last column has the file name with the Benford plot for the location.

`world_output/` — Folder containing Benford plots for world countries and their provinces.

**To see original reports:**

`usa_data/` — Folder with original COVID-19 data for the U.S. from [Covid Tracking Project](https://covidtracking.com/).

`world_data/` — Folder with original COVID-19 data for the world from [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19).

`extra/world.csv` — File with the world data in a more concise way than the original data. 

### How to interpret the results?

Small errors mean the reported cases are likely to be true and accurate, and large errors indicate increased inaccuracy. Large errors can be a sign of insufficient testing, misreporting, or direct falsification.

For the U.S., the error ranges from 0.08 for Oregon to 0.55 for New Jersey. For the world, the error ranges from 0.06 for Jordan to 1.05 for Mordovia, Russia.

Example of small error (good Benford fit):

![Australia New South Wales][plt1]

Example of large error (bad Benford fit):

![Tajikistan][plt2]


---


For questions or comments, please email <adilbekm@yahoo.com>.

February 28, 2021

[plt1]: world_output/australia_new_south_wales.png
[plt2]: world_output/tajikistan.png

