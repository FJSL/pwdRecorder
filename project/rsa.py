# -*- encoding:utf-8 -*-  
import math,random#导入模块  
  
def prime_num(max_num):#生成小于max_num的素数列表  
    prime_num=[]  
    for i in xrange(2,max_num):  
        temp=0  
        sqrt_max_num=int(math.sqrt(i))+1  
        for j in xrange(2,sqrt_max_num):  
            if i%j==0:  
                temp=j  
                break  
        if temp==0:  
            prime_num.append(i)  
  
    return prime_num  
  
def rsa_key():#生成密钥的函数  
    prime=prime_num(400)#小于400的素数列表  
    p=random.choice(prime[-50:-1])#从后50个素数中随机选择一个作为p  
    q=random.choice(prime[-50:-1])#从后50个素数中随机选择一个作为q  
    while(p==q):#如果p和q相等则重新选择  
        q=random.choice(prime[-50:-1])  
    N=p*q  
    r=(p-1)*(q-1)  
    r_prime=prime_num(r)  
    e=random.choice(r_prime)#随机选一个素数  
    d=0  
    for n in xrange(2,r):  
        if (e*n)%r==1:  
            d=n  
            break  
    return ((N,e),(N,d))  
  
def encrypt(pub_key,origal):#生成加密用的公钥  
    N,e=pub_key  
    return (origal**e)%N  
  
def decrypt(pri_key,encry):#生成解密用的私钥  
    N,d=pri_key  
    return (encry**d)%N  