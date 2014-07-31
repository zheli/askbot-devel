"""
General skin settings
"""
from askbot.conf.settings_wrapper import settings
from askbot.deps.livesettings import ConfigurationGroup
from askbot.deps.livesettings import values
from django.utils.translation import ugettext_lazy as _
from askbot.skins import utils as skin_utils
from askbot import const
from askbot.conf.super_groups import CONTENT_AND_UI

WORDS = ConfigurationGroup(
                    'WORDS',
                    _('Site terms vocabulary'),
                    super_group = CONTENT_AND_UI
                )

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ASK_YOUR_QUESTION',
        default=_('Ask Your Question'),
        description=_('Ask Your Question'),
        help_text=_('Used on a button')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_PLEASE_ENTER_YOUR_QUESTION',
        default=_('Please enter your question'),
        description=_('Please enter your question'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ASK_THE_GROUP',
        default=_('Ask the Group'),
        description=_('Ask the Group'),
        help_text=_('Used on a button')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_POST_YOUR_ANSWER',
        default=_('Post Your Answer'),
        description=_('Post Your Answer'),
        help_text=_('Used on a button')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ANSWER_YOUR_OWN_QUESTION',
        default=_('Answer Your Own Question'),
        description=_('Answer Your Own Question'),
        help_text=_('Used on a button')
    )
)

settings.register(
    values.LongStringValue(
        WORDS,
        'WORDS_INSTRUCTION_TO_ANSWER_OWN_QUESTION',
        default=_(
            '<span class="big strong">You are welcome to answer your own question</span>, '
            'but please make sure to give an <strong>answer</strong>. '
            'Remember that you can always <strong>revise your original question</strong>.'
        ),
        description=_('Instruction to answer own questions'),
        help_text=_('HTML is allowed')
    )
)

settings.register(
    values.LongStringValue(
        WORDS,
        'WORDS_INSTRUCTION_TO_POST_ANONYMOUSLY',
        default=_(
            '<span class="strong big">Please start posting anonymously</span> - '
            'your entry will be published after you log in or create a new account.'
        ),
        description=_('Instruction to post anonymously'),
        help_text=_('HTML is allowed')
    )
)

settings.register(
    values.LongStringValue(
        WORDS,
        'WORDS_INSTRUCTION_TO_GIVE_ANSWERS',
        default=_(
            'Please try to <strong>give a substantial answer</strong>, '
            'for discussions, <strong>please use comments</strong> and '
            '<strong>do remember to vote</strong>.'
        ),
        description=_('Instruction to give answers'),
        help_text=_('HTML is allowed')
    )
)

settings.register(
    values.LongStringValue(
        WORDS,
        'WORDS_INSTRUCTION_FOR_THE_CATEGORY_SELECTOR',
        default=_(
            'Categorize your question using this tag selector or '
            'entering text in tag box.'
        ),
        description=_('Instruction for the catogory selector'),
        help_text=_('Plain text only')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_EDIT_YOUR_PREVIOUS_ANSWER',
        default=_('Edit Your Previous Answer'),
        description=_('Edit Your Previous Answer'),
        help_text=_('Used on a button')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ASK_QUESTIONS',
        default=_('ask questions'),
        description=_('ask questions')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ASKED',
        default=_('asked'),
        description=_('asked'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ASKED_FIRST_QUESTION',
        default=_('Asked first question'),
        description=_('Asked first question')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ASKED_BY_ME',
        default=_('Asked by me'),
        description=_('Asked by me')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ASKED_A_QUESTION',
        default=_('Asked a question'),
        description=_('Asked a question')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ANSWERED_A_QUESTION',
        default=_('Answered a question'),
        description=_('Answered a question')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ANSWERED_BY_ME',
        default=_('Answered by me'),
        description=_('Answered by me')
    )
)


settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ACCEPTED_AN_ANSWER',
        default=_('accepted an answer'),
        description=_('accepted an answer')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_GAVE_ACCEPTED_ANSWER',
        default=_('Gave accepted answer'),
        description=_('Gave accepted answer')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ANSWERED',
        default=_('answered'),
        description=_('answered'),
    )
)

settings.register(
    values.LongStringValue(
        WORDS,
        'WORDS_QUESTIONS_COUNTABLE_FORMS',
        default=_('question\nquestions'),
        description=_('Countable plural forms for "queston"'),
        help_text=_('Enter one form per line, pay attention')
    )
)

