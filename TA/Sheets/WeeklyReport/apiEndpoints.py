

class ENDPOINTS:

    ASSIGNEMENTS = "https://uncc.instructure.com/api/v1/courses/{COURSE_ID}/assignment_groups?exclude_response_fields%5B%5D=description&exclude_response_fields%5B%5D=rubric&include%5B%5D=assignments&include%5B%5D=discussion_topic&include%5B%5D=all_dates&include%5B%5D=module_ids&override_assignment_dates=false&per_page=50"
    USERS_LIST = "https://uncc.instructure.com/api/v1/courses/{COURSE_ID}/users?include_inactive=true&include%5B%5D=avatar_url&include%5B%5D=enrollments&include%5B%5D=email&include%5B%5D=observed_users&include%5B%5D=can_be_removed&include%5B%5D=custom_links&per_page=200"
    USER_GRADES = "https://uncc.instructure.com/courses/{COURSE_ID}/grades/{{USER_ID}}"
    USER_SUBMISSION = "https://uncc.instructure.com/courses/{COURSE_ID}/assignments/{ASSIGNMENT_ID}/submissions/{USER_ID}"
