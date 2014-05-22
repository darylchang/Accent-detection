f = open('final.txt','r')
lines = f.readlines()
nums = [line.split()[2] for line in lines]
nums = [float(num[:-1]) for num in nums]
print nums.index(max(nums)), max(nums)
