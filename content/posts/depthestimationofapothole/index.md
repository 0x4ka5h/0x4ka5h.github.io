+++
title = "Depth Estimation of a Pothole on Roads"
description = "This project detects the potholes and estimate approximate depth of the detected potholes. And alert the driver based on the hazardness of the pothole."
date = 2021-12-31T07:34:48+08:30
featured = false
draft = false
comment = false
toc = false
reward = false
categories = [
]
tags = [
]
series = []
images = [""]
+++
### Introduction 
I knew you guys can't bear this much long gap for my presence with our new blogs. That's why this time I came up with a real-time developed project which is submitted to the Government of India.
A hackathon was conducted overall in India. After, 3 rounds of filtering we got selected for the semi-final round based on the prototype presentation. And we cleared that round with our prototype and as a result, we were gone into the finals. It's a hackathon called the Road Safety Hackathon conducted by the Ministry of Road Transport and Highways, Government of India.

As per recent studies, around 4000+ accidents (about 50% casualties) are observed due to potholes in India. However, this is only official data as per the available records. This doesn’t include the data related blaw, blaw, blaw.....  Fine. fine fine......  Shit comes with shit only. Then why discuss it again?
Already, we all know this shit of information cause we daily see accidents happen on roads due to bad infrastructure. That bad infrastructure leads us to create an application that is used for the Government of India by changing Road Infrastructure based on our stored data and vehicle driver to escape from accidents by following our commands. 

Chaaa....Chaa.. why have these people made mistakes related to vehicles, roads, and safety? I'm tired of solving these mistakes. I'll stop taking care about these problems and may be this is last blog about road safety, Accidents Prevention and things which are related with vehicles also.

Random Reader (RR) : "Author!! You always wasting our time by telling nonsence. Come to the point."


Me : "Damn. Seriously? Okay stop kicking my as*s. I will start."


RR : "lamo.. Quick."

### Our Aim

Deep learning and Web based voice alert system based on depth estimation and Hazardness of the detected potholes.

#### Brief Explanation of our Solution

Brief Explanation of our Solution

We created this application in two ways:

 1. Vehicles with Cameras and wifi connectors. These vehicles will detect potholes on road and send information to the cloud. The sent data will be categorized into levels of its hazardness. If it returns medium or high risk, then the system will estimate the pothole depth using Deep learning techniques. At, the same time driver also got an alert from the system when there is a high risk with depth.
2. Vehicles with no facilities can use their mobile phone to access our web application. After giving the destination location, our system will guide the driver in a very safe and best way to reach the destination safely. Here, also the alert will go through sound and the driver can also see maps to visualize the pothole's distance from our current location.


By alerting the driver when Potholes are ahead, we think they will care for us and take diversion or may go slowly to escape from accidents.




We have used YoLov5 for pothole detection purposes cause my personal computer can't bear for my model architecture and also it takes 3 days on CPU. So we would love to use predefined model. After a lot of case study about predefined models, YoLov5 become best match to our goal. But installing required softwares and libraries, we labeled them by hand on our dataset manually means picture by picture by drawing boxes. And we labeled potholes with 3 classes which are small, medium and risk. 

1





























##### Thanks for reading! {align=center}
