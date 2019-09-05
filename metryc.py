from influxdb import InfluxDBClient
import psutil
from time import sleep

client = InfluxDBClient(database="otus")

def get_cpu_load():
	cores = psutil.cpu_percent(interval=0.4, percpu=True)
	print('cores', cores)
	data = {}
	for core, load in enumerate(cores):
		data['cpu{}'.format(core)] = load
	return data

def log_cpu_load():
	cpus = get_cpu_load()
	json_data = []
	for cpu, load in cpus.items():
		json_data.append({
			'measurement': 'cpu_usage',
			'tags':{
				'server': 'localhost',
				'cpu': cpu,
			},
			'fields': {
				'value': load,
			}
		}) 
	return client.write_points(json_data) 

if __name__ == '__main__':
	while True:
		#log_cpu_load()
		print(client.query("SELECT * FROM reqtime"))
		sleep(1)

