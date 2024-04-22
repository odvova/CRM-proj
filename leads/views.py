from django.shortcuts import reverse
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead
from .forms import LeadModelForm, CustomUserCreationForm

#Template Method

class SignUpView(generic.CreateView):
    """
    A view for signing up a new user.

    This view is responsible for rendering the signup form and handling the form submission.
    It inherits from the CreateView class provided by Django.

    Attributes:
        template_name (str): The name of the template used to render the signup form.
        form_class (Form): The form class used for the signup form.
    """
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    """
    A view that renders the landing page template.

    Inherits from the TemplateView class and sets the template_name attribute to "landing.html".
    """
    template_name = "landing.html"


class LeadListView(LoginRequiredMixin, generic.ListView):
    """
    A view that displays a list of leads.

    Attributes:
        template_name (str): The name of the template used to render the view.
        queryset (QuerySet): The queryset used to fetch the leads from the database.
        context_object_name (str): The name of the variable used to store the leads in the template context.
    """
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    """
    A view for displaying the details of a lead.

    This view renders the template 'leads/lead_detail.html' and retrieves
    the lead object from the database using the `Lead` model. The lead object
    is then made available in the template context as 'lead'.

    Attributes:
        template_name (str): The name of the template to be rendered.
        queryset (QuerySet): The queryset used to retrieve the lead object.
        context_object_name (str): The name of the variable used to access
            the lead object in the template context.
    """
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    """
    A view for creating a new lead.

    Inherits from Django's CreateView class and provides a form for creating a new lead.

    Attributes:
        template_name (str): The name of the template used to render the view.
        form_class (ModelForm): The form class used to create a new lead.
    
    Methods:
        get_success_url: Returns the URL to redirect to after a successful form submission.
    """

    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        #TODO send email
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    View for updating a lead.

    This view is responsible for rendering the lead update form and handling the form submission.
    It inherits from the UpdateView class provided by Django.

    Attributes:
        template_name (str): The name of the template used to render the lead update form.
        form_class (Form): The form class used for the lead update form.
        queryset (QuerySet): The queryset used to retrieve the lead object to be updated.

    Methods:
        get_success_url: Returns the URL to redirect to after a successful form submission.

    """

    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")
    

class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    View for deleting a Lead object.

    This view inherits from the DeleteView class provided by Django.
    It displays a confirmation page and deletes the specified Lead object
    when the user confirms the deletion.

    Attributes:
        template_name (str): The name of the template used to render the confirmation page.
        queryset (QuerySet): The queryset used to retrieve the Lead object to be deleted.

    Methods:
        get_success_url: Returns the URL to redirect to after the Lead object is deleted.
    """
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")
    
# Unrefactored code

# def landing_page(request):K
#     return render(request, "landing.html")

# def lead_list(request):
#     leads = Lead.objects.all()
#     context = {
#         "leads": leads
#     }
#     return render(request, "leads/lead_list.html", context)

# def lead_detail(request, pk):
#     lead = Lead.objects.get(id=pk)
#     context = {
#         "lead": lead
#     }  
#     return render(request, "leads/lead_detail.html", context)

# def lead_create(request):
#     form = LeadModelForm()
#     if request.method == "POST":
#         print("Receiving a POST request")
#         form = LeadModelForm(request.POST)   
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")
#     context = {
#         "form": form
#     }
#     return render(request, "leads/lead_create.html", context)

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadModelForm(instance=lead)
#     if request.method == "POST":
#         form = LeadModelForm(request.POST, instance=lead)   
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")
#     context = { 
#         "form": form,
#         "lead": lead
#     }
#     return render(request, "leads/lead_update.html", context)

# def lead_delete(request, pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect("/leads")


