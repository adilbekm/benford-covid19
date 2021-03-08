# Benford's Law Applied to COVID-19 Reports

**A look at COVID-19 case reports from around the world to see how well the numbers of daily positive cases fit into Benford's Law. The better the fit, the more accurate the data.**

### What is Benford's Law?

Numbers that represent real-life events follow a certain regularity. Specifically, the first digit of these numbers follows a strange pattern with the number 1 appearing about 30% of the time, the number 2 about 18% of the time, etc.— a frequency that declines logarithmically. This pattern is known as Benford's Law, and it can be used to identify fraud and other irregularities with reported numbers. To learn more, see this [wikipedia page](https://en.wikipedia.org/wiki/benford's_law) or the 2020 Netflix show [Connected](https://www.netflix.com/title/81031737) (episode "Digits").

### How does it apply to COVID-19 reports?

COVID-19 reports are made of numbers just like any other reports created by people, and that makes it possible to apply Benford's Law. I obtained the daily positive case numbers for the U.S. from [The Covid Tracking Project](https://covidtracking.com/), and for countries around the world from [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19), and calculated the frequency of numbers 1 to 9 in the first digit of the numbers. I compared the results to the expected, or Benford, frequency to get the **Benford Error**—the difference between the actual frequency and the frequency expected by Benford's Law. This error tells how good or bad the data for the location is.

For example, England, UK has reported a total of 266 numbers of daily positive cases of COVID-19 since they started reporting as a standalone location on June 11, 2020. Here are the recent 10 of them: 7393, 6527, 5080, 4738, 5530, 5408, 5643, 5053, 5118, 4497. If you look at each of these 266 numbers, you will find that the number 1 is in the first digit 0.3609 (36.09%) of the time, the number 2 — 0.1616 (16.16%) of the time, and so on. But Benford's Law states that the number 1 should be found in the first digit 0.3010 (30.10%) of the time, the number 2 — 0.1761(17.61%) of the time, etc. So England's report is off by 0.0599 for the number 1, by 0.0144 for the number 2 (the sign of the difference doesn't matter), and so on. For all 9 numbers, their report is off by 0.1673 and that is their Benford Error.

![England][plt1]

### What are the results?

Using the Benford Error, I ranked the locations from best (smallest error) to worst (largest error), and created plots for each location that show the error visually. 

USA:

```
1. Oregon (OR), e=0.08907
2. Arizona (AZ), e=0.09232
3. Guam (GU), e=0.09745
4. Wyoming (WY), e=0.10585
5. District of Columbia (DC), e=0.10765
6. Montana (MT), e=0.12360
7. Utah (UT), e=0.12361
8. Kentucky (KY), e=0.12648
9. Rhode Island (RI), e=0.13078
10. Washington (WA), e=0.14144
11. North Dakota (ND), e=0.14186
12. Alaska (AK), e=0.15673
13. Delaware (DE), e=0.16011
14. Tennessee (TN), e=0.16071
15. Connecticut (CT), e=0.16143
16. Kansas (KS), e=0.16933
17. South Dakota (SD), e=0.17022
18. Alabama (AL), e=0.17037
19. Louisiana (LA), e=0.17428
20. Nevada (NV), e=0.18160
21. California (CA), e=0.18388
22. Wisconsin (WI), e=0.19119
23. North Carolina (NC), e=0.19838
24. Vermont (VT), e=0.20096
25. Georgia (GA), e=0.20259
26. Arkansas (AR), e=0.20706
27. Nebraska (NE), e=0.20751
28. Oklahoma (OK), e=0.21058
29. Puerto Rico (PR), e=0.21087
30. Mississippi (MS), e=0.21348
31. New Hampshire (NH), e=0.21545
32. Texas (TX), e=0.22084
33. Michigan (MI), e=0.22218
34. Hawaii (HI), e=0.22766
35. Ohio (OH), e=0.23136
36. South Carolina (SC), e=0.23540
37. West Virginia (WV), e=0.23874
38. Massachusetts (MA), e=0.24238
39. Idaho (ID), e=0.24322
40. Virginia (VA), e=0.25194
41. Florida (FL), e=0.27465
42. Iowa (IA), e=0.27841
43. Illinois (IL), e=0.30436
44. U.S. Virgin Islands (VI), e=0.31752
45. Maryland (MD), e=0.33492
46. Colorado (CO), e=0.34384
47. New Mexico (NM), e=0.34511
48. Missouri (MO), e=0.35060
49. Minnesota (MN), e=0.36201
50. Maine (ME), e=0.36231
51. Pennsylvania (PA), e=0.36497
52. Indiana (IN), e=0.39093
53. New York (NY), e=0.49235
54. New Jersey (NJ), e=0.55640
55. Northern Mariana Islands (MP), e=0.60669
```

World:

```
1. Jordan, e=0.05968
2. Ukraine, Sumy Oblast, e=0.06433
3. Malawi, e=0.06679
4. Australia, New South Wales, e=0.06832
5. Netherlands, Aruba, e=0.07150
6. Spain, C Valenciana, e=0.08373
7. Peru, Pasco, e=0.08763
8. Namibia, e=0.09391
9. Brazil, Maranhao, e=0.09535
10. Germany, Thuringen, e=0.09792

. . .

661. Russia, Volgograd Oblast, e=0.86618
662. Russia, Ulyanovsk Oblast, e=0.87538
663. Russia, Karachay Cherkess Republic, e=0.91830
664. Russia, Krasnoyarsk Krai, e=0.91867
665. Russia, Krasnodar Krai, e=0.93402
666. Russia, Novosibirsk Oblast, e=0.93850
667. Russia, Saratov Oblast, e=0.93990
668. Russia, Orenburg Oblast, e=0.94119
669. Tajikistan, e=0.98963
670. Russia, Mordovia Republic, e=1.01084
```

For full results, please see the following files:

`usa_rank.csv` — File showing how each U.S. state or territory ranks from best to worst, based on how their COVID-19 case numbers fit into Benford's Law. The last column has the file name with the Benford plot for the location.

`usa_output/` — Folder with Benford plots for U.S. states and territories.

`world_rank.csv` — File showing how each country and province ranks from best to worst, based on how their COVID-19 case numbers fit into Benford's Law. The file is searchable. The last column has the file name with the Benford plot for the location.

`world_output/` — Folder with Benford plots for world countries and their provinces.

To see the original data:

`usa_data/` — Folder with the original COVID-19 data for the U.S. from [The Covid Tracking Project](https://covidtracking.com/).

`extra/usa.csv` — A version of the U.S. data in a more concise format than the original data. 

`world_data/` — Folder with the original COVID-19 data for the world from [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19).

`extra/world.csv` — A version of the world data in a more concise format than the original data. 

### How to interpret the results?

Small errors mean the reported cases are likely to be true and accurate, and large errors indicate inaccuracy. Large errors can be a sign of insufficient testing, misreporting, or direct falsification.

For the U.S., the error ranges from 0.09 for Oregon to 0.56 for New Jersey. For the world, the error ranges from 0.06 for Jordan to 1.01 for Mordovia, Russia.

Example of small error (good Benford fit):

![Jordan][plt2]

Example of large error (bad Benford fit):

![Mordovia Russia][plt3]

### What time period is covered? How many numbers?

The data covers the period from the beginning of COVID-19 reporting in the early 2020 to March 7, 2021, or about 1 year of data or 365 numbers per location, 725 different locations (55 for the U.S. and 670 for the rest of the world). The exact number of numbers (no pun intended) varies by location because they didn't start reporting at the same time. It also varies because zeros and negative numbers are unusable and were dropped. The actual number of numbers used for Benford-ness is included in the output, so the reader can take this metric into account along with the error. About 100 locations were excluded from the ranking because they had too few numbers (less than 50 usable numbers). These are typically small territories or places like cruise ships.  

---

For questions or comments, please email <adilbekm@yahoo.com>

March 8, 2021

[plt1]: world_output/united_kingdom_england.png
[plt2]: world_output/jordan.png
[plt3]: world_output/russia_mordovia_republic.png

