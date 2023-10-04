import openai
import pkg_resources
from django.conf import settings
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Scope, String

from chatgpt.utils import render_template, validate_openai_key


@XBlock.needs("i18n")
class ChatGPTXBlock(XBlock):
    """ """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.


    display_name = String(
        default="ChatGPT",
        display_name="Component Display Name",
        help="The name students see. This name appears in the course ribbon and as a header for the video.",
        scope=Scope.content,
    )

    chat_history = String(help="Chat History", default="", scope=Scope.user_state)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def studio_view(self, context=None):
        context = {
            "i18n_service": self.runtime.service(self, "i18n"),
            'display_name_value': self.display_name,
        }
        frag = Fragment()
        frag.content = render_template("studio-view.html", **context)
        frag.add_css(self.resource_string("static/css/studio-styles.css"))
        frag.add_javascript(self.resource_string("static/js/src/studio.js"))
        frag.initialize_js("ChatGPTXBlockEdit")
        return frag

    def student_view(self, context=None):
        """
        The primary view of the ChatGPTXBlock, shown to students
        when viewing courses.
        """
        openai_api_key = getattr(settings, 'OPENAI_SECRET_KEY', None)
        # Check if the key is valid or not
        if openai_api_key:
            is_key_valid = validate_openai_key(openai_api_key)
        context = {
            "i18n_service": self.runtime.service(self, "i18n"),
            "is_key_set": bool(openai_api_key),
            "is_key_valid": is_key_valid
        }
        frag = Fragment()
        frag.content = render_template("student-view.html", **context)
        frag.add_css(self.resource_string("static/css/student-styles.css"))
        frag.add_javascript(self.resource_string("static/js/src/student.js"))
        frag.initialize_js("ChatGPTXBlock")
        return frag

    @XBlock.json_handler
    def send_message(self, data, suffix=""):
        """Send message to OpenAI, and return the response"""

        openai.api_key = settings.OPENAI_SECRET_KEY
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": data.get("message", "")},
            ],
        )
        # Get the AI's message from the response
        ai_message = openai_response["choices"][0]["message"]["content"]

        # Update chat history
        self.chat_history += f"User: {data.get('message', '')}\nAI: {ai_message}\n"

        # Return AI response
        return {"result": "success", "response": ai_message}

    @XBlock.json_handler
    def save_content(self, data, suffix=""):
        self.display_name = data.get("displayNameVal")
        return {"result": "success"}

    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            (
                "ChatGPTXBlock",
                """
                <ChatGPT/>
                """,
            ),
            (
                "Multiple ChatGPTXBlock",
                """<vertical_demo>
                    <ChatGPT/>
                    <ChatGPT/>
                    <ChatGPT/>
                </vertical_demo>
             """,
            ),
        ]
