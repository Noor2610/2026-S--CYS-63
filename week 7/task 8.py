s1={1,2,3}
s2={4,2,6}
s3={7,2,9}
b=set.intersection(s1,s2,s3)
print(b)
c=s1.intersection_update(s1,s2,s3)
print(c)