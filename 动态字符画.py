import cv2
import os
import shutil
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt 
from moviepy.editor import VideoFileClip, AudioFileClip

import time

# 视频文件名
video_filename = "video.mp4"

# 打开视频文件
video = cv2.VideoCapture(video_filename)

frame_rate = video.get(cv2.CAP_PROP_FPS)  # 获取帧率
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取帧宽度
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取帧高度

def Capture_frames(video):
    # 输出帧的文件夹路径
    output_folder = "temp"

    # 删除目录（如果存在）
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # 创建目录
    os.makedirs(output_folder)

    # 逐帧读取视频并保存每一帧
    frame_count = 0
    while True:
        success, frame = video.read()
        if not success:
            break

        print(f"正获取 第{frame_count}帧")

        # 构建每个帧的文件名
        frame_filename = os.path.join(output_folder, f"{frame_count}.jpg")

        # 保存帧为图像文件
        cv2.imwrite(frame_filename, frame)

        frame_count += 1


def Extract_music(video_filename):
    print("正在加载声音……")
    video = VideoFileClip(video_filename)
    audio = video.audio
    output_file = "temp_audio.mp3"
    audio.write_audiofile(output_file)



def Convert_to_char(frame_width, frame_height):
    width, height = (int(frame_width/5), int(frame_height/5))

    # temp文件夹路径
    temp_folder = "temp"

    file_names = os.listdir(temp_folder)  # 获取文件夹中的所有文件名

    # 使用lambda函数将文件名字符串转换为对应的数字，并按数字进行排序
    jpg_files = sorted(file_names, key=lambda x: int(x.split(".")[0]))


    # 统计jpg文件数量
    jpg_count = len(jpg_files)

    # 输出帧的文件夹路径
    output_folder = "temp_out"

    # 删除目录（如果存在）
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # 创建目录
    os.makedirs(output_folder)

    ASCII = '''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. '''

    total = len(jpg_files)

    completed = 0

    for frame in range(total):
        img = Image.open(os.path.join("temp", str(jpg_files[frame]))).convert('L').resize((width, height))

        txt = ''
        for y in range(height): 
            for x in range(width):
                pos = (x, y)
                gray = img.getpixel(pos)
                index = int(gray/256*70)
                txt += ASCII[index] + ' '
            txt += '\n'

        with open("字符画.txt", "w") as file:
    # 写入字符串
            file.write(txt)

        img_new = Image.new('RGBA', (width*50, height*50))
        draw = ImageDraw.Draw(img_new)
        draw.text((0,0), txt, fill=(0, 0, 0, 255))


        # 去除空白
        bbox = img_new.getbbox()  # 获取画布中非空白区域的边界框
        img_new_cropped = img_new.crop(bbox)  # 根据边界框裁剪画布

        img_new_cropped = img_new_cropped.resize((frame_width, frame_height))

        img_new_final = Image.new('RGBA', (frame_width, frame_height), (255, 255, 255))  # 创建白色背景的图像
        img_new_final = Image.alpha_composite(img_new_final, img_new_cropped)  # 将裁剪后的图像粘贴到新的图像中

        frame_filename = os.path.join(output_folder, f"{frame}.jpg")

        img_new_final_rgb = img_new_final.convert('RGB')

        img_new_final_rgb.save(frame_filename, 'JPEG')

        completed += 1
        # 清除前一行的输出
        print("\r" + " " * 100 + "\r", end="", flush=True)

        # 输出新的内容
        print(f"成功处理 {completed}/{total} 帧")

def Convert():

        # 输出帧的文件夹路径
    output_folder = "JPEG_out"

    # 删除目录（如果存在）
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # 创建目录
    os.makedirs(output_folder)

    image_folder = "temp_out"
    # 获取图像文件列表

    file_names = os.listdir(image_folder)  # 获取文件夹中的所有文件名

    # 使用lambda函数将文件名字符串转换为对应的数字，并按数字进行排序
    image_files = sorted(file_names, key=lambda x: int(x.split(".")[0]))

    for i in range(len(image_files)):

        image_path = os.path.join(image_folder, image_files[i])

        # 打开PNG图像
        png_image = Image.open(image_path)

        # 转换并保存为JPEG图像

        output_file_name = str(image_files[i])[:-4] + '.jpg'
        output_path = os.path.join(output_folder, output_file_name)
        
        png_image.convert('RGB').save(output_path, 'JPEG')

        # 关闭图像文件
        png_image.close()

        #os.remove(image_path)

def Composite_video(frame_rate, frame_width, frame_height):

    print("正在混合帧……")
    # 图像文件夹路径
    image_folder = "temp_out"

    # 输出视频文件名
    output_video = "output.mp4"

    # 获取图像文件列表

    file_names = os.listdir(image_folder)  # 获取文件夹中的所有文件名

    # 使用lambda函数将文件名字符串转换为对应的数字，并按数字进行排序
    image_files = sorted(file_names, key=lambda x: int(x.split(".")[0]))

    # 设置视频帧率和尺寸
    frame_size = (frame_width, frame_height)  # 帧尺寸，根据需求调整

    # 创建视频编写器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video, fourcc, frame_rate, frame_size, True)

    # 逐个读取图像文件并写入视频
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        print(image_path)
        frame = cv2.imread(image_path)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_rgb = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2RGB)
        video_writer.write(frame)

    print("正在混合声音……")
    # 释放视频编写器
    video_writer.release()

        # 加载音频文件
    audio = AudioFileClip("temp_audio.mp3")

    # 加载合成的视频文件
    video = VideoFileClip(output_video)

    # 将音频与视频进行合并
    video = video.set_audio(audio)

    # 设置输出文件名
    final_output = "output_with_audio.mp4"

    # 保存最终合成的视频文件
    video.write_videofile(final_output, codec="libx264", audio_codec="aac")

    # 删除临时合成的视频文件
    os.remove(output_video)

start = time.time()

#Capture_frames(video)
#Extract_music(video_filename)
Convert_to_char(frame_width, frame_height)
#Convert()
#Composite_video(frame_rate, frame_width, frame_height)
# 释放视频对象
video.release()

end = time.time()
time_difference = end - start
print(f"转换完毕，一共花费了 {time_difference} 秒。")