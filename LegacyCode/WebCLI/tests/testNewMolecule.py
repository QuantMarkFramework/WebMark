from ddf import M, N
from django.contrib.auth.models import User
from django.test import Client, TestCase
from ..models import Molecule


class TestNewMolecule(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = N(User, username=M(r'________'), password=M(r'________'))
        self.client.post(
            '/signup/',
            {'username': self.test_user.username,
             'password1': self.test_user.password, 'password2': self.test_user.password}
        )
        self.client.post(
             '/accounts/login/',
             {'username': self.test_user.username, 'password': self.test_user.password})

    def test_add_molecule(self):
        test_molecule = N(Molecule, name=M(r'-____ium ______ide'))
        self.client.post('/newMolecule/',
                         {'name': test_molecule.name,
                          'structure': 'H 0.0 0.0 0.0\nLi 0.0 0.0 1.6',
                          'active_orbitals': 'A1 1 2 4 5 7',
                          'basis_set': 'sto-3g',
                          'transformation': 'Bravyi-Kitaev'})
        result = len(Molecule.objects.filter(name=test_molecule.name))
        self.assertEqual(result, 1)

    def test_add_molecule_with_no_orbitals(self):
        self.client.post('/newMolecule/',
                         {'name': 'Lithium hydride3',
                          'structure': 'H 0.0 0.0 0.0\nLi 0.0 0.0 1.6',
                          'basis_set': 'sto-3g',
                          'transformation': 'Bravyi-Kitaev'})
        result = len(Molecule.objects.filter(name='Lithium hydride3'))
        self.assertEqual(result, 1)
