# Emailer Generic
  - This uses two config.json file to drop customized mails to a list of recipients
  - **Root config.json** is primarily used for keyed lookup of the other config.json file
  - ```json
  {
    "late" : "~/TA/TA/Email/Configs/Late/config.json"
  }
```
  - With this in the root config.json we can run the emailer as
  - ```bash
  python -m TA.Email.EmailGeneric --pathOrName late
```
  - **Config.json** The other config file has following structure
  - ```json
  {
    "template_path": "~/TA/TA/Email/Configs/Late/email.tml",
    "mail_subject": "Activity Plan Due",
    "from": "apokhriy@uncc.edu",
    "cc": ["apokhriy@uncc.edu"],
    "bcc": [],

    "recipients": [{
      "First Name": "ABC",
      "Last Name": "DEF",
      "Email": "abcdef@uncc.edu",
      "Internship Start Date": "01-01-20"
    }]
    }
```
    - **template_path** = Absolute Path to the email template to be used
    - **recipients** = Each of the recipients object in the list should contain the variables needed in the email template
    - **template file** is free flowing text with curly braces {} used for variable substitution
    - ```
      Hey {First Name} {Last Name},

      Base on our records your internship started on {Internship Start Date} but you haven't yet submitted the activity plan.
      If your dates have changed please let me know.
      Mention the new internship start date and the tentative date by which you will be able to turn in the activity plan.

      Thank You
```
