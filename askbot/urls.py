"""
askbot url configuraion file
"""
import os.path
import django
from django.conf import settings

try:
    from django.conf.urls import url, patterns, include
    from django.conf.urls import handler404
except ImportError:
    from django.conf.urls.defaults import url, patterns, include
    from django.conf.urls.defaults import handler404

from django.contrib import admin
from askbot import views
from askbot.feed import RssLastestQuestionsFeed, RssIndividualQuestionFeed
from askbot.sitemap import QuestionsSitemap
from askbot.skins.utils import update_media_revision
from askbot.utils.url_utils import service_url

admin.autodiscover()
#update_media_revision()#needs to be run once, so put it here
if getattr(settings, "ASKBOT_TRANSLATE_URL", False):
    from django.utils.translation import pgettext
else:
    pgettext = lambda context, value: value

feeds = {
    'rss': RssLastestQuestionsFeed,
    'question':RssIndividualQuestionFeed
}
sitemaps = {
    'questions': QuestionsSitemap
}

#prefix is optional, recommended when a variable url prefix
#is used to subdivide the forum into namespaces
#in this case it is safer to use a special prefix to all urls
#except those that are namespaced
PREFIX = getattr(settings, 'ASKBOT_SERVICE_URL_PREFIX', '')

MAIN_PAGE_BASE_URL = getattr(
                        settings, 
                        'ASKBOT_MAIN_PAGE_BASE_URL',
                        pgettext('urls', 'questions')
                    ).strip('/') + '/'
QUESTION_PAGE_BASE_URL = getattr(
                        settings,
                        'ASKBOT_QUESTION_PAGE_BASE_URL',
                        pgettext('urls', 'question')
                    ).strip('/') + '/'

