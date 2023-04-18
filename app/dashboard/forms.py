from django import forms
from home import models as home_models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit


class GolfCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Create a new course",
                "name",
                "hole_count",
                "tee_time_link",
                "website_link",
                "city",
                "state",
                "zip_code",
            ),
            Submit("submit", "Submit", css_class="btn btn-primary btn-sm"),
        )

    class Meta:
        model = home_models.GolfCourse
        fields = [
            "name",
            "hole_count",
            "tee_time_link",
            "website_link",
            "city",
            "state",
            "zip_code",
        ]


class TeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Create a new tee",
                "name",
                "distance",
            ),
            Submit("submit", "Submit", css_class="btn btn-primary btn-sm"),
        )

    class Meta:
        model = home_models.Tee
        fields = ["name", "distance"]
