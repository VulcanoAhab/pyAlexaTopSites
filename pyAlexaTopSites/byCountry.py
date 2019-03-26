import csv
import hmac
import base64
import hashlib
import argparse
import requests

from lxml import etree
from datetime import datetime
from collections import OrderedDict
from urllib.parse import quote, quote_plus, urlencode

class AmazonUtils:
    """
    """

    _region="us-west-1"
    _service="AlexaTopSites"


    @classmethod
    def sign(cls, key, msg):
        """
        """
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    @classmethod
    def getSignatureKey(cls, key, dateStamp, regionName, serviceName):
        """
        """
        kDate = AmazonUtils.sign(("AWS4" + key).encode("utf-8"), dateStamp)
        kRegion = AmazonUtils.sign(kDate, regionName)
        kService = AmazonUtils.sign(kRegion, serviceName)
        kSigning = AmazonUtils.sign(kService, "aws4_request")
        return kSigning


class Ranking:
    """
    """
    def __init__(self,  access_key, access_secret,
                        country_code, count, start):
        """
        """
        self.method="GET"
        self.host="ats.us-west-1.amazonaws.com"
        self.endpoint="http://ats.us-west-1.amazonaws.com/api"
        self.canonical_uri="/api"
        self.region="us-west-1"
        self.service="AlexaTopSites"
        self.access_key=access_key
        self.access_secret=access_secret
        self.country_code=country_code
        self.count=count
        self.start=start
        self.query=OrderedDict({
            "Action":"TopSites",
            "Count":self.count,
            "CountryCode":self.country_code,
            "ResponseGroup":"Country",
            "Start":self.start
                 })
        self.namespaces={"aws": "http://ats.amazonaws.com/doc/2005-07-11"}
        self._alexa_sites={}

    def _mine_text(self, xObject, xPattern):
        """
        """
        elements=xObject.xpath(xPattern,namespaces=self.namespaces)
        if not len(elements):return None
        return elements[0].text

    def _mine_container(self, xObject, xPattern):
        """
        """
        elements=xObject.xpath(xPattern,namespaces=self.namespaces)
        if not len(elements):return None
        return elements[0]

    def _mine_containers(self, xObject, xPattern):
        """
        """
        return xObject.xpath(xPattern,namespaces=self.namespaces)

    def prepare_request(self):
        """
        """
        print("[+] Preparing request.")

        ## set vals
        request_parameters=urlencode(self.query)
        nowDate=datetime.utcnow()
        amzdate=nowDate.strftime("%Y%m%dT%H%M%SZ")
        datestamp=nowDate.strftime("%Y%m%d")
        canonical_querystring=request_parameters
        #create canonical request
        canonical_headers = ("host:" + self.host + "\n"
                             + "x-amz-date:" + amzdate + "\n")
        signed_headers = "host;x-amz-date"
        payload_hash = hashlib.sha256(b"").hexdigest()
        canonical_request = (self.method + "\n" + self.canonical_uri + "\n"
                            + canonical_querystring + "\n" + canonical_headers
                            + "\n" + signed_headers + "\n" + payload_hash)
        #create string to sign
        algorithm = "AWS4-HMAC-SHA256"
        credential_scope = (datestamp + "/" + self.region +
                            "/" + self.service + "/" + "aws4_request")
        string_to_sign = (algorithm + "\n"
            +  amzdate + "\n" +  credential_scope + "\n"
            +  hashlib.sha256(canonical_request.encode()).hexdigest())
        #sign string
        signing_key = AmazonUtils.getSignatureKey(self.access_secret,
                                      datestamp, self.region, self.service)
        signature = hmac.new(signing_key,
                            (string_to_sign).encode("utf-8"),
                            hashlib.sha256).hexdigest()
        #add signed to request
        authorization_header = (algorithm + " " + "Credential="
                               + self.access_key + "/"
                               + credential_scope + ", "
                               +  "SignedHeaders=" + signed_headers
                               + ", " + "Signature=" + signature)
        #final request items
        self.url = self.endpoint + "?" + canonical_querystring
        self.headers={"x-amz-date":amzdate,
                 "Authorization":authorization_header,
                 "Host":self.host}

    @property
    def sites(self):
        """
        """
        if self._alexa_sites:return self._alexa_sites
        r=requests.get(self.url, headers=self.headers)
        r.raise_for_status()
        xml = etree.fromstring(r.text)
        sites = self._mine_containers(xml, "//aws:Site")
        for site in sites:
            site_domain=self._mine_text(site, "./aws:DataUrl")
            country_data=self._mine_container(site, "./aws:Country")
            country_rank=self._mine_text(country_data, "./aws:Rank")
            country_reach=self._mine_text(country_data,
                                          "./aws:Reach/aws:PerMillion")
            country_pageviews=self._mine_text(country_data,
                                              "./aws:PageViews/aws:PerUser")
            global_rank=self._mine_text(site, "./aws:Global/aws:Rank")
            self._alexa_sites[site_domain]={
                "site":site_domain,
                "country_rank":country_rank,
                "country_reach":country_reach,
                "country_pageviews":country_pageviews,
                "global_rank":global_rank
            }
        return self._alexa_sites

    def save_site(self, output_file):
        """
        """
        fieldnames=[
            "site", "country_rank", "country_reach",
            "country_pageviews","global_rank"
        ]
        suffix="_{:%d-%m-%Y}.csv".format(datetime.utcnow())
        output_file=output_file.strip(".csv")+suffix

        fd=open(output_file, "w")
        csvFile=csv.DictWriter(fd, fieldnames=fieldnames)
        csvFile.writeheader()
        print("[+] Making request. Country:{}".format(self.country_code))
        for domain, row in alexa.sites.items():csvFile.writerow(row)
        fd.close()
        print("[+] Done saving file: {}".format(args.output_file))



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get AlexaTopSites"\
                                                 "for a specific country."\
                                                 "Command line with CSV"\
                                                 "output.")
    parser.add_argument("-k", "--access_key_id")
    parser.add_argument("-s", "--secret_access_key")
    parser.add_argument("-c", "--country_code")
    parser.add_argument("-o", "--output_file", default="alexaTopSites")
    parser.add_argument("-a", "--start", type=int, default=1)
    parser.add_argument("-z", "--count", type=int, default=1000)
    args = parser.parse_args()

    if not args.count:
        parser.print_help()
        exit(2)
    access_key_id = args.access_key_id
    secret_access_key = args.secret_access_key
    country_code = args.country_code
    start = args.start
    count = args.count
    output_file=args.output_file

    alexa=Ranking(access_key=access_key_id,
                 access_secret=secret_access_key,
                 country_code=country_code, count=count,
                 start=start)
    alexa.prepare_request()
    alex.save_site(args.output_file)