APP_PATH = os.path.dirname(__file__)
urlpatterns = patterns('',
    url(r'^$', views.readers.index, name='index'),
    # BEGIN Questions (main page) urls. All this urls work both normally and through ajax
    url(
        # Note that all parameters, even if optional, are provided to the view. Non-present ones have None value.
        (r'^%s' % MAIN_PAGE_BASE_URL.strip('/') +
            r'(%s)?' % r'/scope:(?P<scope>\w+)' +
            r'(%s)?' % r'/sort:(?P<sort>[\w\-]+)' +
            r'(%s)?' % r'/tags:(?P<tags>[\w+.#,-]+)' + # Should match: const.TAG_CHARS + ','; TODO: Is `#` char decoded by the time URLs are processed ??
            r'(%s)?' % r'/author:(?P<author>\d+)' +
            r'(%s)?' % r'/page:(?P<page>\d+)' +
            r'(%s)?' % r'/page-size:(?P<page_size>\d+)' +
            r'(%s)?' % r'/query:(?P<query>.+)' +  # INFO: query is last, b/c it can contain slash!!!
        r'/$'),
        views.readers.questions,
        name='questions'
    ),
    url(
        r'^%s(?P<id>\d+)/' % QUESTION_PAGE_BASE_URL,
        views.readers.question,
        name='question'
    ),
    url(
        r'^%s$' % pgettext('urls', 'tags/'),
        views.readers.tags,
        name='tags'
    ),
    url(
        r'^%s$' % pgettext('urls', 'users/'),
        views.users.show_users,
        name='users'
    ),
    url(
        r'^%s%s(?P<group_id>\d+)/(?P<group_slug>.*)/$' % (
                                            pgettext('urls', 'users/'), 
                                            pgettext('urls', 'by-group/')
                                        ),
        views.users.show_users,
        kwargs = {'by_group': True},
        name = 'users_by_group'
    ),
    #todo: rename as user_edit, b/c that's how template is named
    url(
        r'^%s(?P<id>\d+)/%s$' % (pgettext('urls', 'users/'), pgettext('urls', 'edit/')),
        views.users.edit_user,
        name ='edit_user'
    ),
    service_url(#ajax post only
        r'^users/set-primary-language$',
        views.users.user_set_primary_language,
        name='user_set_primary_language'
    ),
    url(
        r'^%s(?P<id>\d+)/(?P<slug>.+)/%s$' % (
            pgettext('urls', 'users/'),
            pgettext('urls', 'subscriptions/'),
        ),
        views.users.user,
        kwargs = {'tab_name': 'email_subscriptions'},
        name = 'user_subscriptions'
    ),
    url(
        r'^%s(?P<id>\d+)/(?P<slug>.+)/%s$' % (
            pgettext('urls', 'users/'),
            pgettext('urls', 'select_languages/'),
        ),
        views.users.user_select_languages,
        name = 'user_select_languages'
    ),
    url(
        r'^%s(?P<id>\d+)/(?P<slug>.+)/$' % pgettext('urls', 'users/'),
        views.users.user,
        name='user_profile'
    ),
    url(
        r'^%s$' % pgettext('urls', 'groups/'),
        views.users.groups,
        name='groups'
    ),
    url(
        r'^%s$' % pgettext('urls', 'badges/'),
        views.meta.badges,
        name='badges'
    ),
    url(
        r'^%s(?P<id>\d+)//*' % pgettext('urls', 'badges/'),
        views.meta.badge,
        name='badge'
    ),
    url(
        r'^sitemap.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps},
        name='sitemap'
    ),
    #feeds
    url(r'^feeds/rss/$', RssLastestQuestionsFeed(), name="latest_questions_feed"),
    url(r'^feeds/question/(?P<pk>\d+)/$', RssIndividualQuestionFeed(), name="individual_question_feed"),
    url(r'^%s$' % pgettext('urls', 'feedback/'), views.meta.feedback, name='feedback'),
    url(
        '^custom\.css$',
        views.meta.config_variable,
        kwargs = {
            'variable_name': 'CUSTOM_CSS',
            'mimetype': 'text/css'
        },
        name = 'custom_css'
    ),
    url(
        '^custom\.js$',
        views.meta.config_variable,
        kwargs = {
            'variable_name': 'CUSTOM_JS',
            'mimetype': 'text/javascript'
        },
        name = 'custom_js'
    ),
    service_url(r'^translate-url/', views.commands.translate_url, name='translate_url'),
    service_url(r'^reorder-badges/', views.commands.reorder_badges, name='reorder_badges'),
    service_url(r'^import-data/$', views.writers.import_data, name='import_data'),
    service_url(r'^%s$' % pgettext('urls', 'about/'), views.meta.about, name='about'),
    service_url(r'^%s$' % pgettext('urls', 'faq/'), views.meta.faq, name='faq'),
    service_url(r'^%s$' % pgettext('urls', 'privacy/'), views.meta.privacy, name='privacy'),
    service_url(
        r'^%s$' % pgettext('urls', 'terms/'),
        views.meta.markdown_flatpage,
        kwargs={'setting_name': 'TERMS', 'page_class': 'terms-page'},
        name='terms'
    ),
    service_url(r'^%s$' % pgettext('urls', 'help/'), views.meta.help, name='help'),
    service_url(
        r'^%s(?P<id>\d+)/%s$' % (pgettext('urls', 'answers/'), pgettext('urls', 'edit/')),
        views.writers.edit_answer,
        name='edit_answer'
    ),
    service_url(
        r'^%s(?P<id>\d+)/%s$' % (pgettext('urls', 'answers/'), pgettext('urls', 'revisions/')),
        views.readers.revisions,
        kwargs = {'post_type': 'answer'},
        name='answer_revisions'
    ),
    service_url(
        r'^get-top-answers/',
        views.readers.get_top_answers,
        name='get_top_answers'
    ),
    # END main page urls
    service_url(
        r'^api/get_questions/',
        views.commands.api_get_questions,
        name='api_get_questions'
    ),
    service_url(
        r'^get-thread-shared-users/',
        views.commands.get_thread_shared_users,
        name='get_thread_shared_users'
    ),
    service_url(
        r'^get-thread-shared-groups/',
        views.commands.get_thread_shared_groups,
        name='get_thread_shared_groups'
    ),
    service_url(
        r'^moderate-group-join-request/',
        views.commands.moderate_group_join_request,
        name='moderate_group_join_request'
    ),
    service_url(
        r'^%s$' % pgettext('urls', 'moderation-queue/'),
        views.moderation.moderation_queue,
        name='moderation_queue'
    ),
    service_url(
        r'^moderate-post-edits/',
        views.moderation.moderate_post_edits,
        name='moderate_post_edits'
    ),
    service_url(
        r'^save-draft-question/',
        views.commands.save_draft_question,
        name = 'save_draft_question'
    ),
    service_url(
        r'^save-draft-answer/',
        views.commands.save_draft_answer,
        name = 'save_draft_answer'
    ),
    service_url(
        r'^share-question-with-group/',
        views.commands.share_question_with_group,
        name='share_question_with_group'
    ),
    service_url(
        r'^share-question-with-user/',
        views.commands.share_question_with_user,
        name='share_question_with_user'
    ),
    service_url(
        r'^get-users-info/',
        views.commands.get_users_info,
        name='get_users_info'
    ),
    service_url(
        r'^get-editor/',
        views.commands.get_editor,
        name='get_editor'
    ),
    service_url(
        r'^get-post-html/',
        views.readers.get_post_html,
        name='get_post_html'
    ),
    service_url(
        r'^%s%s$' % (MAIN_PAGE_BASE_URL, pgettext('urls', 'ask/')),
        views.writers.ask,
        name='ask'
    ),
    service_url(
        r'^%s(?P<id>\d+)/%s$' % (MAIN_PAGE_BASE_URL, pgettext('urls', 'edit/')),
        views.writers.edit_question,
        name='edit_question'
    ),
    service_url(#this url is both regular and ajax
        r'^%s(?P<id>\d+)/%s$' % (MAIN_PAGE_BASE_URL, pgettext('urls', 'retag/')),
        views.writers.retag_question,
        name='retag_question'
    ),
    service_url(
        r'^%s(?P<id>\d+)/%s$' % (MAIN_PAGE_BASE_URL, pgettext('urls', 'close/')),
        views.commands.close,
        name='close'
    ),
    service_url(
        r'^%s(?P<id>\d+)/%s$' % (MAIN_PAGE_BASE_URL, pgettext('urls', 'reopen/')),
        views.commands.reopen,
        name='reopen'
    ),
    service_url(
        r'^%s(?P<id>\d+)/%s$' % (MAIN_PAGE_BASE_URL, pgettext('urls', 'answer/')),
        views.writers.answer,
        name='answer'
    ),
    service_url(
        r'^merge-questions/',
        views.commands.merge_questions,
        name='merge_questions'
    ),
    service_url(#ajax only
        r'^vote$',
        views.commands.vote,
        name='vote'
    ),
    service_url(
        r'^%s(?P<id>\d+)/%s$' % (MAIN_PAGE_BASE_URL, pgettext('urls', 'revisions/')),
        views.readers.revisions,
        kwargs = {'post_type': 'question'},
        name='question_revisions'
    ),
    service_url(#ajax only
        r'^comment/upvote/$',
        views.commands.upvote_comment,
        name = 'upvote_comment'
    ),
    service_url(#ajax only
        r'^post/delete/$',
        views.commands.delete_post,
        name = 'delete_post'
    ),
    service_url(#ajax only
        r'^post_comments/$',
        views.writers.post_comments,
        name='post_comments'
    ),
    service_url(#ajax only
        r'^edit_comment/$',
        views.writers.edit_comment,
        name='edit_comment'
    ),
    service_url(#ajax only
        r'^comment/delete/$',
        views.writers.delete_comment,
        name='delete_comment'
    ),
    service_url(#ajax only
        r'^comment/get-text/$',
        views.readers.get_comment,
        name='get_comment'
    ),
    service_url(
        r'^comment/convert/$',
        views.writers.comment_to_answer,
        name='comment_to_answer'
    ),
    service_url(
        r'^answer/repost-as-comment-under-question/$',
        views.writers.repost_answer_as_comment,
        kwargs={'destination': 'comment_under_question'},
        name='repost_answer_as_comment_under_question'
    ),
    service_url(#post only
        '^answer/repost-as-comment-under-previous-answer/$',
        views.writers.repost_answer_as_comment,
        kwargs={'destination': 'comment_under_previous_answer'},
        name='repost_answer_as_comment_under_previous_answer'
    ),
    service_url(#post only
        r'^answer/publish/$',
        views.commands.publish_answer,
        name='publish_answer'
    ),
    service_url(
        r'^%s%s$' % (pgettext('urls', 'tags/'), pgettext('urls', 'subscriptions/')),
        views.commands.list_bulk_tag_subscription,
        name='list_bulk_tag_subscription'
    ),
    service_url(#post only
        r'^%s%s%s$' % (
            pgettext('urls', 'tags/'), 
            pgettext('urls', 'subscriptions/'), 
            pgettext('urls', 'delete/')
        ),
        views.commands.delete_bulk_tag_subscription,
        name='delete_bulk_tag_subscription'
    ),
    service_url(
        r'^%s%s%s$' % (
            pgettext('urls', 'tags/'), 
            pgettext('urls', 'subscriptions/'), 
            pgettext('urls', 'create/')
        ),
        views.commands.create_bulk_tag_subscription,
        name='create_bulk_tag_subscription'
    ),
    service_url(
        r'^%s%s%s(?P<pk>\d+)/$' % (
            pgettext('urls', 'tags/'), 
            pgettext('urls', 'subscriptions/'), 
            pgettext('urls', 'edit/')
        ),
        views.commands.edit_bulk_tag_subscription,
        name='edit_bulk_tag_subscription'
    ),
    service_url(
        r'^%s$' % pgettext('urls', 'suggested-tags/'),
        views.meta.list_suggested_tags,
        name = 'list_suggested_tags'
    ),
    service_url(#ajax only
        r'^%s$' % 'moderate-suggested-tag',
        views.commands.moderate_suggested_tag,
        name = 'moderate_suggested_tag'
    ),
    #todo: collapse these three urls and use an extra json data var
    service_url(#ajax only
        r'^%s%s$' % ('mark-tag/', 'interesting/'),
        views.commands.mark_tag,
        kwargs={'reason':'good','action':'add'},
        name='mark_interesting_tag'
    ),
    service_url(#ajax only
        r'^%s%s$' % ('mark-tag/', 'ignored/'),
        views.commands.mark_tag,
        kwargs={'reason':'bad','action':'add'},
        name='mark_ignored_tag'
    ),
    service_url(#ajax only
        r'^%s%s$' % ('mark-tag/', 'subscribed/'),
        views.commands.mark_tag,
        kwargs={'reason':'subscribed','action':'add'},
        name='mark_subscribed_tag'
    ),
    service_url(#ajax only
        r'^unmark-tag/',
        views.commands.mark_tag,
        kwargs={'action':'remove'},
        name='unmark_tag'
    ),
    service_url(#ajax only
        r'^set-tag-filter-strategy/',
        views.commands.set_tag_filter_strategy,
        name = 'set_tag_filter_strategy'
    ),
    service_url(
        r'^get-tags-by-wildcard/',
        views.commands.get_tags_by_wildcard,
        name = 'get_tags_by_wildcard'
    ),
    service_url(
        r'^get-tag-list/',
        views.commands.get_tag_list,
        name = 'get_tag_list'
    ),
    service_url(
        r'^load-object-description/',
        views.commands.load_object_description,
        name = 'load_object_description'
    ),
    service_url(#ajax only
        r'^save-object-description/',
        views.commands.save_object_description,
        name = 'save_object_description'
    ),
    service_url(#ajax only
        r'^add-tag-category/',
        views.commands.add_tag_category,
        name = 'add_tag_category'
    ),
    service_url(#ajax only
        r'^rename-tag/',
        views.commands.rename_tag,
        name = 'rename_tag'
    ),
    service_url(#
        r'^delete-tag/',
        views.commands.delete_tag,
        name = 'delete_tag'
    ),
    service_url(#ajax only
        r'^save-group-logo-url/',
        views.commands.save_group_logo_url,
        name = 'save_group_logo_url'
    ),
    service_url(#ajax only
        r'^delete-group-logo/',
        views.commands.delete_group_logo,
        name = 'delete_group_logo'
    ),
    service_url(#ajax only
        r'^add-group/',
        views.commands.add_group,
        name = 'add_group'
    ),
    service_url(#ajax only
        r'^toggle-group-profile-property/',
        views.commands.toggle_group_profile_property,
        name='toggle_group_profile_property'
    ),
    service_url(#ajax only
        r'^set-group-openness/',
        views.commands.set_group_openness,
        name='set_group_openness'
    ),
    service_url(#ajax only
        r'^edit-object-property-text/',
        views.commands.edit_object_property_text,
        name = 'edit_object_property_text'
    ),
    service_url(
        r'^get-groups-list/',
        views.commands.get_groups_list,
        name = 'get_groups_list'
    ),
    service_url(
        r'^toggle-follow-question/',
        views.commands.toggle_follow_question,
        name='toggle_follow_question'
    ),
    service_url(
        r'^swap-question-with-answer/',
        views.commands.swap_question_with_answer,
        name = 'swap_question_with_answer'
    ),
    service_url(
        r'^subscribe-for-tags/$',
        views.commands.subscribe_for_tags,
        name = 'subscribe_for_tags'
    ),
    service_url(
        r'get-html-template/',
        views.commands.get_html_template,
        name='get_html_template'
    ),
    service_url(#ajax only
        r'^messages/markread/$',
        views.commands.read_message,
        name='read_message'
    ),
    service_url(#ajax only
        r'^clear-new-notifications/$',
        views.users.clear_new_notifications,
        name='clear_new_notifications'
    ),
    service_url(#ajax_only
        r'^delete-notifications/$',
        views.users.delete_notifications,
        name='delete_notifications'
    ),
    service_url(#ajax only
        r'^save-post-reject-reason/$',
        views.commands.save_post_reject_reason,
        name='save_post_reject_reason'
    ),
    service_url(#ajax only
        r'^delete-post-reject-reason/$',
        views.commands.delete_post_reject_reason,
        name='delete_post_reject_reason'
    ),
    service_url(#ajax only
        r'^edit-group-membership/$',
        views.commands.edit_group_membership,
        name='edit_group_membership'
    ),
    service_url(#ajax only
        r'^join-or-leave-group/$',
        views.commands.join_or_leave_group,
        name = 'join_or_leave_group'
    ),
    #widgets url!
    service_url(
        r'^%s$' % (pgettext('urls', 'widgets/')),
        views.widgets.widgets,
        name = 'widgets'
    ),
    service_url(
        r'^%s%s(?P<widget_id>\d+)/$' % (
            pgettext('urls', 'widgets/'),
            pgettext('urls', 'ask/')
        ),
        views.widgets.ask_widget,
        name = 'ask_by_widget'
    ),
    service_url(
        r'^%s%s(?P<widget_id>\d+).js$' % (
            pgettext('urls', 'widgets/'),
            pgettext('urls', 'ask/')
        ),
        views.widgets.render_ask_widget_js,
        name = 'render_ask_widget'
    ),
    service_url(
        r'^%s%s(?P<widget_id>\d+).css$' % (
            pgettext('urls', 'widgets/'), 
            pgettext('urls', 'ask/')
        ),
        views.widgets.render_ask_widget_css,
        name = 'render_ask_widget_css'
    ),
    service_url(
        r'^%s%s%s$' % (
            pgettext('urls', 'widgets/'),
            pgettext('urls', 'ask/'),
            pgettext('urls', 'complete/')
        ),
        views.widgets.ask_widget_complete,
        name = 'ask_by_widget_complete'
    ),
    service_url(
        r'^%s(?P<model>\w+)/%s$' % (
            pgettext('urls', 'widgets/'),
            pgettext('urls', 'create/')
        ),
        views.widgets.create_widget,
        name = 'create_widget'
    ),
    service_url(
        r'^%s(?P<model>\w+)/%s(?P<widget_id>\d+)/$' % (
            pgettext('urls', 'widgets/'),
            pgettext('urls', 'edit/')
        ),
        views.widgets.edit_widget,
        name = 'edit_widget'
    ),
    service_url(
        r'^%s(?P<model>\w+)/%s(?P<widget_id>\d+)/$' % (
            pgettext('urls', 'widgets/'),
            pgettext('urls', 'delete/')
        ),
        views.widgets.delete_widget,
        name = 'delete_widget'
    ),
    service_url(
        r'^%s(?P<model>\w+)/$' % (pgettext('urls', 'widgets/')),
        views.widgets.list_widgets,
        name = 'list_widgets'
    ),
    service_url(
        r'^widgets/%s(?P<widget_id>\d+)/$' % MAIN_PAGE_BASE_URL,
        views.widgets.question_widget,
        name='question_widget'
    ),
    service_url(
        r'^get-perms-data/$',
        views.readers.get_perms_data,
        name='get_perms_data'
    ),
    service_url(
        r'^start-sharing-twitter/$',
        views.sharing.start_sharing_twitter,
        name='start_sharing_twitter'
    ),
    service_url(
        r'^save-twitter-access-token/$',
        views.sharing.save_twitter_access_token,
        name='save_twitter_access_token'
    ),
    service_url(#ajax post only
        r'^change-social-sharing-mode/$',
        views.sharing.change_social_sharing_mode,
        name='change_social_sharing_mode'
    ),
    #upload url is ajax only
    service_url(
        r'^%s$' % pgettext('urls', 'upload/'),
        views.writers.upload,
        name='upload'
    ),
    service_url(
        r'^doc/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': os.path.join(APP_PATH,'doc','build','html').replace('\\','/')},
        name='askbot_docs',
    ),
    service_url(
        r'^jsi18n/$',
        'django.views.i18n.javascript_catalog',
        {'domain': 'djangojs','packages': ('askbot',)},
        name = 'askbot_jsi18n'
    ),
    service_url(r'^private-messages/', include('group_messaging.urls')),
    service_url(r'^settings/', include('livesettings.urls')),
    service_url(r'^preview-emails/$', views.emails.list_emails, name='list_emails'),
    service_url(r'^preview-emails/(?P<slug>.+)/$', views.emails.preview_email, name='preview_email'),

    service_url('^api/v1/info/$', views.api_v1.info, name='api_v1_info'),
    service_url('^api/v1/users/$', views.api_v1.users, name='api_v1_users'),
    service_url('^api/v1/users/(?P<user_id>\d+)/$', views.api_v1.user, name='api_v1_user'),
    service_url('^api/v1/questions/$', views.api_v1.questions, name='api_v1_questions'),
    service_url('^api/v1/questions/(?P<question_id>\d+)/$', views.api_v1.question, name='api_v1_question'),
)

