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


class EditGolfCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Edit course",
                "name",
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


class PlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Create a new Player",
                "name",
                "user_account",
            ),
            Submit("submit", "Submit", css_class="btn btn-primary btn-sm"),
        )

    class Meta:
        model = home_models.Player
        fields = ["name", "user_account"]


class GameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Create a new Game",
                "course",
            ),
            Submit("submit", "Submit", css_class="btn btn-primary btn-sm"),
        )

    class Meta:
        model = home_models.Game
        fields = ["course"]


class HoleForm(forms.ModelForm):
    class Meta:
        model = home_models.Hole
        fields = ["par"]


class TeeTimeForm(forms.ModelForm):
    tee_time = forms.DateTimeField(input_formats=["%m-%d-%Y %H:%M"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Create a new Tee Time",
                "course",
                "tee_time",
                "holes_to_play"
            ),
            Submit("submit", "Submit", css_class="btn btn-primary btn-sm"),
        )

    class Meta:
        model = home_models.TeeTime
        fields = ["course", "tee_time", "holes_to_play"]
