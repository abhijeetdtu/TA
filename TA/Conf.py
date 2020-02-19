import  os


class Config:
    studentSOTURL = "https://docs.google.com/spreadsheets/d/1xR9kGeVaMK8NvcwshLdVUNGl8EYb-sEbsvxRR1u5SgM/edit?usp=sharing"
    mentorResponseURL = "https://docs.google.com/spreadsheets/d/1V98hKtOW7FotTpKGhF8eMBB-tifsZ3NKzIG2DXR_hKU/edit#gid=2069876913"
    canvasLoginURL = "https://webauth.uncc.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1"
    courseURL = "https://uncc.instructure.com/courses/118638/"
    baseCourseURL = "https://uncc.instructure.com/courses/"

    courseAssignmentURL = courseURL + "assignments"
    API_URL = "https://uncc.instructure.com/api/v1/courses/{}/analytics"
    studentSummaryAnalyticsURL = API_URL + "/student_summaries?page=1&per_page=1000"
    assignmentSummaryAnalyticsURL = API_URL + "/assignments?async=0"
    
    CORRECTIONS = {
        "NINERIDS" : {
            "penmathsamanideepvarma" : "Manideep Varma Penmathsa"
        }
    }

    DATA_DUMP_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__) , "DataDump"))
