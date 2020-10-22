# Xcode 12 使用xctrace代替instruments采集和分析性能数据
## 1、背景
New Features
- You can now export Analysis Core Tables from existing Instruments .trace files using the xctrace command. See the xctrace man page for more details. (12491801)
- Files with symbol-heavy recordings are now 80-90% smaller, because of optimized .trace symbol storage. (56048324)
Deprecations
- The instruments command is now deprecated in favor of its replacement: xctrace. Use xctrace to record, import, and export data from Instruments .trace files. (36641078)
来自https://developer.apple.com/documentation/xcode-release-notes/xcode-12-release-notes

根据Xcode 12 release note，Apple在Xcode 12 中引入了一个新特性，使用xcrun xctrace命令替代instruments，并提供官方的解析trace文件命令。
至此，原有的instruments+Tracedecoder（https://github.com/Qusic/TraceUtility，仅支持到Xcode 10.1 ）采集分析性能数据方案可以废弃。
## 2、采集性能数据
（1）自定义trace模板
打开instruments，File-New，新建一个Activity Monitor

点“+”，新增一个Core Animation FPS


选中Thermal State，Document-移除Thermal State

保存为自定义模板文件

（2）使用xctrace record命令记录trace
// 查看命令用法
> xcrun xctrace record 

usage: 
    xctrace record [<options>] [--attach | --all-processes | --launch -- command ]
description:
    Perform a new recording on the specified device and target with the given template
常用参数如下：
--template ：指定模板
--all-processes ：记录所有程序
--output ：导出trace文件的路径和文件名
--device ：设备的udid
 --time-limit ：执行时长（ms｜s，如：60s ）
使用示例：
> xcrun xctrace record --template MyTemplate.tracetemplate --all-processes --output 'recording.trace' --device my_udid --time-limit 60s

ps：使用自定义模板会上报一个xctrace[87948:4893789] [MT] DVTAssertions: Warning in /Library/Caches/com.apple.xbs/Sources/Instruments/Instruments-64540.151/Theming/XRTheme.mm:213 的warning，已确定是Apple的bug，将在未来版本修复，不影响命令执行。
（3）使用xctrace export命令将trace解析为xml文件
// 查看命令用法
> xcrun xctrace export

usage:
    xctrace export [<options>] [--toc | --xpath expression]

description:
    Export given .trace using supplied query to the XML file format that can be later read and post-processed
常用参数如下：
--input <file>   ：           trace文件路径
--output <path>   ：  导出的xml文件路径
--toc       ：      导出文件结构
--xpath <expression>     ： 根据 XPath导出指定数据
使用--toc参赛，会解析出当前目录结构，例如使用上文中的模板文件，可以解析出如下数据：
<?xml version="1.0"?>

<trace-toc>
    <run number="1">
        <info>
            <target>
                <device name="Van (14.0.1)" uuid="xxx"/>
            </target>
            <summary/>
        </info>
        <data>
            <table schema="activity-monitor-system"/>
            <table schema="core-animation-fps-estimate"/>
            <table schema="activity-monitor-process-ledger"/>
            <table schema="graphics-statistic"/>
            <table schema="sysmon-process"/>
            <table schema="sysmon-system"/>
            <table schema="activity-monitor-process-live"/>
        </data>
    </run>
</trace-toc>
对于性能采集的数据（CPU、MEM、IO_READ、IO_WRITE、GPU、FPS，需要解析的是
core-animation-fps-estimate 和 activity-monitor-process-live，

即Xpath中/trace-toc/run[@number="1"]/data/table[@schema="core-animation-fps-estimate"]和/trace-toc/run[@number="1"]/data/table[@schema="activity-monitor-process-live"]

解析命令示例：
> xcrun xctrace export --input recording.trace --output recording_fps.xml --xpath '/trace-toc/run[@number="1"]/data/table[@schema="core-animation-fps-estimate"]'
> xcrun xctrace export --input recording.trace --output recording_activity.xml --xpath '/trace-toc/run[@number="1"]/data/table[@schema="activity-monitor-process-live"]'
3、解析脚本
解析出的xml文件中，对于相同的值，在第一次出现的时候会赋予一个id，下一次出现的时候会直接以ref="id"显示，例如下文中的fps=14，percent=4，因此解析xml文件时需要还原数据。