if 'askbot.deps.django_authopenid' in settings.INSTALLED_APPS:
    urlpatterns += (
        service_url(
            r'^%s' % pgettext('urls', 'account/'),
            include('askbot.deps.django_authopenid.urls')
        ),
    )

if 'avatar' in settings.INSTALLED_APPS:
    urlpatterns += (
        #avatar views are added here, because some need
        #either dynamic extra context or custom redirect
        #or extra parameter in the urls
        service_url(
            '^avatar/upload/(?P<user_id>\d+)/$', 
            views.avatar_views.upload,
            name='askbot_avatar_upload'
        ),
        service_url(
            '^avatar/list/(?P<user_id>\d+)/$',
            views.avatar_views.show_list,
            name='askbot_avatar_show_list'
        ),
        service_url(
            '^avatar/set-primary/(?P<user_id>\d+)/$',
            views.avatar_views.set_primary,
            name='askbot_avatar_set_primary'
        ),
        service_url(
            '^avatar/delete/(?P<avatar_id>\d+)/$',
            views.avatar_views.delete,
            name='askbot_avatar_delete'
        ),
        service_url(#this url is used without changes as in the avatar app
            '^avatar/render-primary/(?P<user>[\w\d\.\-_]+)/(?P<size>[\d]+)/$',
            'avatar.views.render_primary',
            name='avatar_render_primary'
        ),
        service_url(
            '^avatar/enable-gravatar/(?P<user_id>[\d]+)/$',
            views.avatar_views.enable_gravatar,
            name='askbot_avatar_enable_gravatar'
        ),
        service_url(
            '^avatar/enable-default-avatar/(?P<user_id>[\d]+)/$',
            views.avatar_views.enable_default_avatar,
            name='askbot_avatar_enable_default_avatar'
        )
    )
