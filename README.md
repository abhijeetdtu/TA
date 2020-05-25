### Progress Report Text Analysis

```bash

#"Internship Activity Plan"
$reportName="Internship Activity Plan"
cd C:\Users\Abhijeet\Documents\GitHub\TA

.\taenv\Scripts\activate
# Make sure to have the virtualenv activated

python -m TA.Sheets.CreateProgressTrackerSheet --id 118638

python -m TA.TextAnalytics.ProgressReport --path-to-folder "C:/Users/Abhijeet/Documents/GitHub/TA/TA/Sheets/_tempWorkspace/118638/$reportName"

Copy-Item C:/Users/Abhijeet/Documents/GitHub/TA/TA/TextAnalytics/Output.html "C:/Users/Abhijeet/Documents/GitHub/TA/TA/TextAnalytics/$reportName.html"

Invoke-Item ".\TA\TextAnalytics\$reportName.html"
```


### Course Analytics

```bash

cd C:\Users\Abhijeet\Documents\GitHub\TA

.\taenv\Scripts\activate
# Make sure to have the virtualenv activated

python -m TA.Sheets.CourseAnalytics --courseId 87897
```
