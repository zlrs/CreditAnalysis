# CreditAnalysis
模拟登录UESTC教务系统并查询所有已修课程信息。
分为两个模块：登录模块和本地数据解析模块

## 登录模块
登录模块位于/session文件夹，配置文件是config.json。它先登录教务系统，再爬取课程数据，输出到.\session\data_page.html

config.json的格式如下：

   键        | 值                | 说明  
-------------|-------------      | -----
headers      | 请求报文头         | 默认已配置好
auth_url     | 校园网登录url      |   默认已配置好
data_url     | 展示课程信息的url   |   默认已配置好
username     | 用户名             | 修改为自己的用户名（学号）
password     | 密码               |  修改为自己的密码

## 分析模块
分析模块位于\analysis文件夹。它解析课程数据并计算学分情况。



## 项目进展

时间 |说明
----|----
init |添加了简单的分析模块
2019/1/11 |添加了登录模块

## 未来开发方向(现存的不足)
- 添加登录模块和分析模块之间的联系机制。目前登录模块和分析模块可以正常单独执行，但是两者没有对接上。
- 思考项目的设计模式
- 思考python脚本的设计模式
- 思考如何插件化，使得其他高校能轻松以插件的形式接入
