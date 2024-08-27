import os


class WXPkgFileInfo:
    file_name = None
    file_name_len = 0
    file_offset = 0
    file_size = 0


def is_dec(wx_file):
    """
    :param file:
    :return: 是否加密
    """
    firstMark = wx_file[:1]
    endMark = wx_file[13:14]
    return firstMark == b'\xbe' and endMark == b'\xed'


def parse_file_info(wx_pkg_file, wxapkg_file_list):
    for wx_file in wxapkg_file_list:
        dirs = app_id + wx_file.file_name
        dir_path, base_filename = os.path.split(dirs)
        folder_path = os.path.join(dir_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        offset = int(wx_file.file_offset.hex(), 16)
        size = int(wx_file.file_size.hex(), 16)
        ff = wx_pkg_file[offset:offset + size]
        with open(dirs, 'a+') as f:
            f.write(ff.decode())
        print(wx_file.file_name, "写入完成")


def exc_header(wx_file):
    pkg_file_len = int(wx_file[14:18].hex(), 16)
    wxapkg_file_list = []
    index = 18
    for i in range(pkg_file_len):
        f = WXPkgFileInfo()
        file_name_len = int(wx_file[index:index + 4].hex(), 16)
        index += 4
        f.file_name_len = file_name_len
        f.file_name = wx_file[index:index + file_name_len].decode()
        index += file_name_len
        f.file_offset = wx_file[index:index + 4]
        index += 4
        f.file_size = wx_file[index:index + 4]
        index += 4
        wxapkg_file_list.append(f)
    parse_file_info(wx_file, wxapkg_file_list)


if __name__ == '__main__':
    app_id = 'dec'
    if not os.path.exists(app_id):
        os.mkdir(app_id)
    file_path = "/Users/didi/Library/Containers/com.tencent.xinWeChat/Data/.wxapplet/packages/wxd9813e0a0d4d4156/1726/_pages_shopping_.wxapkg"
    wxapkg = open(file_path, 'rb').read()
    if not is_dec(wxapkg):
        print("微信小程序未解密,不只支持")
        exit(0)
    exc_header(wxapkg)
