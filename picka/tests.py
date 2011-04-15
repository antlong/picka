import english
import albanian
import timeit

alb = timeit.Timer(albanian.male_full_name).timeit()
eng = timeit.Timer(english.male_full_name).timeit()

print "Albanian: " + str(alb)
print "English: " + str(eng)
