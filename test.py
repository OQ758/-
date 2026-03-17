import cv2
import os

# ---------------------- 配置参数 ----------------------
SAVE_FOLDER = "D:/desk/photo"  # 照片保存文件夹（可修改为你想要的路径）
START_INDEX = 0  # 照片命名起始序号（从0开始）


# ------------------------------------------------------

def init_save_folder():
    """初始化保存文件夹，不存在则创建"""
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        print(f"创建保存文件夹：{SAVE_FOLDER}")
    else:
        print(f"保存文件夹已存在：{SAVE_FOLDER}")


def get_next_file_name():
    """获取下一个照片的文件名（按序号递增）"""
    global START_INDEX
    # 构建文件名（格式：0.jpg, 1.jpg, 2.jpg...）
    file_name = f"{START_INDEX}.jpg"
    file_path = os.path.join(SAVE_FOLDER, file_name)

    # 防止序号重复（如果文件夹中已有该序号文件，自动递增到下一个可用序号）
    while os.path.exists(file_path):
        START_INDEX += 1
        file_name = f"{START_INDEX}.jpg"
        file_path = os.path.join(SAVE_FOLDER, file_name)

    return file_path


def main():
    # 初始化文件夹
    init_save_folder()

    # 打开摄像头（0表示默认摄像头，多个摄像头可尝试1、2等）
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("错误：无法打开摄像头！")
        return

    print("=" * 50)
    print("操作说明：")
    print("1. 按下 'p' 键拍照（照片自动按序号保存）")
    print("2. 按下 'q' 键退出程序")
    print("=" * 50)

    while True:
        # 读取摄像头画面
        ret, frame = cap.read()

        # 检查画面是否读取成功
        if not ret:
            print("警告：无法读取摄像头画面！")
            break

        # 显示实时画面（窗口标题：Camera）
        cv2.imshow("Camera", frame)

        # 等待按键输入（1ms延迟，不阻塞画面显示）
        key = cv2.waitKey(1) & 0xFF

        # 按下 'p' 键拍照保存
        if key == ord('p'):
            file_path = get_next_file_name()
            # 保存照片
            cv2.imwrite(file_path, frame)
            print(f"✅ 照片已保存：{file_path}")
            # 序号自增（确保下一张照片序号正确）
            global START_INDEX
            START_INDEX += 1

        # 按下 'q' 键退出程序
        elif key == ord('q'):
            print("📤 退出程序...")
            break

    # 释放摄像头资源
    cap.release()
    # 关闭所有窗口
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()