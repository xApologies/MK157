import unittest
from validate_promotions import current_tabular_rows, relocated_city_row


class CityRelocationTests(unittest.TestCase):
    def setUp(self):
        self.old = {'serial':'007', 'canonical_name':'Opening Ceremony / civic festival grounds',
                    'status':'WORKING', 'map_region':'southern lobe',
                    'notes':'Citywide celebration extends beyond 007; same venue.'}
        self.new = dict(self.old, serial='008', notes='Citywide celebration extends beyond 008; same venue.')

    def test_only_serial_and_its_note_reference_change(self):
        self.assertEqual(relocated_city_row(self.old, '007', '008'), self.new)
        self.assertEqual(self.old['serial'], '007')
        for a,b in [('007','009'),('005','008'),('007','007')]:
            with self.assertRaises(ValueError): relocated_city_row(self.old, a, b)
        with self.assertRaises(ValueError):
            relocated_city_row(dict(self.old, canonical_name='another shop'), '007', '008')

    def test_only_later_declared_relocation_applies(self):
        errors=[]
        require=lambda ok,msg: errors.append(msg) if not ok else None
        dest='visual-references/CITY_LOCATION_REGISTRY.csv'
        relocation={'destination':dest,'from_value':'007','to_value':'008','before_row':self.old}
        self.assertEqual(current_tabular_rows([self.old], dest, 1, [(3,relocation)], require),[self.new])
        self.assertEqual(errors,[])
        self.assertEqual(current_tabular_rows([self.old], dest, 4, [(3,relocation)], require),[self.old])
        self.assertEqual(current_tabular_rows([self.old], 'other.csv', 1, [(3,relocation)], require),[self.old])
        tampered=dict(self.old,status='LOCKED')
        current_tabular_rows([tampered],dest,1,[(3,relocation)],require)
        self.assertEqual(errors,['relocation source row differs'])


if __name__ == '__main__': unittest.main()
