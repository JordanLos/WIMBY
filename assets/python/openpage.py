import requests
import webbrowser

headers = {'User-Agent':'Mozilla/5.0'}
payload = {'txtPlan': '454'}
session = requests.Session()
webbrowser.open( session.post('http://www.esar.alberta.ca/esarmain.aspx',headers=headers,data=payload) )