settings.register(
    values.LongStringValue(
        WORDS,
        'WORDS_ANSWERS_COUNTABLE_FORMS',
        default=_('answer\nanswers'),
        description=_('Countable plural forms for "answer"'),
        help_text=_('Enter one form per line, pay attention')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_QUESTION_SINGULAR',
        default=_('question'),
        description=_('question (noun, singular)'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_QUESTION_PLURAL',
        default=_('questions'),
        description=_('questions (noun, plural)'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_UNANSWERED_QUESTION_SINGULAR',
        default=_('unanswered question'),
        description=_('unanswered question (singular)'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_UNANSWERED_QUESTION_PLURAL',
        default=_('unanswered questions'),
        description=_('unanswered questions (plural)'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ANSWER_SINGULAR',
        default=_('answer'),
        description=_('answer (noun, sungular)'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_QUESTION_VOTED_UP',
        default=_('Question voted up'),
        description=_('Question voted up'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ANSWER_VOTED_UP',
        default=_('Answer voted up'),
        description=_('Answer voted up'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_UPVOTED_ANSWER',
        default=_('upvoted answer'),
        description=_('upvoted answer'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_NICE_ANSWER',
        default=_('Nice Answer'),
        description=_('Nice Answer'),
        help_text='Badge name'
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_NICE_QUESTION',
        default=_('Nice Question'),
        description=_('Nice Question'),
        help_text='Badge name'
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_GOOD_ANSWER',
        default=_('Good Answer'),
        description=_('Good Answer'),
        help_text='Badge name'
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_GOOD_QUESTION',
        default=_('Good Question'),
        description=_('Good Question'),
        help_text='Badge name'
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_GREAT_ANSWER',
        default=_('Great Answer'),
        description=_('Great Answer'),
        help_text='Badge name'
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_GREAT_QUESTION',
        default=_('Great Question'),
        description=_('Great Question'),
        help_text='Badge name'
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_POPULAR_QUESTION',
        default=_('Popular Question'),
        description=_('Popular Question'),
        help_text='Badge name'
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_NOTABLE_QUESTION',
        default=_('Notable Question'),
        description=_('Notable Question'),
        help_text='Badge name'
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_FAMOUS_QUESTION',
        default=_('Famous Question'),
        description=_('Famous Question'),
        help_text='Badge name'
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_STELLAR_QUESTION',
        default=_('Stellar Question'),
        description=_('Stellar Question'),
        help_text='Badge name'
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_FAVORITE_QUESTION',
        default=_('Favorite Question'),
        description=_('Favorite Question'),
        help_text='Badge name'
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_UPVOTED_ANSWERS',
        default=_('upvoted answers'),
        description=_('upvoted answers'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_SHOW_ONLY_QUESTIONS_FROM',
        default=_('Show only questions from'),
        description=_('Show only questions from'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_PLEASE_ASK_YOUR_QUESTION_HERE',
        default=_('Please ask your question here'),
        description=_('Please ask your question here'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_THIS_QUESTION_HAS_BEEN_DELETED',
        default=_(
                'Sorry, this question has been '
                'deleted and is no longer accessible'
            ),
        description=_('This question has been deleted')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_PLEASE_ENTER_YOUR_QUESTION',
        default=_('Please enter your question'),
        description=_('Please enter your question'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_DELETE_YOUR_QUESTION',
        default=_('delete your question'),
        description=_('delete your question'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ASK_A_QUESTION_INTERESTING_TO_THIS_COMMUNITY',
        default=_('ask a question interesting to this community'),
        description=_('ask a question interesting to this community'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_NO_QUESTIONS_HERE',
        default=_('No questions here.'),
        description=_('No questions here.'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_PLEASE_FOLLOW_QUESTIONS',
        default=_('Please follow some questions or follow some users.'),
        description=_('Please follow some questions or follow some users.'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_PLEASE_FEEL_FREE_TO_ASK_YOUR_QUESTION',
        default=_('Please feel free to ask your question!'),
        description=_('Please feel free to ask your question!'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_SWAP_WITH_QUESTION',
        default=_('swap with question'),
        description=_('swap with question'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_REPOST_AS_A_QUESTION_COMMENT',
        default=_('repost as a question comment'),
        description=_('repost as a question comment'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ONLY_ONE_ANSWER_PER_USER_IS_ALLOWED',
        default=_('(only one answer per user is allowed)'),
        description=_('Only one answer per user is allowed'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ACCEPT_BEST_ANSWERS_FOR_YOUR_QUESTIONS',
        default=_('Accept the best answers for your questions'),
        description=_('Accept the best answers for your questions')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_AUTHOR_OF_THE_QUESTION',
        default=_('author of the question'),
        description=_('author of the question')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ACCEPT_OR_UNACCEPT_THE_BEST_ANSWER',
        default=_('accept or unaccept the best answer'),
        description=_('accept or unaccept the best answer')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ACCEPT_OR_UNACCEPT_OWN_ANSWER',
        default=_('accept or unaccept your own answer'),
        description=_('accept or unaccept your own answer'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_YOU_ALREADY_GAVE_AN_ANSWER',
        default=_('you already gave an answer'),
        description=_('you already gave an answer'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_GAVE_AN_ANSWER',
        default=_('gave an answer'),
        description=_('gave an answer'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ANSWER_OWN_QUESTIONS',
        default=_('answer own questions'),
        description=_('answer own questions'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ANSWERED_OWN_QUESTION',
        default=_('Answered own question'),
        description=_('Answered own question'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_REPOST_AS_A_COMMENT_UNDER_THE_OLDER_ANSWER',
        default=_('repost as a comment under older answer'),
        description=_('repost as a comment under older answer'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_INVITE_OTHERS_TO_HELP_ANSWER_THIS_QUESTION',
        default=_('invite other to help answer this question'),
        description=_('invite other to help answer this question'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_RELATED_QUESTIONS',
        default=_('Related questions'),
        description=_('Related questions'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_QUESTION_TOOLS',
        default=_('Question Tools'),
        description=_('Question Tools'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_THIS_QUESTION_IS_CURRENTLY_SHARED_ONLY_WITH',
        default=_('Phrase: this question is currently shared only with:'),
        description=_('Phrase: this question is currently shared only with:'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_BE_THE_FIRST_TO_ANSWER_THIS_QUESTION',
        default=_('Be the first one to answer this question!'),
        description=_('Be the first one to answer this question!'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_FOLLOWED_QUESTIONS',
        default=_('followed questions'),
        description=_('followed questions'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_FOLLOW_QUESTIONS',
        default=_('follow questions'),
        description=_('follow questions'),
        help_text=_('Indefinite form')
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_COMMENTS_AND_ANSWERS_TO_OTHERS_QUESTIONS',
        default = '',
        description = _('Phrase: comments and answers to others questions'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_YOU_CAN_POST_QUESTIONS_BY_EMAILING_THEM_AT',
        default=_('You can post questions by emailing them at'),
        description=_('You can post questions by emailing them at'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_LIST_OF_QUESTIONS',
        default=_('List of questions'),
        description=_('List of questions'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_COMMUNITY_GIVES_YOU_AWARDS',
        default=_('Community gives you awards for your questions, answers and votes'),
        description=_('Community gives you awards for your questions, answers and votes'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_CLOSE_QUESTION',
        default=_('Close question'),
        description=_('Close question'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_CLOSE_QUESTIONS',
        default=_('close questions'),
        description=_('close questions'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_EDIT_QUESTION',
        default=_('Edit question'),
        description=_('Edit question'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_QUESTION_IN_ONE_SENTENCE',
        default=_('Question - in one sentence'),
        description=_('Question - in one sentence'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_RETAG_QUESTION',
        default=_('Retag question'),
        description=_('Retag question'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_RETAG_QUESTIONS',
        default=_('retag questions'),
        description=_('retag questions'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_REOPEN_QUESTION',
        default=_('Reopen question'),
        description=_('Reopen question'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_THERE_ARE_NO_UNANSWERED_QUESTIONS_HERE',
        default=_('There are no unanswered questions here'),
        description=_('There are no unanswered questions here'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_THIS_ANSWER_HAS_BEEN_SELECTED_AS_CORRECT',
        default=_('this answer has been selected as correct'),
        description=_('this answer has been selected as correct'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_MARK_THIS_ANSWER_AS_CORRECT',
        default=_('mark this answer as correct'),
        description=_('mark this answer as correct'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_LOGIN_SIGNUP_TO_ANSWER',
        default=_('Login/Signup to Answer'),
        description=_('Login/Signup to Answer'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_YOUR_ANSWER',
        default=_('Your Answer'),
        description=_('Your Answer'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ADD_ANSWER',
        default=_('Add Answer'),
        description=_('Add Answer'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_GIVE_AN_ANSWER_INTERESTING_TO_THIS_COMMUNITY',
        default=_('give an answer interesting to this community'),
        description=_('give an answer interesting to this community'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_GIVE_AN_ANSWER_INTERESTING_TO_THIS_COMMUNITY',
        default=_('give an answer interesting to this community'),
        description=_('give an answer interesting to this community'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_GIVE_A_GOOD_ANSWER',
        default=_('give a substantial answer'),
        description=_('give a substantial answer'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_TRY_TO_GIVE_AN_ANSWER',
        default=_('try to give an answer, rather than engage into a discussion'),
        description=_('try to give an answer, rather than engage into a discussion'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_SHOW_ONLY_SELECTED_ANSWERS_TO_ENQUIRERS',
        default=_('show only selected answers to enquirers'),
        description=_('show only selected answers to enquirers'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_UNANSWERED',
        default = _('UNANSWERED'),
        description = _('UNANSWERED'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_EDIT_ANSWER',
        default=_('Edit Answer'),
        description=_('Edit Answer'),
    )
)

settings.register(
    values.StringValue(
        WORDS,
        'WORDS_ANSWERED',
        default=_('Answered'),
        description=_('Answered'),
    )
)
