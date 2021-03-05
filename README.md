# Benford's Law Applied to COVID-19 Reports

**A look at COVID-19 case reports from around the world to see how well the numbers of daily positive cases fit into Benford's Law. The better the fit, the more accurate the data.**

March 3, 2021

### What is Benford's Law?

Numbers that represent real-life events follow a certain regularity. Specifically, the first digit of these numbers follows a strange pattern with the number 1 appearing about 30% of the time, the number 2 about 18% of the time, etc.— a frequency that declines logarithmically. This pattern is known as Benford's Law, and it can be used to identify fraud and other irregularities with reported numbers. To learn more, see this [wikipedia page](https://en.wikipedia.org/wiki/benford's_law) or the 2020 Netflix show [Connected](https://www.netflix.com/title/81031737) (episode "Digits").

### How does it apply to COVID-19 reports?

COVID-19 reports are made of numbers just like any other reports created by people, and that makes it possible to apply Benford's Law. I obtained the daily positive case numbers for the U.S. from [The Covid Tracking Project](https://covidtracking.com/), and for countries around the world from [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19), and calculated the frequency of numbers 1 to 9 in the first digit of the numbers. I compared the results to the expected, or Benford, frequency to get the **Benford Error**—the difference between the actual frequency and the frequency expected by Benford's Law. This error tells how good or bad the data for the location is.

For example, England, UK has reported a total of 262 numbers of daily positive cases of COVID-19 since they started reporting as a standalone location on June 11, 2020. Here are the recent 10 of them: 10296, 8964, 8408, 9420, 7292, 8644, 8623, 7393, 6527, 5080. If you look at each of these 262 numbers, you will find that the number 1 is in the first digit 0.3664 (36.64%) of the time, the number 2 — 0.1641(16.41%) of the time, and so on. But Benford's Law states that the number 1 should be found in the first digit 0.3010 (30.10%) of the time, the number 2 — 0.1761(17.61%) of the time, etc. So England's report is off by 0.0654 for the number 1, by 0.0120 for the number 2 (the sign of the difference doesn't matter), and so on. For all 9 numbers, their report is off by 0.1602 and that is their Benford Error.

![England][plt1]

### What are the results?

Using the Benford Error, I ranked the locations from best (smallest error) to worst (largest error), and created plots for each location that show the error visually. 

`usa_rank.csv` — File showing how each U.S. state or territory ranks from best to worst, based on how their COVID-19 case numbers fit into Benford's Law. The last column has the file name with the Benford plot for the location.

`usa_output/` — Folder with Benford plots for U.S. states and territories.

`world_rank.csv` — File showing how each country and province ranks from best to worst, based on how their COVID-19 case numbers fit into Benford's Law. The file is searchable. The last column has the file name with the Benford plot for the location.

`world_output/` — Folder with Benford plots for world countries and their provinces.

To see original data:

`usa_data/` — Folder with the original COVID-19 data for the U.S. from [The Covid Tracking Project](https://covidtracking.com/).

`world_data/` — Folder with the original COVID-19 data for the world from [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19).

`extra/world.csv` — A version of the world data in a single file, showing the data in a more concise way than the original data. 

### How to interpret the results?

Small errors mean the reported cases are likely to be true and accurate, and large errors indicate inaccuracy. Large errors can be a sign of insufficient testing, misreporting, or direct falsification.

For the U.S., the error ranges from 0.08 for Oregon to 0.55 for New Jersey. For the world, the error ranges from 0.06 for Jordan to 1.03 for Mordovia, Russia.

Example of small error (good Benford fit):

![Jordan][plt2]

Example of large error (bad Benford fit):

![Mordovia Russia][plt3]

### What time period is covered? How many numbers?

The data covers the period from the beginning of COVID-19 reporting in the early 2020 to March 3, 2021, or about 1 year of data or 365 numbers per location, 725 different locations (55 for the U.S. and 670 for the rest of the world). The exact number of numbers (no pun intended) varies by location because they didn't start reporting at the same time. It also varies because zeros and negative numbers are unusable and were dropped. The actual number of numbers used for Benford-ness is included in the output, so the reader can take this metric into account along with the error. About 100 locations were excluded from the ranking because they had too few numbers (less than 50 usable numbers). These are typically small territories or places like cruise ships.  

---

For questions or comments, please email <adilbekm@yahoo.com>

[plt1]: world_output/united_kingdom_england.png
[plt2]: world_output/jordan.png
[plt3]: world_output/russia_mordovia_republic.png

