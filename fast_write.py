import os
import time

# 定义每个文件的最大大小（4GB）
MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024
# 每个目录下的最大文件数量
MAX_FILES_PER_DIR = 100
# 一级目录名称
BASE_DIR = r'F:\\data'

# 创建一级目录
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

def fill_disk():
    dir_count = 0
    file_count = 0
    total_size_written = 0
    while True:
        # 生成当前目录路径
        current_dir = os.path.join(BASE_DIR, f'dir_{dir_count}')
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)
        for i in range(MAX_FILES_PER_DIR):
            file_path = os.path.join(current_dir, f'file_{file_count}.dat')
            try:
                with open(file_path, 'wb') as f:
                    written = 0
                    while written < MAX_FILE_SIZE:
                        # 每次写入 1MB 数据
                        chunk_size = 1024 * 1024
                        data = b'x' * chunk_size
                        try:
                            f.write(data)
                            written += chunk_size
                            total_size_written += chunk_size
                            # 每写入 1GB 数据打印一次进度
                            if total_size_written % (1024 * 1024 * 1024) == 0:
                                print(f"已写入 {total_size_written / (1024 * 1024 * 1024):.2f} GB")
                        except OSError:
                            print("磁盘空间已满或写入错误，停止写入。")
                            return
            except Exception as e:
                print(f"写入文件 {file_path} 时出错: {e}")
            file_count += 1
        dir_count += 1


if __name__ == "__main__":
    start_time = time.time()
    fill_disk()
    end_time = time.time()
    print(f"写入完成，耗时: {end_time - start_time:.2f} 秒")
