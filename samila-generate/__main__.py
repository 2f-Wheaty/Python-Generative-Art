#!/bin/python

import time
import random
import math
import matplotlib.pyplot as plt
from samila import GenerativeImage, Projection

def f1(x,y):
    result = random.uniform(-1,1) * x**2  - math.sin(y**2) + abs(y-x)
    return result

def f2(x,y):
    result = random.uniform(-1,1) * y**3 - math.cos(x**2) + 2*x
    return result

def basic(time):
	for amount in range(int(time)):
		print(f"starting {amount}")
		try:
			t = time.time()
			t = int(t)
			g = GenerativeImage(f1,f2)
			g.generate(seed=t)
			g.plot()
			#plt.show()
			amount = amount + 1
			g.save_image(file_adr=f"webserver/content/samila/basic-function/samila{amount}.png")
		except KeyboardInterrupt:
			print('ending')
			break

def projectionRectilinear(time):
	for amount in range(int(time)):
		g = GenerativeImage(f1,f2)
		g.generate()
		g.plot(projection=Projection.RECTILINEAR)
		g.save_image(file_adr=f"webserver/content/samila/projection-function/samilaRectilinear{amount}.png")

def projectionPolar(time):
	for amount in range(int(time)):
		g = GenerativeImage(f1,f2)
		g.generate()
		g.plot(projection=Projection.POLAR)
		g.save_image(file_adr=f"webserver/content/samila/projection-function/samilaPolar{amount}.png")

def projectionAitoff(time):
	for amount in range(int(time)):
		g = GenerativeImage(f1,f2)
		g.generate()
		g.plot(projection=Projection.AITOFF)
		g.save_image(file_adr=f"webserver/content/samila/projection-function/samilaAitoff{amount}.png")

def projectionHammer(time):
	for amount in range(int(time)):
		g = GenerativeImage(f1,f2)
		g.generate()
		g.plot(projection=Projection.HAMMER)
		g.save_image(file_adr=f"webserver/content/samila/projection-function/samilaHammer{amount}.png")

def projectionLambert(time):
	for amount in range(int(time)):
		g = GenerativeImage(f1,f2)
		g.generate()
		g.plot(projection=Projection.LAMBERT)
		g.save_image(file_adr=f"webserver/content/samila/projection-function/samilaLambert{amount}.png")

def projectionMollweide(time):
	for amount in range(int(time)):
		g = GenerativeImage(f1,f2)
		g.generate()
		g.plot(projection=Projection.MOLLWEIDE)
		g.save_image(file_adr=f"webserver/content/samila/projection-function/samilaMollweide{amount}.png")

def srange(time):
	for amount in range(int(time)):
		g = GenerativeImage(f1,f2)
		g.generate(start = -2*math.pi,step=0.1,stop=0)
		g.plot()
		g.save_image(file_adr=f"webserver/content/samila/range-function/range{amount}.png")

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-B',
						action='store_true',
	                    dest='basic',
	                    help='Runs the different functions from the readme',
	                    )
	parser.add_argument('-P',
	                    default='False',
	                    dest='projection',
	                    help='Runs the projection function from the readme. Choose Rectilinear, Polar, Aitoff, Hammer, Lambert and Mollweide',
	                    type=str
	                    )
	parser.add_argument('-R', '--Range',
	                    default='False',
	                    dest='range',
	                    help='Runs the range function from the readme',
	                    type=str
	                    )
	parser.add_argument('-r', '--Regeneration',
	                    default=False,
	                    dest='regeneration',
	                    help='Runs the regeneration function from the readme',
	                    type=str
	                    )


	args = parser.parse_args()
	if args.basic == True:
		basic()
	elif args.projection != 'False':
		if args.projection.lower() == 'rectilinear':
			projectionRectilinear()
		elif args.projection.lower() == 'polar':
			projectionPolar()
		elif args.projection.lower() == 'aitoff':
			projectionAitoff()
		elif args.projection.lower() == 'hammer':
			projectionHammer()
		elif args.projection.lower() == 'lambert':
			projectionLambert()
		else:
			print('To stay with -P, Please pick Rectilinear, Polar, Aitoff, Hammer, or Lambert.')
	elif args.range != 'Range':
		srange(args.range)
		
	else:
		print(args.projection)
		print('Pick Basic, Projection, Range, or Regeneration')