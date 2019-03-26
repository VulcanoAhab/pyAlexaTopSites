import os
import glob
import unittest
from pyAlexaTopSites.byCountry import Ranking


class TestTopSites(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        self._start=0
        self._code="br"
        self._count=1000
        self._output_file="test_{}_top-sites".format(self._code)
        self._alexa=Ranking(
            access_key=os.getenv("access_key_id"),
            access_secret=os.getenv("secret_access_key"),
            country_code=self._code,
            count=self._count,
            start=self._start
        )

    def test_save_site(self):
        """
        """
        self._alexa.prepare_request()
        self._alexa.save_site(self._output_file)
        files_list=glob.glob(self._output_file+"*")
        self.assertTrue(any(files_list))
        os.remove(files_list[0])


if __name__ == "__main__":
    unittest.main()




### ALEXA_COUNTRIES_CODES

countries_and_codes=[
    ("Andorra","AD"),
    ("UnitedArabEmirates","AE"),
    ("Albania","AL"),
    ("Armenia","AM"),
    ("NetherlandsAntilles","AN"),
    ("Argentina","AR"),
    ("Austria","AT"),
    ("Australia","AU"),
    ("Azerbaijan","AZ"),
    ("BosniaandHerzegovina","BA"),
    ("Barbados","BB"),
    ("Bangladesh","BD"),
    ("Belgium","BE"),
    ("Bulgaria","BG"),
    ("Bahrain","BH"),
    ("Brunei","BN"),
    ("Bolivia","BO"),
    ("Brazil","BR"),
    ("Bahamas","BS"),
    ("Belarus","BY"),
    ("Canada","CA"),
    ("Switzerland","CH"),
    ("Coted&#39;Ivoire","CI"),
    ("Chile","CL"),
    ("Cameroon","CM"),
    ("China","CN"),
    ("Colombia","CO"),
    ("CostaRica","CR"),
    ("SerbiaandMontenegro","CS"),
    ("Cyprus","CY"),
    ("CzechRepublic","CZ"),
    ("Germany","DE"),
    ("Denmark","DK"),
    ("DominicanRepublic","DO"),
    ("Algeria","DZ"),
    ("Ecuador","EC"),
    ("Estonia","EE"),
    ("Egypt","EG"),
    ("Spain","ES"),
    ("Finland","FI"),
    ("France","FR"),
    ("UnitedKingdom","GB"),
    ("Georgia","GE"),
    ("FrenchGuiana","GF"),
    ("Ghana","GH"),
    ("Guadeloupe","GP"),
    ("Greece","GR"),
    ("Guatemala","GT"),
    ("Guam","GU"),
    ("HongKong","HK"),
    ("Honduras","HN"),
    ("Croatia","HR"),
    ("Hungary","HU"),
    ("Indonesia","ID"),
    ("Ireland","IE"),
    ("Israel","IL"),
    ("India","IN"),
    ("Iraq","IQ"),
    ("Iran","IR"),
    ("Iceland","IS"),
    ("Italy","IT"),
    ("Jamaica","JM"),
    ("Jordan","JO"),
    ("Japan","JP"),
    ("Kenya","KE"),
    ("Kyrgyzstan","KG"),
    ("Cambodia","KH"),
    ("SouthKorea","KR"),
    ("Kuwait","KW"),
    ("Kazakhstan","KZ"),
    ("Laos","LA"),
    ("Lebanon","LB"),
    ("SriLanka","LK"),
    ("Lithuania","LT"),
    ("Luxembourg","LU"),
    ("Latvia","LV"),
    ("LibyanArabJamahiriya","LY"),
    ("Morocco","MA"),
    ("Moldova","MD"),
    ("Madagascar","MG"),
    ("Macedonia","MK"),
    ("Mongolia","MN"),
    ("Macao","MO"),
    ("Martinique","MQ"),
    ("Malta","MT"),
    ("Mauritius","MU"),
    ("Maldives","MV"),
    ("Mexico","MX"),
    ("Malaysia","MY"),
    ("NewCaledonia","NC"),
    ("Nigeria","NG"),
    ("Nicaragua","NI"),
    ("Netherlands","NL"),
    ("Norway","NO"),
    ("Nepal","NP"),
    ("NewZealand","NZ"),
    ("Oman","OM"),
    ("Panama","PA"),
    ("Peru","PE"),
    ("FrenchPolynesia","PF"),
    ("Philippines","PH"),
    ("Pakistan","PK"),
    ("Poland","PL"),
    ("PuertoRico","PR"),
    ("PalestinianTerritory","PS"),
    ("Portugal","PT"),
    ("Paraguay","PY"),
    ("Qatar","QA"),
    ("Reunion","RE"),
    ("Romania","RO"),
    ("Russia","RU"),
    ("SaudiArabia","SA"),
    ("Sudan","SD"),
    ("Sweden","SE"),
    ("Singapore","SG"),
    ("Slovenia","SI"),
    ("Slovakia","SK"),
    ("Senegal","SN"),
    ("ElSalvador","SV"),
    ("SyrianArabRepublic","SY"),
    ("Thailand","TH"),
    ("Tunisia","TN"),
    ("Turkey","TR"),
    ("TrinidadandTobago","TT"),
    ("Taiwan","TW"),
    ("Ukraine","UA"),
    ("UnitedStates","US"),
    ("Uruguay","UY"),
    ("Venezuela","VE"),
    ("Vietnam","VN"),
    ("Yemen","YE"),
    ("SouthAfrica","ZA"),
]
