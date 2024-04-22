from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm

class LeadTestCase(TestCase):
    def setUp(self):
        """
        Set up the necessary objects and data for the test case.

        This method is called before each test method is executed.

        It creates a test user, an agent, and a lead object for testing purposes.
        """
        user = get_user_model().objects.create_user(
            username='test_user',
            password='test_password'
        )
        agent = Agent.objects.create(user=user)
        Lead.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            agent=agent
        )

    def test_lead_listing(self):
        """
        Test case for lead listing.

        This method tests the functionality of the lead listing view.
        It sends a GET request to the 'lead-list' URL and checks if the response
        status code is 200 (OK) and if the response contains the name 'John Doe'.
        """
        response = self.client.get(reverse('leads:lead-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_lead_create(self):
        """
        Test case for creating a lead.

        This method sends a POST request to the 'lead-create' URL with the required data
        and asserts that the response status code is 200 (OK). It also checks that the
        first name of the last created Lead object matches the provided value.

        """
        response = self.client.post(reverse('leads:lead-create'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 25
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.last().first_name, 'John')

    def test_lead_update(self):
        """
        Test case for updating a lead.

        This method tests the functionality of updating a lead by sending a POST request
        to the 'lead-update' URL with the lead ID and the updated lead data. It then
        asserts that the response status code is 200 and checks if the lead's first name
        has been updated successfully.

        """
        lead = Lead.objects.first()
        response = self.client.post(reverse('leads:lead-update', args=[lead.id]), {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 25
        })
        self.assertEqual(response.status_code, 200)
        lead.refresh_from_db()
        self.assertEqual(lead.first_name, 'John')

    def test_lead_delete(self):
        """
        Test case for deleting a lead.

        This method tests the functionality of deleting a lead object from the database.
        It verifies that the HTTP response status code is 302 (redirect) and that the
        count of Lead objects in the database is 0 after the deletion.

        """
        lead = Lead.objects.first()
        response = self.client.post(reverse('leads:lead-delete', args=[lead.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lead.objects.count(), 0)

    def test_lead_form(self):
        """
        Test case for the LeadForm class.

        This method tests the validation of the LeadForm by passing a valid data dictionary
        and asserting that the form is valid.

        """
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'age': 30,
        }
        form = LeadForm(data)
        self.assertTrue(form.is_valid())

    def test_lead_form_invalid(self):
        """
        Test case to verify the behavior of the LeadForm when an invalid form is submitted.

        This method creates a LeadForm instance with invalid data and asserts that the form
        is not valid. It also checks if the error message for the 'age' field is as expected.
        """
        form = LeadForm({
            'first_name': 'John',
            'last_name': 'Doe',
            'age': -25
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['age'], ['Ensure this value is greater than or equal to 0.'])

    def test_lead_str(self):
        """
        Test the string representation of a Lead object.

        This method retrieves the first Lead object from the database and compares its string
        representation with the expected value. The test passes if the two values are equal.
        """
        lead = Lead.objects.first()
        self.assertEqual(str(lead), 'John Doe')

    def test_agent_str(self):
        """
        Test case to verify the string representation of an Agent object.

        It retrieves the first Agent object from the database and compares its string representation
        with the email of the associated user. The test passes if the two values are equal.
        """
        agent = Agent.objects.first()
        self.assertEqual(str(agent), agent.user.email)

    
class LandingPageTest(TestCase):
    def test_landing_page_status_code(self):
        """
        Test case for the status code of the landing page.

        This method sends a GET request to the landing page URL and checks if the response
        status code is 200 (OK).
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_landing_page_template(self):
        """
        Test case for the template used in the landing page view.

        This method sends a GET request to the landing page URL and checks if the response
        uses the 'landing.html' template.
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'landing.html')

    