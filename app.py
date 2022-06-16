from flask import Flask,jsonify,request,make_response
from urllib.parse import urlparse
import dotenv
import psutil
import requests
import random
import string
import datetime
app = Flask(__name__)
config=dotenv.dotenv_values("/etc/#name.conf")
rand="".join(random.choices(string.ascii_uppercase + string.digits, k=5))

def db_query(conn,query):
	p = urlparse(conn)
	response=requests.post(
		'http://%s:%s'%(p.hostname,p.port),
		data='{ "username":"%s", "password":"%s", "dbname":"%s", "query":"%s" }'%(p.username,p.password,p.path[1:],query))
	return response
def datetimex(i):
	return str(i.strftime("%d/%m/%Y %H:%M:%S"))
def micro_service(i):
	try:
		return request.get(i+'/health')
	except:
		return False 
@app.route('/health', methods=['GET'])
def health():
	for i in config:
		if i.startswith('micro'):
			exec('%s_flag=micro_service(config["%s"])'%(i,i))
	x=locals()
	db=db_query(config['db'],'SELECT VERSION();')
	return make_response(jsonify({
		'service_tracking':{
			'CPU_usage':str(psutil.cpu_percent()),'RAM_usage':str(psutil.virtual_memory().percent),'STORAGE_usage':str(psutil.disk_usage('/').percent),			'SQLITE_connection':db.status_code==200,
			'REDIS_connection':'To_Be_Implemented',
			'API_logstash':'To_Be_Implemented',
			'micro_ordermanagement':x['micro_ordermanagement_flag'],
			'micro_notification':x['micro_notification_flag'],
		}}),200)

@app.route('/api/tracking/SomeRoute', methods=['GET'])
@app.route('/api/tracking/SomeRoute', methods=['POST'])
@app.route('/api/tracking/SomeRoute', methods=['PUT'])
@app.route('/api/tracking/SomeRoute', methods=['DELETE'])
def SomeFunctionality():
	response={}
	logger(request,response)
	return "<h1>tracking service %s</H1>"%(rand)

def logger(request,response):
	tmp='headers:{'
	for header in request.headers:
		tmp=tmp+'"'+header[0]+'":"'+header[1]+'"'
	tmp=tmp+'}'
	p=open(config["log_path"],"a")
	p.write("[%s] %s %s headers:{%s} data:{%s}\n"%(datetimex(datetime.datetime.now()),request.method,request.full_path,tmp,request.get_data(as_text=True)))
	p.close()

if __name__ == "__main__":
	app.run(host=config["host"],port=config["port"])
