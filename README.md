# ScheduleRelax

平常工作经常面对电脑，经常性的忘记休息，对视力与颈椎影响很大。因此做了这个小工具，可以用来定时关闭显示器，同时忽略键盘与鼠标。程序只能在Ubuntu或者其他Linux发行版下运行，
程序依赖**xinput**与**xprintidle**，可用下列命令安装:

```bash
sudo apt-get install xinput xprintidle
```

可以将脚本设置为开机启动，我一般图方便直接：

```bash
 (python ~/ROOT/bin/ScheduleRelax > /dev/null 2>&1 &)
```

# Support 

如果在**Linux**下使用有任何问题欢迎讨论，有兴趣的可以将程序移植到**Windows**下。


# License

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.

