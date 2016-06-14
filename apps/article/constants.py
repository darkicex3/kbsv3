DEFAULT_TAG_ID = 1
DEFAULT_AUTHOR_ID = 1
DEFAULT_FEEDBACK_ID = 1

is_public_info = "Uncheck this box if you want to specified which groups or users are allowed to access this article."
description_help = "If omitted, the description will be determined by the first bit of the article's content."
keywords_help = "If omitted, the keywords will be the same as the article tags."
tags_help = "Tags that describe this article."
auto_tag_help = "Check this if you want to automatically assign any existing tags to this article based on its content."
followup_for_help = "Select any other articles that this article follows up on."
publish_date_help = "By default the article will be publish once you publish the article. But you can set your own date" \
                    " to publish this article later automatically."
expiration_date = "Leave blank if the article does not expire."
group_help = "Choose one or several group you want to allow access to this specific article."
help_option_content = "Check this box if you want to create an article from a PDF file. In this case you can let" \
                      " the title empty and it will be replaced by the file name (NOT RECOMMENDED)."
help_option_url = "Check this box if you want to create an article from a website. In this case when the user click on" \
                  "the article he will be directly redirect to the url you entered."
by_users_info = "Check this box if you want to authorized specific users."
by_groups_info = "And this one if you want to authorized specific groups."
ess_help = "Do you think this article is extremly IMPORTANT ?"

INJURIES = ""
NEGATIVE_WORDS = ""
MSG_VIEW_ALERT = ""
MSG_USELESS_ALERT = ""

STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
)

RATE_CHOICES = (
    ('0', 'Very Dissatisfied'),
    ('1', 'Dissatisfied'),
    ('2', 'Neutral'),
    ('3', 'Satisfied'),
    ('4', 'Very Satisfied'),
)

TYPE_CHOICES = (
    ('0', 'Right Answer'),
    ('1', 'Wrong Answer'),
)
