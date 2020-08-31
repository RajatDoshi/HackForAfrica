# TellusDoc
## 
Built with :heart: by Ashwin Agnihotri, Rajat Doshi, Roshan Warman, Sukesh Ram.
## 
## Inspiration
The amount of elective procedures in the United States and other countries has dropped significantly as a result of COVID-19. Consequently, doctors who are not actively working with COVID-19 patients are seeing far less work throughput. Meanwhile, Africa has a quarter of the global disease burden but **only 2% of the world’s doctors**. Further, in developing countries, making behavior changes to reduce the reproduction rate is significantly harder, making COVID-19, among other infectious diseases, significantly more potent. Doctors in the U.S. could help those in developing countries suffering from pandemics such as Ebola or COVID-19, but **often lack the ability or funding** to actually connect with and help them. 

Our platform directly **virtually connects American physicians to the patients in Africa**, enabling them to perform telemedicine in their added “free time” from the decrease in elective procedures in their own country. With our platform, American doctors can see patients and prescribe critical treatments, even from thousands of miles away. This process also **alleviates congestion in healthcare systems** by leaving doctors physically present in those countries to focus on the high priority cases, leaving no one behind. Further, crucial and time-critical data like X-rays and blood test results can be **analyzed quickly**, saving lives. 


**btw** "Tellus" in Latin means Earth - the name "TellusDoc" signifies our mission to connect doctors and patients around the globe. TellusDoc bridges the gap between the surplus of American doctors and the shortage of doctors in Africa.



## What it does
In the modern age of telemedicine, it's vital that the services provided by so many doctors around the world can be afforded by those who require them. We provide a self-contained platform for this entire telemedicine process, which also breaks the information and literacy barrier which many of the patients in Africa face. This includes evaluating the patient's clinical status, scheduling them with an appropriate specialist, and providing a video and message interface with built-in transcription and language accommodations. Our user portals allow patients and doctors to keep track of their past and future appointments and also provide an avenue for patients to upload pertinent medical files for their doctor’s reference. We also ensure that the patients who need the most urgent care are matched up with doctors who can best help them through our state-of-the-art triage system. By incorporating both a severity classification, through our preliminary AI diagnoser, and a specialist matching system, we make this possible.

## How we built it
We leveraged **Python Flask** for web app development, using **HTML, Jinja, and CSS** tools to design the various website pages. 

Our platform’s more advanced functions involved **Python and Javascript** API calls, as well as several JS scripts for functions on the page, while the backend relies on **Firebase**. 

Our self-sustainable video chat feature is run in the browser through **websockets**, and a server locally hosted. We use **WebRTC and RecordRTC APIs** to stream audio and video.  

The text-to-speech functionality used the **Mozilla Developer Network Speech Synthesis API**. 

We used **Google Speech-to-text API** for our video call transcription, **Microsoft Azure Translator API** for web page translation, and **API-Medic Symptom Checking API** for the preliminary diagnoses.
 
## Challenges we ran into
Synchronizing scheduling pages via Firebase

Refining our Triage System algorithm

Incorporating the self-sustainable video chat feature

Streaming in browser audio in appropriate format to google speech API

UX of calendar scheduling

## Accomplishments that we're proud of
**Conquering Barriers:** 
**Translation and Transcription Services** allow our site content to be translated and spoken in the user’s native language.

**In-browser video calling service** allows for digital appointments to be directly held on our web app. 

**Direct Messaging System** allows patients to speak to past and current doctors and doctors to speak to all of their patients. 

**Instant File Transfer** allows doctors and patients to securely and reliably send medical information. 

**Quick AI Diagnostics** allows for patients to receive a free, instant diagnosis and for doctors to confirm their medical recommendations. 

**Integrated Patient Portal** allows doctors to access all of their current patients key information (name, condition, condition’s severity, AI Diagnosis, Appointment Date) in one concise interface. Additionally, clicking on the patient’s name will redirect doctor to their recent messages and clicking on the condition will redirect to a medical article (e.g. WebMD, HealthLine) on the topic. 

**Appointment Scheduling Algorithm:** matches patients to doctors, factoring in schedule compatibility, doctor’s speciality/patient’s condition, and severity. 

## What we learned
How to build intricate web applications with **API integration**, highly efficient **backend logic in Firebase**, and a **user-friendly frontend interface via Flask**.  

## What's next for TellusDoc
We are planning on building out a full fledged nonprofit, with additional features such as: order and delivery system for doctors to send critical health supplies based on telemedicine consultation and nurses portal. 

## Try it Out
http://tellusdoc.pythonanywhere.com/

## License
This software is protected under an MIT License.
