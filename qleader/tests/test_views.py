import json
from rest_framework import status
from rest_framework.test import APITransactionTestCase
from qleader.tests.data_handler import (
    post_data, get_home, scipy_examples, gradient_examples, special_examples
    )
from rest_framework.test import force_authenticate, APIRequestFactory
from django.contrib.auth.models import User
from qleader import views


# The test class for views
class ViewsTests(APITransactionTestCase):

    def setup_method(self, method):
        self.factory = APIRequestFactory()
        self.user, self.created = User.objects.get_or_create(username='Testi-Teppo')
        self.user.userprofile.real_name = "Teppo"
        self.user.userprofile.institution = "default institution"
        self.user.userprofile.bio = "default bio text"
        self.user.save()

    # Tests for views/result_receiver.py

    def test_result_receiver_GET(self):
        request = self.factory.get("/api/")
        force_authenticate(request, user=self.user)
        view = views.result_receiver
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_result_receiver_POST_valid_call(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_result_receiver_POST_invalid_call(self):
        response = post_data(self, json.dumps([]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Tests for views/home.py

    def test_home_GET(self):
        response = get_home(self, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 0)
        post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 1)
        self.assertEqual(response.data["results"][0]["optimizer"], "NELDER-MEAD")

    # Tests for views/detail.py

    def test_detail_GET(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        request = self.factory.get("/api/" + str(response.data) + "/")
        force_authenticate(request, user=self.user)
        view = views.detail
        response = view(request, result_id=response.data['result_id'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Tests for views/leaderboard.py

    def test_leaderboard_GET(self):
        response = self.client.get("/leaderboard/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_invoke_leaderboard_closest_minimum(self):
        post_data(self, scipy_examples["NELDER-MEAD"])
        post_data(self, scipy_examples["BFGS"])
        post_data(self, gradient_examples["NESTEROV"])
        response = self.client.get("/leaderboard/closest_minimum/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 3)
        self.assertEqual(response.data["criterion"], "closest_minimum")
        self.assertEqual(response.data["results"][0].get_optimizer(), "NELDER-MEAD")
        self.assertEqual(response.data["results"][1].get_optimizer(), "BFGS")
        self.assertEqual(response.data["results"][2].get_optimizer(), "NESTEROV")

    def test_invoke_leaderboard_smallest_variance(self):
        post_data(self, scipy_examples["NELDER-MEAD"])
        post_data(self, special_examples["BENCHMARK_NELDER-MEAD"])
        response = self.client.get("/leaderboard/smallest_variance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 1)
        self.assertEqual(response.data["criterion"], "smallest_variance")
        self.assertEqual(response.data["results"][0].get_optimizer(), "NELDER-MEAD")

    def test_invoke_leaderboard_min_energy(self):
        post_data(self, scipy_examples["NELDER-MEAD"])
        post_data(self, scipy_examples["BFGS"])
        post_data(self, gradient_examples["NESTEROV"])
        response = self.client.get("/leaderboard/min_energy/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 3)
        self.assertEqual(response.data["criterion"], "min_energy")
        self.assertEqual(response.data["results"][0].get_optimizer(), "NESTEROV")
        self.assertEqual(response.data["results"][1].get_optimizer(), "BFGS")
        self.assertEqual(response.data["results"][2].get_optimizer(), "NELDER-MEAD")

    # Tests for views/delete_result.py

    def test_delete_result_when_authenticated(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        self.assertTrue(len(response.data["results"]) == 1)
        request = self.factory.delete("/api/" + str(response.data["results"][0]["id"]) + "/delete/")
        force_authenticate(request, user=self.user)
        view = views.delete_result
        response = view(request, result_id=str(response.data["results"][0]["id"]))
        response = get_home(self, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 0)

    def test_delete_result_unsuccess_when_not_authenticated(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        self.assertTrue(len(response.data["results"]) == 1)
        self.client.delete("/api/" + str(response.data["results"][0]["id"]) + "/delete/")
        # <- Here should normally the authentication
        response = get_home(self, self.user)
        self.assertTrue(len(response.data["results"]) == 1)

    def test_delete_result_gives_correct_status_GET(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        request = self.factory.get("/api/" + str(response.data["results"][0]["id"]) + "/delete/")
        force_authenticate(request, user=self.user)
        view = views.delete_result
        response = view(request, result_id=str(response.data["results"][0]["id"]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_result_gives_correct_status_if_not_own(self):
        factory = APIRequestFactory()
        user, created = User.objects.get_or_create(username='Testi-Tapio')
        request = factory.post("/api/", data=json.dumps(scipy_examples["NELDER-MEAD"]), format='json')
        view = views.result_receiver
        force_authenticate(request, user=user)
        response = view(request)
        response = get_home(self, user)
        request = self.factory.delete("/api/" + str(response.data["results"][0]["id"]) + "/delete/")
        force_authenticate(request, user=self.user)
        view = views.delete_result
        response = view(request, result_id=str(response.data["results"][0]["id"]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_result_gives_correct_status_when_result_not_found(self):
        request = self.factory.delete("/api/1/delete/")
        force_authenticate(request, user=self.user)
        view = views.delete_result
        response = view(request, result_id=1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Tests for views/change_publicity.py

    def test_change_publicity_when_authenticated(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        id = str(response.data["results"][0]["id"])
        request = self.factory.post("/api/" + id + "/change_publicity/", {'boolean': True})
        force_authenticate(request, user=self.user)
        view = views.change_publicity
        response = view(request, result_id=id)
        request = self.factory.get("/api/" + id + "/")
        force_authenticate(request, user=self.user)
        view = views.detail
        response = view(request, result_id=id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["result"].public)

    def test_change_publicity_unsuccess_when_not_authenticated(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        id = str(response.data["results"][0]["id"])
        request = self.client.post("/api/" + id + "/change_publicity/", {'boolean': True})
        request = self.factory.get("/api/" + id + "/")
        force_authenticate(request, user=self.user)
        view = views.detail
        response = view(request, result_id=id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["result"].public)

    def test_change_publicity_gives_correct_status_GET(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        request = self.factory.get(
            "/api/" + str(response.data["results"][0]["id"]) + "/change_publicity/")
        force_authenticate(request, user=self.user)
        view = views.change_publicity
        response = view(request, result_id=str(response.data["results"][0]["id"]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_change_publicity_gives_correct_status_if_not_own(self):
        factory = APIRequestFactory()
        user, created = User.objects.get_or_create(username='Testi-Tapio')
        request = factory.post("/api/", data=json.dumps(scipy_examples["NELDER-MEAD"]), format='json')
        view = views.result_receiver
        force_authenticate(request, user=user)
        response = view(request)
        response = get_home(self, user)
        request = self.factory.post(
            "/api/" + str(response.data["results"][0]["id"]) + "/change_publicity/")
        force_authenticate(request, user=self.user)
        view = views.change_publicity
        response = view(request, result_id=str(response.data["results"][0]["id"]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_publicity_gives_correct_status_when_result_not_found(self):
        request = self.factory.post("/api/1/change_publicity/")
        force_authenticate(request, user=self.user)
        view = views.change_publicity
        response = view(request, result_id=1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Tests for views/modify_info.py

    def test_modify_info_when_authenticated(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        id = str(response.data["results"][0]["id"])
        request = self.factory.post("/api/" + id + "/modify_info/",
                                    {'info': 'cool', 'github_link': '', 'article_link': ''})
        force_authenticate(request, user=self.user)
        view = views.modify_info
        response = view(request, result_id=id)
        request = self.factory.get("/api/" + id + "/")
        force_authenticate(request, user=self.user)
        view = views.detail
        response = view(request, result_id=id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["result"].info == 'cool')

    def test_modify_info_unsuccess_when_not_authenticated(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        id = str(response.data["results"][0]["id"])
        request = self.client.post("/api/" + id + "/modify_info/",
                                   {'info': 'cool', 'github_link': '', 'article_link': ''})
        request = self.factory.get("/api/" + id + "/")
        force_authenticate(request, user=self.user)
        view = views.detail
        response = view(request, result_id=id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["result"].info == 'cool')

    def test_modify_info_gives_correct_status_GET(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        request = self.factory.get("/api/" + str(response.data["results"][0]["id"]) + "/modify_info/")
        force_authenticate(request, user=self.user)
        view = views.modify_info
        response = view(request, result_id=str(response.data["results"][0]["id"]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_modify_info_gives_correct_status_if_not_own(self):
        factory = APIRequestFactory()
        user, created = User.objects.get_or_create(username='Testi-Tapio')
        request = factory.post("/api/", data=json.dumps(scipy_examples["NELDER-MEAD"]), format='json')
        view = views.result_receiver
        force_authenticate(request, user=user)
        response = view(request)
        response = get_home(self, user)
        request = self.factory.post("/api/" + str(response.data["results"][0]["id"]) + "/modify_info/",
                                    {'info': 'This is the best.', 'github_link': '', 'article_link': ''})
        force_authenticate(request, user=self.user)
        view = views.modify_info
        response = view(request, result_id=str(response.data["results"][0]["id"]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modify_info_gives_correct_status_when_result_not_found(self):
        request = self.factory.post("/api/1/modify_info/")
        force_authenticate(request, user=self.user)
        view = views.modify_info
        response = view(request, result_id=1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_urls_works(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        id = str(response.data["results"][0]["id"])
        request = self.factory.post("/api/" + id + "/modify_info/",
                                    {'info': 'cool',
                                     'github_link': 'https://github.com/quantum-ohtu/WebMark2',
                                     'article_link': 'http://google.com'})
        force_authenticate(request, user=self.user)
        view = views.modify_info
        response = view(request, result_id=id)
        request = self.factory.get("/api/" + id + "/")
        force_authenticate(request, user=self.user)
        view = views.detail
        response = view(request, result_id=id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["result"].info == 'cool')
        self.assertTrue(response.data["result"].github_link ==
                        'https://github.com/quantum-ohtu/WebMark2')
        self.assertTrue(response.data["result"].article_link == 'http://google.com')

    def test_invalid_urls_not_accepted(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = get_home(self, self.user)
        id = str(response.data["results"][0]["id"])
        request = self.factory.post("/api/" + id + "/modify_info/",
                                    {'info': 'cool',
                                     'github_link': 'www.github.com/quantum-ohtu/WebMark2',
                                     'article_link': 'google.com'})
        force_authenticate(request, user=self.user)
        view = views.modify_info
        response = view(request, result_id=id)
        request = self.factory.get("/api/" + id + "/")
        force_authenticate(request, user=self.user)
        view = views.detail
        response = view(request, result_id=id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["result"].info == 'cool')
        self.assertFalse(response.data["result"].github_link ==
                         'www.github.com/quantum-ohtu/WebMark2')
        self.assertFalse(response.data["result"].article_link == 'google.com')

    # Tests for profile.py

    def test_modify_profile_authenticated(self):
        id = self.user.id
        request = self.factory.post("/user/" + str(id) + "/modify_profile/",
                                    {'realName': 'T T', 'institution': '',
                                    'bio': 'more than three words'})
        force_authenticate(request, user=self.user)
        view = views.modify_profile
        response = view(request, user_id=id)
        request = self.factory.get("/user/" + str(id) + "/")
        force_authenticate(request, user=self.user)
        view = views.profile
        response = view(request, user_id=id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["profile_user"].userprofile.real_name == 'T T')
        self.assertTrue(response.data["profile_user"].userprofile.institution == '')
        self.user = User.objects.get(username='Testi-Teppo')
        self.assertEqual(self.user.userprofile.bio, 'more than three words')

    def test_modify_profile_with_bad_authentication(self):
        id = self.user.id
        test_user, test_created = User.objects.get_or_create(username='Error-Elwood')
        request = self.factory.post("/user/" + str(id) + "/modify_profile/",
                                    {'realName': 'T T', 'institution': '',
                                    'bio': 'more than three words'})
        force_authenticate(request, user=test_user)
        view = views.modify_profile
        response = view(request, user_id=id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.user = User.objects.get(username='Testi-Teppo')
        self.assertEqual(self.user.userprofile.real_name, 'Teppo')
        self.assertEqual(self.user.userprofile.bio, 'default bio text')

    def test_modify_profile_without_authentication(self):
        id = self.user.id
        request = self.factory.post("/user/" + str(id) + "/modify_profile/",
                                    {'realName': 'T T', 'institution': '', 'bio': ''})
        view = views.modify_profile
        response = view(request, user_id=id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        request = self.factory.get("/user/" + str(id) + "/")
        view = views.profile
        response = view(request, user_id=id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile_user"].userprofile.real_name, 'Teppo')
        self.user = User.objects.get(username='Testi-Teppo')
        self.assertEqual(self.user.userprofile.institution, 'default institution')
        self.assertEqual(self.user.userprofile.bio, 'default bio text')
