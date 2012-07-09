import picka
import timeit

ma = timeit.Timer(picka.male_full_name).timeit()
fe = timeit.Timer(picka.female_full_name).timeit()

print "Albanian: " + str(ma)
print "English: " + str(fe)
