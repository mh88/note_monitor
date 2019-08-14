# [数据运营](<https://www.growingio.com/data-operation>)

#### 数据规划

数据规划是指收集整理业务部门数据需求，搭建完整的数据指标体系。

这里有两个重要概念：指标和维度！指标（index），也有称度量（measure）。指标用来衡量具体的运营效果，比如 UV、DAU、销售金额、转化率等等。指标的选择来源于具体的业务需求，从需求中归纳事件，从事件对应指标。维度是用来对指标进行细分的属性，比如广告来源、浏览器类型、访问地区等等。选择维度的原则是：记录那些对指标可能产生影响的维度。



#### 数据采集

数据采集是指采集业务数据，向业务部门提供数据报表或者数据看板。

巧妇难为无米之炊，数据采集的重要性不言而喻。目前有三种常见的<u>[数据采集方案](https://docs.growingio.com/docs/sdk-integration/web-js-sdk/)</u>，分别是**埋点**、**可视化埋点**和**无埋点**。相比于埋点方案，无埋点成本低、速度快，不会发生错错埋、漏埋情况。无埋点正在成为市场的新宠儿，越来越多的企业采用了 GrowingIO 的无埋点方案。在无埋点情景下，数据运营可以摆脱埋点需求的桎梏，将更多时间放在业务分析上。

参考：

###### *[Android无埋点的技术选型之路](https://blog.csdn.net/yang69258973/article/details/85244845)*

###### [揭开JS无埋点技术的神秘面纱](<https://blog.csdn.net/VhWfR2u02Q/article/details/80971308>)

###### [代码埋点、可视化埋点与无痕埋点](https://blog.csdn.net/vshuang/article/details/60361314)



#### 数据分析

数据分析是指通过数据挖掘、数据模型等方式，深入分析业务数据；提供数据分析报告，定位问题，并且提出解决方案。

数据分析是数据运营的重点工作，数据规划和数据采集都是为了数据分析服务的。我们的最终目的是通过数据分析的方法定位问题，提出解决方案，促进业务增长。



*思考：*

<u>*APP 内数据收集*</u> 与 <u>*APP 间数据收集*</u>



**Who**    - 手机信息（设备号，机型，IMEI，OS,），个人信息（手机号码，性别，年龄，学历），

**When**  - 手机信息（当前系统时间，事件操作时间，事件停留时间），个人信息（生日，日历排期）

**Where** - 手机信息（GPS，IP，WIFI/4G），个人信息（籍贯，常住地）

**Why**     - 手机信息（App分类，内容标签，标签明细），个人信息（目的，兴趣爱好，工作需要，信息获取，自我提升）



模块名称|行为|内容|时间

App|展示|首页|001

频道|点击|新闻|002

频道|下拉|新闻|003

频道|上拉|新闻|004

频道|退出|新闻|005

频道|点击|资讯|006

频道|下拉|资讯|007

频道|上拉|资讯|008

频道|退出|资讯|010

文章|点击|标题|010

文章|分类|资讯|010



### Android 埋点方案 

*以下资料由 [Github link](https://github.com/search?o=desc&q=android+无埋点&s=stars&type= Repositories) 查询参考，只选部分，更多资料参考link*

- ###### [网易有料](https://github.com/NetEaseYouliao) (*可重点研究*)

  整合网易生态的优质内容和网易20年大数据技术，将定制化信息流和精准广告快速对接到您 的产品中，向终端用户提供个性化内容分发服务

  1. [网易HubbleData之Android无埋点实践](https://mp.weixin.qq.com/s/0dHKu5QIBL_4S7Tum-qW2Q)

  2. [hubbledata](https://github.com/hubbledata)

  3. 开源项目[**LazierTracker**](https://github.com/nailperry-zd/LazierTracker) 

     通过Android字节码插桩插件实现Android端无埋点（或自动埋点），并且支持根据配置文件实现业务数据的自动采集。

     参考 [*58无埋点数据采集技术在Android端实践*](https://mp.weixin.qq.com/s?__biz=MzU4ODM2MjczNA==&mid=2247483765&idx=1&sn=af344801fa14e49f949e7e762880b503&chksm=fddca7f4caab2ee254a29aca117ea1b59e71174e297fd30b5ae38e2fde67eb8858cdea32e2d2&scene=38#wechat_redirect)

  

- ###### [TamicAppMonitoring](<https://github.com/Tamicer/TamicAppMonitoring>) 

  Android App 无痕迹全埋点方案

  本次基于的埋点框架： <https://github.com/Tamicer/SkyMonitoring>

  

- ##### **[AndroidTracker](https://github.com/foolchen/AndroidTracker)**

  `AndroidTracker`是一个Android端的无埋点统计的实现方法。其对`Activity`、`Fragment`的生命周期进行监听，实现了页面浏览以及点击事件的采集。

  针对点击事件的处理，目前兼容`ActionBar`、`ToolBar`的点击，以及[ButterKnife](https://github.com/JakeWharton/butterknife)的点击注解
  
  
  
- [Tracker](https://github.com/Liberuman/Tracker)

  Tracker是一个无埋点SDK，开发者只需要在Application中初始化即可，不需要额外添加任何埋点代码

  

- **[MonitorDemo](https://github.com/liyajun2013/MonitorDemo)**

  Android 无埋点框架 使用ASM插桩实现

  

### SDK开发

- [Android无埋点数据采集SDK及Gradle插件开发](https://blog.csdn.net/yyanjun/article/details/80000781)

- [Android无埋点数据收集SDK关键技术](https://www.jianshu.com/p/b5ffe845fe2d)
