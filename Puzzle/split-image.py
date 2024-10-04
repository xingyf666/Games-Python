from PIL import Image
import os

im = Image.open('星空.jpg')
box = (100, 100, 700, 700)
region = im.crop(box)
region.save('crop.png')

def splitimage(src, rownum, colnum, dstpath):
    img = Image.open(src)
    w, h = img.size
    if rownum <= h and colnum <= w:
        print('Original image info: {}x{}, {}, {}'.format(w, h, img.format, img.mode))
        print('开始处理图片切割，请稍后……')
        s = os.path.split(src)
        if dstpath == '':                       #没有输入路径
            dstpath = s[0]                      #使用原图片所在目录
        fn = s[1].split('.')                        #s[1]是源图片文件名
        basename = fn[0]                        #主文件名
        ext = fn[-1]                                #扩展名
        num = 0
        rowheight = h // rownum
        colwidth = w // colnum
        for r in range(rownum):
            for c in range(colnum):
                box = (c*colwidth, r*rowheight, (c+1)*colwidth, (r+1)*rowheight)
                img.crop(box).save(os.path.join(dstpath, basename+'_'+str(num)+'.'+ext))
                num += 1
        print('图片切割完毕，共生成{}张小图片。'.format(num))
    else:
        print('不合法的行列切割参数！')

src = input('请输入图片文件路径：')
if os.path.isfile(src):
    dstpath = input('请输入图片输出目录（不输入路径则表示使用原图片所在目录）：')
    if dstpath == '' or os.path.exists(dstpath):
        row = int(input('请输入切割行数：'))
        col = int(input('请输入切割列数：'))
        if row > 0 and col > 0:
            splitimage(src, row, col, dstpath)
        else:
            print('无效的行列切割参数！')
    else:
        print('图片输出目录{}不存在！'.format(dstpath))
else:
    print('图片文件{}不存在！'.format(src))
