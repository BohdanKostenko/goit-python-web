import sys
import asyncio
import os
from aiopath import AsyncPath
import aioshutil
from time import time


FORMATS = {"IMAGES": (".jpeg", ".png", ".jpg"),
           "VIDEOS": (".avi", ".mp4", ".mov"),
           "DOCUMENTS": (".doc", ".docx", ".txt", ".pdf",
                         ".xlsx", ".xls", ".pptx", ".csv"),
           "MUSIC": (".mp3", ".ogg", ".wav", ".amr"),
           "ARCHIVE": (".zip", ".tar", ".gztar", ".bztar", ".xztar")}


IGNOR = "ARCHIVE", "IMAGES", "MUSIC", "VIDEOS", "DOCUMENTS", "UNPACKED ARCHIVES"


async def creat_folder(path_to_sorting, folder, files, file):
    path_to_sorting = str(path_to_sorting)
    if not os.path.exists(path_to_sorting + "\\" + folder):
        os.mkdir(path_to_sorting + "\\" + folder)
    if os.path.isfile(files):
        if files != path_to_sorting + "\\" + folder + "\\" + file:
            if file.endswith(FORMATS["ARCHIVE"]):
                name_folder_archive = file.split(".")
                await aioshutil.unpack_archive(files, path_to_sorting + "\\UNPACKED ARCHIVES\\" + name_folder_archive[0])
                os.replace(files, path_to_sorting + "\\" + folder + "\\" + file)
            else:
                os.replace(files, path_to_sorting + "\\" + folder + "\\" + file)


async def remove_folder(folder_path):
    if not os.listdir(folder_path):
        os.removedirs(folder_path)


async def search_file(path_to_sorting, files_list):
    for root, dirs, files in os.walk(path_to_sorting):
        for file in files:
            path_file = os.path.join(root, file)
            ignor_dir = path_file.split("\\")
            for _ in IGNOR:
                if _ not in ignor_dir:
                    files_list.append(path_file)
                else:
                    continue


async def sort_file(path_to_sorting, files_list):
    await asyncio.sleep(0.1)
    for files in files_list:
        file = files.split("\\")
        file = file[-1]
        for folder, format_files in FORMATS.items():
            if file.endswith(format_files):
                await creat_folder(path_to_sorting, folder, files, file)
            else:
                continue


async def normalize(path_to_sorting):

    alphabet = {ord('??'): 'A',
                ord('??'): 'B',
                ord('??'): 'V',
                ord('??'): 'G',
                ord('??'): 'D',
                ord('??'): 'E',
                ord('??'): 'Je',
                ord('??'): 'Zh',
                ord('??'): 'Z',
                ord('??'): 'I',
                ord('??'): 'Y',
                ord('??'): 'K',
                ord('??'): 'L',
                ord('??'): 'M',
                ord('??'): 'N',
                ord('??'): 'P',
                ord('??'): 'R',
                ord('??'): 'S',
                ord('??'): 'T',
                ord('??'): 'U',
                ord('??'): 'F',
                ord('??'): 'Kh',
                ord('??'): 'C',
                ord('??'): 'Ch',
                ord('??'): 'Sh',
                ord('??'): 'Jsh',
                ord('??'): 'Z',
                ord('??'): 'Ih',
                ord('??'): 'Jh',
                ord('??'): 'Eh',
                ord('??'): 'Ju',
                ord('??'): 'Ja',
                ord('??'): 'a',
                ord('??'): 'b',
                ord('??'): 'v',
                ord('??'): 'g',
                ord('??'): 'd',
                ord('??'): 'e',
                ord('??'): 'je',
                ord('??'): 'zh',
                ord('??'): 'z',
                ord('??'): 'i',
                ord('??'): 'y',
                ord('??'): 'k',
                ord('??'): 'l',
                ord('??'): 'm',
                ord('??'): 'n',
                ord('??'): 'p',
                ord('??'): 'r',
                ord('??'): 's',
                ord('??'): 't',
                ord('??'): 'u',
                ord('??'): 'f',
                ord('??'): 'kh',
                ord('??'): 'c',
                ord('??'): 'ch',
                ord('??'): 'sh',
                ord('??'): 'jsh',
                ord('??'): 'z',
                ord('??'): 'ih',
                ord('??'): 'jh',
                ord('??'): 'eh',
                ord('??'): 'ju',
                ord('??'): 'ja'}
    for root, dirs, files in os.walk(path_to_sorting):
        for dir in dirs:
            path_folder = os.path.join(root, dir)
            if os.path.exists(path_folder):
                os.rename(str(path_folder), str(path_folder).translate(alphabet))
        for file in files:
            path_file = os.path.join(root, file)
            if os.path.exists(path_file):
                os.rename(str(path_file), str(path_file).translate(alphabet))


async def main():
    files_list = list()
    try:
        path_to_sorting = AsyncPath(sys.argv[1])
    except Exception:
        print("Wrong! Please try again")
    print(f'Started in {path_to_sorting}')
    start = time()
    await normalize(path_to_sorting)
    await search_file(path_to_sorting, files_list)
    await sort_file(path_to_sorting, files_list)
    for root, dirs, files in os.walk(path_to_sorting):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            await remove_folder(folder_path)
    print(f"Sorting files by the specified path {path_to_sorting} completed succesfully!")
    print(f"Program runtime {round(time() - start, 3)} s")

if __name__ == "__main__":
    asyncio.run(main())
