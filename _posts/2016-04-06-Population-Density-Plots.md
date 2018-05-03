---
title:  "World Population Density Plots"
date:   2016-04-06 14:20:00
description: World population density calculated from the 2015 estimates provided by the CIA World Factbook with colorful plots
keywords: [Python, 2015 population density, 2016 population density, most populated countries, least crowded countries, cartopy, highest population density, lowest population density]
---
I enjoy to peruse the [CIA World Factbook](https://www.cia.gov/library/publications/resources/the-world-factbook/) from time to time. It reminds me of digging though a country specific atlas or encyclopedia. The other day I was looking at their [country comparison](https://www.cia.gov/library/publications/resources/the-world-factbook/rankorder/rankorderguide.html) feature and noticed they didn't have population density available, despite having estimates for country population and area. I went ahead and calculated the population density for the countries, and then made pretty plots (check out the full [imgur](https://imgur.com/a/Pb1i6) gallery) with various color maps of the world's population density. 

![2015 Approximate Population Density Plot](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_rainbow.png)

### Data
I pulled the [population data](https://www.cia.gov/library/publications/resources/the-world-factbook/rankorder/2119rank.html) and [area data](https://www.cia.gov/library/publications/resources/the-world-factbook/rankorder/2147rank.html) from the CIA World Factbook on March 28, 2016. Most of the data is based on 2015 estimates. There is an option to download the data as a tab separated list. I downloaded the data, converted the tab separated list to a comma separated list, and then imported the csv into Python. With Python I calculated the population density, and then used cartopy to plot the density maps with different matplotlib color maps. 

### Python
If we take a look at the data sets, we notice one has 257 entries, while the other has 238 countries. Some of the land area is wildlife reserves or unmanned territories, though neither would have a population. I took the country name to be the unique identify in both lists. Then I simply divided the population by the area. The result is the population density in number of people per square kilometer. I had to make an exception for Vatican City as it had an area of 0 km, and would result in an infinite population density. I exported the countries to a csv file which you can view [here](https://github.com/cjekel/countryPopulationDensity/blob/master/data/countryPopDensity.csv). I uploaded all of the source code, data, and images I generated to my [GitHub](https://github.com/cjekel/countryPopulationDensity). 

### Twenty most densely populated countries
Below are the 20 most densely populated countries. It is important to mention Vatican City as it has an area of 0 square kilometers, and thus results in an infinite population density, even if just one person is living there. South Korea which isn't mentioned comes in as the 22nd most densely populated country.

| Rank   |     Country     |  Population Density (people per sq km) |
|----------|:-------------:|:------:|
|  1 | Macau | 21169 |
|  2 | Monaco | 15268 |
|  3 | Singapore | 8141 |
|  4 | Hong Kong | 6445 |
|  5 | Gaza Strip | 5192 |
|  6 | Gibraltar | 4180 |
|  7 | Bahrain | 1772 |
|  8 | Maldives | 1320 |
|  9 | Malta | 1310 |
| 10 | Bermuda | 1230 |
| 11 | Bangladesh | 1173 |
| 12 | Sint Maarten | 1167 |
| 13 | Guernsey | 847 |
| 14 | Jersey | 839 |
| 15 | Barbados | 676 |
| 16 | Mauritius | 657 |
| 17 | Taiwan | 651 |
| 18 | Aruba | 623 |
| 19 | Lebanon | 595 |
| 20 | Saint Martin | 588 |

### Twenty least densely populated countries  
Below are the 20 least densely populated countries. Most of this data is based from 2015 estimates, I'll try to update it when the new 2016 estimates come out.

| Rank   |     Country     |  Population Density (people per sq km) |
|----------|:-------------:|:------:|
|  1 | Greenland | 0.026  |
|  2 | Svalbard | 0.030  |
|  3 | Falkland Islands (Islas Malvinas) | 0.276  |
|  4 | Pitcairn Islands | 1.021  |
|  5 | Mongolia | 1.913  |
|  6 | Western Sahara | 2.146  |
|  7 | Namibia | 2.684 |
|  8 | Australia | 2.939 |
|  9 | Iceland | 3.223 |
| 10 | Guyana | 3.420 |
| 11 | Mauritania | 3.490 |
| 12 | Canada | 3.515 |
| 13 | Suriname | 3.538 |
| 14 | Libya | 3.644 |
| 15 | Botswana | 3.752 |
| 16 | Niue | 4.577 |
| 17 | Gabon | 6.371 |
| 18 | Kazakhstan | 6.663 |
| 19 | Russia | 8.330 |
| 20 | Central African Republic | 8.654 |

### Plots
Using [Cartopy](https://scitools.org.uk/cartopy/), Python, and [Natural Earth](https://www.naturalearthdata.com/downloads/) I was able to plot the population densities with matplotlib on a world map. I used a normalized scale that went from 0 to 459 to base my color maps. Obvious countries such as Bangladesh have a population density great than 459. However most of the densely populated countries are small islands, so the color plots would have been dull and boring. I could have used a different scale, but non-linear scales can be difficult to follow.

I used the 1:50m scale data from Natural Earth Data. [Admin 0 – Countries](https://www.naturalearthdata.com/downloads/50m-cultural-vectors/) data list to be specific. Now this contains a bunch of attributes, including population estimates. Hindsight says I probably could have just used the data provided from Natural Earth, as this includes population estimates. That would have been much easier, as my unique identifier would have been inherent to the country shape data. I used the 'name_long' attribute to match the country name to the country name provided from the CIA World Factbook. This worked for about 200 of the countries. The rest of the countries I had to manually point to the shape data to the calculated population density. 

I created plots with a variety of different color maps that were available in Matplotlib. I created the images in png format, and also a vector pdf format. All the images can be found in [this](https://github.com/cjekel/countryPopulationDensity/tree/master/images) GitHub folder. If you haven't already, check out the full [imgur](https://imgur.com/a/Pb1i6) gallery! 

I've included some of the better images bellow. 

![Rainbow Population Density](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_rainbow.png)
![YlOrRd Population Density](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_YlOrRd.png)
![YlGnBu Population Density](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_YlGnBu.png)
![winter Population Density](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_winter.png)
![viridis Population Density](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_viridis.png)
![terrain Population Density](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_terrain.png)
![summer Population Density](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_summer.png)
![RdPu Population Density](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_RdPu.png)
![PuBuGn Population Density](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_PuBuGn.png)
![plasma Population Density](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_plasma.png)
![Greys Population Density](https://github.com/cjekel/countryPopulationDensity/raw/master/images/worldPopulationDensity2015_Greys.png)

Please comment if you enjoyed this post!

