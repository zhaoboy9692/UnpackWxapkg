解包微信小程序

适合用来学习

2.文件头里面定义为

  1字节：`0xBE` 
  
 	4字节0x00 00 02 02=文件个数，514个文件

3.读取文件信息

	4字节0x00 00 00 10 =文件名长度 16个长度

	文件名长度个字节0x2f 61 70....6f 6e =文件名 文件名字 /app-config.json

	4字节0x00 00 2c 60 =文件偏移 offset

	4字节0x00 00 5f 94 =文件大小 size

	以上持续循环读取，

4.写入文件

	文件内容从0+offset读取大小为size的内容
