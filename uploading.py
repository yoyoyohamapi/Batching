#! /usr/bin/env python
#coding:utf-8

import argparse
import requests
import json
import os
import os.path

TYPE_SRC = 'src'
TYPE_CROP = 'crop'
TYPE_SEG = 'seg'

def initParser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-v","--version",help="show the version of BatchUploading",action="store_true")
	parser.add_argument("-r","--root",help="required, set the root dir of images")
	parser.add_argument("-u","--url",help="required, set the url of the Uploading REST")
	parser.add_argument("-t","--token",help="required, set the api token of the REST")
	args = parser.parse_args()
	parser.parse_args()
	if args.version:
		version();
	else:
		batching(root=args.root,url=args.url,token=args.token);

def version():
	print 'PatchingUploading.py: 1.0'

def batching(root,url,token):
	headers = {'Authorization':'Bearer '+token,'Accept':'application/json'}
	count = 0
	# 遍历根文件夹，依次处理每张图片
	for parent,dirnames,filenames in os.walk(root):
		for filename in filenames:
			# 获得文件全名
			fullName = os.path.join(parent,filename)
			# 分割文件名提取信息
			pathList = fullName.split('/')
			# 获得图像类型
			fileType = pathList[-2]
			# 对应疾病
			disease = pathList[-3]
			# 设置原图像文件名
			srcFile = fullName.replace(fileType,'src')
			# 设置裁剪后图像文件名
			cropFile =  fullName.replace(fileType,'crop')
			# 设置分割后图像文件名
			segFile = fullName.replace(fileType,'seg')
			# 如果图像类型为src，则新建图像对象,并上传原图
			if(fileType==TYPE_SRC):
				# 上传原图获得图像ID
				imageId = postImg(srcFile,disease,url,headers)
				print ("image %s has been created"%imageId)
				# 上传裁剪后的图
				uploadImg(cropFile,url,headers,TYPE_CROP,imageId)
				# 上传分割后的图
				uploadImg(segFile,url,headers,TYPE_SEG,imageId)
				count = count+1
	print("%d images have been processed"%count)

			


def uploadImg(filename,url,headers,fileType,imageId):
	apiUpload = 'api/images/upload'
	params = {'type':fileType,'image_id':imageId}
	files = {'file': open(filename, 'rb')}
	r = requests.post(url+'/'+apiUpload,headers=headers,params=params,files=files)

def postImg(filename,disease,url,headers):
	apiPost = 'api/images'
	params = {'image[disease]':disease}
	files = {'file':open(filename,'rb')}
	r = requests.post(url+'/'+apiPost,headers=headers,data=params,files=files)
	image = r.json()
	return image['id']

def main():
	initParser()

if __name__ == '__main__':
	main()
