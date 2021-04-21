import matplotlib.pyplot as plt
xs = []
ys = []
with open("/home/homer/workdir/Photodiode_Readings_20210419_pd-test-1618850099.txt", "r") as file1:
   while True:
      ln = file1.readline()
      if not ln:
            break
      vals = ln.strip().split() 
      
      print("ln = %s" % ln)
      print("vals = %f %f" % (float(vals[0]),float(vals[1])))
      if float(vals[1])!=0.0 :
         xs.append(float(vals[0]))
         ys.append(abs(float(vals[1])))

#figp, axs = plt.subplots(1, 1, figsize=(10, 10))
plt.figure(figsize=(10,10))
plt.plot(xs, ys, c='r',marker='+')
plt.xlabel('time', fontsize=20)
plt.ylabel('PD abs(current)', fontsize=20)
plt.yscale('log')
###############################



#fig = plt.figure(figsize=(100,100))
plt.show()
