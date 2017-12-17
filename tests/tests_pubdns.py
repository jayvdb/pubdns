import unittest
import pubdns
from mock import patch

pd = pubdns.PubDNS.__new__(pubdns.PubDNS)

class TestPubDNS(unittest.TestCase):
    """ test pubdns class methods """
    def test_get_data(self):
        """ test _get_data exception """
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 400
            with self.assertRaises(Exception):
                pd._get_data()

    def test_normalize(self):
        """ test normalize method """
        csv = (
            'ip,name,country_id,city,version,error,dnssec,reliability,'
            'checked_at,created_at\n8.8.8.8,google-public-dns-a.google.com.,'
            'US,Mountain View,,,true,1.00,2017-03-14,2009-12-04'
        )

        pd._normalize(csv)
        data = pd.data['US'].pop()
        self.assertEqual(data['city'], 'Mountain View')
        self.assertEqual(data['server'], '8.8.8.8')
        self.assertEqual(data['name'], 'google-public-dns-a.google.com.')
        self.assertEqual(data['reliability'], '1.00')
