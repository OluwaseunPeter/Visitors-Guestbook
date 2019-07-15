import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Visitor , VisitHistory , VisitorDetailChangeHistory , VISITORS_ADDRESS , VISITORS_NAME

# Create your tests here.

def generateVisitPostBody(name = "" ,  address="" , email="" , to_see="" , visit_purpose="" , comment=""):
    return  {
        'name' : name ,
        'address' : address , 
        'email' : email,
        'to_see': to_see  ,
        'visit_purpose' : visit_purpose,
        'comment' : comment ,
    }

visitor_data_1 = generateVisitPostBody(name="Joseph Oluwaseun Peter" ,
                                             address="5 oyebanke street , ojodu" ,
                                             email="JosephOluwaseunPeter@yahoo.com",
                                             to_see="HR",
                                             visit_purpose="Interview")

visitor_data_2 = generateVisitPostBody(name="Adewale Ayuba" ,
                                             address="20 jolak cresent" ,
                                             email="Adex@email.com",
                                             to_see="MD",
                                             visit_purpose="Official")

visitor_data_3 = generateVisitPostBody(name="Kingsley Chuks" ,
                                             address="31 adewaje str" ,
                                             email="Kingsley@email.com",
                                             to_see="HR",
                                             visit_purpose="Interview")

visitor_data_4 = generateVisitPostBody(name="Mobolaji Toyin" ,
                                             address="1 tafa str" ,
                                             email="Mobolaji_Olushafe_Toyin@email.com",
                                             to_see="MD",
                                             visit_purpose="Official")

visitor_datas =  [visitor_data_1 ,visitor_data_2 ,  visitor_data_3 , visitor_data_4]

class VistorWelcomePageViewTest(TestCase):
    url = reverse('visitors_guestbook:index')

    def test_NewGuestCheckIn(self):
        """
        test if Guest can check in successfully
        """
        response = self.client.post(self.url , visitor_data_1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success!")
        self.assertNotContains(response , "Info!")
        pass
    
    def test_GuestCheckInMultipleTime(self):
        """
        test if Guest can check in successfully multiple time
        in a day while having their information updated instead of
        creating new Guest data
        """

        response = self.client.post(self.url , visitor_data_1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success!")
        self.assertNotContains(response , "Info!")

        response = self.client.post(self.url , visitor_data_1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success!")
        self.assertContains(response , "Info!")
    
    def test_GuestCheckInfoUpdate(self):
        """
        test if Guest can check in successfully multiple time
        verify that thier detail is updated correctly with 
        the new detail subimitted
        """

        response = self.client.post(self.url , visitor_data_1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success!")
        self.assertNotContains(response , "Info!")

        temp_visitor_data = visitor_data_1.copy()
        new_name = "Test Name"
        new_address = "Test Address"
        temp_visitor_data["name"] = new_name 
        temp_visitor_data["address"] = new_address
        response = self.client.post(self.url , temp_visitor_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success!")
        self.assertContains(response , "Info!")

        visitor  = Visitor()
        visitor = visitor.getVisitorWithEmail(temp_visitor_data["email"])
        self.assertEqual(visitor.name , temp_visitor_data["name"])
        self.assertEqual(visitor.address , temp_visitor_data["address"])

        visitor_details_changes = visitor.getAllVisitorDetailChangeHistory()
        self.assertQuerysetEqual(visitor_details_changes , 
                            [   
                                f'<VisitorDetailChangeHistory: {new_name} - {VISITORS_NAME} - Change From: {visitor_data_1["name"]}, Change To: {new_name}>',
                                f'<VisitorDetailChangeHistory: {new_name} - {VISITORS_ADDRESS} - Change From: {visitor_data_1["address"]}, Change To: {new_address}>'
                            ])


class VisitorsReportingPageViewTest(TestCase):
    url = reverse('visitors_guestbook:report_all')

    def admin_login(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_AdminOnlyAccessToVisitorsReport(self):
        """
        Test if only admin user have access to this page
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        self.admin_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_ContentOfVisitorOnTheAdminPage(self):
        """
        Test the contents on the Visitors Reporting Page
        """
        welcome_url = reverse('visitors_guestbook:index')
        counter =  0
        for visitor_data in visitor_datas :
            counter += 1

            self.admin_login()
            #Check in the guest
            response = self.client.post(welcome_url , visitor_data)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Success!")
            self.assertNotContains(response , "Info!")

            #Test if admin user is logout after when 
            #we visit the visitor check in page
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 302)

            #Test Number of Vistor Statistic on the 
            #admin Visitor page
            self.admin_login()
            response = self.client.get(self.url)

            self.assertEqual( response.context['total_visit_today'],counter)
            self.assertEqual( response.context['total_visit_for_this_week'],counter)
            self.assertEqual( response.context['total_vist_for_this_month'],counter)
            self.assertEqual( response.context['total_vist'],counter)

            self.assertContains(response , visitor_data["name"])
            self.assertContains(response , visitor_data["address"])
            self.assertContains(response , str.lower(visitor_data["email"]))

class VistorReportingPageViewTest(TestCase):
    #url = reverse('visitors_guestbook:report_all')
    
    def admin_login(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_AdminOnlyAccessToVisitorReport(self):
        """
        Test if only admin user have access to this page
        """

        response = self.client.post(reverse('visitors_guestbook:index') , visitor_data_1)
        visitor  = Visitor()
        visitor = visitor.getVisitorWithEmail(visitor_data_1["email"])

        url = reverse('visitors_guestbook:report_visitor' , args=[visitor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.admin_login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_ContentOfVisitorOnTheAdminPage(self):
        """
        Test if content of Visitor page are correct
        """

        welcome_url = reverse('visitors_guestbook:index')
        
        for visitor_data in visitor_datas :

            #tried checking in more that once a day
            for counter in range(5): 
                self.admin_login()
                #Check in the guest
                response = self.client.post(welcome_url , visitor_data)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Success!")
                if counter > 0:
                    self.assertContains(response , "Info!")
                else:
                    self.assertNotContains(response , "Info!")

                visitor  = Visitor()
                visitor = visitor.getVisitorWithEmail(visitor_data["email"])
                url = reverse('visitors_guestbook:report_visitor' , args=[visitor.id])
                

                #Test if admin user is logout after when 
                #we visit the visitor check in page
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

                #Test Number of Vistor Statistic on the 
                #admin Visitor page
                self.admin_login()
                response = self.client.get(url)

                self.assertEqual( response.context['total_visit_for_this_week'],1)
                self.assertEqual( response.context['total_vist_for_this_month'],1)
                self.assertEqual( response.context['total_vist'],1)

                self.assertContains(response , visitor_data["name"])
                self.assertContains(response , visitor_data["address"])
                self.assertContains(response , str.lower(visitor_data["email"]))