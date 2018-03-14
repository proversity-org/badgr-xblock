"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
import logging
import requests
from django.conf import settings
from xblock.core import XBlock
from django.contrib.auth.models import User
from xblock.fields import Scope, Integer, String, Float, List, Boolean, ScopeIds
from xblockutils.resources import ResourceLoader
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin
from xblockutils.settings import XBlockWithSettingsMixin
logger = logging.getLogger(__name__)
loader = ResourceLoader(__name__)


@XBlock.needs('settings')
@XBlock.wants('badging')
@XBlock.wants('user')
class BadgerXBlock(StudioEditableXBlockMixin, XBlockWithSettingsMixin, XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default=u"Badger"
    )

    issuer_slug = String(
        display_name="Issuer name",
        help="must be lower case unique name.",
        scope=Scope.settings,
        default=u"proversity"
    )

    badge_slug = String(
        display_name="Badge name",
        help="must be lower case unique name.",
        scope=Scope.settings,
        default=u"test-badge"
    )

    badge_name = String(
        display_name="Badge display name",
        help="Badge name that appears in Accomplishments tab",
        scope=Scope.settings,
        default=u"Module 1 Badge"
    )

    image_url = String(
        help="The url for the badge image on Badgr server",
        scope=Scope.user_state,
        default=""
    )

    criteria = String(
        display_name="Criteria",
        help="How does one earn this badge?",
        scope=Scope.settings,
        default=u"Achieve a pass mark of 80% percent or more for course module 1"
    )

    description = String(
        display_name="Description",
        help="What is this badge",
        scope=Scope.settings,
        default=u"A Shiny badge, given to exceptional students"
    )

    section_title = String(
        display_name="Section title",
        help="See the display name of this section",
        scope=Scope.settings,
        default=u"Section"
    )

    pass_mark = Float(
        display_name='Pass mark',
        default=80.0, 
        scope=Scope.settings,
        help="Minium grade required to award this badge",
    )

    received_award = Boolean(
        default = False, 
        scope=Scope.user_state,
        help='Has the user received a badge for this sub-section'
    )

    check_earned = Boolean(
        default = False, 
        scope=Scope.user_state,
        help='Has the user check if they are eligible for a badge.'
    )

    assertion_url = String(
        default = None, 
        scope=Scope.user_state,
        help='The user'
    ) 

    award_message = String(
        display_name='Award message',
        default=u'Well done you are an all star!',
        scope=Scope.settings,
        help='Message the user will see upon receiving a badge',
    )

    motivation_message = String(
        display_name='Motivational message',
        default = u"Don't worry, you will have another opportunity to earn a badge.",
        scope=Scope.settings,
        help='Message the user will see if they do not quailify for a badge'
    )

    button_text = String(
        display_name='Button text',
        default = u"Click here to view your results.",
        scope=Scope.settings,
        help='Text appearing on button'
    )

    button_colour = String(
        display_name='Button colour',
        default = u"#0075b4",
        scope=Scope.settings,
        help='Colour appearing on button'
    )

    button_text_colour = String(
        display_name='Text button colour',
        default = u"#ffffff",
        scope=Scope.settings,
        help='Text colour appearing on button'
    )


    editable_fields = (
        'display_name',
        'description',
        'criteria',
        'issuer_slug',
        'badge_slug',
        'badge_name', 
        'pass_mark',
        'section_title',
        'award_message',
        'motivation_message',
        'button_text',
        'button_colour',
        'button_text_colour'
    )

    show_in_read_only_mode = True
 
    @property
    def api_token(self):
        """
        Returns the Badgr Server API token from Settings Service.
        The API key should be set in both lms/cms env.json files inside XBLOCK_SETTINGS.
        Example:
            "XBLOCK_SETTINGS": {
                "BadgerXBlock": {
                    "BADGR_API_TOKEN": "YOUR API KEY GOES HERE"
                }
            },
        """
        return self.get_xblock_settings().get('BADGR_API_TOKEN', '')

    @property
    def api_url(self):
        """
        Returns the URL of the Badgr Server from the Settings Service.
        The URL hould be set in both lms/cms env.json files inside XBLOCK_SETTINGS.
        Example:
            "XBLOCK_SETTINGS": {
                "BadgerXBlock": {
                    "BADGR_BASE_URL": "YOUR URL  GOES HERE"
                }
            },
        """
        return self.get_xblock_settings().get('BADGR_BASE_URL' '')

    def get_list_of_issuers(self):
        """
        Get a list of issuers from badgr.proversity.org
        """
        issuer_list = requests.get('{}/v1/issuer/issuers'.format(self.api_url),  headers={'Authorization': 'token {}'.format(self.api_token)})
        return issuer_list.json()

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    @XBlock.json_handler
    def new_award_badge(self, data, suffix=''):
        """
        The json handler which uses the badge service to award
        a badge.
        """
        badge_service = self.runtime.service(self, 'badging')
        badge_class = badge_service.get_badge_class(
           slug=self.badge_slug, issuing_component=self.issuer_slug,
            course_id=self.runtime.course_id,
            display_name=self.badge_name,
            description=self.description,
            criteria=self.criteria
        )
        
        # Award the badge
        user = self.runtime.get_real_user(self.runtime.anonymous_student_id)
        badge_class.award(user)
        badge_assertions = badge_service.assertions_for_user(user=user)
        slug_assertions = badge_service.slug_assertion_for_user(user=user, slug=self.badge_slug)
        self.received_award = True
        self.check_earned = True
        self.image_url = slug_assertions[0]['image_url']
        self.assertion_url = slug_assertions[0]['assertion_url']

        badge_html_dict = {
            "image_url": self.image_url,
            "assertion_url": self.assertion_url,
            "description": self.description,
            "criteria": self.criteria,
        }
        return badge_html_dict


    @XBlock.json_handler
    def no_award_received(self, data, suffix=''):
        """
        The json handler which uses the badge service to deal with no
        badge being earned.
        """
        self.received_award = False
        self.check_earned = True

        return {"image_url": self.image_url, "assertion_url": self.assertion_url}

    @property
    def current_user_key(self):
        user = self.runtime.service(self, 'user').get_current_user()
        # We may be in the SDK, in which case the username may not really be available.
        return user.opt_attrs.get('edx-platform.username', 'username')


    @XBlock.supports("multi_device")
    def student_view(self, context=None):
        """
        The primary view of the BadgerXBlock, shown to students
        when viewing courses.
        """
        if self.runtime.get_real_user is not None:
            user = self.runtime.get_real_user(self.runtime.anonymous_student_id)
        else:
            user = User.objects.get(username=self.current_user_key)

        context = {
            'received_award': self.received_award,
            'check_earned': self.check_earned,
            'section_title': self.section_title,
            'image_url': self.image_url,
            'award_message': self.award_message,
            'button_text': self.button_text,
            'button_colour': self.button_colour,
            'button_text_colour': self.button_text_colour
        }

        frag = Fragment(loader.render_django_template("static/html/badger.html", context).format(self=self))
        frag.add_css(self.resource_string("static/css/badger.css"))
        frag.add_javascript(self.resource_string("static/js/src/badger.js"))
        frag.initialize_js('BadgerXBlock', {
            'user': str(user.username),
            'pass_mark': self.pass_mark,
            'section_title': self.section_title,
            'award_message': self.award_message,
            'motivation_message': self.motivation_message,
            'course_id':  str(self.runtime.course_id),
            'badgrApiToken': self.api_token,
            'badge_slug': self.badge_slug
        })

        return frag


    def studio_view(self, context):
        """
        Render a form for editing this XBlock
        """
        frag = Fragment()
        context = {'fields': []}
        
        # Build a list of all the fields that can be edited:
        for field_name in self.editable_fields:
            field = self.fields[field_name]
            assert field.scope in (Scope.content, Scope.settings), (
                "Only Scope.content or Scope.settings fields can be used with "
                "StudioEditableXBlockMixin. Other scopes are for user-specific data and are "
                "not generally created/configured by content authors in Studio."
            )
            field_info = self._make_field_info(field_name, field)
            if field_info is not None:
                context["fields"].append(field_info)
        frag.content = loader.render_django_template("static/html/badger_edit.html", context)
        frag.add_javascript(loader.load_unicode("static/js/src/badger_edit.js"))
        frag.initialize_js('StudioEditableXBlockMixin', {
            'badgrApiToken': self.api_token
        })
        return frag

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("BadgerXBlock",
             """<badger/>
             """),
            ("Multiple BadgerXBlock",
             """<vertical_demo>
                <badger/>
                <badger/>
                <badger/>
                </vertical_demo>
             """),
        ]
