from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Molecule, Algorithm_type, Average_history, Algorithm
from ..models import Algorithm_version, Metrics
from django.urls import reverse
from django.utils import timezone
from ..views.worker_api import as_average_history
import datetime
import pytz


class AlgorithmComparisonTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user("testuser", "test@example.com", "secret")
        other_user = User.objects.create_user("otheruser", "other@example.com", "secret")

        algorithm_type = Algorithm_type.objects.create(type_name="VQE")
        algorithm_type.save()

        molecule = Molecule.objects.create(name="water", structure="H2O")
        molecule.save()

        cls.my_algorithm = Algorithm.objects.create(
            user=user, name="my public algorithm",
            algorithm_type=algorithm_type, public=True
        )
        cls.my_private_algorithm = Algorithm.objects.create(
            user=user, name="my private algorithm",
            algorithm_type=algorithm_type, public=False
        )
        cls.other_user_public_algorithm = Algorithm.objects.create(
            user=other_user, name="other user public algorithm",
            algorithm_type=algorithm_type, public=True
        )
        cls.other_user_private_algorithm = Algorithm.objects.create(
            user=other_user, name="other user private algorithm",
            algorithm_type=algorithm_type, public=False
        )

        cls.my_algorithm.save()
        cls.my_private_algorithm.save()
        cls.other_user_private_algorithm.save()
        cls.other_user_public_algorithm.save()

        av1 = Algorithm_version(algorithm_id=cls.my_algorithm,
                                timestamp=timezone.now(),
                                algorithm='algo description',
                                circuit="circuit:\nRy(target=(0,), parameter=a)\nX(target=(2,))",
                                optimizer_module='scipy',
                                optimizer_method='BFGS')
        av1.save()

        av2 = Algorithm_version(algorithm_id=cls.my_private_algorithm,
                                timestamp=timezone.now(),
                                algorithm='algo description',
                                circuit="circuit:\nRy(target=(0,), parameter=a)\nX(target=(2,))",
                                optimizer_module='scipy',
                                optimizer_method='BFGS')
        av2.save()

        av3 = Algorithm_version(algorithm_id=cls.other_user_private_algorithm,
                                timestamp=timezone.now(),
                                algorithm='algo description',
                                circuit="circuit:\nRy(target=(0,), parameter=a)\nX(target=(2,))",
                                optimizer_module='scipy',
                                optimizer_method='BFGS')
        av3.save()

        av4 = Algorithm_version(algorithm_id=cls.other_user_public_algorithm,
                                timestamp=timezone.now(),
                                algorithm='algo description',
                                circuit="circuit:\nRy(target=(0,), parameter=a)\nX(target=(2,))",
                                optimizer_module='scipy',
                                optimizer_method='BFGS')
        av4.save()

        m1 = Metrics(algorithm_version=av1, molecule=molecule, gate_depth=1, qubit_count=2,
                     average_iterations=4, success_rate=5.2)
        m1.save()
        m2 = Metrics(algorithm_version=av2, molecule=molecule, gate_depth=11, qubit_count=12,
                     average_iterations=14, success_rate=15.2)
        m2.save()
        m3 = Metrics(algorithm_version=av3, molecule=molecule, gate_depth=21, qubit_count=22,
                     average_iterations=24, success_rate=25.2)
        m3.save()
        m4 = Metrics(algorithm_version=av4, molecule=molecule, gate_depth=31, qubit_count=32,
                     average_iterations=34, success_rate=35.2)
        m4.save()

    def setUp(self):
        self.client.login(username="testuser", password="secret")

    def test_random_parameters_are_handled_correctly(self):
        response = self.client.get("/compare/a/exec()")
        self.assertEqual(response.status_code, 404)

    def test_cannot_compare_nonexistent_algorithms(self):
        response = self.client.get("/compare/10/11")
        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)

    def test_cannot_compare_algorithm_to_itself(self):
        response = self.client.get(
            f"/compare/{self.my_algorithm.pk}/{self.my_algorithm.pk}"
        )
        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)

    def test_can_compare_to_private_by_current_user(self):
        response = self.client.get(
            f"/compare/{self.my_algorithm.pk}/{self.my_private_algorithm.pk}"
        )
        self.assertEqual(response.status_code, 200)

    def test_cannot_compare_to_private_algorithm_by_other_user(self):
        response = self.client.get(
            f"/compare/{self.my_algorithm.pk}/{self.other_user_private_algorithm.pk}"
        )
        self.assertEqual(response.status_code, 403)

    def test_can_compare_to_public_algorithm_by_other_user(self):
        response = self.client.get(
            f"/compare/{self.my_algorithm.pk}/{self.other_user_public_algorithm.pk}"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_benchmark_results_average_history(self):
        av1 = Algorithm_version(algorithm_id=self.my_algorithm,
                                timestamp=timezone.now(),
                                algorithm='algo description',
                                circuit="circuit:\nRy(target=(0,), parameter=a)\nX(target=(2,))",
                                optimizer_module='scipy',
                                optimizer_method='BFGS')
        molecule = Molecule(
            name="hydrogen",
            structure="H 0.0 0.0 0.0",
            active_orbitals="A1 0",
            basis_set="scipy",
            transformation="BFGS"
        )
        molecule.save()
        av1.save()
        metrics = Metrics(
            algorithm_version=av1,
            molecule=molecule,
            gate_depth=381,
            qubit_count=None,
            average_iterations=None,
            success_rate=None)
        metrics.save()
        metricsObject = Metrics.objects.get(gate_depth=381)
        result = {'average_history': [0.23, 0.34, 0.45, 0.56], 'metrics_id': metricsObject.pk}
        as_average_history(result)
        self.assertEqual(len(Average_history.objects.all()), 4)


class TestViewData(TestCase):

    @classmethod
    def setUpTestAlgorithms(self):
        self.algos = []
        for i in range(3):
            a = Algorithm(name='Algo'+str(i+1), public=(i % 2 == 0),
                          algorithm_type=self.types[i], user=self.u1,
                          article_link='https://alink'+str(i+1)+'.com',
                          github_link='https://gtlink'+str(i+1)+'.com')
            a.save()
            self.algos.append(a)

        for i in range(3):
            a = Algorithm(name='Algo'+str(i+4), public=(i % 2 == 0),
                          algorithm_type=self.types[i], user=self.u2,
                          article_link='https://alink'+str(i+4)+'.com',
                          github_link='https://gtlink'+str(i+4)+'.com')
            a.save()
            self.algos.append(a)

    def setUpTestAlgorithmVersions(self):
        for i in range(6):
            av = Algorithm_version(algorithm_id=self.algos[i],
                                   timestamp=datetime.datetime(2021, 2, 10, 10, 0, 0, 0, pytz.UTC),
                                   algorithm='algorithm'+str(i+1)+'\nversion1\n',
                                   circuit="circuit:\nRy(target=(0,), parameter=a)\nX(target=(2,))",
                                   optimizer_module='scipy',
                                   optimizer_method='BFGS')
            av.save()
            av = Algorithm_version(algorithm_id=self.algos[i],
                                   timestamp=datetime.datetime(2021, 2, 10, 11, 0, 0, 0, pytz.UTC),
                                   algorithm='algorithm'+str(i+1)+'\nversion2\n',
                                   circuit="circuit:\nRy(target=(0,), parameter=a)",
                                   optimizer_module='scipy',
                                   optimizer_method='BFGS')
            av.save()

    @classmethod
    def setUpTestData(self):
        self.u1 = User.objects.create_user('Bob', 'bob@example.com', 'bobpassword')
        self.u1.save()
        self.u2 = User.objects.create_user('Alice', 'alice@example.com', 'alicepassword')
        self.u2.save()
        self.types = []
        for i in range(3):
            at = Algorithm_type(type_name='type'+str(i+1))
            at.save()
            self.types.append(at)
        self.setUpTestAlgorithms()
        self.setUpTestAlgorithmVersions(self)

    def setUp(self):
        self.client.login(username="Bob", password="bobpassword")

    def test_my_algorithms_view(self):
        response = str(self.client.get("/myAlgorithms/").content)
        self.assertFalse(response.find('Algo1') < 0)
        self.assertFalse(response.find('Algo2') < 0)
        self.assertFalse(response.find('Algo3') < 0)
        self.assertTrue(response.find('Algo4') < 0)
        self.assertTrue(response.find('Algo5') < 0)
        self.assertTrue(response.find('Algo6') < 0)
        self.assertFalse(response.find('https://alink1.com') < 0)
        self.assertFalse(response.find('https://gtlink1.com') < 0)

    def test_index_view(self):
        response = str(self.client.get("/").content)
        self.assertFalse(response.find('Algo1') < 0)
        self.assertTrue(response.find('Algo2') < 0)
        self.assertFalse(response.find('Algo4') < 0)
        self.assertTrue(response.find('Algo5') < 0)

    def test_add_new_version_to_other_user_algorithm(self):
        a = Algorithm.objects.get(name='Algo4')
        response = self.client.post('/addVersion/?index='+str(a.pk),
                                    {'algorithm': 'print(1)\nexec()'})
        self.assertEqual(response.status_code, 403)

    def test_add_new_version_view(self):
        a = Algorithm.objects.get(name='Algo3')
        response = str(self.client.get('/addVersion/?index='+str(a.pk)).content)
        self.assertFalse(response.find('Algo3') < 0)
        self.assertFalse(response.find('version2') < 0)

    def test_algorithm_details_view(self):
        a = Algorithm.objects.get(name='Algo3')
        response = str(self.client.get('/algorithm/'+str(a.pk)).content)
        self.assertFalse(response.find('Algo3') < 0)
        self.assertFalse(response.find('https://alink3.com') < 0)
        self.assertFalse(response.find('https://gtlink3.com') < 0)

    def test_algorithm_details_other_user_view(self):
        a = Algorithm.objects.get(name='Algo4')
        response = str(self.client.get('/algorithm/'+str(a.pk)).content)
        self.assertFalse(response.find('Algo4') < 0)
        self.assertFalse(response.find('https://alink4.com') < 0)
        self.assertFalse(response.find('https://gtlink4.com') < 0)
        a = Algorithm.objects.get(name='Algo5')
        response = self.client.get('/algorithm/'+str(a.pk))
        self.assertEqual(response.status_code, 403)

    def test_update_other_user_details(self):
        a = Algorithm.objects.get(name='Algo4')
        response = self.client.get('/updateAlgorithm/?index='+str(a.pk))
        self.assertEqual(response.status_code, 403)
