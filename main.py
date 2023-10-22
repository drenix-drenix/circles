import logging
from aiogram import Bot, Dispatcher, types, executor
from moviepy.editor import *

API_TOKEN = "6848051764:AAH8nf-gYdUZox6VDF8ZWmZe2xWCRXTqq-c"


logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)




async def start(message: types.Message):
    await message.answer("👋 Привет, я бот превращающий обычный видео в кружки. Отправьте мне видео, и я преобразую его в видеокружок.\n⚠️ Не забудьте разрешить голосовые сообщения в настройках, если вы их ограничили!")

async def process_video(message: types.Message):
    video_file_id = message.video.file_id
    await message.bot.download_file_by_id(video_file_id, "input_video.mp4")

    input_video = VideoFileClip("input_video.mp4")
    w, h = input_video.size
    circle_size = 360
    aspect_ratio = float(w) / float(h)
    
    if w > h:
        new_w = int(circle_size * aspect_ratio)
        new_h = circle_size
    else:
        new_w = circle_size
        new_h = int(circle_size / aspect_ratio)
        
    resized_video = input_video.resize((new_w, new_h))
    output_video = resized_video.crop(x_center=resized_video.w/2, y_center=resized_video.h/2, width=circle_size, height=circle_size)
    output_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")

    with open("output_video.mp4", "rb") as video:
        await message.bot.send_video_note(chat_id=message.chat.id, video_note=video, duration=int(output_video.duration), length=circle_size)


dp.register_message_handler(start, commands=["start"])
dp.register_message_handler(process_video, content_types=types.ContentType.VIDEO)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
