## 紫橙班牌实用工具 v3-Beta

#### 部署

找一台 VPS(或自建服务器), 直接在 incich_school_utilities 目录下运行 `python3 main.py`. (初次运行需要根据提示配置.)

依赖: 

- 相关 python 库(在 pip 上都有)，screenfetch 用于查看服务器信息

- ~~网易云音乐需要 ffmpeg 用于转码, ffmpeg 需要支持 amr 转码.~~

- 经过测试，班牌可直接播放 mp3 文件，无需转码成 amr

#### 基础功能: 

- 获取所有学校的邀请码: 直接运行 python get_code.py
- 在班牌上听网易云音乐
- 在班牌上使用百度百科搜索
- **[DOING]** 在班牌上访问服务器文件
- **[TODO]** 在班牌上使用 Microsoft Todo
- **[TODO]** 在班牌上发送 QQ 消息

#### 进阶功能:

- 提供了 python 包装的 api, 在 /incich_school_utilities/incich_api 下, 有能力的人可以自行开发.

本项目基于：https://github.com/lyc8503/IncichSchoolUtilities 进行二次开发
